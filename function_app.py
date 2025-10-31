import azure.functions as func
import logging
import json
import traceback

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

# ==================== REGLAS EMBEBIDAS ====================

PROVIDER_RULES = [
    {
        "Provedor": "UTE",
        "Referencia de cobro ": "5130300000",
        "ARTICULO": 12565,
        "Lugar de ubicación": "Planta R21 (Totem Planta R21)"
    },
    {
        "Provedor": "UTE",
        "Referencia de cobro ": "1776641000",
        "ARTICULO.1": 12565,
        "Lugar de ubicación.1": "Electricidad (LO)",
        "Cantidad": 0.8,
        "ARTICULO.2": 12220,
        "Lugar de ubicación.2": "Electricidad (IN)",
        "Cantidad.1": 0.1,
        "ARTICULO.3": 12883,
        "Lugar de ubicación.3": "Electricidad (SE)",
        "Cantidad.2": 0.1,
        "ARTICULO.4": 13371,
        "Lugar de ubicación.4": "Gastos no deducibles (AD)",
        "Cantidad.3": 1.0
    },
    {
        "Provedor": "UTE",
        "Referencia de cobro ": "6143597175",
        "ARTICULO.1": 12565,
        "Lugar de ubicación.1": "Electricidad (LO)",
        "Cantidad": 0.8,
        "ARTICULO.2": 12220,
        "Lugar de ubicación.2": "Electricidad (IN)",
        "Cantidad.1": 0.1,
        "ARTICULO.3": 12883,
        "Lugar de ubicación.3": "Electricidad (SE)",
        "Cantidad.2": 0.1,
        "ARTICULO.4": 13371,
        "Lugar de ubicación.4": "Gastos no deducibles (AD)",
        "Cantidad.3": 1.0
    },
    {
        "Provedor": "UTE",
        "Referencia de cobro ": "4226951000",
        "ARTICULO.1": 12565,
        "Lugar de ubicación.1": "Electricidad (LO)",
        "Cantidad": 0.8,
        "ARTICULO.2": 12220,
        "Lugar de ubicación.2": "Electricidad (IN)",
        "Cantidad.1": 0.15,
        "ARTICULO.3": 12883,
        "Lugar de ubicación.3": "Electricidad (SE)",
        "Cantidad.2": 0.05,
        "ARTICULO.4": 13371,
        "Lugar de ubicación.4": "Gastos no deducibles (AD)",
        "Cantidad.3": 1.0
    },
    {
        "Provedor": "UTE",
        "Referencia de cobro ": "8551680000",
        "ARTICULO.1": 12565,
        "Lugar de ubicación.1": "Electricidad (LO)",
        "Cantidad": 0.67,
        "ARTICULO.2": 12220,
        "Lugar de ubicación.2": "Electricidad (IN)",
        "Cantidad.1": 0.25,
        "ARTICULO.3": 12883,
        "Lugar de ubicación.3": "Electricidad (AD)",
        "Cantidad.2": 0.08,
        "ARTICULO.4": 13371,
        "Lugar de ubicación.4": "Gastos no deducibles (AD)",
        "Cantidad.3": 1.0
    },
    {
        "Provedor": "UTE",
        "Referencia de cobro ": "7474180000",
        "ARTICULO": 12565,
        "Lugar de ubicación": "Planta Semillas Ombues"
    },
    {
        "Provedor": "UTE",
        "Referencia de cobro ": "6515260000",
        "ARTICULO": 13360,
        "Lugar de ubicación": "Oficinas Dolores"
    },
    {
        "Provedor": "ANTEL",
        "N° Contrato": "5535257",
        "Artiuclo": 12089
    },
    {
        "Provedor": "ANTEL",
        "N° Contrato": "5535261",
        "Artiuclo": 12089
    },
    {
        "Provedor": "ANTEL",
        "N° Contrato": "5561330",
        "Artiuclo": 12089
    },
    {
        "Provedor": "ANTEL",
        "Lugar de ubicación": "Planta Semillas Ombues",
        "Artiuclo": 13210,
        "Cta Contable ": "Telefonía fija PS - planta Ombúes"
    },
    {
        "Provedor": "ANTEL",
        "Lugar de ubicación": "Oficinas Dolores",
        "Artiuclo": 13340,
        "Cta Contable ": "Telefonía fija AD"
    },
    {
        "Provedor": "ANTEL",
        "Lugar de ubicación": "Planta Young",
        "Artiuclo": 12554,
        "Cta Contable ": "Telefonía fija LO - planta Young"
    },
    {
        "Provedor": "ANTEL",
        "Lugar de ubicación": "Planta R21",
        "Artiuclo": 12554,
        "Cta Contable ": "Telefonía fija LO - Planta R21"
    },
    {
        "Provedor": "OSE",
        "Localidad": "Young",
        "cantidad": 0.8,
        "items": [
            {"Artículo": 12228, "Descripción": "Otros gastos de estructura (IN)", "cantidad": 0.8},
            {"Artículo": 12891, "Descripción": "Otros gastos de estructura (SE)", "cantidad": 0.1},
            {"Artículo": 12571, "Descripción": "Otros gastos de estructura (LO)", "cantidad": 0.1}
        ]
    }
]

