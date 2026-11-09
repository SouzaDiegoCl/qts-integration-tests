const formulario = document.querySelector("#reserva-form");
const mensagem = document.querySelector("#mensagem");
const lista = document.querySelector("#reservas");
const listaVazia = document.querySelector("#lista-vazia");
const campoData = document.querySelector("#data");

const hoje = new Date();
const dataLocal = new Date(hoje.getTime() - hoje.getTimezoneOffset() * 60000);
campoData.min = dataLocal.toISOString().slice(0, 10);

function mostrarMensagem(texto, tipo) {
  mensagem.textContent = texto;
  mensagem.className = tipo;
}

async function carregarReservas() {
  try {
    const resposta = await fetch("/api/reservas");
    if (!resposta.ok) throw new Error("Não foi possível carregar as reservas.");
    const reservas = await resposta.json();
    lista.replaceChildren();
    listaVazia.hidden = reservas.length > 0;
    for (const reserva of reservas) {
      const item = document.createElement("li");
      item.textContent = `${reserva.sala} — ${reserva.data} às ${reserva.horario} — ${reserva.nome}`;
      lista.append(item);
    }
  } catch (erro) {
    mostrarMensagem(erro.message, "erro");
  }
}

formulario.addEventListener("submit", async (evento) => {
  evento.preventDefault();
  const dados = Object.fromEntries(new FormData(formulario));
  try {
    const resposta = await fetch("/api/reservas", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(dados),
    });
    if (!resposta.ok) {
      const erro = await resposta.json();
      throw new Error(typeof erro.detail === "string" ? erro.detail : "Confira os dados informados.");
    }
    formulario.reset();
    mostrarMensagem("Reserva realizada com sucesso.", "sucesso");
    await carregarReservas();
  } catch (erro) {
    mostrarMensagem(erro.message, "erro");
  }
});

carregarReservas();
