# Guia de Contribuição

Obrigado pelo interesse em contribuir com o NeuroTranslator PT-EN! Este documento fornece diretrizes para contribuições.

## 🚀 Como Contribuir

### 1. Fork e Clone
```bash
git fork https://github.com/seu-usuario/NeuroTranslator_PT_EN
git clone https://github.com/seu-usuario/NeuroTranslator_PT_EN.git
cd NeuroTranslator_PT_EN
```

### 2. Configuração do Ambiente
```bash
# Instalar dependências
pip install -r requirements.txt

# Executar testes
python -m pytest tests/

# Iniciar servidor de desenvolvimento
cd web
python -m http.server 8000
```

### 3. Estrutura de Branches
- `main`: Branch principal (produção)
- `develop`: Branch de desenvolvimento
- `feature/nome-da-feature`: Novas funcionalidades
- `fix/nome-do-bug`: Correções de bugs
- `docs/nome-da-doc`: Atualizações de documentação

### 4. Padrões de Código

#### Python
- Seguir PEP 8
- Usar type hints
- Documentar funções com docstrings
- Cobertura de testes > 80%

#### JavaScript
- Usar ES6+
- Comentários JSDoc para funções principais
- Seguir padrões de nomenclatura consistentes

#### Commits
```
tipo(escopo): descrição breve

Descrição detalhada (opcional)

Closes #123
```

Tipos: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

### 5. Pull Request

1. Criar branch a partir de `develop`
2. Implementar mudanças
3. Adicionar/atualizar testes
4. Atualizar documentação
5. Fazer commit seguindo padrões
6. Abrir PR para `develop`

#### Template de PR
```markdown
## Descrição
Breve descrição das mudanças

## Tipo de Mudança
- [ ] Bug fix
- [ ] Nova funcionalidade
- [ ] Breaking change
- [ ] Documentação

## Testes
- [ ] Testes passando
- [ ] Novos testes adicionados
- [ ] Testado manualmente

## Checklist
- [ ] Código segue padrões do projeto
- [ ] Self-review realizado
- [ ] Documentação atualizada
```

## 🐛 Reportar Bugs

Use o template de issue para bugs:
- Descrição clara do problema
- Passos para reproduzir
- Comportamento esperado vs atual
- Screenshots (se aplicável)
- Ambiente (OS, browser, versão)

## 💡 Sugerir Funcionalidades

Para novas funcionalidades:
- Descrever o problema que resolve
- Propor solução detalhada
- Considerar alternativas
- Avaliar impacto na performance

## 📋 Processo de Review

1. **Automático**: CI/CD verifica testes e linting
2. **Manual**: Maintainer revisa código e funcionalidade
3. **Aprovação**: Merge após aprovação e testes passando

## 🏷️ Versionamento

Seguimos [Semantic Versioning](https://semver.org/):
- `MAJOR`: Breaking changes
- `MINOR`: Novas funcionalidades (backward compatible)
- `PATCH`: Bug fixes

## 📞 Contato

- Issues: Para bugs e funcionalidades
- Discussions: Para perguntas gerais
- Email: [seu-email@exemplo.com]

## 📄 Licença

Ao contribuir, você concorda que suas contribuições serão licenciadas sob a mesma licença do projeto.