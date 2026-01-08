# Transformación ANTEL a Formato SAP

## Descripción

Esta funcionalidad transforma facturas de ANTEL al formato SAP requerido, separando los montos por tipo de IVA y generando renglones individuales para cada concepto.

## Endpoint

```
POST /api/adp_transform_sap
```

## Características

### 1. Detección Automática del Artículo

- **Artículo 13342**: Se aplica cuando la adenda contiene el texto `"SERVICIO PC9249 - P90285 - P90288"`
- **Artículo 13340**: Se aplica en los demás casos

### 2. Separación por Tipo de IVA

La función genera **3 renglones SAP**:

1. **Monto Gravado al 22%** 
   - Items con descripción que contiene: "GRAVADO", "TASA BASICA"
   - TaxCode: `IVA_CTB2`
   - U_SE_TipoVenta: `13342` o `13340` (según adenda)
   - CostingCode4: `301.9999`

2. **Monto Exento**
   - Items con descripción que contiene: "NO GRAVADO", "EXENTO", "ENVIO"
   - TaxCode: `IVA_EXE`
   - U_SE_TipoVenta: `13342` o `13340` (según adenda)
   - CostingCode4: `301.9999`

3. **Redondeo / No Facturable**
   - Items con descripción que contiene: "REDONDEO"
   - TaxCode: `IVA_EXE`
   - U_SE_TipoVenta: `13371`
   - CostingCode4: `301.9998`

## Formato de Entrada

```json
{
    "IVA": 14517.65,
    "neto": 70012.65,
    "fecha": "01/11/2025",
    "items": [
        {
            "monto": 65927.87,
            "cantidad": 1,
            "p_unitario": 65927.87,
            "descripcion": "SERVICIO DE TELECOMUNICACIONES GRAVADO TASA BASICA"
        },
        {
            "monto": 4025.35,
            "cantidad": 1,
            "p_unitario": 4025.35,
            "descripcion": "SERVICIO DE TELECOMUNICACIONES NO GRAVADO"
        },
        {
            "monto": 61.48,
            "cantidad": 1,
            "p_unitario": 61.48,
            "descripcion": "ENVIO DE FACTURA"
        },
        {
            "monto": -0.35,
            "cantidad": 1,
            "p_unitario": -0.35,
            "descripcion": "REDONDEO REDONDEO"
        }
    ],
    "total": 84532.0,
    "codigo": "G226142",
    "moneda": "UYU",
    "proveedor_nombre": "Administración Nacional de Telecomunicaciones",
    "subtotal_gravado_22": 65989.35,
    "no_facturable": -0.35,
    "adenda_de_la_factura": "Número de cuenta: 04093602000189 Código de distribución: 01 45 004 000000 Vto. próxima factura: 19-12-2025 Servicios incluidos: SERVICIO PC9249 - P90285 - P90288 Info debito bancario: 128SCOTIABANK Código de barras: 82111G 0226142202511010000084532000000065989350002104093602000189740"
}
```

## Formato de Salida

```json
[
    {
        "DocDate": "2025-11-01",
        "TaxDate": "2025-11-01",
        "Comments": "Consumo Octubre enlaces",
        "JournalMemo": "Factura de ANTEL por servicios de Telefonía / Datos",
        "U_SE_TipoVenta": "13342",
        "ItemCode": "1",
        "Quantity": 1,
        "UnitPrice": "65.989,35",
        "TaxCode": "IVA_CTB2",
        "WarehouseCode": "01",
        "CostingCode4": "301.9999",
        "U_TipoMovimiento": "5"
    },
    {
        "DocDate": "2025-11-01",
        "TaxDate": "2025-11-01",
        "Comments": "Consumo Octubre enlaces",
        "JournalMemo": "Factura de ANTEL por servicios de Telefonía / Datos",
        "U_SE_TipoVenta": "13342",
        "ItemCode": "1",
        "Quantity": 1,
        "UnitPrice": "4.086,83",
        "TaxCode": "IVA_EXE",
        "WarehouseCode": "01",
        "CostingCode4": "301.9999",
        "U_TipoMovimiento": "5"
    },
    {
        "DocDate": "2025-11-01",
        "TaxDate": "2025-11-01",
        "Comments": "Gastos no deducibles (AD)",
        "JournalMemo": "Factura de ANTEL por Gastos no deducibles",
        "U_SE_TipoVenta": "13371",
        "ItemCode": "1",
        "Quantity": 1,
        "UnitPrice": "-0,35",
        "TaxCode": "IVA_EXE",
        "WarehouseCode": "01",
        "CostingCode4": "301.9998",
        "U_TipoMovimiento": "5"
    }
]
```

