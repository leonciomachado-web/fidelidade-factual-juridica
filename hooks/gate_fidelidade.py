#!/usr/bin/env python3
"""Hook PreToolUse (Write|Edit|MultiEdit): gate da skill fidelidade-factual-juridica.

Impede a gravacao de texto que contenha citacao de lei, artigo, sumula, acordao,
decreto etc. enquanto a skill fidelidade-factual-juridica nao tiver sido invocada
NESTA sessao. Hooks nao invocam skills; este apenas nega a gravacao ate que o modelo
a invoque (a mensagem de negacao diz como).

Quando dispara (arquivo de texto, fora das isencoes):
  (a) o texto gravado contem citacao legal/jurisprudencial, OU
  (b) o caminho contem algum fragmento listado em PASTAS_EXTRAS (vazio por padrao).

Como sabe se a skill ja foi invocada: le o transcript da sessao (transcript_path),
interpreta cada linha como JSON e procura (1) uma chamada real da ferramenta Skill ou
(2) um slash command digitado pelo usuario. Basta UMA invocacao por sessao.

Limites conhecidos (ver README): subagentes sao isentos; gravacao via Bash nao e
coberta; a liberacao vale pela sessao inteira, mesmo depois de compactacao; falha
ABERTO (libera) quando a skill nao e encontrada, o transcript nao esta legivel ou
ocorre qualquer erro interno.
"""
import json
import os
import re
import sys

SKILL = "fidelidade-factual-juridica"

# "deny" bloqueia a gravacao. "ask" pede decisao ao humano (melhor para quem prefere
# nao travar sessoes autonomas).
MODO = "deny"

# Ferramentas de gravacao examinadas.
FERRAMENTAS = {"Write", "Edit", "MultiEdit"}

# Extensoes de texto que o gate examina.
EXTENSOES = {".md", ".markdown", ".mdx", ".txt", ".rst", ".adoc", ".html", ".htm", ".rtf", ".tex"}

# Fragmentos de caminho que ativam o gate mesmo sem citacao no texto.
# Exemplo: ["/pecas/", "/casos/"]. Vazio = so o criterio de conteudo vale.
PASTAS_EXTRAS = []

# Caminhos que nunca disparam o gate.
ISENTOS = re.compile(
    r"(?i)(/node_modules/|/\.git/|/\.claude/|"
    r"(^|/)(CLAUDE|README|CHANGELOG|LICENSE)(\.[a-z]+)?$)"
)

_N = r"(?:n[º°o.]*\s*)?"  # "n.", "nº", "n°" opcional
_QUALIF = r"(?:(?:complementar|federal|estadual|municipal|ordin[aá]ria|legislativo)\s+)*"
_TRIB = r"(?:(?:tcu|stf|stj|tst|cnj)\s+)?"

CITACAO = re.compile(
    "(?i)("
    + "|".join(
        [
            r"\bart(?:igo)?s?\.?\s*\d",
            r"§\s*\d",
            r"\binciso\s+(?:[ivxlc]+|\d+)\b",
            r"\blei\s+" + _QUALIF + _N + r"\d",
            r"\blc\s+" + _N + r"\d",
            r"\bs[uú]mula\s+(?:vinculante\s+)?" + _TRIB + _N + r"\d",
            r"\bac[oó]rd[aã]o\s+" + _TRIB + _N + r"\d",
            r"\bdecreto(?:-lei)?\s+" + _QUALIF + _N + r"\d",
            r"\b(?:resp|aresp|agrg|agint|hc|rms|adi|adpf|adc|re|rcl|ms)\s*n?[º°.]*\s*\d[\d.]{2,}",
            r"\btema\s+(?:\d{1,3}\.\d{3}|\d{3,})\b",
            r"\btema\s+\d+\s+(?:do|da)\s+(?:stf|stj)",
            r"\bcf\s*/\s*\d{2}\b",
            r"\b(?:instru[cç][aã]o\s+normativa|portaria|resolu[cç][aã]o|medida\s+provis[oó]ria|enunciado)\s+(?:[\w/.-]+\s+)?"
            + _N
            + r"\d",
        ]
    )
    + ")"
)

_TAG_SLASH = re.compile(
    r"<command-name>/?(?:[\w.-]+:)?" + re.escape(SKILL) + r"</command-name>"
)


