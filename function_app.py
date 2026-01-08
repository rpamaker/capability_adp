import azure.functions as func
import logging
import json
import traceback
import unicodedata

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

# ==================== REGLAS EMBEBIDAS ====================

PROVIDER_RULES = [
            # === REGLAS UTE ===
            {
                "Provedor": "UTE",
                "Referencia de cobro": "5130300000",
                "Localidad": "Rincón de Ruíz",
                "Lugar de ubicación": "Planta R21 (Totem Planta R21)",
                "Dirección del suministro": "Ruta 21 Km. 318.500 Ent.Izq. s/n",
                "ARTICULO": 12565,
                "Descripción": "Electricidad (LO)",
                "Cantidad": 1,
                "TaxCode": "IVA_CTB2",
                "WarehouseCode": "1",
                "CostingCode4": "002.9999",
                "DimCode": 4,
                "articulos_adicionales": [
                    {
                        "ARTICULO": 13371,
                        "Descripción": "Gastos no deduciables",
                        "Cantidad": 1,
                        "TaxCode": "IVA_EXE",
                        "WarehouseCode": "1",
                "CostingCode4": "301.9998",
                "DimCode": 4
                    }
                ]
            },
            {
                "Provedor": "UTE",
                "Referencia de cobro": "1776641000",
                "Localidad": "Young",
                "Lugar de ubicación": "Casita 80% LO, 10 SEM e 10% IN",
                "Dirección del suministro": "Cont. Batlle y Ordoñez Continuacion",
                "articulos": [
                    {
                        "ARTICULO": 12565,
                        "Descripción": "Electricidad (LO)",
                        "Cantidad": 0.8,
                        "TaxCode": "IVA_CTB2",
                        "WarehouseCode": "1",
                        "CostingCode4": "002.9999",
                        "DimCode": 4
                    },
                    {
                        "ARTICULO": 12220,
                        "Descripción": "Electricidad (IN)",
                        "Cantidad": 0.1,
                        "TaxCode": "IVA_CTB2",
                        "WarehouseCode": "1",
                        "CostingCode4": "313.9999",
                        "DimCode": 4
                    },
                    {
                        "ARTICULO": 12883,
                        "Descripción": "Electricidad (SE)",
                        "Cantidad": 0.1,
                        "TaxCode": "IVA_CTB2",
                        "WarehouseCode": "1",
                        "CostingCode4": ""
                    },
                    {
                        "ARTICULO": 13371,
                        "Descripción": "Gastos no deducibles (AD)",
                        "Cantidad": 1.0,
                        "TaxCode": "IVA_EXE",
                        "WarehouseCode": "1",
                        "CostingCode4": "301.9998",
                        "DimCode": 4
                    }
                ]
            },
            {
                "Provedor": "UTE",
                "Referencia de cobro": "6143597175",
                "Localidad": "Young",
                "Lugar de ubicación": "Planta Young (suministro bomba de incendio) 80%LO, 10% SEM, 10% IN",
                "Dirección del suministro": "Ruta 25 (km 17 al 23) 0039",
                "articulos": [
                    {
                        "ARTICULO": 12565,
                        "Descripción": "Electricidad (LO)",
                        "Cantidad": 0.8,
                        "TaxCode": "IVA_CTB2",
                        "WarehouseCode": "1",
                        "CostingCode4": "002.9999",
                        "DimCode": 4
                    },
                    {
                        "ARTICULO": 12220,
                        "Descripción": "Electricidad (IN)",
                        "Cantidad": 0.1,
                        "TaxCode": "IVA_CTB2",
                        "WarehouseCode": "1",
                        "CostingCode4": "313.9999",
                        "DimCode": 4
                    },
                    {
                        "ARTICULO": 12883,
                        "Descripción": "Electricidad (SE)",
                        "Cantidad": 0.1,
                        "TaxCode": "IVA_CTB2",
                        "WarehouseCode": "1",
                        "CostingCode4": ""
                    },
                    {
                        "ARTICULO": 13371,
                        "Descripción": "Gastos no deducibles (AD)",
                        "Cantidad": 1.0,
                        "TaxCode": "IVA_EXE",
                        "WarehouseCode": "1",
                        "CostingCode4": "301.9998",
                        "DimCode": 4
                    }
                ]
            },
            {
                "Provedor": "UTE",
                "Referencia de cobro": "4226951000",
                "Localidad": "Young",
                "Lugar de ubicación": "Planta Young (80% LO, 15% SEM Y 5% IN)",
                "Dirección del suministro": "Ruta 25 (km 17 al 23) s/n 001",
                "articulos": [
                    {
                        "ARTICULO": 12565,
                        "Descripción": "Electricidad (LO)",
                        "Cantidad": 0.8,
                        "TaxCode": "IVA_CTB2",
                        "WarehouseCode": "1",
                        "CostingCode4": "002.9999",
                        "DimCode": 4
                    },
                    {
                        "ARTICULO": 12220,
                        "Descripción": "Electricidad (IN)",
                        "Cantidad": 0.15,
                        "TaxCode": "IVA_CTB2",
                        "WarehouseCode": "1",
                        "CostingCode4": "313.9999",
                        "DimCode": 4
                    },
                    {
                        "ARTICULO": 12883,
                        "Descripción": "Electricidad (SE)",
                        "Cantidad": 0.05,
                        "TaxCode": "IVA_CTB2",
                        "WarehouseCode": "1",
                        "CostingCode4": ""
                    },
                    {
                        "ARTICULO": 13371,
                        "Descripción": "Gastos no deducibles (AD)",
                        "Cantidad": 1.0,
                        "TaxCode": "IVA_EXE",
                        "WarehouseCode": "1",
                        "CostingCode4": "301.9998",
                        "DimCode": 4
                    }
                ]
            },
            {
                "Provedor": "UTE",
                "Referencia de cobro": "8551680000",
                "Localidad": "Dolores",
                "Lugar de ubicación": "Planta R21 (67% LO, 25% IN, 8%Sistema AD)",
                "Dirección del suministro": "Ruta 21 Km 318.500 Ent.izq 1333 s/n",
                "articulos": [
                    {
                        "ARTICULO": 12565,
                        "Descripción": "Electricidad (LO)",
                        "Cantidad": 0.67,
                        "TaxCode": "IVA_CTB2",
                        "WarehouseCode": "1",
                        "CostingCode4": "002.9999",
                        "DimCode": 4
                    },
                    {
                        "ARTICULO": 12220,
                        "Descripción": "Electricidad (IN)",
                        "Cantidad": 0.25,
                        "TaxCode": "IVA_CTB2",
                        "WarehouseCode": "1",
                        "CostingCode4": "313.9999",
                        "DimCode": 4
                    },
                    {
                        "ARTICULO": 12883,
                        "Descripción": "Electricidad (AD)",
                        "Cantidad": 0.08,
                        "TaxCode": "IVA_CTB2",
                        "WarehouseCode": "1",
                        "CostingCode4": ""
                    },
                    {
                        "ARTICULO": 13371,
                        "Descripción": "Gastos no deducibles (AD)",
                        "Cantidad": 1.0,
                        "TaxCode": "IVA_EXE",
                        "WarehouseCode": "1",
                        "CostingCode4": "301.9998",
                        "DimCode": 4
                    }
                ]
            },
            {
                "Provedor": "UTE",
                "Referencia de cobro": "7474180000",
                "Localidad": "Ombues de Lavalle",
                "Lugar de ubicación": "Planta Semillas",
                "Dirección del suministro": "Ruta 55 (km 27,500 a 29,500)",
                "ARTICULO": 13221,
                "Descripción": "Electricidad (PS)",
                "TaxCode": "IVA_CTB2",
                "WarehouseCode": "1",
                "CostingCode4": "368.8022",
                "DimCode": 4,
                "articulos_adicionales": [
                    {
                        "ARTICULO": 13371,
                        "Descripción": "Gastos no deduciables (AD)",
                        "TaxCode": "IVA_EXE",
                        "WarehouseCode": "1",
                        "CostingCode4": "301.9998",
                        "DimCode": 4
                    }
                ]
            },
            {
                "Provedor": "UTE",
                "Referencia de cobro": "6515260000",
                "Localidad": "Dolores",
                "Lugar de ubicación": "Oficinas Dolores",
                "Dirección del suministro": "Avda. Asencio 1400",
                "ARTICULO": 13351,
                "Descripción": "Electricidad (PS)",
                "TaxCode": "IVA_CTB2",
                "WarehouseCode": "1",
                "CostingCode4": "301.9999",
                "DimCode": 4,
                "articulos_adicionales": [
                    {
                        "ARTICULO": 13371,
                        "Descripción": "Gastos no deduciables (AD)",
                        "TaxCode": "IVA_EXE",
                        "WarehouseCode": "1",
                        "CostingCode4": "301.9998",
                        "DimCode": 4
                    }
                ]
            },

            # === REGLAS ANTEL ACTUALIZADAS ===
            {
                "Provedor": "ANTEL",
                "Lugar de ubicación": "Planta Semillas Ombues",
                "Dirección": "Ruta R55",
                "Nº de Teléfono": "45762770 Servicio A65153 - M65553 (Telefonia fija PS)",
                "Artiuclo": 13210,
                "Descripción del Artículo": "Telefonía fija PS - planta Ombúes",
                "TaxCode": "IVA_CTB2",
                "WarehouseCode": "1",
                "CostingCode4": "368.8022",
                "DimCode": 4
            },
            {
                "Provedor": "ANTEL",
                "Lugar de ubicación": "Oficinas Dolores",
                "Dirección": "Asencio 1400",
                "Nº de Teléfono": "45343370  y 45349436",
                "Artiuclo": 13340,
                "Descripción del Artículo": "Telefonía fija AD -",
                "TaxCode": "IVA_CTB2",
                "WarehouseCode": "1",
                "CostingCode4": "301.9999",
                "DimCode": 4
            },
            {
                "Provedor": "ANTEL",
                "Lugar de ubicación": "Planta Young",
                "Dirección": "Cl Batlle y Ordoñez, Continuación",
                "Nº de Teléfono": "45677467 y ADSL",
                "Artiuclo": 12554,
                "Descripción del Artículo": "Telefonía fija LO - planta Young",
                "TaxCode": "IVA_CTB2",
                "WarehouseCode": "1",
                "CostingCode4": "001.9999",
                "DimCode": 4
            },
            {
                "Provedor": "ANTEL",
                "Lugar de ubicación": "Planta R21 e internet",
                "Dirección": "Asencio 1400",
                "Nº de Teléfono": "45345177  y  403481",
                "Artiuclo": 12554,
                "Descripción del Artículo": "Telefonía fija LO - Planta R21",
                "TaxCode": "IVA_CTB2",
                "WarehouseCode": "1",
                "CostingCode4": "002.9999",
                "DimCode": 4
            },
            {
                "Provedor": "ANTEL",
                "Lugar de ubicación": "Oficinas Dolores",
                "Dirección": "Asencio 1400( Enlaces de datos AD)",
                "Nº de Teléfono": "Servicio E24863 - E24864 - P31715 - P33275 - P33277 - U35453 - U42652",
                "Artiuclo": 13342,
                "Descripción del Artículo": "Enlace de datos AD - adm central",
                "TaxCode": "IVA_CTB2",
                "WarehouseCode": "1",
                "CostingCode4": "301.9999",
                "DimCode": 4
            },

            # === REGLAS ANTEL (ANCEL) ===
            {
                "Provedor": "ANTEL (Ancel)",
                "Nº de Teléfono": "Vera LTE2",
                "N° Contrato": "5535257",
                "articulos": [
                    {
                        "Artiuclo": 12089,
                        "Descripción del Artículo": "Enlace datos AC",
                        "TaxCode": "IVA_CTB2",
                        "WarehouseCode": "1",
                        "CostingCode4": "315.9999",
                        "DimCode": 4
                    },
                    {
                        "Artiuclo": 13371,
                        "Descripción del Artículo": "Gastos no deduciables",
                        "TaxCode": "IVA_EXE",
                        "WarehouseCode": "1",
                        "CostingCode4": "301.9998",
                        "DimCode": 4
                    }
                ]
            },
            {
                "Provedor": "ANTEL (Ancel)",
                "Nº de Teléfono": "Vera LTE2",
                "N° Contrato": "5535261",
                "articulos": [
                    {
                        "Artiuclo": 12089,
                        "Descripción del Artículo": "Enlace datos AC",
                        "TaxCode": "IVA_CTB2",
                        "WarehouseCode": "1",
                        "CostingCode4": "315.9999",
                        "DimCode": 4
                    },
                    {
                        "Artiuclo": 13371,
                        "Descripción del Artículo": "Gastos no deduciables",
                        "TaxCode": "IVA_EXE",
                        "WarehouseCode": "1",
                        "CostingCode4": "301.9998",
                        "DimCode": 4
                    }
                ]
            },
            {
                "Provedor": "ANTEL (Ancel)",
                "Nº de Teléfono": "Vera LTE2",
                "N° Contrato": "5561330",
                "articulos": [
                    {
                        "Artiuclo": 12089,
                        "Descripción del Artículo": "Enlace datos AC",
                        "TaxCode": "IVA_CTB2",
                        "WarehouseCode": "1",
                        "CostingCode4": "315.9999",
                        "DimCode": 4
                    },
                    {
                        "Artiuclo": 13371,
                        "Descripción del Artículo": "Gastos no deduciables",
                        "TaxCode": "IVA_EXE",
                        "WarehouseCode": "1",
                        "CostingCode4": "301.9998",
                        "DimCode": 4
                    }
                ]
            },

                    # === REGLAS OSE ACTUALIZADAS ===
        {
            "Provedor": "OSE",
            "Localidad": "Central (Dolores, Soriano)",
            "Concepto": "Importes con IVA y sin IVA",
            "articulos": [
                {
                    "Articulo": 13360,
                    "Descripción": "Otros gastos de estructura (AD)",
                    "Cantidad": 1,
                    "Regla": "Sumar ambos y cargar bajo este artículo",
                    "TaxCode": "IVA_CTB2",
                    "WarehouseCode": "1",
                    "CostingCode4": "301.9999",
                    "DimCode": 4
                },
                {
                    "Articulo": 13371,
                    "Descripción": "Gastos no deducibles (AD)",
                    "Cantidad": 1,
                    "Regla": "Siempre se usa para ajustes",
                    "TaxCode": "IVA_EXE",
                    "WarehouseCode": "1",
                    "CostingCode4": "301.9998",
                    "DimCode": 4
                }
            ]
        },{
            "Provedor": "OSE",
            "Localidad": "Young",
             "cantidad": 0.8,
            "items": [
                {
                    "Articulo": 12228,
                    "Descripción": "Otros gastos de estructura (IN)",
                    "Cantidad": 0.8,
                    "TaxCode": "IVA_CTB2",
                    "WarehouseCode": "1",
                    "CostingCode4": "313.9999",
                    "DimCode": 4
                },
                {
                    "Articulo": 12891,
                    "Descripción": "Otros gastos de estructura (SE)",
                    "Cantidad": 0.1,
                    "TaxCode": "IVA_CTB2",
                    "WarehouseCode": "1",
                    "CostingCode4": "368.9999",
                    "DimCode": 4
                },
                {
                    "Articulo": 12571,
                    "Descripción": "Otros gastos de estructura (LO) 10%",
                    "Cantidad": 0.1,
                    "TaxCode": "IVA_CTB2",
                    "WarehouseCode": "1",
                    "CostingCode4": "001.9999",
                    "DimCode": 4
                },
                {
                    "Articulo": 13371,
                    "Descripción": "Gastos no deducibles (AD)",
                    "Cantidad": 1,
                    "Regla": "Redondeo",
                    "TaxCode": "IVA_EXE",
                    "WarehouseCode": "1",
                    "CostingCode4": "301.9998",
                    "DimCode": 4
                }
            ]
        }
    
]

