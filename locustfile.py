"""
DoaZap — Stress Test (Locust)

Cenários:
  HealthUser (peso 3) — GET e POST /api/health
  ReadUser   (peso 5) — leitura de ONGs (listagem e por ID)
  WriteUser  (peso 2) — ciclo CREATE → UPDATE → DELETE de ONGs

Uso:
  locust -f locustfile.py                          # UI web em localhost:8089
  locust -f locustfile.py --headless -u 50 -r 5 --run-time 2m --html report.html
"""

import os
import random
import uuid

from dotenv import load_dotenv
from locust import HttpUser, between, task

load_dotenv()

API_KEY = os.getenv("API_KEY", "")
AUTH_HEADERS = {"X-API-Key": API_KEY}

# Dados de apoio para geração de ONGs temporárias
_CATEGORIES = ["Saúde", "Educação", "Fome", "Animais", "Assistência Social", "Crianças"]
_STATES = ["SP", "RJ", "MG", "RS", "BA", "PR"]
_CITIES = {
    "SP": "São Paulo",
    "RJ": "Rio de Janeiro",
    "MG": "Belo Horizonte",
    "RS": "Porto Alegre",
    "BA": "Salvador",
    "PR": "Curitiba",
}


def _random_ong_payload() -> dict:
    state = random.choice(_STATES)
    return {
        "name": f"ONG Stress Test {uuid.uuid4().hex[:8]}",
        "category": random.choice(_CATEGORIES),
        "city": _CITIES[state],
        "state": state,
        "email": f"stress-{uuid.uuid4().hex[:6]}@test.local",
    }


# ---------------------------------------------------------------------------
# Cenário 1: Health Check
# ---------------------------------------------------------------------------

class HealthUser(HttpUser):
    """Valida disponibilidade e latência do health check (GET e POST)."""

    weight = 3
    wait_time = between(1, 3)

    @task
    def get_health(self):
        self.client.get("/api/health", name="/api/health [GET]")

    @task
    def post_health(self):
        self.client.post("/api/health", name="/api/health [POST]")


# ---------------------------------------------------------------------------
# Cenário 2: Leitura de ONGs
# ---------------------------------------------------------------------------

class ReadUser(HttpUser):
    """Simula leituras de dados sem efeitos colaterais."""

    weight = 5
    wait_time = between(1, 3)

    def on_start(self):
        """Busca IDs de ONGs existentes para uso nas tasks de leitura por ID."""
        self._ong_ids: list[str] = []
        resp = self.client.get(
            "/api/ongs?limit=100",
            name="/api/ongs [on_start]",
        )
        if resp.status_code == 200:
            data = resp.json()
            self._ong_ids = [ong["id"] for ong in data if "id" in ong]

    @task(3)
    def list_ongs(self):
        self.client.get("/api/ongs", name="/api/ongs [GET]")

    @task(2)
    def list_ongs_by_state(self):
        state = random.choice(_STATES)
        self.client.get(
            f"/api/ongs?state={state}",
            name="/api/ongs?state=:uf [GET]",
        )

    @task(2)
    def list_ongs_by_category(self):
        category = random.choice(_CATEGORIES)
        self.client.get(
            f"/api/ongs?category={category}",
            name="/api/ongs?category=:cat [GET]",
        )

    @task(3)
    def get_ong_by_id(self):
        if not self._ong_ids:
            return
        ong_id = random.choice(self._ong_ids)
        self.client.get(
            f"/api/ongs/{ong_id}",
            name="/api/ongs/:id [GET]",
        )


# ---------------------------------------------------------------------------
# Cenário 3: Ciclo de Escrita (CREATE → UPDATE → DELETE)
# ---------------------------------------------------------------------------

class WriteUser(HttpUser):
    """Ciclo completo de escrita: cria, atualiza e remove uma ONG temporária."""

    weight = 2
    wait_time = between(2, 5)

    def on_start(self):
        self._ong_id: str | None = None

    @task(1)
    def create_ong(self):
        resp = self.client.post(
            "/api/ongs",
            json=_random_ong_payload(),
            headers=AUTH_HEADERS,
            name="/api/ongs [POST]",
        )
        if resp.status_code == 201:
            self._ong_id = resp.json().get("id")

    @task(1)
    def update_ong(self):
        if not self._ong_id:
            return
        self.client.put(
            f"/api/ongs/{self._ong_id}",
            json={"name": f"ONG Atualizada {uuid.uuid4().hex[:6]}"},
            headers=AUTH_HEADERS,
            name="/api/ongs/:id [PUT]",
        )

    @task(1)
    def delete_ong(self):
        if not self._ong_id:
            return
        resp = self.client.delete(
            f"/api/ongs/{self._ong_id}",
            headers=AUTH_HEADERS,
            name="/api/ongs/:id [DELETE]",
        )
        if resp.status_code == 204:
            self._ong_id = None
