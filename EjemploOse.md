Descripción | P. Unitario | Desc | Rec | Cantidad | Importe

Cargo Fijo Agua Potable (G) — IVA básico — 1.392,33

Cargo Fijo Agua Potable (G) — IVA básico — 181,84

Consumo Agua Potable Básico (G) — IVA básico — 155,66 × 14,00 = 2.182,04

Cargo Fijo Saneamiento — No gravado — 271,41

Cargo Variable Saneamiento — No gravado — 2.182,04

Ajuste por Redondeo — No facturable — -0,03

Totales:

No facturable: -0,03

Subtotal gravado (22%): 3.756,21

Subtotal no gravado (0%): 2.453,45

IVA (22%): 826,37

Total a pagar: 7.036,00

💻 Registro en SAP (Imagen 1)
Nº Artículo	Descripción del artículo	Cantidad	Precio por unidad	Indicador de Impuesto
13360	Otros gastos de estructura (AD)	1	UYU 3.756,2100	IVA_CTBZ
13360	Otros gastos de estructura (AD)	1	UYU 2.453,4500	IVA_EXE
13371	Gastos no deducibles (AD)	-1	UYU 0,0300	IVA_EXE
🔄 Relación factura ↔ SAP
Concepto factura	Artículo SAP	Observación
Subtotal gravado (22%) 3.756,21	13360	Gasto estructural gravado
Subtotal no gravado 2.453,45	13360	Gasto estructural exento
Ajuste por redondeo -0,03	13371	Gasto no deducible / ajuste