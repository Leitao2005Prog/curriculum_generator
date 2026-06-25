from pathlib import Path
import yaml

def check_tags():
    input_dir = Path("input")
    
    # 1. Carrega os Tiers
    comp_file = next((input_dir / n for n in ["skills.yaml", "competence.yaml", "competences.yaml"] if (input_dir / n).exists()), None)
    if not comp_file:
        print("❌ Arquivo de competências não encontrado.")
        return
        
    with open(comp_file, "r", encoding="utf-8") as f:
        comp_data = yaml.safe_load(f) or {}
        
    tier_config = comp_data.get("tier_config", {})
    # Junta todas as palavras que possuem um tier definido em um set para busca rápida
    mapped_tags = set()
    for tier_list in tier_config.values():
        for tag in tier_list:
            mapped_tags.add(tag.lower())
            
    # 2. Coleta todas as tags usadas nas skills e nas experiências
    used_tags = set()
    
    # Busca nas skills
    skills_bank = comp_data.get("skills_bank", [])
    for skill in skills_bank:
        for tag in skill.get("tags", []):
            used_tags.add(tag.lower())
            
    # Busca nas experiências
    exp_file = input_dir / "experience.yaml" if (input_dir / "experience.yaml").exists() else input_dir / "experiences.yaml"
    if exp_file.exists():
        with open(exp_file, "r", encoding="utf-8") as f:
            exp_data = yaml.safe_load(f) or {}
        for exp in exp_data.get("experience_bank", []):
            for tag in exp.get("tags", []):
                used_tags.add(tag.lower())
            for bullet in exp.get("bullets", []):
                for tag in bullet.get("tags", []):
                    used_tags.add(tag.lower())

    # 3. Compara
    unmapped = used_tags - mapped_tags
    
    if unmapped:
        print("⚠️  [LINTER] Existem tags usadas que NÃO estão mapeadas em nenhum Tier:")
        for tag in sorted(unmapped):
            print(f"  - {tag}")
        print("\n💡 Dica: Adicione-as no 'tier_config' do seu YAML de competências para garantir a pontuação correta.")
    else:
        print("✅ [LINTER] Tudo certo! Todas as tags estão mapeadas nos seus Tiers.")

if __name__ == "__main__":
    check_tags()