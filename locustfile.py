from datetime import date, timedelta
from random import randint

from locust import HttpUser, between, task


class Estudante(HttpUser):
    wait_time = between(0.2, 0.8)

    @task(3)
    def listar_reservas(self):
        self.client.get("/api/reservas", name="GET /api/reservas")

    @task(1)
    def criar_reserva(self):
        numero = randint(1, 1_000_000)
        dados = {
            "nome": f"Estudante {numero}",
            "email": f"estudante{numero}@example.com",
            "sala": f"Sala {randint(1, 3)}",
            "data": (date.today() + timedelta(days=randint(1, 3650))).isoformat(),
            "horario": ["09:00", "14:00", "19:00"][randint(0, 2)],
        }
        with self.client.post("/api/reservas", json=dados, name="POST /api/reservas", catch_response=True) as resposta:
            if resposta.status_code == 409:
                resposta.success()
