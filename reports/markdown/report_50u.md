# Relatório de Stress Test — 50 Usuários

**Data:** 2026-02-23
**Ferramenta:** Locust 2.32.4
**Alvo:** https://doacao-whatsapp.onrender.com
**Configuração:** 50 usuários, rampa 8/s, duração 60s
**Distribuição:** HealthUser ×15 · ReadUser ×25 · WriteUser ×10

---

## Resumo Geral

| Métrica | Valor |
|---------|-------|
| Total de requisições | 24 |
| Falhas | 15 (62,50%) |
| RPS médio | 0,41 req/s |
| Latência média | 2 828 ms |
| Latência P95 | 4 700 ms |
| Latência P50 | 270 ms |

> **Status: FALHA** — O Render Free Tier não suportou 50 usuários simultâneos.
> A maior parte das requisições aos endpoints de leitura e escrita retornou 503.

---

## Resultados por Endpoint

| Método | Endpoint | Reqs | Falhas | % Falha | P50 (ms) | P95 (ms) | Média (ms) |
|--------|----------|-----:|-------:|--------:|---------:|---------:|-----------:|
| GET | /api/health [GET] | 1 | 0 | 0% | 4 700 | 4 700 | 4 685 |
| POST | /api/health [POST] | 1 | 0 | 0% | 4 200 | 4 200 | 4 182 |
| GET | /api/ongs [GET] | 1 | 1 | 100% | 250 | 250 | 246 |
| POST | /api/ongs [POST] | 4 | 4 | 100% | 250 | 740 | 365 |
| GET | /api/ongs [on_start] | 7 | 0 | 0% | 3 800 | 34 000 | 7 818 |
| GET | /api/ongs/:id [GET] | 7 | 7 | 100% | 240 | 330 | 254 |
| GET | /api/ongs?category=:cat | 1 | 1 | 100% | 310 | 310 | 311 |
| GET | /api/ongs?state=:uf | 2 | 2 | 100% | 270 | 270 | 246 |

---

## Erros Registrados

| Método | Endpoint | Erro | Ocorrências |
|--------|----------|------|------------:|
| GET | /api/ongs [GET] | 503 Service Unavailable | 1 |
| POST | /api/ongs [POST] | 503 Service Unavailable | 4 |
| GET | /api/ongs/:id [GET] | 503 Service Unavailable | 7 |
| GET | /api/ongs?category=:cat | 503 Service Unavailable | 1 |
| GET | /api/ongs?state=:uf | 503 Service Unavailable | 2 |

---

## Diagnóstico

- **Saturação total confirmada**: 62,5% de falhas com apenas 24 requisições em 60 segundos.
- O throughput caiu para **0,41 req/s**, inferior ao teste de 30 usuários (0,63 req/s),
  evidenciando que o servidor está completamente sobrecarregado.
- Os endpoints de health check sobreviveram (sem falhas), mas com latência de ~4 segundos.
- O `on_start` dos `ReadUser` registrou tempos de até **34 segundos**, confirmando fila
  de conexões crítica no servidor.
- A escrita (`POST /api/ongs`) teve 100% de falhas, mostrando que operações de banco
  são as primeiras a serem descartadas sob pressão.

## Conclusão

Com 50 usuários, o sistema está em colapso total. O RPS efetivo é menor que com 30 usuários,
indicando que aumentar a carga além do ponto de ruptura piora o throughput em vez de mantê-lo.
O **ponto de ruptura do Render Free Tier está entre 20 e 30 usuários simultâneos**.
