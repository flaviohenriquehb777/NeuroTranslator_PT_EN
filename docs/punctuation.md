# Pontuação automática (fala)

Quando você usa o microfone (Web Speech API), o texto reconhecido costuma vir sem pontuação. Para melhorar legibilidade, qualidade de tradução e naturalidade do TTS, o NeuroTranslator aplica um pós-processamento offline no texto final reconhecido.

## Pipeline

1. Recebe o texto final do reconhecimento (raw)
2. Normaliza espaços e capitaliza a primeira palavra
3. Aplica regras conservadoras de pontuação (offline)
4. Atualiza o campo “Texto Original” com a versão pontuada
5. Traduz usando o texto pontuado

## Regras locais (offline)

- Vírgula após marcadores iniciais: “então”, “aliás”, “enfim”, “assim”, “na verdade”
- Vírgula antes de conectores quando aparecem no meio: “mas”, “porém”, “contudo”, “porque”, “por isso”, “ou seja”
- Interrogação em perguntas simples no PT quando começam com: “como”, “quando”, “onde”, “qual”, “quais”, “quem”, “por que”, “por quê”, “o que”, “que horas”
- Finalização conservadora com ponto em frases mais longas, se não houver pontuação terminal

## Métricas

O painel de métricas (📊) mostra:

- engine usada (ex.: `local-rules`)
- latência de pontuação
- número de mudanças aplicadas

## Limitações

- As regras são intencionalmente conservadoras (preferem “menos pontuação” a pontuação agressiva).
- O resultado pode não atingir a qualidade de modelos proprietários em casos ambíguos.