# ==================== FUNCIONES AUXILIARES ====================

def _get_first(d: dict, keys):
    for k in keys:
        if k in d and d[k] is not None:
            return d[k]
    return None

def _normalize_upper(text: str) -> str:
    if text is None:
        return ""
    try:
        text = str(text)
    except Exception:
        return ""
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')
    return text.upper()

def _digits_only(s: str | None) -> str:
    if not s:
        return ""
    return ''.join(ch for ch in str(s) if ch.isdigit())

def _phone_tokens(text: str | None) -> set[str]:
    digits = _digits_only(text)
    # Si viene concatenado (ej: 4534337045349436) también intentamos partir en dos números de 7-9 dígitos si es posible
    tokens = set()
    cur = ""
    for ch in str(text or ""):
        if ch.isdigit():
            cur += ch
        else:
            if len(cur) >= 6:
                tokens.add(cur)
            cur = ""
    if len(cur) >= 6:
        tokens.add(cur)
    if not tokens and len(digits) >= 12:
        # heurística: intentar cortar a la mitad si parece dos números pegados
        mid = len(digits) // 2
        tokens.add(digits[:mid])
        tokens.add(digits[mid:])
    if not tokens and digits:
        tokens.add(digits)
    return tokens

def _extract_articulo(d: dict):
    return _get_first(d, ["ARTICULO", "Articulo", "Artiuclo", "Artículo"])  # admite mis-typo

