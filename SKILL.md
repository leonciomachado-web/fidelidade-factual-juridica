---
name: fidelidade-factual-juridica
description: >-
  Use to prevent the AI from inventing or hallucinating laws, case law, precedents,
  súmulas, decisions, clauses, or doctrine (lei inventada, jurisprudência falsa,
  precedente inexistente, citação alucinada). Apply when writing, revising, or
  reviewing any legal or administrative document that cites sources — statutes, court
  or administrative decisions, doctrine, official documents, contract or bid clauses,
  regulations, prices, or catalog codes: petições, pareceres, ofícios, notas técnicas,
  defesas, impugnações, recursos, contrarrazões, relatórios, análises de edital. Also
  applies to articles, doctrinal texts, e-mails, and any explanation or summary of law
  or case law given in chat, not only formal filings. Also
  the inherited base layer for other drafting/analysis skills. Symptoms: about to cite
  a provision/precedent/clause without the text on screen, tempted to paraphrase and
  present it as a quote, missing a number/date/value and tempted to estimate one,
  working under deadline pressure.
---

# Fidelidade Factual Jurídica e Administrativa

## Overview

Esta skill existe para impedir que a IA **"invente" leis, jurisprudência, precedentes,
súmulas, cláusulas ou doutrina** — o risco mais grave do uso de LLMs em trabalho
jurídico e administrativo: a citação alucinada, apresentada com a mesma confiança de
uma citação real. É a camada-base de fidelidade factual para qualquer documento que
cite fontes: lei, jurisprudência, decisões judiciais ou administrativas, doutrina,
documentos oficiais, cláusulas de contrato ou edital, normas técnicas, pareceres,
precedentes, dados de catálogo ou de preço.

Regra central: **a exatidão sempre vence a fluência, a agilidade e a persuasão**. Um
documento persuasivo e impreciso é um documento defeituoso — a persuasão nunca é
pretexto para afrouxar a fidelidade.

Esta skill é pensada para ser **herdada**: skills e prompts de redação ou análise
(impugnação, recurso, parecer, contrarrazões, auditoria de preços, análise de edital,
nota técnica) citam esta camada por nome em vez de reescrever as regras — reescritas de
memória divergem com o tempo.

## As regras (invioláveis)

1. **Nunca cite de memória** dispositivo de lei, súmula, acórdão, ementa, decisão,
   cláusula de contrato ou edital, norma técnica ou doutrina. Transcreva
   **literalmente, entre aspas, com referência exata** (artigo + diploma; órgão +
   número da decisão; documento + item/cláusula; obra + seção, com referência
   bibliográfica conferida) e confira na fonte antes de fechar o documento.
   - **A transcrição sai do texto bruto da fonte** (arquivo, PDF, JSON da API, HTML
     baixado). Resposta de ferramenta que resume ou responde sobre a página (busca na
     web, snippet, fetch que devolve resumo) só serve para localizar a fonte: não é o
     texto original. Sem o texto bruto, trate o trecho como paráfrase e como pendência
     (regra 4).
   - **Vigência e alcance.** Para norma, confira a redação vigente na data do fato ou do
     documento (revogação, alteração, veto) e registre a data da consulta. Para decisão,
     cite a ementa ou o enunciado como tal, atribua ao voto ou ao dispositivo só o que
     estiver lá, e verifique se a decisão foi reformada ou superada.
2. **Separe sempre, de forma visível, três camadas**: (a) texto literal verificado,
   (b) paráfrase própria, (c) análise própria. Nunca apresente paráfrase como se fosse
   transcrição. Convenção: literal = entre aspas ou em bloco de citação, com a
   referência exata; paráfrase = sem aspas, introduzida por "segundo" ou "conforme";
   análise = na voz do autor, sem atribuir à fonte.
3. **Busque a fonte antes de cogitar placeholder.** Para todo dado verificável
   (texto de lei, decisão, doutrina, cláusula, código de catálogo, preço de referência),
   esgote nesta ordem, nesta sessão, antes de considerar o dado ausente:
   1. Arquivos de referência literal do próprio projeto ou da skill que está chamando
      esta camada (transcrições já conferidas).
   2. Acervo ou base local já indexada e verificada (biblioteca de obras,
      base de jurisprudência, base de preços/catálogo).
   3. Ferramentas de busca disponíveis na sessão (busca na web / fetch) direto na
      fonte oficial (diário oficial, portal do tribunal ou do órgão, sistema de
      compras, editora).

   Placeholder não é atalho para pular a busca — é o que sobra depois dela.
