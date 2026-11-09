from playwright.sync_api import Page, expect


class ReservasPage:
    def __init__(self, page: Page, url: str):
        self.page = page
        self.url = url

    def abrir(self):
        self.page.goto(self.url)
        expect(self.page.get_by_role("heading", name="Reservas de salas de estudo")).to_be_visible()

    def preencher(self, dados: dict):
        self.page.get_by_label("Nome").fill(dados["nome"])
        self.page.get_by_label("E-mail").fill(dados["email"])
        self.page.get_by_label("Sala", exact=True).select_option(label=dados["sala"])
        self.page.get_by_label("Data").fill(dados["data"])
        self.page.get_by_label("Horário").select_option(label=dados["horario"])

    def reservar(self):
        self.page.get_by_role("button", name="Reservar sala").click()

    def mensagem(self, texto: str):
        expect(self.page.get_by_role("status")).to_have_text(texto)
