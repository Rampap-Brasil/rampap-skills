"""
ETL MRP -> Template de Campanhas PRs - Rampap

Transforma o export bruto do MRP (Sankhya) no template de campanhas,
filtrando produtos inativos (Ativo="N") e em ruptura (Em ruptura=1).

Uso:
    python etl_mrp.py --mrp <export_mrp.xlsx> --template <template_campanha.xlsx> --output <saida.xlsx> [--lang pt-BR]

Os logs de execução saem na língua preferencial do usuário (ver MESSAGES / --lang).
Código, identificadores e chaves do MESSAGES ficam em inglês; o texto dos logs é dado localizado.
"""

from __future__ import annotations

import argparse
import io
import os
import sys
from copy import copy
from pathlib import Path

# Corrige a codificação no console do Windows
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

# --- Strings de log localizadas ---
# As chaves/código ficam em inglês; os valores são o conteúdo de log por idioma.
# Para adicionar um idioma, acrescente um bloco de chave; o inglês é o fallback.
DEFAULT_LANG = "pt-BR"

MESSAGES = {
    "en": {
        "openpyxl_missing": "openpyxl not found. Install it with: pip install openpyxl",
        "header_title": "ETL MRP -> PRs Campaign Template - Rampap",
        "summary_title": "ETL SUMMARY",
        "step_extract": "[1/4] EXTRACT - Extracting MRP data...",
        "step_transform_ativo": "[2/4] TRANSFORM - Filtering Ativo='N'...",
        "step_transform_ruptura": "[3/4] TRANSFORM - Filtering Em ruptura=1...",
        "step_load": "[4/4] LOAD - Loading into template...",
        "opening_mrp": "Opening MRP export: {path}",
        "rows_extracted": "  Rows extracted: {n}",
        "filter_ativo": "  After Ativo='N' filter: {kept} rows (removed: {removed})",
        "filter_ruptura": "  After Em ruptura=1 filter: {kept} rows (removed: {removed})",
        "inserting_formulas": "  Inserting formulas into columns CL-CT ({n} rows)...",
        "opening_template": "Opening template: {path}",
        "sheet_not_found": "  ERROR: tab '{sheet}' not found in the template!",
        "clearing_sheet": "  Clearing tab '{sheet}'...",
        "clearing_sheet_cols": "  Clearing tab '{sheet}' (columns A-CK)...",
        "writing_rows": "  Writing {n} rows into '{sheet}'...",
        "saving": "Saving result to: {path}",
        "done": "ETL completed successfully!",
        "summary_original": "  Original MRP export:    {n} rows",
        "summary_mrp_ativos": "  MRP ativos (Ativo=N):   {n} rows",
        "summary_it_pr1": "  IT PR1 (Ruptura=1):     {n} rows",
        "summary_output": "  Generated file:         {path}",
    },
    "pt-BR": {
        "openpyxl_missing": "openpyxl não encontrado. Instale com: pip install openpyxl",
        "header_title": "ETL MRP -> Template de Campanhas PRs - Rampap",
        "summary_title": "RESUMO DO ETL",
        "step_extract": "[1/4] EXTRACT - Extraindo dados do MRP...",
        "step_transform_ativo": "[2/4] TRANSFORM - Filtrando Ativo='N'...",
        "step_transform_ruptura": "[3/4] TRANSFORM - Filtrando Em ruptura=1...",
        "step_load": "[4/4] LOAD - Carregando no template...",
        "opening_mrp": "Abrindo export MRP: {path}",
        "rows_extracted": "  Linhas extraídas: {n}",
        "filter_ativo": "  Após filtro Ativo='N': {kept} linhas (removidas: {removed})",
        "filter_ruptura": "  Após filtro Em ruptura=1: {kept} linhas (removidas: {removed})",
        "inserting_formulas": "  Inserindo fórmulas nas colunas CL-CT ({n} linhas)...",
        "opening_template": "Abrindo template: {path}",
        "sheet_not_found": "  ERRO: aba '{sheet}' não encontrada no template!",
        "clearing_sheet": "  Limpando aba '{sheet}'...",
        "clearing_sheet_cols": "  Limpando aba '{sheet}' (colunas A-CK)...",
        "writing_rows": "  Escrevendo {n} linhas em '{sheet}'...",
        "saving": "Salvando resultado em: {path}",
        "done": "ETL concluído com sucesso!",
        "summary_original": "  Export MRP original:    {n} linhas",
        "summary_mrp_ativos": "  MRP ativos (Ativo=N):   {n} linhas",
        "summary_it_pr1": "  IT PR1 (Ruptura=1):     {n} linhas",
        "summary_output": "  Arquivo gerado:         {path}",
    },
}

# Idioma ativo para os logs; sobrescrito por --lang em main().
_LANG = DEFAULT_LANG


