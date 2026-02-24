# Relatório Consolidado — Stress Test DoaZap

**Data:** 2026-02-23
**Ferramenta:** Locust 2.32.4
**Alvo:** https://doacao-whatsapp.onrender.com
**Infraestrutura:** Render Free Tier (instância única, sem auto-scaling)

---

## Resumo Executivo

| Usuários | Duração | Reqs | Falhas | % Falha | RPS | P50 (ms) | P95 (ms) | Média (ms) | Status |
|:--------:|:-------:|-----:|-------:|--------:|----:|---------:|---------:|-----------:|:------:|
| 10 | 30s | 82 | 0 | 0% | 2,82 | 620 | 1 700 | 857 | ✅ OK |
| 20 | 45s | 231 | 0 | 0% | 5,24 | 1 500 | 3 300 | 1 545 | ✅ OK |
| 30 | 45s | 27 | 14 | 51,9% | 0,63 | 1 800 | 36 000 | 7 250 | ❌ FALHA |
| 50 | 60s | 24 | 15 | 62,5% | 0,41 | 270 | 4 700 | 2 828 | ❌ FALHA |
| 100 | 60s | 100 | 75 | 75,0% | 1,71 | 240 | 34 000 | 2 750 | ❌ FALHA |

---

## Ponto de Ruptura

**O sistema começa a colapsar entre 20 e 30 usuários simultâneos.**

- Com **20 usuários**: 0% de falhas, RPS de 5,24, P95 de 3,3 s — sistema estável
- Com **30 usuários**: 52% de falhas, RPS despenca para 0,63 — colapso iniciado
- A partir daí, mais carga **não aumenta** o throughput — o RPS com 100 usuários (1,71)
  ainda é inferior ao RPS com 20 usuários (5,24)

---

## Evolução do RPS

```
RPS
5,24 ┤             ██
     │             ██
2,82 ┤    ██        ██
     │    ██        ██
1,71 ┤    ██        ██                   ██
     │    ██        ██                   ██
0,63 ┤    ██        ██        ██         ██
0,41 ┤    ██        ██        ██   ██    ██
     └───────────────────────────────────────
          10u       20u       30u  50u  100u
```

---

## Taxa de Falhas por Carga

```
Falhas%
75%  ┤                                        ██
63%  ┤                             ██         ██
52%  ┤                        ██   ██         ██
     │                        ██   ██         ██
 0%  ┤    ██        ██        ██   ██         ██
     └──────────────────────────────────────────
          10u       20u       30u  50u        100u
```

---

## Comparativo por Endpoint

### Latência Média (ms)

| Endpoint | 10u | 20u | 30u | 50u | 100u |
|----------|----:|----:|----:|----:|-----:|
| GET /api/health | 1 354 | 2 157 | 7 200 | 4 685 | 2 957 |
| POST /api/health | 1 422 | 2 303 | 5 832 | 4 182 | 4 032 |
| GET /api/ongs | 571 | 1 367 | 229* | 246* | 461* |
| GET /api/ongs/:id | 519 | 1 076 | 235* | 254* | 2 594* |
| GET /api/ongs?state=:uf | 549 | 1 228 | 2 514 | 246* | 295* |
| GET /api/ongs?category=:cat | 836 | 1 374 | 230* | 311* | 457* |
| POST /api/ongs | 861 | 1 324 | — | 365* | 498* |
| PUT /api/ongs/:id | — | 1 424 | — | — | — |
| DELETE /api/ongs/:id | 968 | 2 076 | — | — | — |

> \* Baixa latência aparente porque o Render retornou 503 imediatamente (fast-fail),
> sem processar a requisição.

### Latência P95 (ms)

| Endpoint | 10u | 20u | 30u | 50u | 100u |
|----------|----:|----:|----:|----:|-----:|
| GET /api/health | 1 700 | 3 800 | 7 200 | 4 700 | 35 000 |
| GET /api/ongs | 1 000 | 3 100 | 240 (503) | 250 (503) | 3 400 (503) |
| GET /api/ongs/:id | 830 | 2 400 | 240 (503) | 330 (503) | 33 000 (503) |

---

## Análise de Erros

### 10 e 20 usuários
Nenhuma falha registrada. ✅

### 30 usuários (14 falhas)
| Erro | Ocorrências |
|------|------------:|
| 502 Bad Gateway (GET /api/health) | 1 |
| 503 Service Unavailable (GET /api/ongs) | 4 |
| 503 Service Unavailable (GET /api/ongs/:id) | 4 |
| 503 Service Unavailable (GET /api/ongs?category=:cat) | 4 |
| 503 Service Unavailable (GET /api/ongs?state=:uf) | 1 |

