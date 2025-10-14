# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an Azure Functions Python application that serves as a "capability" within the Pometrix document processing system. It receives invoice data extracted from PDFs (primarily from OSE - Obras Sanitarias del Estado), processes it according to business rules, and returns modified invoice line items for accounting purposes.

The capability integrates with Pometrix backend via HTTP endpoints and is designed to handle specific vendor invoices with custom transformations based on address/location fields.

## Architecture

**Azure Functions Setup:**
- Python 3.11 runtime with Azure Functions v4
- Function app uses `@app.route()` decorators (Function App programming model v2)
- HTTP triggers with anonymous auth level
- Deployed to Azure: `capability-adp.azurewebsites.net`

**Data Flow:**
1. Pometrix backend extracts data from PDF invoices using document types configured with JSON schemas
2. Backend calls this capability via HTTP POST with extracted invoice data
3. Function applies business logic based on vendor and address fields
4. Function returns modified invoice with transformed line items
5. Backend uses the modified data for accounting system integration

**Key Data Structures:**
- Invoice payloads contain: `proveedor_nombre`, `proveedor_id`, `domicilio`, `items[]`, `neto`, `IVA`, `total`, `fecha`, `codigo`, `moneda`, `tax_cod`
- Each item has: `descripcion`, `cantidad`, `p_unitario`, `monto`, `articulo` (accounting article code)
- Metadata fields prefixed with `__mcp_*` are added by Pometrix platform

**Business Logic Pattern:**
The main transformation logic follows this pattern:
1. Check if vendor matches target criteria (e.g., OSE)
2. Match address/location using fuzzy matching
3. Calculate `subtotal_gravado_22` (sum of taxable items at 22%)
4. Calculate `no_facturable` (non-deductible amounts like printing costs)
5. Replace all items with new accounting-specific line items distributed by location/cost center
6. Each location has specific `articulo` codes for expense categorization

## Common Commands

**Local Development:**
```bash
# Run function locally
func start

# Access local endpoint
# http://localhost:7071/api/http_trigger_echo
```

**Deployment:**
```bash
# Login to Azure
az login
# Select subscription: [2] Microsoft Azure Sponsorship (rpamaker.com)

# Deploy to Azure
func azure functionapp publish capability-adp

# Deployed endpoint
# https://capability-adp.azurewebsites.net/api/http_trigger_echo
```

**Testing:**
- Test payloads are in `tests/OSE-test1/` and `tests/OSE-test2/`
- Use these payloads to test transformations locally before deploying
- Send POST requests with JSON body matching the schema in `pometrix_config_notes/`

## Integration with Pometrix Backend

**Backend Configuration:**
1. Create/edit capability: `https://backend.pometrix.com/admin/document/capability/`
2. Link capability to document type: `https://backend.pometrix.com/admin/document/documenttype/`
3. View execution logs: `https://backend.pometrix.com/admin/document/capabilityexecution/`

**Document Type Schema:**
- Schema definitions are in `pometrix_config_notes/document_type_pdffactura_V*.json`
- These define the expected structure of data extracted from PDFs
- Required fields: `fecha`, `codigo`, `moneda`, `proveedor_nombre`, `proveedor_id`, `neto`, `IVA`, `total`, `items`

## Development Notes

**Address Matching:**
- The capability relies on fuzzy matching of the `domicilio` field to determine which transformation to apply
- Known issue: Address extraction from PDFs may be unreliable (see `tests/OSE-test1/test1.md`)
- Different addresses trigger different accounting distributions (e.g., "DOLORES, SORIANO" vs "YOUNG, RIO NEGRO")

**Accounting Article Codes:**
- Article codes (e.g., 13360, 13371, 12228) map to specific expense categories in the accounting system
- Different cost centers have different article codes
- Example: "Otros gastos de estructura (AD)" vs "(IN)" vs "(SE)" vs "(LO)" represent different departments

**Cost Distribution:**
- Some locations split costs across multiple departments (e.g., YOUNG, RIO NEGRO: 80% IN, 10% SE, 10% LO)
- Non-deductible expenses are tracked separately with negative quantities

## Files of Interest

- `function_app.py` - Main function definitions and business logic
- `host.json` - Azure Functions host configuration
- `requirements.txt` - Python dependencies (minimal: just azure-functions)
- `local.settings.json` - Local environment configuration (encrypted)
- `log.md` / `log-referencia.md` - Development notes and deployment history
- `pometrix_config_notes/` - JSON schemas for document types
- `tests/OSE-test*/` - Test payloads and expected results