# ==================== FUNCIONES AUXILIARES ====================

def parse_numeric(value):
    """Convierte valores numéricos manejando diferentes formatos."""
    try:
        if isinstance(value, (int, float)):
            return float(value)
        if isinstance(value, str):
            value = value.replace(".", "").replace(",", ".")
            return float(value)
        return 0.0
    except:
        return 0.0


def get_subtotal(body):
    """
    Obtiene el subtotal gravado desde el body.
    Busca en orden: subtotal_gravado_22, neto, subtotal_gravado
    """
    subtotal = body.get("subtotal_gravado_22")
    if subtotal is not None:
        return parse_numeric(subtotal)
    
    neto = body.get("neto")
    if neto is not None:
        return parse_numeric(neto)
    
    subtotal_gravado = body.get("subtotal_gravado")
    if subtotal_gravado is not None:
        return parse_numeric(subtotal_gravado)
    
    logging.warning("⚠️ No se encontró campo de subtotal, usando 0")
    return 0.0


def detect_provider(body):
    """Detecta el proveedor desde el JSON."""
    proveedor = body.get("proveedor_nombre", "").upper()
    
    if "UTE" in proveedor or "USINAS" in proveedor or "TRASMISIONES" in proveedor:
        return "UTE"
    elif "OSE" in proveedor or "OBRAS SANITARIAS" in proveedor:
        return "OSE"
    elif "ANTEL" in proveedor:
        return "ANTEL"
    
    return "UNKNOWN"


def find_ute_rule(referencia):
    """Busca regla UTE por referencia exacta."""
    ref_str = str(referencia).strip()
    
    for rule in PROVIDER_RULES:
        if rule.get("Provedor") == "UTE":
            rule_ref = str(rule.get("Referencia de cobro ", "")).strip()
            if rule_ref == ref_str:
                logging.info(f"✅ Regla UTE encontrada para referencia: {ref_str}")
                return rule
    
    logging.warning(f"⚠️ No se encontró regla UTE para referencia: {ref_str}")
    return None


def find_ose_rule(domicilio):
    """Busca regla OSE por localidad."""
    domicilio_upper = domicilio.upper()
    
    for rule in PROVIDER_RULES:
        if rule.get("Provedor") == "OSE":
            localidad = rule.get("Localidad", "").upper()
            if localidad in domicilio_upper or domicilio_upper in localidad:
                logging.info(f"✅ Regla OSE encontrada para: {domicilio}")
                return rule
    
    logging.warning(f"⚠️ No se encontró regla OSE para: {domicilio}")
    return None


def find_antel_rule(body):
    """Busca regla ANTEL por contrato o ubicación."""
    contrato = body.get("numero_contrato") or body.get("N° Contrato")
    domicilio = body.get("domicilio", "").upper()
    
    if contrato:
        contrato_str = str(contrato).strip()
        for rule in PROVIDER_RULES:
            if rule.get("Provedor") == "ANTEL" and "N° Contrato" in rule:
                if str(rule["N° Contrato"]) == contrato_str:
                    logging.info(f"✅ Regla ANTEL encontrada para contrato: {contrato_str}")
                    return rule
    
    for rule in PROVIDER_RULES:
        if rule.get("Provedor") == "ANTEL" and "Lugar de ubicación" in rule:
            ubicacion = rule["Lugar de ubicación"].upper()
            if ubicacion in domicilio or domicilio in ubicacion:
                logging.info(f"✅ Regla ANTEL encontrada para ubicación")
                return rule
    
    logging.warning("⚠️ No se encontró regla ANTEL")
    return None


# ==================== TRANSFORMACIONES ====================