### 50 usuários (15 falhas)
| Erro | Ocorrências |
|------|------------:|
| 503 Service Unavailable (POST /api/ongs) | 4 |
| 503 Service Unavailable (GET /api/ongs/:id) | 7 |
| 503 Service Unavailable (GET /api/ongs) | 1 |
| 503 Service Unavailable (GET /api/ongs?category=:cat) | 1 |
| 503 Service Unavailable (GET /api/ongs?state=:uf) | 2 |

### 100 usuários (75 falhas)
| Erro | Ocorrências |
|------|------------:|
| 503 Service Unavailable (GET /api/health) | 12 |
| 503 Service Unavailable (POST /api/health) | 8 |
| 503 Service Unavailable (GET /api/ongs) | 13 |
| 503 Service Unavailable (GET /api/ongs/:id) | 13 |
| 503 Service Unavailable (GET /api/ongs?category=:cat) | 9 |
| 503 Service Unavailable (GET /api/ongs?state=:uf) | 10 |
| 503 Service Unavailable (POST /api/ongs) | 10 |

---

## Diagnóstico

### Por que o sistema colapsa entre 20 e 30 usuários?

O Render Free Tier aloca **um único worker Uvicorn** para a aplicação. A instância não
escala horizontalmente e não possui warm standby. Quando 25–30 conexões simultâneas chegam:

1. O Uvicorn (single-process) enfileira as requisições além de sua capacidade de processamento.
2. O Render detecta a sobrecarga e começa a rejeitar novas conexões com `503 Service Unavailable`.
3. As requisições que passam ficam aguardando na fila de conexões do banco (Supabase
   Connection Pooler), gerando latências de 30–36 segundos.

### Por que o RPS baixo latência é ilusório após o colapso?

Com 30+ usuários, o Render responde com 503 imediatamente (~230ms), sem processar a
requisição. Isso resulta em latência aparentemente "baixa" para endpoints que falharam —
na verdade é o servidor rejeitando conexões rapidamente.

### Capacidade atual (Render Free Tier)

| Faixa | Usuários | Comportamento |
|-------|:--------:|---------------|
| ✅ Operação normal | ≤ 20 | Sem falhas, latência aceitável |
| ⚠️ Zona de risco | 20–30 | Ponto de ruptura — possíveis erros esporádicos |
| ❌ Saturação | > 30 | 503 Service Unavailable generalizado |

---

## Recomendações

| Prioridade | Ação | Impacto Esperado |
|:----------:|------|-----------------|
| 1 | **Upgrade para Render Starter** ($7/mês) — RAM dedicada, sem cold start | Suportar 50–100+ usuários sem falhas |
| 2 | **Adicionar cache Redis** (ex: Upstash Free) para `GET /api/ongs` | Reduzir carga no banco, aumentar RPS de leitura |
| 3 | **Configurar `pool_size` e `max_overflow`** no SQLAlchemy | Reduzir latência de banco em picos |
| 4 | **Múltiplos workers Uvicorn** (`--workers 2`) | Dobrar throughput no mesmo servidor |
| 5 | **Implementar circuit breaker** no cliente | Evitar cascata de falhas em alta carga |

---

## Arquivos de Evidência

| Cenário | Markdown | HTML (GitHub Pages) | CSVs |
|---------|----------|---------------------|------|
| 10 usuários | [report_10u.md](report_10u.md) | [report_10u.html](https://leonardosouza.github.io/doazap-stress-test/reports/html/report_10u.html) | [results/10u/](../../results/10u/) |
| 20 usuários | [report_20u.md](report_20u.md) | [report_20u.html](https://leonardosouza.github.io/doazap-stress-test/reports/html/report_20u.html) | [results/20u/](../../results/20u/) |
| 30 usuários | [report_30u.md](report_30u.md) | [report_30u.html](https://leonardosouza.github.io/doazap-stress-test/reports/html/report_30u.html) | [results/30u/](../../results/30u/) |
| 50 usuários | [report_50u.md](report_50u.md) | [report_50u.html](https://leonardosouza.github.io/doazap-stress-test/reports/html/report_50u.html) | [results/50u/](../../results/50u/) |
| 100 usuários | [report_100u.md](report_100u.md) | [report_100u.html](https://leonardosouza.github.io/doazap-stress-test/reports/html/report_100u.html) | [results/100u/](../../results/100u/) |
