# PRD — Reservas de salas de estudo

## Objetivo

Permitir que estudantes reservem uma sala de estudo para uma data e um horário. A aplicação serve como sistema sob teste para integração, interface, acessibilidade e carga.

## Regras de negócio

- O formulário solicita nome, e-mail, sala, data e horário.
- As salas disponíveis são `Sala 1`, `Sala 2` e `Sala 3`.
- Os horários disponíveis são `09:00`, `14:00` e `19:00`.
- Uma sala aceita apenas uma reserva por data e horário.
- A data deve ser igual ou posterior à data atual.
- Nome deve conter de 2 a 80 caracteres; e-mail deve ser válido.
- Se a notificação externa configurada falhar, a reserva não é gravada.

## Rotas

| Método | Rota | Resposta |
| --- | --- | --- |
| GET | `/` | Página HTML com formulário e lista de reservas. |
| GET | `/api/health` | Estado da aplicação. |
| GET | `/api/reservas` | Lista de reservas ordenada por data e horário. |
| POST | `/api/reservas` | Cria reserva (`201`), informa conflito (`409`), dados inválidos (`422`) ou falha de notificação (`502`). |

## Interface web

Página única com título, campos identificados por rótulos, botão de envio, região de mensagens e lista das reservas. Ao criar uma reserva, a lista é atualizada sem recarregar a página. Erros são informados em texto.

## Requisitos não funcionais avaliados

- **Adequação funcional e confiabilidade (ISO/IEC 25010):** validação, conflito de horário e falha externa cobertos por testes de integração.
- **Usabilidade e acessibilidade:** interface navegável por teclado e auditoria automatizada WCAG 2.1 AA com Axe-core.
- **Eficiência de desempenho:** teste de carga com Locust; registrar RPS, p95 e taxa de falhas.
- **Manutenibilidade e testabilidade:** Factory para dados sintéticos, Fixtures com isolamento e Page Object Model nos testes E2E.

## Limites

Não há autenticação, alteração ou cancelamento de reservas. O SQLite atende ao escopo didático; não foi projetado para alto volume de escrita concorrente.
