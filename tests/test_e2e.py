from datetime import date, timedelta

import pytest
from playwright.sync_api import Page, expect

from tests.factories import ReservaFactory
from tests.pages.reservas_page import ReservasPage


@pytest.mark.e2e
def test_reserva_pela_interface(page: Page, servidor: str):
    # Arrange
    tela = ReservasPage(page, servidor)
    dados = ReservaFactory.criar(data=(date.today() + timedelta(days=31)).isoformat())
    tela.abrir()
    tela.preencher(dados)
    # Act
    tela.reservar()
    # Assert
    tela.mensagem("Reserva realizada com sucesso.")
    expect(page.get_by_role("list", name="Reservas cadastradas").get_by_text(dados["nome"], exact=False)).to_be_visible()


@pytest.mark.e2e
def test_conflito_pela_interface(page: Page, servidor: str):
    # Arrange
    tela = ReservasPage(page, servidor)
    dados = ReservaFactory.criar(data=(date.today() + timedelta(days=32)).isoformat())
    tela.abrir()
    tela.preencher(dados)
    tela.reservar()
    tela.mensagem("Reserva realizada com sucesso.")
    tela.preencher(ReservaFactory.criar(data=dados["data"]))
    # Act
    tela.reservar()
    # Assert
    tela.mensagem("Horário já reservado para esta sala")