def _extract_cantidad(d: dict, default: float = 1.0) -> float:
    val = _get_first(d, ["Cantidad", "cantidad"])
    return parse_numeric(val) if val is not None else default

def _extract_descripcion(d: dict, fallback: str = "") -> str:
    return (
        _get_first(d, [
            "Descripción",
            "Descripción del Artículo",
            "descripcion",
            "Lugar de ubicación",
        ])
        or fallback
    )

_EXTRA_KEYS_WHITELIST = {
    "TaxCode",
    "WarehouseCode",
    "CostingCode4",
    "Descripción del Artículo",
    "Dirección",
    "Localidad",
    "Lugar de ubicación",
    "Concepto",
    "Regla",
    "Nº de Teléfono",
}

def _collect_extras(source_item: dict, rule_scope: dict) -> dict:
    extras = {}
    for key in _EXTRA_KEYS_WHITELIST:
        if key in source_item and source_item[key] is not None:
            extras[key] = source_item[key]
        elif key in rule_scope and rule_scope[key] is not None:
            extras[key] = rule_scope[key]
    return extras

# Asegurar que todos los items lleven estos campos
_REQUIRED_CODE_KEYS = ("TaxCode", "WarehouseCode", "CostingCode4")

def _ensure_code_fields(item: dict, rule_scope: dict | None):
    for key in _REQUIRED_CODE_KEYS:
        if key not in item or item[key] is None:
            if rule_scope and key in rule_scope and rule_scope[key] is not None:
                item[key] = rule_scope[key]
            else:
                item[key] = ""