def t(key: str, **kwargs) -> str:
    """Busca uma string de log localizada, com fallback para inglês e depois para a própria chave."""
    table = MESSAGES.get(_LANG, MESSAGES["en"])
    template = table.get(key) or MESSAGES["en"].get(key, key)
    return template.format(**kwargs)


def resolve_lang(lang: str | None) -> str:
    """Retorna um código de idioma suportado, com padrão DEFAULT_LANG."""
    if lang and lang in MESSAGES:
        return lang
    return DEFAULT_LANG


try:
    from openpyxl import load_workbook
    from openpyxl.utils import get_column_letter
except ImportError:
    print(t("openpyxl_missing"))
    sys.exit(1)


# --- Constantes ---
HEADER_ROW_MRP = 3          # Linha com os cabeçalhos no export MRP
DATA_START_ROW_MRP = 4      # Primeira linha de dados no export MRP
MAX_COL_LETTER = "CK"       # Última coluna a copiar (coluna 89)
MAX_COL_INDEX = 89           # Número de colunas de A até CK

# Índices de coluna (base 1) usados para filtrar
COL_ATIVO = 68               # BP = coluna 68 (Ativo)
COL_EM_RUPTURA = 84          # CF = coluna 84 (Em ruptura)

SHEET_MRP_ATIVOS = "MRP ativos"
SHEET_IT_PR1 = "IT PR1"


def parse_args():
    parser = argparse.ArgumentParser(description="ETL MRP -> Template de Campanhas PRs")
    parser.add_argument("--mrp", required=True, help="Caminho do export MRP do Sankhya (.xlsx)")
    parser.add_argument("--template", required=True, help="Caminho do template de campanha (.xlsx)")
    parser.add_argument("--output", required=False, help="Caminho do arquivo de saída (.xlsx)")
    parser.add_argument(
        "--lang",
        required=False,
        default=DEFAULT_LANG,
        help=f"Idioma dos logs de execução (suportados: {', '.join(MESSAGES)}; padrão: {DEFAULT_LANG})",
    )
    return parser.parse_args()


def get_output_path(template_path: str, output_path: str | None) -> Path:
    template = Path(template_path)
    if output_path:
        return Path(output_path)
    return template.parent / f"{template.stem}_ETL{template.suffix}"


def extract_mrp_data(mrp_path: str) -> tuple[list[list], int]:
    """
    Extrai os dados do export MRP, pulando as linhas de metadados e a última linha.
    Retorna (rows, original_count).
    """
    print(t("opening_mrp", path=mrp_path))
    wb = load_workbook(mrp_path, data_only=True)
    ws = wb.active

    all_rows = []
    for row in ws.iter_rows(min_row=DATA_START_ROW_MRP, max_col=MAX_COL_INDEX, values_only=True):
        all_rows.append(list(row))

    wb.close()

    # Remove a última linha (metadados/totais)
    if all_rows:
        all_rows = all_rows[:-1]

    original_count = len(all_rows)
    print(t("rows_extracted", n=original_count))
    return all_rows, original_count


def filter_ativo_n(rows: list[list]) -> list[list]:
    """Mantém apenas as linhas onde Ativo (col BP, índice 67) = 'N'."""
    filtered = [r for r in rows if r[COL_ATIVO - 1] == "N"]
    print(t("filter_ativo", kept=len(filtered), removed=len(rows) - len(filtered)))
    return filtered


def filter_em_ruptura(rows: list[list]) -> list[list]:
    """Mantém apenas as linhas onde Em ruptura (col CF, índice 83) = 1."""
    filtered = [r for r in rows if r[COL_EM_RUPTURA - 1] == 1]
    print(t("filter_ruptura", kept=len(filtered), removed=len(rows) - len(filtered)))
    return filtered


def clear_sheet_data(ws, start_row: int = 2):
    """Limpa todos os dados de start_row até o fim, preservando a linha 1 (cabeçalhos)."""
    for row in ws.iter_rows(min_row=start_row, max_col=MAX_COL_INDEX):
        for cell in row:
            cell.value = None


def copy_formatting(source_cell, target_cell):
    """Copia a formatação de célula da origem para o destino."""
    if source_cell.has_style:
        target_cell.font = copy(source_cell.font)
        target_cell.border = copy(source_cell.border)
        target_cell.fill = copy(source_cell.fill)
        target_cell.number_format = source_cell.number_format
        target_cell.protection = copy(source_cell.protection)
        target_cell.alignment = copy(source_cell.alignment)


def write_rows_to_sheet(ws, rows: list[list], start_row: int = 2):
    """Escreve as linhas na planilha a partir de start_row, apenas colunas A até CK."""
    for i, row_data in enumerate(rows):
        for j, value in enumerate(row_data):
            if j < MAX_COL_INDEX:
                ws.cell(row=start_row + i, column=j + 1, value=value)


