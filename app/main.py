import sqlite3
from pathlib import Path

from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.models import Reserva, ReservaEntrada
from app.repository import ReservaRepository, get_repository
from app.services import FalhaNotificacao, enviar_notificacao


BASE = Path(__file__).resolve().parent
app = FastAPI(title="Reservas de salas de estudo")
app.mount("/static", StaticFiles(directory=BASE / "static"), name="static")


@app.get("/", include_in_schema=False)
def pagina_inicial() -> FileResponse:
    return FileResponse(BASE / "static" / "index.html")


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/reservas", response_model=list[Reserva])
def listar_reservas(repositorio: ReservaRepository = Depends(get_repository)) -> list[Reserva]:
    return repositorio.listar()


@app.post("/api/reservas", response_model=Reserva, status_code=201)
def criar_reserva(
    entrada: ReservaEntrada,
    repositorio: ReservaRepository = Depends(get_repository),
) -> Reserva:
    if repositorio.existe(entrada):
        raise HTTPException(status_code=409, detail="Horário já reservado para esta sala")
    try:
        enviar_notificacao(entrada)
    except FalhaNotificacao as erro:
        raise HTTPException(status_code=502, detail=str(erro)) from erro
    try:
        return repositorio.criar(entrada)
    except sqlite3.IntegrityError as erro:
        raise HTTPException(status_code=409, detail="Horário já reservado para esta sala") from erro
