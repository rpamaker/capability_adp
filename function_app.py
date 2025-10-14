import azure.functions as func
import logging
import json

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