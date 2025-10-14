import azure.functions as func
import logging
import json
from Levenshtein import ratio

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="http_trigger_echo")
def http_trigger_echo(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed the ECHO request.')

    try:
        req_body = req.get_json()
    except ValueError:
        return func.HttpResponse(
            "Invalid JSON",
            status_code=400
        )

    # Ejemplo: responder con parte del payload
    rut = req_body.get("referencia_de_cobro", "undefined")

    result = {
        "status": "ok",
        "message": f"Procesado RUT: {rut}",
        "received": req_body
    }
    logging.info(f"Processed data: {result}")

    return func.HttpResponse(
        json.dumps(req_body),
        status_code=200,
        mimetype="application/json"
    )


def fuzzy_match(text1: str, text2: str, threshold: float = 0.8) -> bool:
    """
    Performs fuzzy string matching between two strings.
    Returns True if similarity ratio is above threshold.
    """
    if not text1 or not text2:
        return False
    return ratio(text1.upper(), text2.upper()) >= threshold


def parse_numeric_value(value) -> float:
    """
    Converts numeric values that may be strings with comma decimals to float.
    Examples: "11.117,03" -> 11117.03, 11117.03 -> 11117.03
    """
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        # Handle format like "11.117,03" (European format)
        value = value.replace(".", "").replace(",", ".")
        return float(value)
    return 0.0


@app.route(route="http_trigger_ose_transform")
def http_trigger_ose_transform(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processing OSE transformation request.')

    try:
        req_body = req.get_json()
    except ValueError:
        return func.HttpResponse(
            "Invalid JSON",
            status_code=400
        )

    # Check if provider is OSE
    proveedor_nombre = req_body.get("proveedor_nombre", "")
    proveedor_upper = proveedor_nombre.upper()
    if not ("OSE" in proveedor_upper or "OBRAS SANITARIAS" in proveedor_upper):
        # If not OSE, return original request body
        logging.info(f"Provider {proveedor_nombre} is not OSE, returning original data.")
        return func.HttpResponse(
            json.dumps(req_body),
            status_code=200,
            mimetype="application/json"
        )

    # Get domicilio for location matching
    domicilio = req_body.get("domicilio", "")

    # Parse subtotal_gravado_22 and no_facturable
    subtotal_gravado_22 = parse_numeric_value(req_body.get("subtotal_gravado_22", 0))
    no_facturable = parse_numeric_value(req_body.get("no_facturable", 0))

    logging.info(f"Processing OSE invoice for location: {domicilio}")
    logging.info(f"subtotal_gravado_22: {subtotal_gravado_22}, no_facturable: {no_facturable}")

    new_items = []

    # Match location and create appropriate line items
    if fuzzy_match(domicilio, "DOLORES, SORIANO"):
        logging.info("Matched location: DOLORES, SORIANO")
        new_items = [
            {
                "monto": round(subtotal_gravado_22, 2),
                "cantidad": 1,
                "p_unitario": round(subtotal_gravado_22, 2),
                "descripcion": "Otros gastos de estructura (AD)",
                "articulo": 13360
            },
            {
                "monto": round(no_facturable, 2),
                "cantidad": -1,
                "p_unitario": round(no_facturable, 2),
                "descripcion": "Gastos no deducibles (AD)",
                "articulo": 13371
            }
        ]
    elif fuzzy_match(domicilio, "YOUNG, RIO NEGRO"):
        logging.info("Matched location: YOUNG, RIO NEGRO")
        new_items = [
            {
                "monto": round(subtotal_gravado_22 * 0.8, 2),
                "cantidad": 0.8,
                "p_unitario": round(subtotal_gravado_22 * 0.8, 2),
                "descripcion": "Otros gastos de estructura (IN)",
                "articulo": 12228
            },
            {
                "monto": round(subtotal_gravado_22 * 0.1, 2),
                "cantidad": 0.1,
                "p_unitario": round(subtotal_gravado_22 * 0.1, 2),
                "descripcion": "Otros gastos de estructura (SE)",
                "articulo": 12891
            },
            {
                "monto": round(subtotal_gravado_22 * 0.1, 2),
                "cantidad": 0.1,
                "p_unitario": round(subtotal_gravado_22 * 0.1, 2),
                "descripcion": "Otros gastos de estructura (LO)",
                "articulo": 12571
            },
            {
                "monto": round(no_facturable, 2),
                "cantidad": 1,
                "p_unitario": round(no_facturable, 2),
                "descripcion": "Gastos no deducibles (AD)",
                "articulo": 13371
            }
        ]
    else:
        # Location not matched, return original data
        logging.warning(f"Location '{domicilio}' did not match any known patterns. Returning original data.")
        return func.HttpResponse(
            json.dumps(req_body),
            status_code=200,
            mimetype="application/json"
        )

    # Replace items in the request body
    req_body["items"] = new_items

    logging.info(f"Transformed invoice with {len(new_items)} new items")

    return func.HttpResponse(
        json.dumps(req_body),
        status_code=200,
        mimetype="application/json"
    )