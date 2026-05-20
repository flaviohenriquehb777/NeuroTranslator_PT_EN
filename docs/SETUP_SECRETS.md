# Configuração de Secrets (HF_TOKEN)

## 1) Gerar o token no Hugging Face

1. Acesse: https://huggingface.co/settings/tokens
2. Clique em **New token**
3. Selecione **Write** (necessário para fazer push no Space)
4. Garanta que você está logado no usuário dono do Space (neste projeto: **Flaviohb7**)
5. Copie o token gerado

## 2) Adicionar no GitHub Actions

1. Abra o repositório no GitHub
2. Vá em **Settings → Secrets and variables → Actions**
3. Clique em **New repository secret**
4. Nome: `HF_TOKEN`
5. Valor: cole o token do Hugging Face

## 3) OAuth (GitHub ↔ Hugging Face)

Se necessário, confira a conexão do GitHub no Hugging Face:
https://huggingface.co/settings/connected-applications
