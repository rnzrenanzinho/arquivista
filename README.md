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


## Memória do Arquivista
- Os COREs ficam em `data/memoria/`.
- Cada CORE é um arquivo JSON independente e legível.
- Essa memória é simples, exportável e reconstruível.
- Novos COREs podem ser adicionados criando novos arquivos `.json`.
- A rota `/memoria` mostra os COREs carregados.
- A rota `/memoria/<nome_arquivo>` mostra os detalhes de um CORE específico.

## Deploy Online
Este projeto está pronto para deploy automático em serviços conectados ao GitHub, como Render e Railway.

### Pré-requisitos
- Repositório no GitHub com este projeto.
- Arquivos de deploy presentes na raiz:
  - `requirements.txt` (dependências)
  - `Procfile` (comando web)
  - `runtime.txt` (versão do Python)

### Comando local (desenvolvimento)
```bash
python run.py
```

### Comando de produção sugerido
```bash
gunicorn run:app
```

### Passos para conectar no Render (deploy automático)
1. Faça push do código para o GitHub.
2. No Render, clique em **New +** > **Web Service**.
3. Conecte sua conta GitHub e selecione o repositório `arquivista`.
4. Configure:
   - **Runtime**: Python
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn run:app`
5. Salve e crie o serviço.
6. A cada novo push na branch configurada, o deploy será automático.

### Passos para conectar no Railway (deploy automático)
1. Faça push do código para o GitHub.
2. No Railway, clique em **New Project** > **Deploy from GitHub repo**.
3. Selecione o repositório `arquivista`.
4. O Railway detectará Python automaticamente; confirme o start command:
   - `gunicorn run:app`
5. Conclua a criação do projeto.
6. Novos pushes no GitHub disparam deploy automático.
