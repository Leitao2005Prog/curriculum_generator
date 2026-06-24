"""
Carregamento de arquivos YAML, suporte a múltiplos bancos modulares
e resolução de placeholders ${VARIAVEL} usando valores de um arquivo de secrets.
"""
import re
from pathlib import Path
import yaml

PLACEHOLDER_RE = re.compile(r"\$\{([A-Z0-9_]+)\}")


def load_yaml(path: Path):
    """Lê um arquivo YAML e devolve um dict (ou {} se o arquivo estiver vazio)."""
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def load_modular_resume(input_dir: Path) -> dict:
    """
    Lê os arquivos YAML modulares da pasta input/ e os combina em um único
    dicionário 'master' unificado na memória. 
    Blindado contra variações de nomes de arquivos (singular, plural, skills vs competence).
    """
    master = {}

    # 1. Carrega dados estruturais e introduções
    desc_path = input_dir / "description.yaml" if (input_dir / "description.yaml").exists() else input_dir / "descriptions.yaml"
    descriptions = load_yaml(desc_path)
    master.update(descriptions)

    # 2. Carrega as competências técnicas (Tentando skills.yaml, competence.yaml ou competences.yaml)
    comp_path = None
    for name in ["skills.yaml", "competence.yaml", "competences.yaml"]:
        if (input_dir / name).exists():
            comp_path = input_dir / name
            break
            
    if comp_path:
        competence = load_yaml(comp_path)
        master["skills_bank"] = competence.get("skills_bank", [])
    else:
        print("[yaml_io] Erro: Nenhum arquivo de competências encontrado (skills.yaml ou competence.yaml).")
        master["skills_bank"] = []

    # 3. Carrega o histórico de experiências
    exp_path = input_dir / "experience.yaml" if (input_dir / "experience.yaml").exists() else input_dir / "experiences.yaml"
    experiences = load_yaml(exp_path)
    master["experience_bank"] = experiences.get("experience_bank", [])

    # 4. Carrega as formações principais e complementares
    edu_path = input_dir / "education.yaml" if (input_dir / "education.yaml").exists() else input_dir / "educations.yaml"
    education = load_yaml(edu_path)
    master["education_bank"] = education.get("education_bank", [])
    master["extra_education_bank"] = education.get("extra_education_bank", [])

    return master
def resolve_placeholders(value, secrets):
    """
    Substitui recursivamente qualquer ${CHAVE} encontrada em strings
    (dentro de dicts, listas os strings soltas) pelo valor correspondente
    em `secrets`.
    """
    if isinstance(value, dict):
        return {k: resolve_placeholders(v, secrets) for k, v in value.items()}

    if isinstance(value, list):
        return [resolve_placeholders(v, secrets) for v in value]

    if isinstance(value, str):
        def repl(match):
            key = match.group(1)
            return str(secrets.get(key, match.group(0)))
        return PLACEHOLDER_RE.sub(repl, value)

    return value