# Inabalável — Autoestima, Autoconfiança e Autoeficácia

Manual pessoal, em português, sobre como construir autoestima, autoconfiança e autoeficácia que não dependem do resultado do mês — com fundamentação bíblica (NVI) e científica (estudos universitários), diagramas, protocolos práticos e um plano de 30 dias.

## O que é

Um site de página única, autocontido, dividido em dez partes:

| Parte | Conteúdo |
|---|---|
| 0 | Resumo em catorze linhas e seis trilhas de leitura |
| 1 | Diagnóstico — a anatomia dos quinze construtos em quatro andares, os três pilares, autoestima contingente, ciclo cognitivo, viés de negatividade, teoria do sociômetro, as seis dimensões de bem-estar, escassez e banda cognitiva |
| 2 | A lógica científica — Beck, Bandura, Baumeister, Neff, Dweck, Duckworth, Ericsson, Oettingen, Gollwitzer, Rosenthal, Kross, Rutledge, Crum, Waldinger, Brown, Tangney, Gilbert, Wood, Fogg, Milkman, Lally, Lembke, Worthington, Antonovsky, Vygotsky, Csikszentmihalyi, Fava, Seligman, Santos — e os mitos (lei da atração, mantras, pose de poder) |
| 3 | Fundamento bíblico — valor recebido, graça vs desempenho, culpa vs vergonha, restituição, apostas, renovação da mente, crítica à teologia da prosperidade, identidade depois do fracasso, autoesquecimento (1Co 4), José, o filho pródigo, Elias, cultura de honra e vergonha, falar com a própria alma, o lamento, palavras hebraicas |
| 4 | A ponte — onde Bíblia e ciência coincidem, onde não se encontram, e o que acontece quando a epidemiologia mede participação religiosa |
| 5 | Como construir — os sete mecanismos, declaração de identidade, comunidade, perdão, quando buscar ajuda, o autodiagnóstico interativo, e uma seção dedicada para cada pilar: autoimagem e os três "eus", autoconhecimento, autoaceitação, autorrespeito, amor-próprio, autoperdão, autoconfiança calibrada, autodisciplina, assertividade e autorresponsabilidade |
| 6 | Execução — rotina diária, plano de 30 dias com checklist, métricas de processo |
| 7 | As oito áreas da vida (com roda de avaliação) e a aplicação ao trabalho de SDR |
| 8 | Referências (estudos com links) e índice de versículos por tema |
| 9 | Onze fichas imprimíveis |
| 10 | Biblioteca comentada — tese, ideias práticas, capítulo de entrada e índice por dor |

Trinta diagramas em SVG inline, todos legíveis em tema claro e escuro.

## Autodiagnóstico

A Parte 5.6 traz sete instrumentos respondidos na própria página, com cálculo, faixas interpretativas e histórico com gráfico de evolução:

1. **Escala de Autoestima de Rosenberg** — adaptação brasileira de Hutz (2000), revisada por Hutz & Zanon (UFRGS, 2011)
2. **Escala de Autocompaixão, versão curta** — Neff & Raes (tradução livre)
3. **Contingências do valor pessoal** — versão reduzida inspirada em Crocker & Wolfe (não validada)
4. **As seis dimensões de bem-estar** — versão curta inspirada em Ryff (não validada)
5. **Inventário de integridade** (autorrespeito) — construído para este manual (não validado)
6. **Inventário de autoabandono** (amor-próprio) — construído para este manual (não validado)
7. **Calibragem de confiança por domínio** — construído para este manual (não validado)

Todos os dados ficam apenas no `localStorage` do navegador. Nada é enviado a lugar nenhum. Os instrumentos são de autoconhecimento e acompanhamento, não de diagnóstico clínico — isso está sinalizado na própria página.

## Como abrir

```bash
open autoestima-inabalavel/index.html      # macOS
xdg-open autoestima-inabalavel/index.html  # Linux
```

Basta abrir o arquivo no navegador — não há build, dependência nem servidor.

## Detalhes técnicos

- **Arquivo único**: HTML, CSS e JS inline; nenhuma requisição externa (compatível com a CSP de artifacts).
- **Tema**: acompanha o do sistema e tem alternador manual, persistido em `localStorage`.
- **Navegação**: índice lateral com busca (filtra por texto, sem acentuação) e scrollspy; seis trilhas de leitura na Parte 0.1 para quem não quer ler linearmente.
- **Checklists e autodiagnóstico**: marcações, notas da roda das áreas e histórico de pontuações ficam salvos no navegador (`localStorage`).
- **Impressão**: `@media print` esconde navegação e evita quebra dentro dos blocos — as fichas da Parte 9 saem prontas para uso em papel.
- **Acessibilidade**: cada `figure` tem `figcaption` e cada `svg` tem `role="img"` com `aria-label`.

## Republicar como artifact

O mesmo `index.html` é a fonte publicada. Depois de editar, republicar com a ferramenta Artifact apontando para o mesmo caminho de arquivo mantém a mesma URL.

## Aviso

Material de estudo e treino. Não substitui acompanhamento psicológico, médico ou pastoral. Em emergência no Brasil: **CVV 188** (24h, gratuito) ou o CAPS mais próximo.
