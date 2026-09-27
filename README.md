# ColetaCartolaFC

Pipeline ETL em Python que coleta dados da API não oficial do Cartola FC
e os armazena em um cluster MongoDB, separados em três coleções distintas.

---

## Visão Geral do Projeto

```
ColetaCartolaFC/
├── .env             ← Credenciais locais (NÃO versionar)
├── .env.example     ← Modelo de variáveis de ambiente
├── .gitignore
├── requirements.txt
├── api.py           ← Pessoa 1 — Extração (chamada à API)
├── conexao.py       ← Pessoa 1 — Conexão ao MongoDB
├── processamento.py ← Pessoa 2 — Transformação e Carga (ETL Core)
└── main.py          ← Pessoa 2 — Orquestração (ponto de entrada)
```

---

## Pré-requisitos

- Python 3.9 ou superior
- MongoDB acessível (local ou Atlas)
- Acesso à internet (para chamar a API do Cartola FC)

---

## Configuração do Ambiente

### 1. Criar e ativar o ambiente virtual

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

> **Linux/macOS:** `source .venv/bin/activate`

### 2. Instalar as dependências

```powershell
python -m pip install -r requirements.txt
```

### 3. Configurar as variáveis de ambiente

Copie o arquivo de exemplo e edite com os seus dados:

```powershell
Copy-Item .env.example .env
```

Abra o `.env` e ajuste os valores:

```dotenv
# URI de conexão ao MongoDB
# Exemplo local:  mongodb://localhost:27017
# Exemplo Atlas:  mongodb+srv://<usuario>:<senha>@<cluster>.mongodb.net/
MONGODB_URI=mongodb://localhost:27017

# Nome do banco de dados de destino
DATABASE_NAME=cartola_fc_db
```

> O arquivo `.env` está listado no `.gitignore` e **nunca** deve ser versionado.

---

## Como Executar

Com o ambiente virtual ativado e o `.env` configurado, execute:

```powershell
python main.py
```

### Saída esperada

```
Conectando ao MongoDB...
Buscando dados na API...
Gravando dados dos clubes...
Gravando dados dos atletas...
Gravando status do mercado...
Finalizado com sucesso.
```

Os logs detalhados (com timestamp e nível) são exibidos durante a execução,
por exemplo:

```
2026-09-27T16:32:12 [INFO] conexao: Conexao com o MongoDB estabelecida. Banco: cartola_fc_db
2026-09-27T16:32:12 [INFO] api: Dados do mercado obtidos com sucesso.
2026-09-27T16:32:12 [INFO] processamento: Clubes processados: 20 inseridos, 0 atualizados.
2026-09-27T16:32:12 [INFO] processamento: Atletas inseridos: 780 documentos.
2026-09-27T16:32:12 [INFO] processamento: Status do mercado inserido com sucesso.
```

---

## Coleções no MongoDB

Todas as coleções são criadas automaticamente no banco `cartola_fc_db`
(configurável via `DATABASE_NAME` no `.env`).

### `clubes_rodada_atual`

Estratégia: **`UpdateOne` com `upsert=True`** — atualiza o clube se já existir,
insere se for novo. Nunca gera duplicatas.

```json
{
  "_id": 293,
  "nome": "Fluminense",
  "abreviacao": "FLU",
  "escudos": {
    "60x60": "https://s.sde.globo.com/.../fluminense_60x60.png",
    "45x45": "https://s.sde.globo.com/.../fluminense_45x45.png",
    "30x30": "https://s.sde.globo.com/.../fluminense_30x30.png"
  },
  "nome_fantasia": "Fluminense"
}
```

### `atletas_rodada_atual`

Estratégia: **`delete_many` + `insert_many`** — limpa tudo antes de inserir,
garantindo que apenas os dados da última consulta estejam presentes.
Cada atleta recebe o campo `timestamp_coleta`.

```json
{
  "atleta_id": 37624,
  "nome": "Fábio",
  "apelido": "Fábio",
  "foto": "https://s.sde.globo.com/.../fabio_220x220.png",
  "preco_num": 5.33,
  "variacao_num": -0.42,
  "clube_id": 262,
  "posicao_id": 1,
  "status_id": 7,
  "jogos_num": 15,
  "pontos_num": 3.4,
  "media_num": 2.22,
  "scout": { "DS": 51, "SG": 3 },
  "timestamp_coleta": "2026-09-27T19:32:12+00:00"
}
```

### `mercado_rodada_atual`

Estratégia: **`delete_many` + `insert_one`** — mantém apenas o status mais recente.
O documento recebe `timestamp_coleta`.

```json
{
  "rodada_atual": 19,
  "status_mercado": 1,
  "aviso": "",
  "fechamento": {
    "dia": 17, "mes": 8, "ano": 2024,
    "hora": 15, "minuto": 0,
    "timestamp": 1723917600
  },
  "timestamp_coleta": "2026-09-27T19:32:12+00:00"
}
```

---

## Fonte de Dados

- **Endpoint:** `https://api.cartola.globo.com/atletas/mercado`
- **Tipo:** GET público (sem autenticação)
- **Chaves retornadas:** `atletas`, `clubes`, `posicoes`, `status`,
  `rodada_atual`, `status_mercado`, `aviso`, `fechamento`

---

## Dependências

| Biblioteca | Versão | Uso |
|---|---|---|
| `requests` | ≥ 2.31, < 3 | Chamadas HTTP à API |
| `pymongo` | ≥ 4.6, < 5 | Driver MongoDB |
| `python-dotenv` | ≥ 1.0, < 2 | Leitura do `.env` |

---

## Entregas

- **Pessoa 1:** Consegui conectar ao MongoDB e obter os dados da API em formato JSON.
- **Pessoa 2:** Implementei o módulo de processamento ETL e a orquestração completa do pipeline.