# 🧹 DataCleaner

Web app para limpeza automática de arquivos CSV e Excel (XLSX/XLS), construído com Flask + pandas.

## ✨ O que faz

- Remove linhas duplicadas
- Remove espaços extras em campos de texto
- Preenche valores nulos com `N/A`
- Padroniza nomes das colunas (minúsculas e sem espaços)
- Exibe prévia dos dados limpos antes do download
- Retorna o arquivo limpo em CSV

---

## 🚀 Rodando localmente

### Pré-requisitos
- Python 3.10+

### Instalação

```bash
git clone https://github.com/seu-usuario/data-cleaner.git
cd data-cleaner

python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install -r requirements.txt
python app.py
```

Acesse: [http://localhost:5000](http://localhost:5000)

---

## 🐳 Rodando com Docker

```bash
docker build -t data-cleaner .
docker run -p 5000:5000 data-cleaner
```

Acesse: [http://localhost:5000](http://localhost:5000)

---

## 📁 Estrutura do projeto

```
data-cleaner/
├── app.py               # Aplicação Flask
├── requirements.txt     # Dependências Python
├── Dockerfile           # Imagem Docker
├── .gitignore
├── README.md
├── templates/
│   └── index.html       # Interface web
├── uploads/             # Arquivos enviados (gerado automaticamente)
└── clean/               # Arquivos limpos (gerado automaticamente)
```

---

## 🔌 Endpoints da API

| Método | Rota | Descrição |
|--------|------|-----------|
| `GET` | `/` | Interface web |
| `POST` | `/upload` | Envia e processa o arquivo |
| `GET` | `/download/<filename>` | Baixa o arquivo limpo |

### Exemplo com `curl`

```bash
curl -X POST http://localhost:5000/upload \
  -F "file=@meus_dados.csv" \
  -o resultado.json
```

---

## 🛠 Tecnologias

- [Flask](https://flask.palletsprojects.com/)
- [pandas](https://pandas.pydata.org/)
- [openpyxl](https://openpyxl.readthedocs.io/)
- [Gunicorn](https://gunicorn.org/) (produção)
