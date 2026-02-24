# DoaZap — Stress Test

Script de carga para a API DoaZap utilizando [Locust](https://locust.io/).

## Pré-requisitos

- Python 3.11+

## Instalação

```bash
cd stress-test
pip install -r requirements.txt
cp .env.example .env
# Edite .env com suas credenciais
```

## Configuração (`.env`)

| Variável | Descrição | Default |
|----------|-----------|---------|
| `BASE_URL` | URL base da API | `https://doacao-whatsapp.onrender.com` |
| `API_KEY` | Chave para rotas protegidas de ONGs | — |

## Cenários

| Classe | Peso | Endpoints |
|--------|:----:|-----------|
| `HealthUser` | 3 | `GET /api/health`, `POST /api/health` |
| `ReadUser` | 5 | `GET /api/ongs`, `GET /api/ongs/:id` |
| `WriteUser` | 2 | `POST /api/ongs` → `PUT` → `DELETE` |

> `WriteUser` rastreia internamente o ID criado e o remove ao final do ciclo,
> garantindo que nenhuma ONG "suja" permaneça no banco.

## Como executar

### Com UI web (recomendado)

```bash
locust -f locustfile.py
```

Acesse `http://localhost:8089` e configure:
- **Host:** `https://doacao-whatsapp.onrender.com`
- **Number of users:** 20
- **Spawn rate:** 2

### Headless (CI/CD)

```bash
# 50 usuários, rampa de 5/s, durante 2 minutos, com relatório HTML
locust -f locustfile.py \
  --headless \
  --host https://doacao-whatsapp.onrender.com \
  -u 50 -r 5 \
  --run-time 2m \
  --html report.html \
  --csv results
```

Os arquivos `report.html`, `results_stats.csv` e `results_failures.csv` serão gerados
no diretório atual.

## Interpretando os resultados

| Métrica | Referência saudável |
|---------|---------------------|
| RPS (requests/s) | > 10 para endpoints de leitura |
| P95 latência GET /health | < 500 ms |
| P95 latência GET /ongs | < 1 000 ms |
| P95 latência POST /ongs | < 2 000 ms |
| Taxa de falhas | < 1% |
