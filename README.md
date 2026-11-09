# Reservas de salas de estudo

Aplicação FastAPI para reservar salas de estudo. O projeto inclui testes de integração, interface, acessibilidade e carga para a atividade AT2 de Qualidade e Teste de Software.

## Requisitos

- Python 3.12 ou superior
- [`uv`](https://docs.astral.sh/uv/)
- Google Chrome ou navegador Chromium instalado pelo Playwright

## Instalação e execução

```bash
uv sync
uv run playwright install chromium # necessário caso Chrome não esteja instalado
uv run uvicorn app.main:app --reload
```

Abra `http://127.0.0.1:8000`. O banco SQLite é criado em `data/reservas.db`. Para usar outro arquivo, defina `BOOKINGS_DB`.

## Testes

```bash
uv run pytest -v
uv run pytest -v -m integration
uv run pytest -v -m 'e2e or accessibility'
```

Os testes de integração usam banco temporário, Factory com `Faker("pt_BR")` e mocks da chamada HTTP de notificação. Os testes E2E iniciam um servidor separado e usam Chrome quando ele está disponível no sistema.

## Carga

Em um terminal, inicie a aplicação:

```bash
uv run uvicorn app.main:app
```

Em outro terminal, execute o Locust com interface em `http://localhost:8089`:

```bash
uv run locust --host http://127.0.0.1:8000
```

Para repetir uma execução curta sem interface:

```bash
uv run locust --headless --host http://127.0.0.1:8000 -u 10 -r 2 -t 20s --csv locust_resultado
```

### Métricas medidas

Execução local em 08/11/2026, com 10 usuários, entrada de 2 usuários por segundo e duração de 20 segundos. A aplicação foi iniciada com Uvicorn e banco SQLite temporário; a notificação externa estava desativada. Foram 365 requisições no total.

| Usuários | Duração |   RPS |  p95 |     Falhas |
| --------: | --------: | ----: | ---: | ---------: |
|        10 |      20 s | 18,35 | 6 ms | 0/365 (0%) |

Os valores são da linha agregada do resumo do Locust. O p95 é aproximado e esta execução curta não representa capacidade máxima de produção.

## Documentação

- [Requisitos do produto](PRD.md)
- [Regras de contexto](AGENTS.md)
- [Uso de IA](AI_USAGE.md)
