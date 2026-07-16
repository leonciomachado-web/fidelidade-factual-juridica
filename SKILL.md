---
name: fidelidade-factual-juridica
description: >-
  Use when writing, revising, or reviewing any Brazilian legal document, brief, petition,
  opinion, or edital analysis (peça jurídica, impugnação, recurso, parecer, contrarrazões,
  pesquisa de preços, análise de edital) that cites law, jurisprudence, doctrine, prices,
  or catalog codes — or when any other legal skill in this workspace (redacao-juridica,
  recurso-tcu, contrarrazoes-agravo, pesquisa-precos-catmat, dilacao-prazo-defesa,
  impugnacao-edital, analise-edital) needs its inherited base layer of factual and
  citation fidelity. Symptoms this applies: about to cite an article/súmula/acórdão
  without the text on screen, tempted to paraphrase and present it as a quote, missing a
  price/date/process number and tempted to estimate one, working under deadline pressure.
---

# Fidelidade Factual Jurídica

## Overview

Camada-base herdada por toda skill jurídica deste workspace. Regra central: **a exatidão
sempre vence a fluência, a agilidade e a persuasão**. Uma peça persuasiva e imprecisa é uma
peça defeituosa — a persuasão nunca é pretexto para afrouxar a fidelidade.

Esta skill nasceu porque quatro skills (`redacao-juridica`, `recurso-tcu`,
`contrarrazoes-agravo`, `pesquisa-precos-catmat`) já citavam uma "camada-base herdada
`fidelidade-factual-juridica`" **de memória**, cada uma reescrevendo o texto com palavras
próprias e já divergentes entre si. Esta skill é a fonte única — as skills-filhas apontam
para ela em vez de reescrevê-la.

## As regras (invioláveis)

1. **Nunca cite de memória** dispositivo de lei, súmula, acórdão, ementa, cláusula de
   edital ou doutrina. Transcreva **literalmente, entre aspas, com referência exata**
   (artigo + diploma; órgão + número do acórdão; obra + seção pela referência ABNT
   conferida) e confira na fonte oficial antes de fechar a peça.
2. **Separe sempre, de forma visível, três camadas**: (a) texto literal verificado,
   (b) paráfrase própria, (c) análise própria. Nunca apresente paráfrase como se fosse
   transcrição.
3. **Busque a fonte antes de cogitar placeholder.** Para todo dado verificável
   publicamente (texto de lei, súmula, acórdão, doutrina, preço de catálogo, código
   CATMAT/PDM), esgote nesta ordem, nesta sessão, antes de considerar o dado ausente:
   1. Arquivo de referência literal da própria skill (ex.:
      `referencias/01-cpc-agravo-literal.md`).
   2. Acervo local já indexado (`base-de-teses/livros`, `jurisprudencia-tcu`,
      `CONTEXT.md`, bases de preço/CATMAT).
   3. Ferramentas de busca disponíveis nesta sessão (WebSearch/WebFetch) direto na
      fonte oficial (Planalto, tribunal, portal do órgão).

   Placeholder não é atalho para pular a busca — é o que sobra depois dela.
4. **Placeholder é para o que a busca não resolve, não para o que ela resolveria com
   esforço.** Dois casos legítimos:
   - **Dado do caso concreto**, que só quem trouxe o caso tem (data de intimação,
     número de processo, nome de parte) — isso nunca é "buscável"; pergunte. Convenção:
     `[CHAVE_EM_CAIXA_ALTA]`.
   - **Dado público que a busca desta sessão genuinamente não confirmou** (fonte fora
     do ar, texto não localizado após tentativa real nas três fontes da regra 3) —
     registre o que já foi tentado. Convenção:
     `[CONFERIR NA FONTE: o que verificar — já tentei X, Y; não confirmei]`.

   Nunca preencha com suposição ou "valor plausível" em nenhum dos dois casos.
5. **Nunca invente preço, código (CATMAT/PDM), número de artigo, acórdão, súmula ou dado
   técnico.** Em dúvida, busque (regra 3); se a busca não resolver, marque como
   pendência (regra 4) em vez de arredondar para o que parece certo.
6. **Em conflito, a exatidão vence** — agilidade, persuasão, fluência ou prazo cedem. A
   pressão de prazo justifica buscar rápido, nunca pular a busca.
7. **Toda minuta de peça carrega o aviso**: *"Esta minuta requer revisão por profissional
   habilitado antes do protocolo."*

## Sinais de alerta — pare e corrija

- Prestes a citar um artigo, súmula ou acórdão sem o texto na tela.
- "Tenho certeza" do número do dispositivo mas não conferi na fonte **desta sessão**.
- Sob pressão de prazo, pensando "deixa eu preencher, confiro depois".
- Prestes a parafrasear um trecho de lei/doutrina e apresentá-lo entre aspas.
- Falta um dado e a tentação é estimar "um valor razoável" em vez de marcar placeholder.
- Prestes a marcar `[CONFERIR NA FONTE: ...]` **sem ter tentado buscar** — arquivo de
  referência da skill, acervo local, WebSearch/WebFetch na fonte oficial.

## Tabela de racionalizações

| Desculpa | Realidade |
|---|---|
| "Eu sei esse artigo de cor" | Memória de LLM erra número de artigo com a mesma confiança com que acerta. Confira sempre na fonte. |
| "É só uma paráfrase, não muda o sentido" | Paráfrase apresentada entre aspas é citação inventada. Separe e rotule (a)/(b)/(c). |
| "Não tenho o dado agora, vou estimar um valor razoável" | A estimativa vira fato na peça assim que sai da tela. Use placeholder e pergunte. |
| "O prazo está apertado, confiro depois" | "Depois" costuma ser depois de protocolado. Confira antes de entregar. |
| "Não tenho a fonte aqui, vou marcar placeholder e seguir" | Placeholder é o que sobra depois de buscar (regra 3), não um jeito de pular a busca. WebSearch/WebFetch e o acervo local resolvem a maior parte na hora. |
| "É só um esclarecimento informal, não a peça final" | Toda saída desta camada, formal ou não, segue a mesma regra. |

## Como as skills-filhas herdam

Cada skill de conteúdo ou forma cita esta camada **por nome**, num bloco curto no topo do
seu `SKILL.md`, e complementa só o que for específico dela (onde fica o arquivo de
referência literal, qual placeholder é o padrão local). Não copie as regras acima por
extenso — aponte para esta skill.

Bloco padrão a colar no topo da skill-filha:

```
> **Camada-base herdada — skill `fidelidade-factual-juridica`.** Esta skill aplica
> integralmente a camada-base de fidelidade factual. Em conflito, a exatidão vence
> [agilidade/persuasão/fluência — ajuste ao contexto]. [Acrescente aqui só o que for
> específico desta skill: arquivo de referência literal, placeholder de domínio, etc.]
```

## Skills que herdam esta camada

Confirmadas (apontam para esta skill por nome): `redacao-juridica`, `recurso-tcu`,
`contrarrazoes-agravo`, `pesquisa-precos-catmat`. A skill `analise-edital` aplica uma
regra equivalente ("Fidelidade textual") de forma independente, com convenção de
placeholder própria (`[CONFERIR NA FONTE: ...]`) — compatível com esta camada, não
precisa mudar. A skill `impugnacao-edital` (`juridico/impugnacao/SKILL.md`) ainda não
referencia esta camada — candidata a receber o bloco padrão numa próxima revisão, mas
fora do escopo desta.