## Campos de Salida

Cada renglón SAP contiene los siguientes campos:

| Campo | Descripción | Ejemplo |
|-------|-------------|---------|
| `DocDate` | Fecha del documento (ISO format) | "2025-11-01" |
| `TaxDate` | Fecha impositiva (ISO format) | "2025-11-01" |
| `Comments` | Comentario descriptivo | "Consumo Octubre enlaces" |
| `JournalMemo` | Memo del asiento | "Factura de ANTEL por servicios de Telefonía / Datos" |
| `U_SE_TipoVenta` | Artículo/Código de venta | "13342", "13340", "13371" |
| `ItemCode` | Código del item | "1" |
| `Quantity` | Cantidad | 1 |
| `UnitPrice` | Precio unitario (formato europeo) | "65.989,35" |
| `TaxCode` | Código de impuesto | "IVA_CTB2", "IVA_EXE" |
| `WarehouseCode` | Código de almacén | "01" |
| `CostingCode4` | Código de costeo | "301.9999", "301.9998" |
| `U_TipoMovimiento` | Tipo de movimiento | "5" |

## Formato de Precio

El campo `UnitPrice` se formatea con:
- **Separador de miles**: punto (`.`)
- **Separador decimal**: coma (`,`)
- **Ejemplo**: `65.989,35` (sesenta y cinco mil novecientos ochenta y nueve con treinta y cinco)

## Lógica de Clasificación

### Monto Gravado 22%
```python
if "GRAVADO" in descripcion or "TASA BASICA" in descripcion:
    # Clasificar como gravado al 22%
```

### Monto Exento
```python
if "NO GRAVADO" in descripcion or "EXENTO" in descripcion or "ENVIO" in descripcion:
    # Clasificar como exento
```

### Redondeo
```python
if "REDONDEO" in descripcion:
    # Clasificar como redondeo (artículo 13371)
```

## Ejemplo de Uso

### Request

```bash
curl -X POST http://localhost:7071/api/adp_transform_sap \
  -H "Content-Type: application/json" \
  -d @tests/test_antel_sap_simple.json
```

### Response

```json
[
    {
        "DocDate": "2025-11-01",
        "TaxDate": "2025-11-01",
        "Comments": "Consumo Octubre enlaces",
        "JournalMemo": "Factura de ANTEL por servicios de Telefonía / Datos",
        "U_SE_TipoVenta": "13342",
        "ItemCode": "1",
        "Quantity": 1,
        "UnitPrice": "65.989,35",
        "TaxCode": "IVA_CTB2",
        "WarehouseCode": "01",
        "CostingCode4": "301.9999",
        "U_TipoMovimiento": "5"
    },
    ...
]
```

## Validación

El endpoint solo procesa facturas de **ANTEL**. Si se envía una factura de otro proveedor, retorna:

```json
{
    "error": "Este endpoint solo procesa facturas de ANTEL",
    "proveedor_detectado": "UTE"
}
```

## Notas Técnicas

1. **Conversión de Fecha**: Las fechas se convierten del formato `DD/MM/YYYY` al formato ISO `YYYY-MM-DD`
2. **Suma de Items**: Los montos se suman por categoría (gravado, exento, redondeo)
3. **Formato Numérico**: Los números se formatean con separador de miles y decimales europeo
4. **Detección de Adenda**: Se busca el patrón exacto `"PC9249"`, `"P90285"` y `"P90288"` en la adenda

## Función Principal

La función principal es `transform_antel_to_sap(body)` ubicada en `function_app.py` líneas 1118-1229.

## Testing

Los datos de prueba se encuentran en:
- `tests/test_antel_sap.py` - Script de prueba completo
- `tests/test_antel_sap_simple.json` - Datos de prueba en formato JSON