def _apply_article_defaults(item: dict) -> None:
    try:
        art = int(float(item.get("articulo", 0)))
    except Exception:
        return
    if art == 13371:
        item["TaxCode"] = "IVA_EXE"
        item["WarehouseCode"] = "1"
        item["CostingCode4"] = "301.9998"

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
    proveedor = _normalize_upper(body.get("proveedor_nombre", ""))
    
    if "UTE" in proveedor or "USINAS" in proveedor or "TRASMISIONES" in proveedor:
        return "UTE"
    elif "OSE" in proveedor or "OBRAS SANITARIAS" in proveedor:
        return "OSE"
    elif "ANTEL" in proveedor or "ADMINISTRACION NACIONAL DE TELECOMUNICACIONES" in proveedor:
        return "ANTEL"
    
    return "UNKNOWN"


def find_ute_rule(referencia):
    """Busca regla UTE por referencia exacta."""
    ref_str = str(referencia).strip()
    
    for rule in PROVIDER_RULES:
        if rule.get("Provedor") == "UTE":
            rule_ref = str(
                rule.get("Referencia de cobro")
                or rule.get("Referencia de cobro ", "")
            ).strip()
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
    domicilio = _normalize_upper(body.get("domicilio", "") or body.get("direccion", ""))
    telefono_in = body.get("numero_de_telefono") or body.get("telefono") or body.get("Nº de Teléfono")
    phone_tokens_in = _phone_tokens(telefono_in)
    
    # 1) Match por contrato exacto si viene
    if contrato:
        contrato_str = str(contrato).strip()
        for rule in PROVIDER_RULES:
            prov_norm = _normalize_upper(rule.get("Provedor", ""))
            if "ANTEL" in prov_norm and "N° Contrato" in rule:
                if str(rule["N° Contrato"]) == contrato_str:
                    logging.info(f"✅ Regla ANTEL encontrada por contrato: {contrato_str}")
                    return rule
    
    # 2) Match por N° de Teléfono (comparando solo dígitos)
    if phone_tokens_in:
        for rule in PROVIDER_RULES:
            prov_norm = _normalize_upper(rule.get("Provedor", ""))
            if "ANTEL" in prov_norm and ("Nº de Teléfono" in rule or "N° de Teléfono" in rule or "Telefono" in rule or "Teléfono" in rule):
                tel_rule = rule.get("Nº de Teléfono") or rule.get("N° de Teléfono") or rule.get("Teléfono") or rule.get("Telefono")
                rule_tokens = _phone_tokens(tel_rule)
                if rule_tokens and (phone_tokens_in & rule_tokens):
                    logging.info("✅ Regla ANTEL encontrada por teléfono")
                    return rule
    
    # 3) Match por Dirección si está en el body y en la regla
    if domicilio:
        for rule in PROVIDER_RULES:
            prov_norm = _normalize_upper(rule.get("Provedor", ""))
            if "ANTEL" in prov_norm and "Dirección" in rule:
                dir_rule = _normalize_upper(rule.get("Dirección", ""))
                if dir_rule and (dir_rule in domicilio or domicilio in dir_rule):
                    logging.info("✅ Regla ANTEL encontrada por dirección")
                    return rule
    
    # 4) Fallback por Lugar de ubicación como antes
    for rule in PROVIDER_RULES:
        prov_norm = _normalize_upper(rule.get("Provedor", ""))
        if "ANTEL" in prov_norm and "Lugar de ubicación" in rule:
            ubicacion = _normalize_upper(rule["Lugar de ubicación"])
            if ubicacion in domicilio or domicilio in ubicacion or any(token in ubicacion for token in domicilio.split() if len(token) >= 4):
                logging.info("✅ Regla ANTEL encontrada por lugar de ubicación")
                return rule
    
    logging.warning("⚠️ No se encontró regla ANTEL")
    return None


