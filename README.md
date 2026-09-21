# ColetaCartolaFc

## Pessoa 1: API e conexao

Esta etapa consulta o endpoint `https://api.cartola.globo.com/atletas/mercado` e
prepara a conexao com o MongoDB.

### Estrutura da resposta da API

Na consulta realizada em 21/09/2026, o JSON retornou estas chaves de topo:

- `atletas`: lista com os jogadores disponiveis no mercado.
- `clubes`: mapa de identificadores de clubes para seus dados.
- `posicoes`: mapa de identificadores de posicoes para seus dados.
- `status`: mapa de identificadores de status para seus dados.

Cada item de `atletas` inclui, entre outros campos, `atleta_id`, `clube_id`,
`posicao_id`, `status_id`, `preco_num`, `pontos_num`, `media_num`, `scout`,
`nome`, `apelido`, `slug`, `foto` e `entrou_em_campo`. Os campos `clube_id`,
`posicao_id` e `status_id` permitem relacionar o atleta aos mapas de apoio.

### Configuracao

Requer Python 3.9 ou superior. Instale as dependencias:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Copie `.env.example` para `.env` e informe a URI do MongoDB em `MONGODB_URI`.
O arquivo `.env` esta ignorado pelo Git para evitar o vazamento de credenciais.

### Uso

```python
from api import buscar_dados_mercado
from conexao import conectar_mongodb

dados = buscar_dados_mercado()
db = conectar_mongodb()
```

`buscar_dados_mercado()` verifica erros HTTP com `raise_for_status()` e registra
falhas de rede ou de JSON. `conectar_mongodb()` faz um `ping` para confirmar a
conexao e retorna o banco `cartola_fc_db`.

Entrega da Pessoa 1: **Consegui conectar ao MongoDB e obter os dados da API em formato JSON.**