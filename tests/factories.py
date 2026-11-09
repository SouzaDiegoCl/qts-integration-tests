from datetime import date, timedelta

from faker import Faker


class ReservaFactory:
    fake = Faker("pt_BR")

    @classmethod
    def criar(cls, **alteracoes) -> dict:
        reserva = {
            "nome": cls.fake.name(),
            "email": cls.fake.email(),
            "sala": "Sala 1",
            "data": (date.today() + timedelta(days=30)).isoformat(),
            "horario": "09:00",
        }
        return {**reserva, **alteracoes}
