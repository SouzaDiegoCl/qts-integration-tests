from datetime import date
from typing import Literal

from pydantic import BaseModel, EmailStr, Field, field_validator


Sala = Literal["Sala 1", "Sala 2", "Sala 3"]
Horario = Literal["09:00", "14:00", "19:00"]


class ReservaEntrada(BaseModel):
    nome: str = Field(min_length=2, max_length=80)
    email: EmailStr
    sala: Sala
    data: date
    horario: Horario

    @field_validator("nome")
    @classmethod
    def nome_sem_espacos_vazios(cls, valor: str) -> str:
        valor = valor.strip()
        if len(valor) < 2:
            raise ValueError("Informe um nome com pelo menos 2 caracteres")
        return valor

    @field_validator("data")
    @classmethod
    def data_futura(cls, valor: date) -> date:
        if valor < date.today():
            raise ValueError("A data não pode estar no passado")
        return valor


class Reserva(ReservaEntrada):
    id: int