# ==================== TRANSFORMACIONES ====================

def transform_ute(body):
    """Transforma items para UTE."""
    referencia = body.get("referencia_de_cobro", "")
    subtotal = get_subtotal(body)
    no_facturable = parse_numeric(body.get("no_facturable", 0))
    
    # Buscar redondeo en los items si no está en el campo no_facturable
    if no_facturable == 0:
        items_originales = body.get("items", [])
        for item in items_originales:
            desc_upper = _normalize_upper(item.get("descripcion", ""))
            if "REDONDEO" in desc_upper:
                no_facturable = parse_numeric(item.get("monto", 0))
                logging.info(f"  → Redondeo detectado en items: {no_facturable:.2f}")
                break
    
    logging.info(f"📋 UTE - Ref: {referencia}, Subtotal: {subtotal}, No fact: {no_facturable}")
    
    rule = find_ute_rule(referencia)
    new_items = []
    
    # Soporte esquema nuevo basado en lista 'articulos'
    if rule and isinstance(rule.get("articulos"), list):
        logging.info("🔄 UTE: esquema 'articulos'")
        for it in rule["articulos"]:
            articulo_val = _extract_articulo(it)
            if articulo_val is None:
                continue
            articulo_int = int(float(articulo_val))

            cantidad = _extract_cantidad(it, default=1.0)
            descripcion = _extract_descripcion(it, fallback=rule.get("Lugar de ubicación", "Energía eléctrica"))

            if articulo_int == 13371:
                if no_facturable != 0:
                    monto = round(no_facturable, 2)
                    # Si el monto es negativo, la cantidad también debe ser negativa
                    cantidad_redondeo = -1 if monto < 0 else 1
                    item = {
                        "monto": monto,
                        "cantidad": cantidad_redondeo,
                        "p_unitario": abs(monto),
                        "descripcion": descripcion,
                        "articulo": articulo_int,
                    }
                    item.update(_collect_extras(it, rule))
                    _ensure_code_fields(item, rule)
                    _apply_article_defaults(item)
                    new_items.append(item)
            else:
                monto = round(subtotal * cantidad, 2)
                item = {
                    "monto": monto,
                    "cantidad": cantidad,
                    "p_unitario": round(monto, 2),
                    "descripcion": descripcion,
                    "articulo": articulo_int,
                }
                item.update(_collect_extras(it, rule))
                _ensure_code_fields(item, rule)
                _apply_article_defaults(item)
                new_items.append(item)

        for it in rule.get("articulos_adicionales", []) or []:
            articulo_val = _extract_articulo(it)
            if articulo_val is None:
                continue
            articulo_int = int(float(articulo_val))
            descripcion = _extract_descripcion(it, fallback="Ajustes o redondeos")
            if articulo_int == 13371 and no_facturable != 0:
                monto = round(no_facturable, 2)
                # Si el monto es negativo, la cantidad también debe ser negativa
                cantidad_redondeo = -1 if monto < 0 else 1
                item = {
                    "monto": monto,
                    "cantidad": cantidad_redondeo,
                    "p_unitario": abs(monto),
                    "descripcion": descripcion,
                    "articulo": articulo_int,
                }
                item.update(_collect_extras(it, rule))
                _ensure_code_fields(item, rule)
                _apply_article_defaults(item)
                new_items.append(item)
        return new_items

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
                    monto = round(no_facturable, 2)
                    # Si el monto es negativo, la cantidad también debe ser negativa
                    cantidad_redondeo = -1 if monto < 0 else 1
                    new_items.append({
                        "monto": monto,
                        "cantidad": cantidad_redondeo,
                        "p_unitario": abs(monto),
                        "descripcion": descripcion,
                        "articulo": articulo_int
                    })
            else:
                # Artículo normal con porcentaje
                cantidad = float(rule.get(cant_key, 1.0))
                monto = round(subtotal * cantidad, 2)
                tmp_item = {
                    "monto": monto,
                    "cantidad": cantidad,
                    "p_unitario": round(monto, 2),
                    "descripcion": descripcion,
                    "articulo": articulo_int
                }
                tmp_item.update(_collect_extras(rule, rule))
                _ensure_code_fields(tmp_item, rule)
                new_items.append(tmp_item)
        
        # Verificar si falta el artículo 13371
        has_13371 = any(item["articulo"] == 13371 for item in new_items)
        if not has_13371 and no_facturable != 0:
            monto = round(no_facturable, 2)
            # Si el monto es negativo, la cantidad también debe ser negativa
            cantidad_redondeo = -1 if monto < 0 else 1
            adj_item = {
                "monto": monto,
                "cantidad": cantidad_redondeo,
                "p_unitario": abs(monto),
                "descripcion": "Gastos no deducibles (AD)",
                "articulo": 13371
            }
            adj_item.update(_collect_extras(rule, rule))
            _ensure_code_fields(adj_item, rule)
            _apply_article_defaults(adj_item)
            new_items.append(adj_item)
    
    elif rule:
        # Regla simple (un solo artículo)
        logging.info("🔄 Aplicando regla simple")
        
        articulo = rule.get("ARTICULO")
        if articulo:
            articulo_int = int(float(articulo))
        else:
            articulo_int = 13360
        
        descripcion = rule.get("Lugar de ubicación", "Energía eléctrica")
        
        base_item = {
            "monto": round(subtotal, 2),
            "cantidad": 1,
            "p_unitario": round(subtotal, 2),
            "descripcion": descripcion,
            "articulo": articulo_int,
        }
        base_item.update(_collect_extras(rule, rule))
        _ensure_code_fields(base_item, rule)
        new_items.append(base_item)
        
        if no_facturable != 0:
            monto = round(no_facturable, 2)
            # Si el monto es negativo, la cantidad también debe ser negativa
            cantidad_redondeo = -1 if monto < 0 else 1
            adj_item2 = {
                "monto": monto,
                "cantidad": cantidad_redondeo,
                "p_unitario": abs(monto),
                "descripcion": "Ajustes o redondeos",
                "articulo": 13371
            }
            _ensure_code_fields(adj_item2, rule)
            _apply_article_defaults(adj_item2)
            new_items.append(adj_item2)
    
    else:
        # Sin regla - valores por defecto
        logging.warning("⚠️ Usando valores por defecto UTE")
        def_item = {
            "monto": round(subtotal, 2),
            "cantidad": 1,
            "p_unitario": round(subtotal, 2),
            "descripcion": "Energía eléctrica",
            "articulo": 13360
        }
        _ensure_code_fields(def_item, None)
        _apply_article_defaults(def_item)
        new_items.append(def_item)
        
        if no_facturable != 0:
            monto = round(no_facturable, 2)
            # Si el monto es negativo, la cantidad también debe ser negativa
            cantidad_redondeo = -1 if monto < 0 else 1
            adj_item = {
                "monto": monto,
                "cantidad": cantidad_redondeo,
                "p_unitario": abs(monto),
                "descripcion": "Ajustes o redondeos",
                "articulo": 13371
            }
            _ensure_code_fields(adj_item, None)
            _apply_article_defaults(adj_item)
            new_items.append(adj_item)
    
    return new_items