def transform_ute(body):
    """Transforma items para UTE."""
    referencia = body.get("referencia_de_cobro", "")
    subtotal = get_subtotal(body)
    no_facturable = parse_numeric(body.get("no_facturable", 0))
    
    logging.info(f"📋 UTE - Ref: {referencia}, Subtotal: {subtotal}, No fact: {no_facturable}")
    
    rule = find_ute_rule(referencia)
    new_items = []
    
    if rule and "ARTICULO.1" in rule:
        # Desglose múltiple
        logging.info("🔄 Aplicando desglose múltiple")
        
        for i in range(1, 10):
            art_key = f"ARTICULO.{i}"
            if art_key not in rule:
                break
            
            articulo = rule[art_key]
            if not articulo:
                continue
            
            cant_key = "Cantidad" if i == 1 else f"Cantidad.{i-1}"
            desc_key = f"Lugar de ubicación.{i}"
            
            articulo_int = int(float(articulo))
            descripcion = rule.get(desc_key, f"Artículo {articulo}")
            
            if articulo_int == 13371:
                # Artículo de ajustes
                if no_facturable != 0:
                    new_items.append({
                        "monto": round(no_facturable, 2),
                        "cantidad": 1,
                        "p_unitario": round(no_facturable, 2),
                        "descripcion": descripcion,
                        "articulo": articulo_int
                    })
            else:
                # Artículo normal con porcentaje
                cantidad = float(rule.get(cant_key, 1.0))
                monto = round(subtotal * cantidad, 2)
                new_items.append({
                    "monto": monto,
                    "cantidad": cantidad,
                    "p_unitario": round(monto, 2),
                    "descripcion": descripcion,
                    "articulo": articulo_int
                })
        
        # Verificar si falta el artículo 13371
        has_13371 = any(item["articulo"] == 13371 for item in new_items)
        if not has_13371 and no_facturable != 0:
            new_items.append({
                "monto": round(no_facturable, 2),
                "cantidad": 1,
                "p_unitario": round(no_facturable, 2),
                "descripcion": "Gastos no deducibles (AD)",
                "articulo": 13371
            })
    
    elif rule:
        # Regla simple (un solo artículo)
        logging.info("🔄 Aplicando regla simple")
        
        articulo = rule.get("ARTICULO")
        if articulo:
            articulo_int = int(float(articulo))
        else:
            articulo_int = 13360
        
        descripcion = rule.get("Lugar de ubicación", "Energía eléctrica")
        
        new_items.append({
            "monto": round(subtotal, 2),
            "cantidad": 1,
            "p_unitario": round(subtotal, 2),
            "descripcion": descripcion,
            "articulo": articulo_int
        })
        
        if no_facturable != 0:
            new_items.append({
                "monto": round(no_facturable, 2),
                "cantidad": 1,
                "p_unitario": round(no_facturable, 2),
                "descripcion": "Ajustes o redondeos",
                "articulo": 13371
            })
    
    else:
        # Sin regla - valores por defecto
        logging.warning("⚠️ Usando valores por defecto UTE")
        new_items.append({
            "monto": round(subtotal, 2),
            "cantidad": 1,
            "p_unitario": round(subtotal, 2),
            "descripcion": "Energía eléctrica",
            "articulo": 13360
        })
        
        if no_facturable != 0:
            new_items.append({
                "monto": round(no_facturable, 2),
                "cantidad": 1,
                "p_unitario": round(no_facturable, 2),
                "descripcion": "Ajustes o redondeos",
                "articulo": 13371
            })
    
    return new_items


def transform_ose(body):
    """Transforma items para OSE."""
    domicilio = body.get("domicilio", "")
    subtotal = get_subtotal(body)
    no_facturable = parse_numeric(body.get("no_facturable", 0))
    
    logging.info(f"📋 OSE - Domicilio: {domicilio}, Subtotal: {subtotal}, No fact: {no_facturable}")
    
    rule = find_ose_rule(domicilio)
    new_items = []
    
    if rule and rule.get("cantidad") == 0.8:
        # Desglose Young (80/10/10)
        logging.info("🔄 Aplicando desglose Young (80/10/10)")
        new_items = [
            {
                "monto": round(subtotal * 0.8, 2),
                "cantidad": 0.8,
                "p_unitario": round(subtotal * 0.8, 2),
                "descripcion": "Otros gastos de estructura (IN)",
                "articulo": 12228
            },
            {
                "monto": round(subtotal * 0.1, 2),
                "cantidad": 0.1,
                "p_unitario": round(subtotal * 0.1, 2),
                "descripcion": "Otros gastos de estructura (SE)",
                "articulo": 12891
            },
            {
                "monto": round(subtotal * 0.1, 2),
                "cantidad": 0.1,
                "p_unitario": round(subtotal * 0.1, 2),
                "descripcion": "Otros gastos de estructura (LO)",
                "articulo": 12571
            }
        ]
    else:
        # Regla estándar
        logging.info("🔄 Aplicando regla OSE estándar")
        new_items.append({
            "monto": round(subtotal, 2),
            "cantidad": 1,
            "p_unitario": round(subtotal, 2),
            "descripcion": "Otros gastos de estructura (AD)",
            "articulo": 13360
        })
    
    if no_facturable != 0:
        new_items.append({
            "monto": round(no_facturable, 2),
            "cantidad": 1,
            "p_unitario": round(no_facturable, 2),
            "descripcion": "Gastos no deducibles (AD)",
            "articulo": 13371
        })
    
    return new_items


