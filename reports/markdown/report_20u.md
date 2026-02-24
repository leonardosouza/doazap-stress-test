# Stress Test — 20 Usuários Simultâneos

**Data:** 2026-02-23  
**Alvo:** https://doacao-whatsapp.onrender.com  
**Configuração:** 20 usuários · rampa 4/s · duração 45s

## Resultados por Endpoint

| Endpoint | Reqs | Falhas | %Falha | Avg (ms) | P95 (ms) | P99 (ms) | RPS |
|---|---:|---:|---:|---:|---:|---:|---:|
| `/api/health [GET]` | 31 | 0 | 0.0% | 2157 | 3800 | 4300 | 0.70 |
| `/api/health [POST]` | 30 | 0 | 0.0% | 2303 | 4000 | 4200 | 0.68 |
| `/api/ongs [GET]` | 40 | 0 | 0.0% | 1367 | 3100 | 3700 | 0.91 |
| `/api/ongs [POST]` | 15 | 0 | 0.0% | 1324 | 4100 | 4100 | 0.34 |
| `/api/ongs [on_start]` | 10 | 0 | 0.0% | 1263 | 3400 | 3400 | 0.23 |
| `/api/ongs/:id [DELETE]` | 7 | 0 | 0.0% | 2076 | 4200 | 4200 | 0.16 |
| `/api/ongs/:id [GET]` | 36 | 0 | 0.0% | 1076 | 2400 | 3000 | 0.82 |
| `/api/ongs/:id [PUT]` | 11 | 0 | 0.0% | 1424 | 4200 | 4200 | 0.25 |
| `/api/ongs?category=:cat [GET]` | 15 | 0 | 0.0% | 1374 | 3900 | 3900 | 0.34 |
| `/api/ongs?state=:uf [GET]` | 36 | 0 | 0.0% | 1228 | 2100 | 3300 | 0.82 |
| **TOTAL** | **231** | **0** | **0.0%** | **1545** | **3300** | **4200** | **5.24** |

## Erros

Nenhuma falha registrada. ✅

## Diagnóstico

- **Taxa de falhas:** 0% — dentro do limite aceitável
- Render Free Tier suporta 20 usuários simultâneos com estabilidade
- Latência média de 1545ms e P95 de 3300ms — aceitável para API conversacional
