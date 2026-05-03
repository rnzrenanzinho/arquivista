# Manual de Reconstrução do Arquivista

Este manual garante que o Arquivista possa ser recriado em outra máquina sempre que necessário.

## 1) Instalar Python
Instale Python 3.11 ou superior e confirme:

```bash
python --version
```

## 2) Baixar ou clonar o projeto
```bash
git clone <URL_DO_REPOSITORIO>
cd arquivista
```

## 3) Criar ambiente virtual
```bash
python -m venv .venv
```

Ativar no Linux/macOS:
```bash
source .venv/bin/activate
```

Ativar no Windows (PowerShell):
```powershell
.venv\Scripts\Activate.ps1
```

## 4) Instalar dependências
```bash
pip install -r requirements.txt
```

## 5) Rodar o app
```bash
python run.py
```

## 6) Preservar a pasta `data/`
A pasta `data/` guarda as bases de memória e backups. Nunca descarte esta pasta em migrações.

## 7) Fazer backup do projeto
Faça backup completo da pasta do projeto em mídia externa, nuvem confiável e repositório versionado.
