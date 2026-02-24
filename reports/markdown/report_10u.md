# Stress Test — 10 Usuários Simultâneos

**Data:** 2026-02-23  
**Alvo:** https://doacao-whatsapp.onrender.com  
**Configuração:** 10 usuários · rampa 2/s · duração 30s

## Resultados por Endpoint

| Endpoint | Reqs | Falhas | %Falha | Avg (ms) | P95 (ms) | P99 (ms) | RPS |
|---|---:|---:|---:|---:|---:|---:|---:|
| `/api/health [GET]` | 7 | 0 | 0.0% | 1354 | 1700 | 1700 | 0.24 |
| `/api/health [POST]` | 15 | 0 | 0.0% | 1422 | 2000 | 2000 | 0.52 |
| `/api/ongs [GET]` | 15 | 0 | 0.0% | 571 | 1000 | 1000 | 0.52 |
| `/api/ongs [POST]` | 3 | 0 | 0.0% | 861 | 1000 | 1000 | 0.10 |
| `/api/ongs [on_start]` | 5 | 0 | 0.0% | 1031 | 1700 | 1700 | 0.17 |
| `/api/ongs/:id [DELETE]` | 1 | 0 | 0.0% | 968 | 970 | 970 | 0.03 |
| `/api/ongs/:id [GET]` | 14 | 0 | 0.0% | 519 | 830 | 830 | 0.48 |
| `/api/ongs?category=:cat [GET]` | 10 | 0 | 0.0% | 836 | 1400 | 1400 | 0.34 |
| `/api/ongs?state=:uf [GET]` | 12 | 0 | 0.0% | 549 | 940 | 940 | 0.41 |
| **TOTAL** | **82** | **0** | **0.0%** | **857** | **1700** | **2000** | **2.82** |

## Erros

Nenhuma falha registrada. ✅

## Diagnóstico

- **Taxa de falhas:** 0.0% — dentro do limite aceitável (<1%)
- Render Free Tier suporta bem a carga de 10 usuários simultâneos
- Latências de leitura (GET /api/ongs) abaixo de 600ms em média
- Health check com latência mais alta (~1.3s) — overhead do New Relic agent