def transform_ose(body):
    """Transforma items para OSE."""
    domicilio = body.get("domicilio", "")
    subtotal = get_subtotal(body)
    no_facturable = parse_numeric(body.get("no_facturable", 0))
    
    # Buscar redondeo en los items si no está en el campo no_facturable
    if no_facturable == 0:
        items_originales = body.get("items", [])
        for item in items_originales:
            desc_upper = _normalize_upper(item.get("descripcion", ""))
            if "REDONDEO" in desc_upper:
                no_facturable = parse_numeric(item.get("monto", 0))
                logging.info(f"  → Redondeo detectado en items: {no_facturable:.2f}")
                break
    
    logging.info(f"📋 OSE - Domicilio: {domicilio}, Subtotal: {subtotal}, No fact: {no_facturable}")
    
    rule = find_ose_rule(domicilio)
    new_items = []
    
    # Caso 1: regla con desglose clásico (cantidad=0.8 → 80/10/10)
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
        # Extras por ítem (si la regla define items/articulos) + extras de regla + códigos
        seq = rule.get("articulos") if isinstance(rule.get("articulos"), list) else rule.get("items")
        article_to_rule_item = {}
        if isinstance(seq, list):
            for r_it in seq:
                a_val = _extract_articulo(r_it) or _get_first(r_it, ["Artículo"])  # soporta acento
                if a_val is None:
                    continue
                try:
                    article_to_rule_item[int(float(a_val))] = r_it
                except Exception:
                    continue
        extras_rule = _collect_extras({}, rule)
        for it in new_items:
            rule_item = article_to_rule_item.get(it["articulo"]) if article_to_rule_item else None
            if rule_item:
                it.update(_collect_extras(rule_item, rule))
            it.update(extras_rule)
            _ensure_code_fields(it, rule)
    # Caso 2: regla con lista de articulos o items (nuevo esquema)
    elif rule and (isinstance(rule.get("articulos"), list) or isinstance(rule.get("items"), list)):
        logging.info("🔄 OSE: esquema 'articulos/items'")
        seq = rule.get("articulos") if isinstance(rule.get("articulos"), list) else rule.get("items")
        for it in seq:
            articulo_val = _extract_articulo(it)
            if articulo_val is None:
                articulo_val = _get_first(it, ["Artículo"])  # variante con acento
            if articulo_val is None:
                continue
            articulo_int = int(float(articulo_val))

            cantidad = _extract_cantidad(it, default=1.0)
            descripcion = _extract_descripcion(it, fallback="Otros gastos de estructura")

            if articulo_int == 13371:
                if no_facturable != 0:
                    monto = round(no_facturable, 2)
                    # Si el monto es negativo, la cantidad también debe ser negativa
                    cantidad_redondeo = -1 if monto < 0 else 1
                    item = {
                        "monto": monto,
                        "cantidad": cantidad_redondeo,
                        "p_unitario": abs(monto),
                        "descripcion": descripcion,
                        "articulo": articulo_int,
                    }
                    item.update(_collect_extras(it, rule))
                    _ensure_code_fields(item, rule)
                    _apply_article_defaults(item)
                    new_items.append(item)
            else:
                # Si la regla indica proporciones, se aplica sobre subtotal
                monto = round(subtotal * cantidad, 2)
                item = {
                    "monto": monto,
                    "cantidad": cantidad,
                    "p_unitario": round(monto, 2),
                    "descripcion": descripcion,
                    "articulo": articulo_int,
                }
                item.update(_collect_extras(it, rule))
                _ensure_code_fields(item, rule)
                _apply_article_defaults(item)
                new_items.append(item)
    else:
        # Regla estándar
        logging.info("🔄 Aplicando regla OSE estándar")
        base = {
            "monto": round(subtotal, 2),
            "cantidad": 1,
            "p_unitario": round(subtotal, 2),
            "descripcion": "Otros gastos de estructura (AD)",
            "articulo": 13360,
        }
        base.update(_collect_extras({}, rule or {}))
        _ensure_code_fields(base, rule)
        new_items.append(base)
    
    if no_facturable != 0:
        monto = round(no_facturable, 2)
        # Si el monto es negativo, la cantidad también debe ser negativa
        cantidad_redondeo = -1 if monto < 0 else 1
        adj_item = {
            "monto": monto,
            "cantidad": cantidad_redondeo,
            "p_unitario": abs(monto),
            "descripcion": "Gastos no deducibles (AD)",
            "articulo": 13371
        }
        # Intentar heredar extras específicos del artículo 13371 de la regla si existen
        rule_item_13371 = None
        if rule and (isinstance(rule.get("articulos"), list) or isinstance(rule.get("items"), list)):
            seq2 = rule.get("articulos") if isinstance(rule.get("articulos"), list) else rule.get("items")
            for r_it in seq2:
                a_val = _extract_articulo(r_it) or _get_first(r_it, ["Artículo"])  # soporta acento
                try:
                    if a_val is not None and int(float(a_val)) == 13371:
                        rule_item_13371 = r_it
                        break
                except Exception:
                    continue
        if rule_item_13371:
            adj_item.update(_collect_extras(rule_item_13371, rule))
        _ensure_code_fields(adj_item, rule)
        _apply_article_defaults(adj_item)
        new_items.append(adj_item)
    
    return new_items


