# fidelidade-factual-juridica

Skill para agentes de IA (Claude Code e compatíveis) que **impede a IA de "inventar"
leis, jurisprudência, precedentes, súmulas ou doutrina** — a citação alucinada é o
risco mais grave do uso de LLMs em trabalho jurídico e administrativo, porque sai com
a mesma confiança de uma citação real.

Aplica uma camada-base de fidelidade factual a qualquer documento que cite fontes —
lei, jurisprudência, decisões judiciais ou administrativas, doutrina, documentos
oficiais, cláusulas de contrato ou edital, normas técnicas, preços e códigos de
catálogo. Regras centrais: nunca citar de memória, sempre buscar a fonte antes de
recorrer a um placeholder, e separar com clareza texto literal, paráfrase e análise
própria.

Nasceu de um problema real: quatro skills jurídicas diferentes citavam essa camada-base
de memória, cada uma reescrevendo a regra com palavras próprias e já divergentes entre
si. Esta skill é a fonte única, pensada para ser herdada por outras skills de redação
e análise (impugnação, recurso, parecer, contrarrazões, nota técnica, auditoria de
preços, análise de edital).

## Instalação

Copie a pasta para o diretório de skills do seu agente (ex.: `~/.claude/skills/` no
Claude Code) e referencie-a pelo nome `fidelidade-factual-juridica` a partir de outras
skills jurídicas.

## Hooks opcionais (aplicação automática)

Sozinha, a skill só age quando é invocada. Para que o agente a aplique sem depender de
lembrar, a pasta `hooks/` traz dois hooks em Python 3 (funcionam em Linux, macOS,
Windows e no Claude Code na web, sem PowerShell):

| Hook | Evento | O que faz |
|---|---|---|
| `lembrete_fidelidade.py` | `SessionStart` | Injeta a regra no início da sessão e após cada compactação. Não bloqueia nada. |
| `gate_fidelidade.py` | `PreToolUse` (`Write\|Edit\|MultiEdit`) | Nega a gravação de texto com citação de lei, artigo, súmula, acórdão, decreto, resolução etc. até a skill ser invocada na sessão. Depois de uma invocação, não bloqueia mais. |

**Comece só pelo lembrete.** O bloqueio é opcional: ative-o depois de ver o lembrete
funcionar e só se você quiser a trava mecânica.

### O que o gate NÃO faz (leia antes de confiar nele)

O gate é um cinto de segurança para arquivos de texto, não uma garantia:

- **Subagentes são isentos.** Se o agente principal delega a redação a um subagente, o
  que o subagente grava não passa pelo gate. É uma decisão de projeto: o agente
  principal deve conferir o que o subagente devolve.
- **Verifica uma invocação por sessão, não a aplicação das regras.** Depois de uma
  compactação o texto da skill pode sair do contexto, mas o gate continua liberado. O
  lembrete (que roda de novo após a compactação) mitiga, mas não substitui a conferência.
- **Não cobre gravação via Bash** (`cat > arquivo.md`, scripts), `.docx`/`.pdf` gerados
  por script, `NotebookEdit` nem texto de chat. Para esses vale o lembrete.
- **A detecção de citação é por padrões e é curta de propósito.** Pega formas comuns
  (`art. 5`, `Lei nº 14.133`, `Súmula 331`, `Acórdão 1234/2023`, `REsp 1.234.567`,
  `Tema 1.075`, `CF/88`, `§ 2º`, `Instrução Normativa 67` etc.), mas não todas, e tem
  falsos positivos (`art. 5` num texto que nada tem de jurídico). Em `Edit`, só o trecho
  novo é examinado.
- **Falha aberto e em silêncio**: se a skill não for encontrada (procura em
  `$CLAUDE_PROJECT_DIR/.claude/skills/`, `$CLAUDE_CONFIG_DIR/skills/` e
  `~/.claude/skills/`), se o transcript não estiver legível ou se ocorrer qualquer erro,
  o gate libera a gravação e não avisa. Faça o autoteste abaixo para saber se ele está
  ativo no seu ambiente.

