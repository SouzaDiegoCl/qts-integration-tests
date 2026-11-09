import pytest
from axe_playwright_python.sync_playwright import Axe
from playwright.sync_api import Page, expect

from tests.pages.reservas_page import ReservasPage


@pytest.mark.accessibility
def test_pagina_sem_violacoes_wcag_21_aa(page: Page, servidor: str):
    tela = ReservasPage(page, servidor)
    tela.abrir()
    resultados = Axe().run(
        page,
        options={
            "runOnly": {"type": "tag", "values": ["wcag2a", "wcag2aa", "wcag21a", "wcag21aa"]},
            "resultTypes": ["violations"],
        },
    )
    assert resultados.violations_count == 0, resultados.generate_report()


@pytest.mark.accessibility
def test_navegacao_por_teclado(page: Page, servidor: str):
    tela = ReservasPage(page, servidor)
    tela.abrir()
    page.keyboard.press("Tab")
    expect(page.get_by_label("Nome")).to_be_focused()
    page.keyboard.press("Tab")
    expect(page.get_by_label("E-mail")).to_be_focused()
    page.keyboard.press("Tab")
    expect(page.get_by_label("Sala", exact=True)).to_be_focused()
