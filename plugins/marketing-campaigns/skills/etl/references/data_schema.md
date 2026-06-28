# MRP Data Schema — Column Dictionary

89 columns (A through CK) of the Sankhya MRP export.

> Column names in the **Name** column below are the literal headers from the Sankhya export.
> They are matched verbatim by the ETL and are intentionally kept in their original form.

## Product Identification (A-N)

| Col | Name | Type | Description |
|-----|------|------|-------------|
| A | Grupo | text | Product group |
| B | Subgrupo | text | Subgroup |
| C | Marca | text | Manufacturer brand |
| D | Master | text | Master code |
| E | Categoria | text | Product category |
| F | Fabricante | text | Manufacturer name |
| G | UF Fab | text | Manufacturer state |
| H | Cidade Fab | text | Manufacturer city |
| I | Cod. Bemol | integer | Internal Bemol code |
| J | Cod. Barras | text | Barcode (EAN) |
| K | Cod. Fab | text | Manufacturer code |
| L | Cod. Rampap | integer | Internal Rampap code |
| M | Produto | text | Product name/description |
| N | UN | text | Unit of measure |

## Monthly Sales (O-AP) — Pattern repeated for 7 months

Each month has 4 columns: Qtd, Vlr, Prom, % Desc.

| Period | Qtd | Vlr (R$) | Prom (R$) | % Desc |
|--------|-----|----------|-----------|--------|
| month-6 | O | P | Q | R |
| month-5 | S | T | U | V |
| month-4 | W | X | Y | Z |
| month-3 | AA | AB | AC | AD |
| month-2 | AE | AF | AG | AH |
| month-1 | AI | AJ | AK | AL |
| current month | AM | AN | AO | AP |

- **Qtd**: quantity sold (integer)
- **Vlr**: sales value (decimal, R$)
- **Prom**: value on promotion (decimal, R$)
- **% Desc**: discount percentage applied (decimal, %)

## Turnover and ABC Classification (AQ-AX)

| Col | Name | Type | Description |
|-----|------|------|-------------|
| AQ | Giro90d | decimal | Turnover over the last 90 days |
| AR | Giro60d | decimal | Turnover over the last 60 days |
| AS | Giro30d | decimal | Turnover over the last 30 days |
| AT | Giro15d | decimal | Turnover over the last 15 days |
| AU | Giro mes atual | decimal | Current month turnover |
| AV | ABC Qtd | text | ABC classification by quantity (A/B/C) |
| AW | ABC Vlr | text | ABC classification by value |
| AX | ABC Mrg | text | ABC classification by margin |

## Stock (AY-BF)

| Col | Name | Type | Description |
|-----|------|------|-------------|
| AY | Est atual | integer | Current stock |
| AZ | Est bloqueado | integer | Blocked stock |
| BA | Est transito | integer | In-transit stock |
| BB | Est total | integer | Total stock |
| BC | Est res | integer | Reserved stock |
| BD | Est disp | integer | Available stock |
| BE | Cob atual | decimal | Current coverage (days) |
| BF | Custo unit | decimal | Unit cost (R$) |

## Costs and Prices (BG-BU)

| Col | Name | Type | Description |
|-----|------|------|-------------|
| BG | Custo rep | decimal | Replacement cost (R$) |
| BH | Novo(90d) | text | Whether the product is new in the last 90 days (S/N) |
| BI | Preco tabela | decimal | List price (R$) |
| BJ | Mark-up | decimal | Mark-up (%) |
| BK | Preco Bemol | decimal | Bemol price (R$) |
| BL | Dt cadastro | date | Registration date |
| BM | Dt ult comp | date | Last purchase date |
| BN | Dt ult ent | date | Last inbound date |
| BO | Dt ult venda | date | Last sale date |
| BP | **Ativo** | text | Active product: "S" (yes) / "N" (no) |
| BQ | Custo est atual | decimal | Current stock cost (R$) |
| BR | Custo est transito | decimal | In-transit stock cost (R$) |
| BS | Custo est total | decimal | Total stock cost (R$) |
| BT | Preco est atual | decimal | Current stock price (R$) |
| BU | Preco est total | decimal | Total stock price (R$) |

## Status and Flags (BV-CE)

| Col | Name | Type | Description |
|-----|------|------|-------------|
| BV | Ativo compras | text | Active for purchasing: "S"/"N" |
| BW | CST | integer | Tax Situation Code (Código de Situação Tributária) |
| BX | Em showroom | text | Displayed in showroom: "S"/"N" |

### Per-store flags (presence marked with "X"):

| Col | Store |
|-----|-------|
| BY | Cidade Nova |
| BZ | Torquato |
| CA | Matriz |
| CB | Manauara |
| CC | Nova Cidade |
| CD | Camapua |
| CE | AM Shopping |

## Out-of-stock and Suggestions (CF-CK)

| Col | Name | Type | Description |
|-----|------|------|-------------|
| CF | **Em ruptura** | integer | Out of stock: 1 (yes) / empty (no) |
| CG | Sug Systock | integer | Systock suggestion (quantity) |
| CH | Dt pri ent | date | First inbound date |
| CI | Cob total | decimal | Total coverage (days) |
| CJ | Est pend | integer | Pending stock |
| CK | Cob futura | decimal | Future coverage (days) |

## Calculated Columns in IT PR1 (CL-CT)

These columns exist only in the `IT PR1` tab of the template and contain formulas:

| Col | Name | Formula | Description |
|-----|------|---------|-------------|
| CL | Venda dos últimos 90 dias | =AJ+AF+AB | Sum of Vlr for months -1, -2, -3 |
| CM | Média dos últimos 90 dias | =CL/3 | Monthly average revenue |
| CN | Increm (%) esperado | (manual) | Increment percentage set by the manager |
| CO | Meta de Faturamento | =CM+(CM*CN) | Monthly target with increment |
| CP | Increm (R$) esperado | =CM*CN | Increment in BRL |
| CQ | Qtd dos últimos 90 dias | =AI+AE+AA | Sum of Qtd for months -1, -2, -3 |
| CR | QTD Média dos últimos 90 dias | =CQ/3 | Monthly average quantity |
| CS | Campanha | (manual) | Campaign name/code |
| CT | Promoção | (manual) | Type of promotion applied |