def transform_antel(body):
    """Transforma items para ANTEL."""
    subtotal = get_subtotal(body)
    no_facturable = parse_numeric(body.get("no_facturable", 0))
    
    logging.info(f"📋 ANTEL - Subtotal: {subtotal}")
    
    rule = find_antel_rule(body)
    
    articulo = 13340
    descripcion = "Telefonía / Datos"
    
    if rule:
        articulo = rule.get("Artiuclo") or rule.get("Artículo") or articulo
        descripcion = rule.get("Cta Contable ") or descripcion
    
    new_items = [{
        "monto": round(subtotal, 2),
        "cantidad": 1,
        "p_unitario": round(subtotal, 2),
        "descripcion": descripcion,
        "articulo": int(float(articulo))
    }]
    
    if no_facturable != 0:
        new_items.append({
            "monto": round(no_facturable, 2),
            "cantidad": 1,
            "p_unitario": round(no_facturable, 2),
            "descripcion": "Gastos no deducibles (AD)",
            "articulo": 13371
        })
    
    return new_items


# ==================== ENDPOINT PRINCIPAL ====================

@app.route(route="adp_transform", methods=["POST"])
def adp_transform(req: func.HttpRequest) -> func.HttpResponse:
    """
    Endpoint unificado para transformar facturas de UTE, OSE y ANTEL.
    POST /api/adp_transform
    """
    
    logging.info("=" * 60)
    logging.info("🚀 ADP TRANSFORMER - Iniciando procesamiento")
    logging.info("=" * 60)
    
    try:
        # Leer body
        try:
            body = req.get_json()
        except ValueError as e:
            logging.error(f"❌ JSON inválido: {str(e)}")
            return func.HttpResponse(
                json.dumps({"error": "JSON inválido", "details": str(e)}),
                status_code=400,
                mimetype="application/json"
            )
        
        logging.info(f"📥 Datos recibidos: {json.dumps(body, indent=2, ensure_ascii=False)}")
        
        # Detectar proveedor
        provider = detect_provider(body)
        logging.info(f"🏢 Proveedor detectado: {provider}")
        
        if provider == "UNKNOWN":
            logging.warning("⚠️ Proveedor no reconocido")
            return func.HttpResponse(
                json.dumps({
                    "error": "Proveedor no reconocido",
                    "proveedor_nombre": body.get("proveedor_nombre", ""),
                    "data_original": body
                }, ensure_ascii=False),
                status_code=200,
                mimetype="application/json"
            )
        
        # Transformar según proveedor
        if provider == "UTE":
            new_items = transform_ute(body)
        elif provider == "OSE":
            new_items = transform_ose(body)
        elif provider == "ANTEL":
            new_items = transform_antel(body)
        else:
            return func.HttpResponse(
                json.dumps({"error": "Proveedor no soportado"}),
                status_code=400,
                mimetype="application/json"
            )
        
        # Actualizar body
        body["items"] = new_items
        body["_transform_info"] = {
            "provider": provider,
            "items_count": len(new_items),
            "processed": True
        }
        
        logging.info(f"✅ Transformación exitosa - {len(new_items)} items generados")
        logging.info(f"📤 Respuesta: {json.dumps(body, indent=2, ensure_ascii=False)}")
        
        return func.HttpResponse(
            json.dumps(body, ensure_ascii=False, indent=2),
            status_code=200,
            mimetype="application/json",
            charset="utf-8"
        )
    
    except Exception as e:
        error_trace = traceback.format_exc()
        logging.error(f"❌ Error en transformación: {error_trace}")
        
        return func.HttpResponse(
            json.dumps({
                "error": "Error interno del servidor",
                "message": str(e),
                "trace": error_trace
            }, ensure_ascii=False),
            status_code=500,
            mimetype="application/json"
        )


# ==================== ENDPOINT DE PRUEBA ====================

@app.route(route="health", methods=["GET"])
def health(req: func.HttpRequest) -> func.HttpResponse:
    """Health check endpoint."""
    return func.HttpResponse(
        json.dumps({"status": "ok", "service": "ADP Transformer"}),
        status_code=200,
        mimetype="application/json"
    )