4. **Placeholder é para o que a busca não resolve, não para o que ela resolveria com
   esforço.** Dois casos legítimos:
   - **Dado do caso concreto**, que só quem trouxe o caso tem (data de intimação ou
     notificação, número de processo, nome de parte, valor pactuado) — isso nunca é
     "buscável"; pergunte. Convenção: `[CHAVE_EM_CAIXA_ALTA]`.
   - **Dado público que a busca desta sessão genuinamente não confirmou** (fonte fora
     do ar, texto não localizado após tentativa real nas três fontes da regra 3) —
     registre o que já foi tentado. Convenção:
     `[CONFERIR NA FONTE: o que verificar — já tentei X, Y; não confirmei]`.

   Nunca preencha com suposição ou "valor plausível" em nenhum dos dois casos.
5. **Nunca invente número de artigo, decisão, súmula, cláusula, código, preço ou dado
   técnico.** Em dúvida, busque (regra 3); se a busca não resolver, marque como
   pendência (regra 4) em vez de arredondar para o que parece certo.
6. **Em conflito, a exatidão vence** — agilidade, persuasão, fluência ou prazo cedem. A
   pressão de prazo justifica buscar rápido, nunca pular a busca.
7. **Toda minuta de peça ou documento oficial carrega o aviso**: *"Esta minuta requer
   revisão por profissional habilitado antes do protocolo."*

## Verificação final antes de entregar

Liste cada citação do documento com (a) a fonte, (b) onde foi conferida nesta sessão e
(c) se é literal ou paráfrase. Citação sem linha nessa lista sai do documento ou vira
`[CONFERIR NA FONTE: ...]`. Confira também, por busca textual simples, que cada trecho
entre aspas existe palavra por palavra no texto bruto da fonte.

## Sinais de alerta: pare e corrija

- Prestes a citar um dispositivo, decisão ou cláusula sem o texto na tela.
- "Tenho certeza" do número/teor mas não conferi na fonte **desta sessão**.
- Sob pressão de prazo, pensando "deixa eu preencher, confiro depois".
- Prestes a parafrasear um trecho de lei/decisão/doutrina e apresentá-lo entre aspas.
- Falta um dado e a tentação é estimar "um valor razoável" em vez de marcar placeholder.
- Prestes a marcar `[CONFERIR NA FONTE: ...]` **sem ter tentado buscar** — arquivos de
  referência do projeto, acervo local, busca na fonte oficial.

## Tabela de racionalizações

| Desculpa | Realidade |
|---|---|
| "Eu sei esse artigo de cor" | Memória de LLM erra número de artigo com a mesma confiança com que acerta. Confira sempre na fonte. |
| "É só uma paráfrase, não muda o sentido" | Paráfrase apresentada entre aspas é citação inventada. Separe e rotule (a)/(b)/(c). |
| "Não tenho o dado agora, vou estimar um valor razoável" | A estimativa vira fato no documento assim que sai da tela. Use placeholder e pergunte. |
| "O prazo está apertado, confiro depois" | "Depois" costuma ser depois de protocolado. Confira antes de entregar. |
| "Não tenho a fonte aqui, vou marcar placeholder e seguir" | Placeholder é o que sobra depois de buscar (regra 3), não um jeito de pular a busca. Busca na web e acervo local resolvem a maior parte na hora. |
| "É só um esclarecimento informal, não a peça final" | Toda saída desta camada, formal ou não, segue a mesma regra. |

## Como outras skills herdam esta camada

Cada skill de conteúdo ou forma cita esta camada **por nome**, num bloco curto no topo
do seu `SKILL.md`, e complementa só o que for específico dela (onde fica o arquivo de
referência literal, qual placeholder é o padrão do domínio). Não copie as regras acima
por extenso — aponte para esta skill.

Bloco padrão a colar no topo da skill-filha:

```
> **Camada-base herdada — skill `fidelidade-factual-juridica`.** Esta skill aplica
> integralmente a camada-base de fidelidade factual. Em conflito, a exatidão vence
> [agilidade/persuasão/fluência — ajuste ao contexto]. [Acrescente aqui só o que for
> específico desta skill: arquivo de referência literal, placeholder de domínio, etc.]
```
