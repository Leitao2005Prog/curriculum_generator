"""
Monta a lista de contatos exibida na barra superior do currículo,
combinando os valores do YAML (address, phone, email, linkedin, github)
com o registro de tipos definido em icons.py.
"""
from icons import CONTACT_TYPES


def _normalize_value(ctx, key):
    """
    Lê um campo de contato do contexto. `address` pode vir como lista
    (múltiplas linhas no YAML) e nesse caso é unida com ', '.
    """
    raw = ctx.get(key)
    if isinstance(raw, list):
        return ", ".join(v for v in raw if v)
    return raw or ""


def build_contacts(ctx):
    """
    Devolve a lista de contatos prontos para o template, cada um como:
        {"key": ..., "icon": <svg>, "text": ..., "href": ... ou None}

    Itens sem valor no YAML são omitidos automaticamente.

    O texto exibido (`text`) é sempre o valor original do YAML (endereço,
    telefone, o email em si, ou a URL por extenso de linkedin/github) —
    nunca um link "técnico" como mailto:...?subject=... mesmo quando o
    `href` por trás é mais elaborado (caso do email, que vira um mailto:
    com assunto pré-preenchido).
    """
    contacts = []

    for contact_type in CONTACT_TYPES:
        value = _normalize_value(ctx, contact_type["key"])
        if not value:
            continue

        href = contact_type["make_href"](value, ctx)

        # linkedin/github mostram a URL completa como texto (decisão de
        # design já validada); os demais mostram o valor original do YAML.
        if href and contact_type["key"] in ("linkedin", "github"):
            text = href
        else:
            text = value

        contacts.append({
            "key": contact_type["key"],
            "icon": contact_type["icon"],
            "text": text,
            "href": href,
        })

    return contacts