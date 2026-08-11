# Inabalável — Autoestima, Autoconfiança e Autoeficácia

Manual pessoal, em português, sobre como construir autoestima, autoconfiança e autoeficácia que não dependem do resultado do mês — com fundamentação bíblica (NVI) e científica (estudos universitários), diagramas, protocolos práticos e um plano de 30 dias.

## O que é

Um site de página única, autocontido, dividido em nove partes:

| Parte | Conteúdo |
|---|---|
| 0 | Resumo em dez linhas e como usar o material |
| 1 | Diagnóstico — os três pilares, autoestima contingente, o ciclo cognitivo, viés de negatividade |
| 2 | A lógica científica — Beck, Bandura, Baumeister, Neff, Dweck, Duckworth, Ericsson, Oettingen, Gollwitzer, Rosenthal, e os mitos (lei da atração, mantras, pose de poder) |
| 3 | Fundamento bíblico — valor recebido, graça vs desempenho, culpa vs vergonha, restituição, apostas, renovação da mente, crítica à teologia da prosperidade, identidade depois do fracasso |
| 4 | A ponte — onde Bíblia e ciência coincidem e onde não se encontram |
| 5 | Como construir — os sete mecanismos, declaração de identidade, comunidade, perdão, quando buscar ajuda |
| 6 | Execução — rotina diária, plano de 30 dias com checklist, métricas de processo |
| 7 | Aplicação no trabalho de SDR |
| 8 | Referências (estudos com links) e índice de versículos por tema |
| 9 | Seis fichas imprimíveis |

Quinze diagramas em SVG inline, todos legíveis em tema claro e escuro.

## Como abrir

```bash
open autoestima-inabalavel/index.html      # macOS
xdg-open autoestima-inabalavel/index.html  # Linux
```

Basta abrir o arquivo no navegador — não há build, dependência nem servidor.

## Detalhes técnicos

- **Arquivo único**: HTML, CSS e JS inline; nenhuma requisição externa (compatível com a CSP de artifacts).
- **Tema**: acompanha o do sistema e tem alternador manual, persistido em `localStorage`.
- **Checklists**: as marcações das Partes 6 e 9 ficam salvas no navegador (`localStorage`).
- **Impressão**: `@media print` esconde navegação e evita quebra dentro dos blocos — as fichas da Parte 9 saem prontas para uso em papel.
- **Acessibilidade**: cada `figure` tem `figcaption` e cada `svg` tem `role="img"` com `aria-label`.

## Republicar como artifact

O mesmo `index.html` é a fonte publicada. Depois de editar, republicar com a ferramenta Artifact apontando para o mesmo caminho de arquivo mantém a mesma URL.

## Aviso

Material de estudo e treino. Não substitui acompanhamento psicológico, médico ou pastoral. Em emergência no Brasil: **CVV 188** (24h, gratuito) ou o CAPS mais próximo.