def skill_existe() -> bool:
    raizes = []
    projeto = os.environ.get("CLAUDE_PROJECT_DIR")
    if projeto:
        raizes.append(os.path.join(projeto, ".claude"))
    config = os.environ.get("CLAUDE_CONFIG_DIR")
    if config:
        raizes.append(config)
    raizes.append(os.path.join(os.path.expanduser("~"), ".claude"))
    return any(os.path.isfile(os.path.join(r, "skills", SKILL, "SKILL.md")) for r in raizes)


def _nome_bate(nome) -> bool:
    return isinstance(nome, str) and nome.split(":")[-1] == SKILL


def _percorre(no):
    """Itera todos os dicts aninhados de um objeto JSON."""
    if isinstance(no, dict):
        yield no
        for v in no.values():
            yield from _percorre(v)
    elif isinstance(no, list):
        for v in no:
            yield from _percorre(v)


def _textos_do_usuario(obj) -> list:
    """Textos digitados pelo usuario (nao inclui tool_result)."""
    if obj.get("type") != "user":
        return []
    conteudo = (obj.get("message") or {}).get("content")
    if isinstance(conteudo, str):
        return [conteudo]
    if isinstance(conteudo, list):
        return [
            b.get("text", "")
            for b in conteudo
            if isinstance(b, dict) and b.get("type") == "text"
        ]
    return []


def skill_ja_invocada(transcript: str) -> bool:
    with open(transcript, "r", encoding="utf-8", errors="replace") as f:
        for linha in f:
            if SKILL not in linha:
                continue
            try:
                obj = json.loads(linha)
            except ValueError:
                continue
            for no in _percorre(obj):
                if (
                    no.get("type") == "tool_use"
                    and no.get("name") == "Skill"
                    and _nome_bate((no.get("input") or {}).get("skill"))
                ):
                    return True
            if any(_TAG_SLASH.search(t) for t in _textos_do_usuario(obj)):
                return True
    return False


def textos_gravados(ferramenta: str, entrada: dict) -> str:
    if ferramenta == "Write":
        return entrada.get("content") or ""
    if ferramenta == "Edit":
        return entrada.get("new_string") or ""
    edicoes = entrada.get("edits") or []
    return "\n".join(
        e.get("new_string") or "" for e in edicoes if isinstance(e, dict)
    )


def negar(caminho: str) -> None:
    motivo = (
        f"BLOQUEADO: a skill {SKILL} ainda nao foi aplicada nesta sessao. "
        f"O arquivo '{caminho}' contem citacao de lei, jurisprudencia ou doutrina "
        "(ou esta numa pasta de trabalho juridico). Regra dura: nada citado de memoria; "
        "tudo transcrito literalmente da fonte, conferida nesta sessao. Faca agora: "
        f"(1) invoque a skill {SKILL} com a ferramenta Skill; "
        "(2) siga as regras dela (buscar a fonte antes de recorrer a placeholder, "
        "transcrever literal entre aspas com referencia exata, separar literal, "
        "parafrase e analise, nunca usar resumo de ferramenta como se fosse o texto "
        "original); (3) so entao regrave este arquivo. Depois de invocada uma vez, "
        "este bloqueio nao volta nesta sessao."
    )
    decisao = "ask" if MODO == "ask" else "deny"
    print(
        json.dumps(
            {
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": decisao,
                    "permissionDecisionReason": motivo,
                }
            }
        )
    )


def main() -> None:
    bruto = sys.stdin.buffer.read().decode("utf-8-sig", errors="replace")
    if not bruto.strip():
        return
    dados = json.loads(bruto)

    if dados.get("agent_id"):
        return
    ferramenta = dados.get("tool_name")
    if ferramenta not in FERRAMENTAS:
        return

    entrada = dados.get("tool_input") or {}
    if not isinstance(entrada, dict):
        return
    caminho = (entrada.get("file_path") or "").replace("\\", "/")
    if not caminho:
        return
    if os.path.splitext(caminho)[1].lower() not in EXTENSOES:
        return
    if ISENTOS.search(caminho):
        return

    texto = textos_gravados(ferramenta, entrada)
    tem_citacao = bool(texto and CITACAO.search(texto))
    em_pasta_extra = any(p.lower() in caminho.lower() for p in PASTAS_EXTRAS)
    if not (tem_citacao or em_pasta_extra):
        return

    if not skill_existe():
        return
    transcript = dados.get("transcript_path")
    if not transcript or not os.path.isfile(transcript):
        return
    if skill_ja_invocada(transcript):
        return

    negar(caminho)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass
    sys.exit(0)