def add_it_pr1_formulas(ws, num_rows: int, start_row: int = 2):
    """
    Adiciona as fórmulas calculadas nas colunas CL-CT do IT PR1.
    Essas fórmulas calculam as médias de venda de 90 dias e as metas de incremento.

    Mapeamento de colunas (base 1):
      AJ=36 (Vlr mes-1), AF=32 (Vlr mes-2), AB=28 (Vlr mes-3)
      AI=35 (Qtd mes-1), AE=31 (Qtd mes-2), AA=27 (Qtd mes-3)
      CL=90, CM=91, CN=92, CO=93, CP=94, CQ=95, CR=96, CS=97, CT=98
    """
    print(t("inserting_formulas", n=num_rows))
    for i in range(num_rows):
        row = start_row + i
        # CL: venda dos últimos 90 dias = AJ + AF + AB
        ws.cell(row=row, column=90, value=f"=AJ{row}+AF{row}+AB{row}")
        # CM: média dos últimos 90 dias = CL / 3
        ws.cell(row=row, column=91, value=f"=CL{row}/3")
        # CN: increm (%) esperado — manual, deixa vazio
        # CO: meta de faturamento = CM + (CM * CN)
        ws.cell(row=row, column=93, value=f"=CM{row}+(CM{row}*CN{row})")
        # CP: increm (R$) esperado = CM * CN
        ws.cell(row=row, column=94, value=f"=CM{row}*CN{row}")
        # CQ: qtd dos últimos 90 dias = AI + AE + AA
        ws.cell(row=row, column=95, value=f"=AI{row}+AE{row}+AA{row}")
        # CR: qtd média dos últimos 90 dias = CQ / 3
        ws.cell(row=row, column=96, value=f"=CQ{row}/3")
        # CS: Campanha — manual, deixa vazio
        # CT: Promoção — manual, deixa vazio


def load_data_into_template(template_path: str, output_path: Path,
                            mrp_ativos_rows: list[list],
                            it_pr1_rows: list[list]):
    """
    Abre o template, limpa as abas de destino, cola os dados filtrados, adiciona fórmulas e salva.
    """
    print(t("opening_template", path=template_path))
    wb = load_workbook(template_path)

    # --- MRP ativos ---
    if SHEET_MRP_ATIVOS not in wb.sheetnames:
        print(t("sheet_not_found", sheet=SHEET_MRP_ATIVOS))
        sys.exit(1)

    ws_mrp = wb[SHEET_MRP_ATIVOS]
    print(t("clearing_sheet", sheet=SHEET_MRP_ATIVOS))
    clear_sheet_data(ws_mrp, start_row=2)
    print(t("writing_rows", n=len(mrp_ativos_rows), sheet=SHEET_MRP_ATIVOS))
    write_rows_to_sheet(ws_mrp, mrp_ativos_rows, start_row=2)

    # --- IT PR1 ---
    if SHEET_IT_PR1 not in wb.sheetnames:
        print(t("sheet_not_found", sheet=SHEET_IT_PR1))
        sys.exit(1)

    ws_it = wb[SHEET_IT_PR1]
    print(t("clearing_sheet_cols", sheet=SHEET_IT_PR1))
    clear_sheet_data(ws_it, start_row=2)
    print(t("writing_rows", n=len(it_pr1_rows), sheet=SHEET_IT_PR1))
    write_rows_to_sheet(ws_it, it_pr1_rows, start_row=2)

    # Adiciona as fórmulas em CL-CT
    add_it_pr1_formulas(ws_it, len(it_pr1_rows), start_row=2)

    # --- Salva ---
    print(t("saving", path=output_path))
    wb.save(str(output_path))
    wb.close()
    print(t("done"))


def main():
    global _LANG
    args = parse_args()
    _LANG = resolve_lang(args.lang)
    output_path = get_output_path(args.template, args.output)

    print("=" * 60)
    print(t("header_title"))
    print("=" * 60)

    # Extract
    print("\n" + t("step_extract"))
    rows, original_count = extract_mrp_data(args.mrp)

    # Transform
    print("\n" + t("step_transform_ativo"))
    mrp_ativos_rows = filter_ativo_n(rows)

    print("\n" + t("step_transform_ruptura"))
    it_pr1_rows = filter_em_ruptura(mrp_ativos_rows)

    # Load
    print("\n" + t("step_load"))
    load_data_into_template(args.template, output_path, mrp_ativos_rows, it_pr1_rows)

    # Resumo
    print("\n" + "=" * 60)
    print(t("summary_title"))
    print("=" * 60)
    print(t("summary_original", n=original_count))
    print(t("summary_mrp_ativos", n=len(mrp_ativos_rows)))
    print(t("summary_it_pr1", n=len(it_pr1_rows)))
    print(t("summary_output", path=output_path))
    print("=" * 60)


if __name__ == "__main__":
    main()
