#!/usr/bin/env python3
"""Hook SessionStart (startup|resume|clear|compact): lembrete da skill
fidelidade-factual-juridica no inicio da sessao e depois de cada compactacao.

Hooks nao invocam skills; este injeta a regra no contexto para que o modelo a
aplique ANTES de escrever, inclusive no chat e em formatos que o gate
(gate_fidelidade.py) nao alcanca, como .docx gerado por script.
"""
import json
import sys

MENSAGEM = (
    "REGRA DURA (fidelidade factual): antes de escrever, revisar ou resumir qualquer "
    "texto que cite lei, jurisprudencia, doutrina, clausula de edital ou contrato, ou "
    "dado verificavel (peca, parecer, artigo, e-mail, analise, ate resposta no chat), "
    "invoque a skill fidelidade-factual-juridica com a ferramenta Skill. Citacao so "
    "literal e conferida na fonte desta sessao; nunca de memoria, e nunca a partir de "
    "resumo de ferramenta (a resposta do WebFetch e o snippet de busca nao sao o texto "
    "original: buscar o texto bruto). O que a busca nao confirmar vira placeholder, "
    "nunca suposicao."
)

if __name__ == "__main__":
    try:
        print(
            json.dumps(
                {
                    "hookSpecificOutput": {
                        "hookEventName": "SessionStart",
                        "additionalContext": MENSAGEM,
                    }
                }
            )
        )
    except Exception:
        pass
    sys.exit(0)
