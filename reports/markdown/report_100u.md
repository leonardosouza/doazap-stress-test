# Stress Test — 100 Usuários Simultâneos

**Data:** 2026-02-23  
**Alvo:** https://doacao-whatsapp.onrender.com  
**Configuração:** 100 usuários · rampa 10/s · duração 60s

## Resultados por Endpoint

| Endpoint | Reqs | Falhas | %Falha | Avg (ms) | P95 (ms) | P99 (ms) | RPS |
|---|---:|---:|---:|---:|---:|---:|---:|
| `/api/health [GET]` | 15 | 12 | 80.0% | 2957 | 35000 | 35000 | 0.26 ⚠️ |
| `/api/health [POST]` | 11 | 8 | 72.7% | 4032 | 35000 | 35000 | 0.19 ⚠️ |
| `/api/ongs [GET]` | 14 | 13 | 92.9% | 461 | 3400 | 3400 | 0.24 ⚠️ |
| `/api/ongs [POST]` | 11 | 10 | 90.9% | 498 | 2300 | 2300 | 0.19 ⚠️ |
| `/api/ongs [on_start]` | 15 | 0 | 0.0% | 8700 | 34000 | 34000 | 0.26 |
| `/api/ongs/:id [GET]` | 14 | 13 | 92.9% | 2594 | 33000 | 33000 | 0.24 ⚠️ |
| `/api/ongs?category=:cat [GET]` | 10 | 9 | 90.0% | 457 | 2500 | 2500 | 0.17 ⚠️ |
| `/api/ongs?state=:uf [GET]` | 10 | 10 | 100.0% | 295 | 700 | 700 | 0.17 ⚠️ |
| **TOTAL** | **100** | **75** | **75.0%** | **2750** | **34000** | **35000** | **1.71** |

## Erros

| Método | Endpoint | Erro | Ocorrências |
|---|---|---|---:|
| `POST` | `/api/health [POST]` | 503 Server Error: Service Unavailable for url: /api/health [POST] | 8 |
| `GET` | `/api/ongs?state=:uf [GET]` | 503 Server Error: Service Unavailable for url: /api/ongs?state=:uf [GET] | 10 |
| `GET` | `/api/ongs/:id [GET]` | 503 Server Error: Service Unavailable for url: /api/ongs/:id [GET] | 13 |
| `POST` | `/api/ongs [POST]` | 503 Server Error: Service Unavailable for url: /api/ongs [POST] | 10 |
| `GET` | `/api/ongs [GET]` | 503 Server Error: Service Unavailable for url: /api/ongs [GET] | 13 |
| `GET` | `/api/health [GET]` | 503 Server Error: Service Unavailable for url: /api/health [GET] | 12 |
| `GET` | `/api/ongs?category=:cat [GET]` | 503 Server Error: Service Unavailable for url: /api/ongs?category=:cat [GET] | 9 |

## Diagnóstico

- **Causa raiz:** `503 Service Unavailable` em todos os endpoints — servidor sobrecarregado
- **Limite identificado:** Render Free Tier satura com ~100 usuários simultâneos
- **Breaking point estimado:** entre 10 e 100 usuários (recomenda-se testar 20, 30 e 50)
- **Recomendação:** upgrade para Render Starter ($7/mês) ou habilitar auto-scaling

## Comparativo

| Métrica | 10 usuários | 100 usuários |
|---|---:|---:|
| Total de requisições | 82 | 100 |
| Falhas | 0 | 75 |
| Taxa de falhas | 0.0% | 75.0% |
| Latência média | 857ms | 2750ms |
| P95 | 1700ms | 34000ms |
| RPS | 2.82 | 1.71 |
