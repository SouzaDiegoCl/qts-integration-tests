import httpx
import pytest

from tests.factories import ReservaFactory


@pytest.mark.integration
def test_lista_inicial_vazia(client):
    # Arrange: banco temporário criado pela fixture.
    # Act
    resposta = client.get("/api/reservas")
    # Assert
    assert resposta.status_code == 200
    assert resposta.json() == []


@pytest.mark.integration
def test_cria_e_lista_reserva(client):
    # Arrange
    dados = ReservaFactory.criar()
    # Act
    criacao = client.post("/api/reservas", json=dados)
    listagem = client.get("/api/reservas")
    # Assert
    assert criacao.status_code == 201
    assert criacao.json()["id"] > 0
    assert criacao.json()["nome"] == dados["nome"]
    assert listagem.status_code == 200
    assert len(listagem.json()) == 1
    assert listagem.json()[0]["email"] == dados["email"]


@pytest.mark.integration
def test_recusa_horario_ocupado(client):
    # Arrange
    dados = ReservaFactory.criar()
    client.post("/api/reservas", json=dados)
    # Act
    resposta = client.post("/api/reservas", json=ReservaFactory.criar(**{
        "sala": dados["sala"], "data": dados["data"], "horario": dados["horario"]
    }))
    # Assert
    assert resposta.status_code == 409
    assert resposta.json()["detail"] == "Horário já reservado para esta sala"
    assert len(client.get("/api/reservas").json()) == 1


@pytest.mark.integration
def test_valida_email_e_nao_grava(client):
    # Arrange
    dados = ReservaFactory.criar(email="email-invalido")
    # Act
    resposta = client.post("/api/reservas", json=dados)
    # Assert
    assert resposta.status_code == 422
    assert client.get("/api/reservas").json() == []


@pytest.mark.integration
def test_notificacao_externa_com_sucesso(client, monkeypatch, mocker):
    # Arrange
    monkeypatch.setenv("NOTIFICATION_URL", "https://notificacao.example/reservas")
    envio = mocker.patch("app.services.httpx.post")
    envio.return_value.raise_for_status.return_value = None
    dados = ReservaFactory.criar()
    # Act
    resposta = client.post("/api/reservas", json=dados)
    # Assert
    assert resposta.status_code == 201
    envio.assert_called_once()
    assert envio.call_args.kwargs["json"]["email"] == dados["email"]


@pytest.mark.integration
def test_falha_externa_nao_grava_reserva(client, monkeypatch, mocker):
    # Arrange
    monkeypatch.setenv("NOTIFICATION_URL", "https://notificacao.example/reservas")
    envio = mocker.patch("app.services.httpx.post", side_effect=httpx.ConnectError("sem conexão"))
    # Act
    resposta = client.post("/api/reservas", json=ReservaFactory.criar())
    # Assert
    assert resposta.status_code == 502
    assert resposta.json()["detail"] == "Não foi possível confirmar a notificação"
    envio.assert_called_once()
    assert client.get("/api/reservas").json() == []
