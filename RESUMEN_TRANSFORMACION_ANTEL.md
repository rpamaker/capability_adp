# Resumen de Transformación ANTEL - Caso PC9249

## 📊 Visualización del Proceso

```
┌─────────────────────────────────────────────────────────────────────┐
│                    FACTURA ANTEL RECIBIDA                           │
│                                                                     │
│  Adenda: "...SERVICIO PC9249 - P90285 - P90288..."                │
│                                                                     │
│  Items originales:                                                  │
│  1. GRAVADO TASA BASICA .................. 65927.87               │
│  2. NO GRAVADO ........................... 4025.35                │
│  3. ENVIO DE FACTURA ..................... 61.48                  │
│  4. REDONDEO ............................. -0.35                  │
│                                                                     │
│  subtotal_gravado_22: 65989.35                                     │
└─────────────────────────────────────────────────────────────────────┘
                              ↓
                    ┌─────────────────┐
                    │ DETECCIÓN       │
                    │ PC9249 ✓        │
                    │ P90285 ✓        │
                    │ P90288 ✓        │
                    └─────────────────┘
                              ↓
                    ┌─────────────────┐
                    │ CLASIFICACIÓN   │
                    │ POR TIPO IVA    │
                    └─────────────────┘
                              ↓
         ┌────────────────────┼────────────────────┐
         │                    │                    │
    ┌────▼────┐         ┌────▼────┐         ┌────▼────┐
    │ GRAVADO │         │ EXENTO  │         │REDONDEO │
    │  22%    │         │         │         │         │
    └────┬────┘         └────┬────┘         └────┬────┘
         │                   │                    │
         │                   │                    │
┌────────▼─────────┐ ┌───────▼──────────┐ ┌──────▼───────────┐
│ RENGLÓN 1        │ │ RENGLÓN 2        │ │ RENGLÓN 3        │
│                  │ │                  │ │                  │
│ Art: 13342       │ │ Art: 13342       │ │ Art: 13371       │
│ IVA: IVA_CTB2    │ │ IVA: IVA_EXE     │ │ IVA: IVA_EXE     │
│ Monto: 65989.35  │ │ Monto: 4086.83   │ │ Monto: -0.35     │
│ CC4: 301.9999    │ │ CC4: 301.9999    │ │ CC4: 301.9998    │
└──────────────────┘ └──────────────────┘ └──────────────────┘
```

## 🔢 Tabla de Cálculos

| Item Original | Monto | Clasificación | Renglón Destino |
|---------------|-------|---------------|-----------------|
| SERVICIO GRAVADO TASA BASICA | 65927.87 | Gravado 22% | Renglón 1 |
| ENVIO DE FACTURA | 61.48 | **Gravado 22%** ⚠️ | Renglón 1 |
| **SUMA GRAVADOS** | **65989.35** | **Gravado 22%** | **Renglón 1** |
| (usa subtotal_gravado_22) | **65989.35** ✓ | **Coincide!** | **Renglón 1** |
| SERVICIO NO GRAVADO | 4025.35 | Exento | Renglón 2 |
| REDONDEO REDONDEO | -0.35 | Redondeo | Renglón 3 |

## 📋 Resultado Final