def transform_antel(body):
    """Transforma items para ANTEL."""
    subtotal = get_subtotal(body)
    no_facturable = parse_numeric(body.get("no_facturable", 0))
    items_originales = body.get("items", [])
    adenda = body.get("adenda_de_la_factura", "")
    
    logging.info(f"📋 ANTEL - Subtotal: {subtotal}")
    
    # Detectar caso especial PC9249 - P90285 - P90288
    es_caso_enlaces_pc9249 = "PC9249" in adenda and "P90285" in adenda and "P90288" in adenda
    
    if es_caso_enlaces_pc9249:
        logging.info("✅ Detectado caso especial: SERVICIO PC9249 - P90285 - P90288 → Artículo 13342")
        logging.info("🔄 Generando renglones separados por tipo de IVA")
        
        # Obtener monto gravado 22% directamente del campo subtotal_gravado_22
        monto_gravado_22 = parse_numeric(body.get("subtotal_gravado_22", 0))
        logging.info(f"  ✓ Monto gravado 22%: {monto_gravado_22:.2f} (subtotal_gravado_22)")
        
        # Sumar items NO GRAVADOS para el monto exento
        monto_exento = 0.0
        monto_redondeo = 0.0
        
        for item in items_originales:
            desc_upper = _normalize_upper(item.get("descripcion", ""))
            monto = parse_numeric(item.get("monto", 0))
            
            if "REDONDEO" in desc_upper:
                monto_redondeo += monto
                logging.info(f"  → Redondeo: {monto:.2f}")
            elif "NO GRAVADO" in desc_upper or "EXENTO" in desc_upper:
                monto_exento += monto
                logging.info(f"  → Exento (NO GRAVADO): {monto:.2f}")
        
        new_items = []
        
        # 1. Renglón gravado al 22% (si existe)
        if monto_gravado_22 != 0:
            item_gravado = {
                "monto": round(monto_gravado_22, 2),
                "cantidad": 1,
                "p_unitario": round(monto_gravado_22, 2),
                "descripcion": "Telefonía / Datos",
                "articulo": 13342,
                "TaxCode": "IVA_CTB2",
                "WarehouseCode": "1",
                "CostingCode4": "301.9999"
            }
            new_items.append(item_gravado)
            logging.info(f"  ➤ Item gravado 22%: {monto_gravado_22:.2f} (Art. 13342, IVA_CTB2)")
        
        # 2. Renglón exento (si existe)
        if monto_exento != 0:
            item_exento = {
                "monto": round(monto_exento, 2),
                "cantidad": 1,
                "p_unitario": round(monto_exento, 2),
                "descripcion": "Telefonía / Datos",
                "articulo": 13342,
                "TaxCode": "IVA_EXE",
                "WarehouseCode": "1",
                "CostingCode4": "301.9999"
            }
            new_items.append(item_exento)
            logging.info(f"  ➤ Item exento: {monto_exento:.2f} (Art. 13342, IVA_EXE)")
        
        # 3. Renglón redondeo (si existe)
        if monto_redondeo != 0 or no_facturable != 0:
            monto_ajuste = monto_redondeo if monto_redondeo != 0 else no_facturable
            monto = round(monto_ajuste, 2)
            # Si el monto es negativo, la cantidad también debe ser negativa
            cantidad_redondeo = -1 if monto < 0 else 1
            item_redondeo = {
                "monto": monto,
                "cantidad": cantidad_redondeo,
                "p_unitario": abs(monto),
                "descripcion": "Gastos no deducibles (AD)",
                "articulo": 13371,
                "TaxCode": "IVA_EXE",
                "WarehouseCode": "1",
                "CostingCode4": "301.9998"
            }
            new_items.append(item_redondeo)
            logging.info(f"  ➤ Item redondeo: {monto:.2f} (Art. 13371, IVA_EXE)")
        
        logging.info(f"✅ Generados {len(new_items)} renglones para caso PC9249")
        return new_items
    
    # Flujo normal para otros casos de ANTEL
    rule = find_antel_rule(body)
    
    articulo = 13340
    descripcion = "Telefonía / Datos"
    new_items = []

    if rule and isinstance(rule.get("articulos"), list):
        logging.info("🔄 ANTEL: esquema 'articulos'")
        for it in rule["articulos"]:
            articulo_val = _extract_articulo(it)
            if articulo_val is None:
                continue
            articulo_int = int(float(articulo_val))
            cantidad = _extract_cantidad(it, default=1.0)
            desc = _extract_descripcion(it, fallback=descripcion)
            monto = round(subtotal * cantidad, 2) if articulo_int != 13371 else round(no_facturable, 2)
            if articulo_int == 13371 and no_facturable == 0:
                continue
            item = {
                "monto": monto,
                "cantidad": 1 if articulo_int == 13371 else cantidad,
                "p_unitario": monto,
                "descripcion": desc,
                "articulo": articulo_int,
            }
            item.update(_collect_extras(it, rule))
            _ensure_code_fields(item, rule)
            _apply_article_defaults(item)
            new_items.append(item)
    else:
        if rule:
            articulo = rule.get("Artiuclo") or rule.get("Artículo") or articulo
            descripcion = (
                rule.get("Descripción del Artículo")
                or rule.get("Cta Contable ")
                or descripcion
            )
        base_item = {
            "monto": round(subtotal, 2),
            "cantidad": 1,
            "p_unitario": round(subtotal, 2),
            "descripcion": descripcion,
            "articulo": int(float(articulo)),
        }
        base_item.update(_collect_extras({}, rule or {}))
        _ensure_code_fields(base_item, rule)
        _apply_article_defaults(base_item)
        new_items = [base_item]
    
    if no_facturable != 0:
        monto = round(no_facturable, 2)
        # Si el monto es negativo, la cantidad también debe ser negativa
        cantidad_redondeo = -1 if monto < 0 else 1
        adj_item = {
            "monto": monto,
            "cantidad": cantidad_redondeo,
            "p_unitario": abs(monto),
            "descripcion": "Gastos no deducibles (AD)",
            "articulo": 13371
        }
        _ensure_code_fields(adj_item, rule)
        _apply_article_defaults(adj_item)
        new_items.append(adj_item)
    
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