### Instalação no projeto (vale também na nuvem)

1. Copie `SKILL.md` para `.claude/skills/fidelidade-factual-juridica/SKILL.md` do
   repositório.
2. Copie o **conteúdo** de `hooks/` para `.claude/hooks/`, de modo que o resultado seja
   `.claude/hooks/lembrete_fidelidade.py` e `.claude/hooks/gate_fidelidade.py`
   (e não `.claude/hooks/hooks/...`).
3. Copie um dos exemplos de `exemplos/` para `.claude/settings.json` (ou mescle com o
   que já existir):
   - `settings.so-lembrete.json`: só o lembrete (recomendado como ponto de partida);
   - `settings.lembrete-e-bloqueio.json`: lembrete mais o gate.
4. Faça commit. O Claude Code na web lê `.claude/` do repositório clonado.

Para instalar só para o seu usuário, use `~/.claude/skills/`, `~/.claude/hooks/` e
`~/.claude/settings.json`, trocando `$CLAUDE_PROJECT_DIR/.claude/hooks/` por
`$HOME/.claude/hooks/` nos comandos.

#### Windows

Os comandos dos exemplos usam sintaxe de shell POSIX (Git Bash, Linux, macOS, nuvem).
Se o seu Claude Code no Windows executa os hooks em outro shell, a variável precisa ser
escrita na sintaxe desse shell, senão o caminho fica errado e o hook **não roda, sem
erro visível**:

| Shell que executa o hook | Comando |
|---|---|
| Bash (Git Bash, Linux, macOS, nuvem) | `python3 "$CLAUDE_PROJECT_DIR/.claude/hooks/gate_fidelidade.py"` |
| PowerShell | `python3 "$env:CLAUDE_PROJECT_DIR/.claude/hooks/gate_fidelidade.py"` |
| cmd.exe | `python3 "%CLAUDE_PROJECT_DIR%\.claude\hooks\gate_fidelidade.py"` |

Em testes, a forma de Bash falhou no PowerShell e no cmd (a variável não expande e o
Python não acha o arquivo), e as formas corretas de cada shell funcionaram.

Se `python3` não existir no Windows (ou for o atalho da Microsoft Store), use `py -3`
ou `python` no lugar. O lançador `py -3` funcionou em PowerShell e cmd nos testes.
Para saber qual shell o seu Claude Code usa para hooks, rode o autoteste abaixo e veja
se ele imprime o `deny`.

**Hooks executam código no seu computador.** Leia os dois arquivos `.py` antes de
habilitá-los (são curtos, não fazem rede, não executam comandos e não escrevem em disco).

### Autoteste do gate

Com a skill instalada, rode no raiz do projeto (o transcript é um arquivo qualquer que
não contém a invocação da skill):

```
echo '{}' > /tmp/transcript.jsonl
echo '{"tool_name":"Write","transcript_path":"/tmp/transcript.jsonl","tool_input":{"file_path":"x.md","content":"conforme o art. 5"}}' \
  | CLAUDE_PROJECT_DIR=. python3 .claude/hooks/gate_fidelidade.py
```

Se o gate estiver ativo, ele imprime um JSON com `"permissionDecision": "deny"`. Se não
imprimir nada, ele não está encontrando a skill ou o transcript e está liberando tudo.

### Ajustes

- **`MODO`** no topo de `gate_fidelidade.py`: `"deny"` bloqueia; `"ask"` pede decisão a
  uma pessoa (melhor para não travar sessões autônomas).
- **`PASTAS_EXTRAS`**: preencha com fragmentos de caminho (ex.: `["/pecas/"]`) para o
  gate disparar nessas pastas mesmo sem citação no texto.

## Licença

MIT — ver `LICENSE`.
