import os

import httpx

from app.models import ReservaEntrada


class FalhaNotificacao(Exception):
    pass


def enviar_notificacao(entrada: ReservaEntrada) -> None:
    url = os.getenv("NOTIFICATION_URL")
    if not url:
        return
    try:
        resposta = httpx.post(url, json=entrada.model_dump(mode="json"), timeout=3)
        resposta.raise_for_status()
    except httpx.HTTPError as erro:
        raise FalhaNotificacao("Não foi possível confirmar a notificação") from erro
