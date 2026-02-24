# Relatório de Stress Test — 30 Usuários

**Data:** 2026-02-23
**Ferramenta:** Locust 2.32.4
**Alvo:** https://doacao-whatsapp.onrender.com
**Configuração:** 30 usuários, rampa 6/s, duração 45s
**Distribuição:** HealthUser ×9 · ReadUser ×15 · WriteUser ×6

---

## Resumo Geral

| Métrica | Valor |
|---------|-------|
| Total de requisições | 27 |
| Falhas | 14 (51,85%) |
| RPS médio | 0,63 req/s |
| Latência média | 7 250 ms |
| Latência P95 | 36 000 ms |
| Latência P50 | 1 800 ms |

> **Status: FALHA** — O Render Free Tier não suportou 30 usuários simultâneos.
> A maioria dos endpoints retornou 503 Service Unavailable ou 502 Bad Gateway.

---

## Resultados por Endpoint

| Método | Endpoint | Reqs | Falhas | % Falha | P50 (ms) | P95 (ms) | Média (ms) |
|--------|----------|-----:|-------:|--------:|---------:|---------:|-----------:|
| GET | /api/health [GET] | 1 | 1 | 100% | 7 200 | 7 200 | 7 200 |
| POST | /api/health [POST] | 2 | 0 | 0% | 6 700 | 6 700 | 5 832 |
| GET | /api/ongs [GET] | 4 | 4 | 100% | 230 | 240 | 229 |
| GET | /api/ongs/:id [GET] | 4 | 4 | 100% | 240 | 240 | 235 |
| GET | /api/ongs?category=:cat | 4 | 4 | 100% | 230 | 250 | 230 |
| GET | /api/ongs?state=:uf | 2 | 1 | 50% | 4 800 | 4 800 | 2 514 |
| GET | /api/ongs [on_start] | 10 | 0 | 0% | 5 600 | 36 000 | 16 909 |

---

## Erros Registrados

| Método | Endpoint | Erro | Ocorrências |
|--------|----------|------|------------:|
| GET | /api/health [GET] | 502 Bad Gateway | 1 |
| GET | /api/ongs [GET] | 503 Service Unavailable | 4 |
| GET | /api/ongs/:id [GET] | 503 Service Unavailable | 4 |
| GET | /api/ongs?category=:cat | 503 Service Unavailable | 4 |
| GET | /api/ongs?state=:uf | 503 Service Unavailable | 1 |

---

## Diagnóstico

- **Ponto de ruptura confirmado**: a aplicação já colapsa com 30 usuários simultâneos.
- O throughput caiu para **0,63 req/s** (vs. 5,24 req/s com 20 usuários).
- Apenas o `POST /api/health` manteve-se saudável, possivelmente porque o Render
  priorizou a primeira conexão disponível durante a saturação.
- O `on_start` dos `ReadUser` chegou a aguardar **36 segundos** por uma resposta,
  indicando fila de conexões no servidor.

## Conclusão

O intervalo de colapso está **entre 20 e 30 usuários** no plano Free Tier do Render.
