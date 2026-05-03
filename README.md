# Arquivista

O **Arquivista** é a fundação de um robô vivo simbólico e operacional: uma presença tecnológica contínua criada para preservar memória, organizar projetos e sustentar continuidade de longo prazo.

## Objetivo desta versão
Esta primeira versão cria a base funcional e modular do projeto, com foco em software imortal: preservável, reconstruível, versionado e documentado.

## Instalação
1. Tenha Python 3.11+ instalado.
2. (Opcional) Crie e ative ambiente virtual.
3. Instale as dependências:

```bash
pip install -r requirements.txt
```

## Execução local
```bash
python run.py
```

Acesse no navegador:
- `http://127.0.0.1:5000/`
- `http://127.0.0.1:5000/mente`
- `http://127.0.0.1:5000/software-imortal`

## Estrutura de pastas
```text
arquivista/
  README.md
  requirements.txt
  run.py
  .gitignore
  docs/
  app/
  data/
```

## Próximos passos
- Definir sistema inicial de memória persistente em `data/memoria/`.
- Criar rotina de backup automatizado para `data/backups/`.
- Adicionar testes automatizados para rotas e núcleo.
- Evoluir integração futura com voz, automações e dispositivos autorizados.