### JSON de Salida
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
            "monto": 4025.35,
            "cantidad": 1,
            "p_unitario": 4025.35,
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
    ],
    "_transform_info": {
        "provider": "ANTEL",
        "items_count": 3,
        "processed": true
    }
}
```

## ✅ Verificación

| Campo | Valor Esperado | ✓ |
|-------|----------------|---|
| **Cantidad de renglones** | 3 | ✓ |
| **Artículo renglón 1** | 13342 | ✓ |
| **Artículo renglón 2** | 13342 | ✓ |
| **Artículo renglón 3** | 13371 | ✓ |
| **Monto gravado** | 65989.35 (incluye ENVIO) | ✓ |
| **Monto exento** | 4025.35 (solo NO GRAVADO) | ✓ |
| **Monto redondeo** | -0.35 | ✓ |
| **IVA renglón 1** | IVA_CTB2 | ✓ |
| **IVA renglones 2 y 3** | IVA_EXE | ✓ |
| **CostingCode4 renglones 1-2** | 301.9999 | ✓ |
| **CostingCode4 renglón 3** | 301.9998 | ✓ |

## 🎯 Puntos Clave

### 1. Detección Automática
- ✅ Se activa cuando la adenda contiene: `PC9249 + P90285 + P90288`
- ✅ No requiere configuración manual

### 2. Artículos
- ✅ **13342**: Para servicios de telefonía/datos (gravados y exentos)
- ✅ **13371**: Solo para redondeos/no deducibles

### 3. Separación por IVA
- ✅ **IVA_CTB2**: Servicios gravados al 22%
- ✅ **IVA_EXE**: Servicios exentos + redondeos

### 4. Códigos de Costeo
- ✅ **301.9999**: Servicios normales (renglones 1 y 2)
- ✅ **301.9998**: Gastos no deducibles (renglón 3)

## 🔍 Palabras Clave de Clasificación

### Prioridad de Clasificación

1. **Redondeo** (Prioridad Máxima)
   ```
   "REDONDEO"
   ```

2. **Exento**
   ```
   "NO GRAVADO" | "EXENTO"
   ```

3. **Gravado 22%** (Por Defecto)
   ```
   Todo lo demás (GRAVADO, TASA BASICA, ENVIO, etc.)
   ```

**⚠️ IMPORTANTE**: 
- "ENVIO DE FACTURA" se clasifica como **GRAVADO** (no exento)
- Solo items con "NO GRAVADO" o "EXENTO" explícito son exentos
- El `subtotal_gravado_22` tiene prioridad sobre la suma calculada

## 📊 Comparación: Antes vs Después

### ❌ Antes (Resultado Incorrecto)
```json
{
    "items": [
        {
            "monto": 65989.35,
            "articulo": 13340,  // ❌ Artículo incorrecto
            "TaxCode": ""       // ❌ Sin separación por IVA
        },
        {
            "monto": -0.35,
            "articulo": 13371
        }
    ]
}
```
**Problema**: No separaba por tipo de IVA, usaba artículo incorrecto.

### ✅ Después (Resultado Correcto)
```json
{
    "items": [
        {
            "monto": 65989.35,
            "articulo": 13342,     // ✅ Artículo correcto
            "TaxCode": "IVA_CTB2"  // ✅ Gravado 22%
        },
        {
            "monto": 4086.83,
            "articulo": 13342,     // ✅ Mismo artículo
            "TaxCode": "IVA_EXE"   // ✅ Exento
        },
        {
            "monto": -0.35,
            "articulo": 13371,     // ✅ Redondeo
            "TaxCode": "IVA_EXE"
        }
    ]
}
```
**Solución**: 3 renglones separados, artículos correctos, separación por IVA.

## 🚀 Uso

### Endpoint
```
POST /api/adp_transform
```

### Ejemplo de Request
```bash
curl -X POST http://localhost:7071/api/adp_transform \
  -H "Content-Type: application/json" \
  -d @tests/test_antel_pc9249.json
```

### Response
Retorna el JSON completo con los 3 renglones transformados.

## 📝 Notas Importantes

1. **⚠️ ENVIO DE FACTURA es GRAVADO**: A diferencia de versiones anteriores, "ENVIO" NO se clasifica como exento
2. **Prioridad del subtotal_gravado_22**: Si este campo existe, sobrescribe la suma calculada de items gravados
3. **Clasificación por defecto = Gravado**: Todo lo que NO sea "REDONDEO", "NO GRAVADO" o "EXENTO" se considera gravado
4. **Suma automática exentos**: Solo items con "NO GRAVADO" o "EXENTO" explícito
5. **Redondeo flexible**: Toma el item con "REDONDEO" o el campo `no_facturable`
6. **Case-sensitive**: La detección de PC9249, P90285, P90288 es sensible a mayúsculas/minúsculas

### 🔄 Cambio Importante
**Antes**: "ENVIO" → Exento ❌  
**Ahora**: "ENVIO" → Gravado ✓

Esto asegura que el `subtotal_gravado_22` coincida con la suma de items gravados.

