"""
Ponto de entrada: lê os YAMLs modulares de input/, lê os requisitos da vaga em vaga.txt,
aplica o motor de pontuação inteligente por Tiers/Keywords, monta o
contexto e renderiza o template HTML final.
"""
import sys
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape

BASE_DIR = Path(__file__).resolve().parent
INPUT_DIR = BASE_DIR / "input"
TEMPLATES_DIR = BASE_DIR / "templates"
OUTPUT_DIR = BASE_DIR / "output"
SRC_DIR = BASE_DIR / "src"

sys.path.insert(0, str(SRC_DIR))

# Trocamos load_yaml por load_modular_resume
from yaml_io import load_modular_resume, load_yaml, resolve_placeholders  # noqa: E402
from selection import apply_selection  # noqa: E402
from context import prepare_context  # noqa: E402
from page_check import check_overflow, print_overflow_warning, compute_density  # noqa: E402
from pdf_export import export_pdf  # noqa: E402

VAGA_TXT = INPUT_DIR / "vaga.txt"
SECRETS = INPUT_DIR / "secrets.yaml"
OUTPUT_HTML = OUTPUT_DIR / "resume.html"
OUTPUT_PDF = OUTPUT_DIR / "resume.pdf"
TEMPLATE_NAME = "template.html"


def main():
    # AQUI ESTÁ A MÁGICA: O Python monta o quebra-cabeça dos arquivos para você
    master_raw = load_modular_resume(INPUT_DIR)
    secrets = load_yaml(SECRETS)

    master = resolve_placeholders(master_raw, secrets)

    # Lê a vaga de forma segura
    vaga_text = ""
    if VAGA_TXT.exists():
        vaga_text = VAGA_TXT.read_text(encoding="utf-8")
        print(f"[render] Lendo requisitos e palavras-chave de: {VAGA_TXT}")
    else:
        print("[render] Aviso: vaga.txt não encontrado. Gerando versão genérica por Tiers de peso.")

    # Processamento e montagem do contexto
    filtered = apply_selection(master, vaga_text)
    context = prepare_context(filtered)

    estimated_mm, usable_mm, overflow = check_overflow(
        context["body_sections"], context.get("extra_education")
    )
    if overflow:
        print_overflow_warning(estimated_mm, usable_mm)

    density = compute_density(
        context["body_sections"],
        context.get("extra_education"),
        context["competency_blocks"],
    )
    context["density"] = density
    print(
        f"[page_check] densidade calculada: experience={density['experience']} "
        f"side={density['side']} (1.0 = espaçamento normal)"
    )

    env = Environment(
        loader=FileSystemLoader(str(TEMPLATES_DIR)),
        autoescape=select_autoescape(["html", "xml"]),
        trim_blocks=True,
        lstrip_blocks=True,
    )

    template = env.get_template(TEMPLATE_NAME)
    html = template.render(**context)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_HTML.write_text(html, encoding="utf-8")
    print(f"HTML gerado em: {OUTPUT_HTML}")

    if export_pdf(OUTPUT_HTML, OUTPUT_PDF):
        print(f"PDF gerado em: {OUTPUT_PDF}")


if __name__ == "__main__":
    main()