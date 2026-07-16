# fidelidade-factual-juridica

Skill para agentes de IA (Claude Code e compatíveis) que aplica uma camada-base de
fidelidade factual a qualquer trabalho jurídico: nunca citar lei, jurisprudência ou
doutrina de memória, sempre buscar a fonte antes de recorrer a um placeholder, e separar
com clareza texto literal, paráfrase e análise própria.

Nasceu de um problema real: quatro skills jurídicas diferentes citavam essa camada-base
de memória, cada uma reescrevendo a regra com palavras próprias e já divergentes entre
si. Esta skill é a fonte única.

## Instalação

Copie a pasta para o diretório de skills do seu agente (ex.: `~/.claude/skills/` no
Claude Code) e referencie-a pelo nome `fidelidade-factual-juridica` a partir de outras
skills jurídicas.

## Licença

MIT — ver `LICENSE`.
