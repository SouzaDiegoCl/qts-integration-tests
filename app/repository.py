import os
import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

from app.models import Reserva, ReservaEntrada


class ReservaRepository:
    def __init__(self, caminho: str | Path):
        self.caminho = Path(caminho)
        self.caminho.parent.mkdir(parents=True, exist_ok=True)
        with self._conectar() as conexao:
            conexao.execute(
                """
                CREATE TABLE IF NOT EXISTS reservas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    email TEXT NOT NULL,
                    sala TEXT NOT NULL,
                    data TEXT NOT NULL,
                    horario TEXT NOT NULL,
                    UNIQUE (sala, data, horario)
                )
                """
            )

    @contextmanager
    def _conectar(self) -> Iterator[sqlite3.Connection]:
        conexao = sqlite3.connect(self.caminho, timeout=10)
        conexao.row_factory = sqlite3.Row
        try:
            yield conexao
            conexao.commit()
        except Exception:
            conexao.rollback()
            raise
        finally:
            conexao.close()

    def listar(self) -> list[Reserva]:
        with self._conectar() as conexao:
            linhas = conexao.execute(
                "SELECT * FROM reservas ORDER BY data, horario, sala"
            ).fetchall()
        return [Reserva.model_validate(dict(linha)) for linha in linhas]

    def existe(self, entrada: ReservaEntrada) -> bool:
        with self._conectar() as conexao:
            linha = conexao.execute(
                "SELECT 1 FROM reservas WHERE sala = ? AND data = ? AND horario = ?",
                (entrada.sala, entrada.data.isoformat(), entrada.horario),
            ).fetchone()
        return linha is not None

    def criar(self, entrada: ReservaEntrada) -> Reserva:
        with self._conectar() as conexao:
            cursor = conexao.execute(
                "INSERT INTO reservas (nome, email, sala, data, horario) VALUES (?, ?, ?, ?, ?)",
                (
                    entrada.nome,
                    str(entrada.email),
                    entrada.sala,
                    entrada.data.isoformat(),
                    entrada.horario,
                ),
            )
            identificador = cursor.lastrowid
        return Reserva(id=identificador, **entrada.model_dump())


def get_repository() -> ReservaRepository:
    return ReservaRepository(os.getenv("BOOKINGS_DB", "data/reservas.db"))
