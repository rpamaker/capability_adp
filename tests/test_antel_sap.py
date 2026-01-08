#!/usr/bin/env python3
"""
Script de prueba para transformación ANTEL a formato SAP
"""

import json
import sys
import os

# Agregar el directorio padre al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from function_app import transform_antel_to_sap, detect_provider

# Datos de prueba proporcionados por el usuario
test_data = {
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
    "tax_cod": "22%",
    "domicilio": "Montevideo",
    "__mcp_status": "TAG",
    "proveedor_id": "211003420017",
    "no_facturable": -0.35,
    "__mcp_timestamp": "2025-11-12T23:06:23.292956+00:00",
    "numero_de_cuenta": "04093602000189",
    "proveedor_nombre": "Administración Nacional de Telecomunicaciones",
    "__mcp_document_id": 4632,
    "__mcp_human_status": "PROCESSING",
    "__mcp_reference_key": None,
    "subtotal_gravado_22": 65989.35,
    "adenda_de_la_factura": "Número de cuenta: 04093602000189 Código de distribución: 01 45 004 000000 Vto. próxima factura: 19-12-2025 Servicios incluidos: SERVICIO PC9249 - P90285 - P90288 Info debito bancario: 128SCOTIABANK Código de barras: 82111G 0226142202511010000084532000000065989350002104093602000189740",
    "__mcp_document_file_url": "https://rpamaker.blob.core.windows.net/adp/Documents/invoice/1-11 ANTEL _EFacturaG 226142 Vto 20-11.pdf",
    "__mcp_document_file_name": "1-11 ANTEL _EFacturaG 226142 Vto 20-11.pdf"
}

# Resultado esperado
expected_output = [
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

def main():
    print("=" * 80)
    print("TEST: Transformación ANTEL a formato SAP")
    print("=" * 80)
    
    # Verificar proveedor
    provider = detect_provider(test_data)
    print(f"\n✓ Proveedor detectado: {provider}")
    
    if provider != "ANTEL":
        print(f"✗ ERROR: Se esperaba ANTEL, se obtuvo {provider}")
        return False
    
    # Ejecutar transformación
    print("\n🔄 Ejecutando transformación...")
    result = transform_antel_to_sap(test_data)
    
    # Mostrar resultado
    print("\n📤 RESULTADO:")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    
    # Validaciones
    print("\n" + "=" * 80)
    print("VALIDACIONES")
    print("=" * 80)
    
    success = True
    
    # 1. Verificar cantidad de items
    if len(result) == 3:
        print(f"✓ Cantidad de renglones: {len(result)} (esperado: 3)")
    else:
        print(f"✗ Cantidad de renglones: {len(result)} (esperado: 3)")
        success = False
    
    # 2. Verificar que todos tienen artículo 13342 excepto el de redondeo
    for i, item in enumerate(result):
        if i < 2:  # Los primeros dos deben ser 13342
            if item["U_SE_TipoVenta"] == "13342":
                print(f"✓ Item {i+1}: Artículo correcto (13342)")
            else:
                print(f"✗ Item {i+1}: Artículo incorrecto (esperado: 13342, obtenido: {item['U_SE_TipoVenta']})")
                success = False
        else:  # El último debe ser 13371
            if item["U_SE_TipoVenta"] == "13371":
                print(f"✓ Item {i+1}: Artículo correcto (13371 - Redondeo)")
            else:
                print(f"✗ Item {i+1}: Artículo incorrecto (esperado: 13371, obtenido: {item['U_SE_TipoVenta']})")
                success = False
    
    # 3. Verificar separación por IVA
    gravado_item = result[0]
    exento_item = result[1]
    
    if gravado_item["TaxCode"] == "IVA_CTB2":
        print(f"✓ Item gravado: TaxCode correcto (IVA_CTB2)")
    else:
        print(f"✗ Item gravado: TaxCode incorrecto (esperado: IVA_CTB2, obtenido: {gravado_item['TaxCode']})")
        success = False
    
    if exento_item["TaxCode"] == "IVA_EXE":
        print(f"✓ Item exento: TaxCode correcto (IVA_EXE)")
    else:
        print(f"✗ Item exento: TaxCode incorrecto (esperado: IVA_EXE, obtenido: {exento_item['TaxCode']})")
        success = False
    
    # 4. Verificar campos obligatorios
    required_fields = ["DocDate", "TaxDate", "Comments", "JournalMemo", "U_SE_TipoVenta", 
                       "ItemCode", "Quantity", "UnitPrice", "TaxCode", "WarehouseCode", 
                       "CostingCode4", "U_TipoMovimiento"]
    
    all_fields_present = True
    for item in result:
        for field in required_fields:
            if field not in item:
                print(f"✗ Falta campo obligatorio: {field}")
                all_fields_present = False
                success = False
    
    if all_fields_present:
        print(f"✓ Todos los campos obligatorios están presentes")
    
    # 5. Verificar detección de caso especial PC9249
    if "PC9249" in test_data.get("adenda_de_la_factura", ""):
        print(f"✓ Adenda contiene SERVICIO PC9249 - P90285 - P90288")
        if result[0]["U_SE_TipoVenta"] == "13342":
            print(f"✓ Artículo 13342 aplicado correctamente para caso especial")
        else:
            print(f"✗ Artículo incorrecto para caso especial PC9249")
            success = False
    
    # Resultado final
    print("\n" + "=" * 80)
    if success:
        print("✅ TODAS LAS PRUEBAS PASARON")
    else:
        print("❌ ALGUNAS PRUEBAS FALLARON")
    print("=" * 80)
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

