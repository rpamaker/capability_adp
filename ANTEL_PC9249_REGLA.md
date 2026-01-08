# Regla Especial ANTEL PC9249 - P90285 - P90288

## Descripción

Regla especial implementada para facturas de ANTEL que contienen el texto **"SERVICIO PC9249 - P90285 - P90288"** en la adenda.

## Comportamiento

Cuando se detecta esta adenda específica, el sistema genera automáticamente **3 renglones separados** por tipo de IVA:

### 1. Renglón Gravado al 22%
- **Artículo**: 13342
- **TaxCode**: IVA_CTB2
- **WarehouseCode**: 1
- **CostingCode4**: 301.9999
- **Descripción**: "Telefonía / Datos"
- **Monto**: Suma de todos los items con descripción que contenga "GRAVADO" o "TASA BASICA", o usa el campo `subtotal_gravado_22`

### 2. Renglón Exento
- **Artículo**: 13342
- **TaxCode**: IVA_EXE
- **WarehouseCode**: 1
- **CostingCode4**: 301.9999
- **Descripción**: "Telefonía / Datos"
- **Monto**: Suma de items con "NO GRAVADO", "EXENTO" o "ENVIO" en la descripción

### 3. Renglón Redondeo
- **Artículo**: 13371
- **TaxCode**: IVA_EXE
- **WarehouseCode**: 1
- **CostingCode4**: 301.9998
- **Descripción**: "Gastos no deducibles (AD)"
- **Monto**: Item con "REDONDEO" en descripción, o campo `no_facturable`

## Ejemplo Real

### Entrada
```json
{
    "IVA": 14517.65,
    "neto": 70012.65,
    "fecha": "01/11/2025",
    "items": [
        {
            "monto": 65927.87,
            "descripcion": "SERVICIO DE TELECOMUNICACIONES GRAVADO TASA BASICA"
        },
        {
            "monto": 4025.35,
            "descripcion": "SERVICIO DE TELECOMUNICACIONES NO GRAVADO"
        },
        {
            "monto": 61.48,
            "descripcion": "ENVIO DE FACTURA"
        },
        {
            "monto": -0.35,
            "descripcion": "REDONDEO REDONDEO"
        }
    ],
    "subtotal_gravado_22": 65989.35,
    "no_facturable": -0.35,
    "adenda_de_la_factura": "...SERVICIO PC9249 - P90285 - P90288..."
}
```

### Salida Generada
```json
{
    "items": [
        {
            "monto": 65989.35,
            "cantidad": 1,
            "p_unitario": 65989.35,
            "descripcion": "Telefonía / Datos",
            "articulo": 13342,
            "TaxCode": "IVA_CTB2",
            "WarehouseCode": "1",
            "CostingCode4": "301.9999"
        },
        {
            "monto": 4086.83,
            "cantidad": 1,
            "p_unitario": 4086.83,
            "descripcion": "Telefonía / Datos",
            "articulo": 13342,
            "TaxCode": "IVA_EXE",
            "WarehouseCode": "1",
            "CostingCode4": "301.9999"
        },
        {
            "monto": -0.35,
            "cantidad": 1,
            "p_unitario": -0.35,
            "descripcion": "Gastos no deducibles (AD)",
            "articulo": 13371,
            "TaxCode": "IVA_EXE",
            "WarehouseCode": "1",
            "CostingCode4": "301.9998"
        }
    ]
}
```

## Cálculo de Montos

### Monto Gravado 22%
El sistema calcula el monto gravado así:
1. Suma **TODOS** los items que NO sean "REDONDEO", "NO GRAVADO" o "EXENTO"
2. Si existe el campo `subtotal_gravado_22`, lo usa (tiene prioridad máxima)

**En el ejemplo**: 
- Item "GRAVADO TASA BASICA": 65927.87
- Item "ENVIO DE FACTURA": 61.48
- **Suma**: 65989.35
- Campo `subtotal_gravado_22`: **65989.35** ✓ (coincide!)

### Monto Exento
Suma solo los items con estas palabras en la descripción:
- "NO GRAVADO"
- "EXENTO"

**En el ejemplo**:
- "NO GRAVADO": 4025.35
- **Total**: 4025.35

**⚠️ IMPORTANTE**: "ENVIO DE FACTURA" se clasifica como **GRAVADO**, no como exento

### Monto Redondeo
Toma el item con "REDONDEO" en la descripción o el campo `no_facturable`.

**En el ejemplo**:
- Item "REDONDEO REDONDEO": -0.35
- Campo `no_facturable`: -0.35
- **Resultado**: -0.35

## Detección de la Regla

La regla se activa cuando se cumplen **TODAS** estas condiciones en la adenda:
1. Contiene el texto `"PC9249"`
2. Contiene el texto `"P90285"`
3. Contiene el texto `"P90288"`

```python
es_caso_enlaces_pc9249 = "PC9249" in adenda and "P90285" in adenda and "P90288" in adenda
```

## Ubicación en el Código

La lógica está implementada en la función `transform_antel()` en el archivo `function_app.py`, líneas 1047-1197.

```python
def transform_antel(body):
    # ...
    es_caso_enlaces_pc9249 = "PC9249" in adenda and "P90285" in adenda and "P90288" in adenda
    
    if es_caso_enlaces_pc9249:
        # Lógica especial para PC9249
        # Genera 3 renglones separados por tipo de IVA
```

## Casos de Uso

Esta regla se aplica típicamente a facturas de:
- **Servicios de enlaces de datos** de ANTEL
- **Oficinas centrales** (Dolores, Montevideo)
- Facturas con múltiples servicios de telecomunicaciones

## Diferencia con Otros Casos ANTEL

| Caso | Artículo | Renglones | Separación IVA |
|------|----------|-----------|----------------|
| **PC9249** | 13342 | 3 | Sí (gravado/exento/redondeo) |
| Otros enlaces (regla normal) | 13342 | 1-2 | No |
| Telefonía fija AD | 13340 | 1-2 | No |
| Telefonía fija PS | 13210 | 1-2 | No |
| Telefonía fija LO | 12554 | 1-2 | No |

## Logs de Procesamiento

Cuando se detecta este caso, el sistema genera los siguientes logs:

```
📋 ANTEL - Subtotal: 70012.65
✅ Detectado caso especial: SERVICIO PC9249 - P90285 - P90288 → Artículo 13342
🔄 Generando renglones separados por tipo de IVA
  ➤ Item gravado 22%: 65989.35 (Art. 13342, IVA_CTB2)
  ➤ Item exento: 4086.83 (Art. 13342, IVA_EXE)
  ➤ Item redondeo: -0.35 (Art. 13371, IVA_EXE)
✅ Generados 3 renglones para caso PC9249
```

## Testing

Archivo de prueba: `tests/test_antel_pc9249.json`

Para probar:
```bash
curl -X POST http://localhost:7071/api/adp_transform \
  -H "Content-Type: application/json" \
  -d @tests/test_antel_pc9249.json
```

## Notas Importantes

1. ⚠️ **El artículo siempre es 13342** para los dos primeros renglones (gravado y exento)
2. ⚠️ **El artículo 13371** solo se usa para el redondeo
3. ⚠️ **El `subtotal_gravado_22` tiene prioridad** sobre la suma de items gravados si está presente
4. ⚠️ **La detección es case-sensitive** para los códigos PC9249, P90285, P90288
5. ✅ **Los montos se suman automáticamente** por categoría (gravado/exento/redondeo)

