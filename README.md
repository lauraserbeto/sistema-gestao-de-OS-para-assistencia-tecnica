# Backend Challenge 2026

API REST profissional para gestão de ordens de serviço de uma assistência técnica, desenvolvida em FastAPI como parte da atividade **DESAFIO DE PROGRAMADOR API - Backend Challenge 2026**.

## Sumário

- [Visão geral](#visão-geral)
- [Tecnologias](#tecnologias)
- [Planejamento da entrega](#planejamento-da-entrega)
- [Entrega 1 - Infraestrutura, autenticação e clientes](#entrega-1---infraestrutura-autenticação-e-clientes)
- [Arquitetura do projeto](#arquitetura-do-projeto)
- [Como executar](#como-executar)
- [Usuários seed](#usuários-seed)
- [Autenticação](#autenticação)
- [Endpoints implementados](#endpoints-implementados)
- [Integração externa](#integração-externa)
- [Orientações para as próximas entregas](#orientações-para-as-próximas-entregas)

## Visão geral

O sistema tem como objetivo substituir planilhas e processos manuais usados por uma assistência técnica para controlar clientes, técnicos, ordens de serviço, peças, históricos e relatórios operacionais.

Nesta primeira entrega, foi implementada a base da API: estrutura do projeto, banco de dados, autenticação JWT, controle de perfis, rotas protegidas, gestão de clientes e integração externa com ViaCEP.

## Tecnologias

- Python
- FastAPI
- SQLAlchemy
- Alembic
- SQLite para execução local
- JWT com `python-jose`
- Hash de senha com `bcrypt`
- HTTPX para consumo de API externa
- Swagger gerado automaticamente pelo FastAPI

## Planejamento da entrega

### Divisão de responsabilidades

- Entrega 1: Laura Beatriz Silva Serbêto | Matríula: 2321107
- Entrega 2: Vitor Martins Melo | Matrícula: 2320023
- Entrega 3: 
- Entrega 4: 

## Detalhamento da Entrega 1 - Infraestrutura, autenticação e clientes

Responsável: Laura Beatriz Silva Serbêto

### O que estava previsto

- [x] Setup inicial do projeto em FastAPI.
- [x] Criação da estrutura de pastas com separação de responsabilidades.
- [x] Configuração do banco de dados.
- [x] Criação de migrations.
- [x] Criação de seeds iniciais.
- [x] Implementação de autenticação JWT.
- [x] Implementação de login.
- [x] Implementação de logout.
- [x] Criação de rotas protegidas.
- [x] Criação de controle por perfil:  'administrador', 'tecnico' e 'atendente'.
- [x] CRUD de clientes.
- [x] Busca de clientes por nome, CPF, e-mail ou telefone.
- [x] Integração com ViaCEP para preencher endereço automaticamente pelo CEP.

### O que foi feito

- [x] Criada a aplicação FastAPI em 'app/main.py'.
- [x] Criada a configuração centralizada em 'app/core/config.py'.
- [x] Criada a camada de banco em 'app/database'.
- [x] Criados os modelos 'User', 'Client' e 'RevokedToken'.
- [x] Criadas migrations Alembic para usuários, clientes e tokens revogados.
- [x] Criado seed com usuários iniciais para os três perfis.
- [x] Implementado login com JWT.
- [x] Implementado logout com blacklist de token no banco.
- [x] Implementada rota 'GET /api/v1/auth/me'.
- [x] Implementada rota 'POST /api/v1/auth/register' restrita a administrador.
- [x] Implementadas dependências de segurança: 'get_current_user' e 'require_roles(...)'.
- [x] Implementado CRUD completo de clientes.
- [x] Implementada busca avançada de clientes.
- [x] Implementada normalização de CPF, telefone, e-mail, UF e CEP.
- [x] Implementada validação de duplicidade de CPF e e-mail.
- [x] Implementada integração com ViaCEP no cadastro e atualização de cliente.
- [x] Adicionado '.gitignore' para evitar envio de 'venv', '.env', banco local e caches.
- [x] Validada a execução local com migrations, seed, login, logout, criação, busca e edição de cliente.

## Detalhamento da Entrega 2 - Ordens de serviço

Responsável: Vitor Martins Melo | Matrícula: 2320023

### O que estava previsto

- [x] Modelagem e migration da tabela de OS.
- [x] Relacionamentos: Cliente x OS x Técnico.
- [x] Abertura de OS.
- [x] Atualização de status da OS.
- [x] Atribuição de técnico.
- [x] Encerramento de OS.
- [x] Impedir conclusão de OS sem técnico responsável.
- [x] Bloquear edição de OS já concluídas ou canceladas.
- [x] Validar controle de prioridade (baixa, média, alta, urgente).
- [x] Validar limite máximo de 5 ordens em andamento por técnico.
- [x] Exigir e registrar motivo em caso de cancelamento.

### O que foi feito

- [x] Criado o modelo `OrdemServico` em `app/models/ordem_servico.py` com enums `OSStatus` e `OSPriority`.
- [x] Adicionadas chaves estrangeiras para `clients.id`, `users.id` (técnico) e `users.id` (aberta por).
- [x] Adicionados relacionamentos inversos nos modelos `User` e `Client`.
- [x] Criada migration `202605310001_create_ordens_servico.py` encadeada na entrega anterior.
- [x] Criado `app/repositories/os_repository.py` com listagem filtrada e contagem de OS ativas por técnico.
- [x] Criado `app/services/os_service.py` com todas as regras de negócio.
- [x] Criado `app/routers/ordens_servico.py` com 7 endpoints e controle de acesso por perfil.
- [x] Criados schemas Pydantic em `app/schemas/ordem_servico.py`.
- [x] Numeração automática das OS no formato `OS-{ANO}-{sequencial}`.
- [x] Transição automática de status: `aberta` → `em_andamento` ao atribuir técnico.

### Endpoints implementados

#### Ordens de Serviço

- `POST` → `/api/v1/os` = Abre nova OS (`administrador`, `atendente`)
- `GET` → `/api/v1/os` = Lista OS com filtros opcionais (`todos`)
- `GET` → `/api/v1/os/{os_id}` = Detalha OS (`todos`)
- `PUT` → `/api/v1/os/{os_id}` = Edita OS aberta ou em andamento (`administrador`, `atendente`)
- `PATCH` → `/api/v1/os/{os_id}/assign` = Atribui técnico (`administrador`, `atendente`)
- `PATCH` → `/api/v1/os/{os_id}/close` = Conclui OS (`administrador`, `tecnico`)
- `PATCH` → `/api/v1/os/{os_id}/cancel` = Cancela OS com motivo (`administrador`, `atendente`)

#### Filtros disponíveis em `GET /api/v1/os`

- `status` — `aberta`, `em_andamento`, `concluida`, `cancelada`
- `priority` — `baixa`, `media`, `alta`, `urgente`
- `client_id` — filtra por cliente
- `technician_id` — filtra por técnico
- `search` — busca por título ou número da OS
- `skip` / `limit` — paginação

#### Exemplo de abertura de OS

```json
{
  "title": "Notebook não liga",
  "description": "Cliente relata que o notebook não liga após queda.",
  "priority": "alta",
  "client_id": 1,
  "technician_id": 2
}
```

Resposta:

```json
{
  "id": 1,
  "numero": "OS-2026-000001",
  "status": "em_andamento",
  "priority": "alta",
  "client": { "id": 1, "name": "Maria Souza", ... },
  "technician": { "id": 2, "name": "Técnico", ... },
  "opened_by": { "id": 3, "name": "Atendente", ... },
  "assigned_at": "2026-05-31T...",
  "closed_at": null,
  "cancellation_reason": null
}
```

#### Exemplo de cancelamento

```json
{
  "cancellation_reason": "Cliente desistiu do conserto após orçamento."
}
```

### Regras de negócio

| Regra | Comportamento |
|---|---|
| Conclusão sem técnico | `409 Conflict` — OS precisa de técnico responsável |
| Editar OS terminal | `409 Conflict` — bloqueado se `concluida` ou `cancelada` |
| Técnico com 5 OS ativas | `409 Conflict` — limite máximo por técnico |
| Cancelamento sem motivo | `422 Unprocessable` — campo obrigatório (mín. 5 chars) |
| Prioridade inválida | `422 Unprocessable` — aceita apenas os 4 valores do enum |

## Detalhamento da Entrega 3 - Peças e históricos
[]

## Detalhamento da Entrega 4 - Relatórios, testes e documentação
[]

## Arquitetura do projeto

```text
app/
  core/
    config.py          
    security.py        
  database/
    base.py            
    session.py         
    seed.py            
  dependencies/
    auth.py            
  models/
    user.py            
    client.py          
    revoked_token.py
    ordem_servico.py       ← Entrega 2
  repositories/
    user_repository.py
    client_repository.py
    token_repository.py
    os_repository.py       ← Entrega 2
  routers/
    auth.py            
    clients.py
    ordens_servico.py      ← Entrega 2
  schemas/
    auth.py
    user.py
    client.py
    ordem_servico.py       ← Entrega 2
  services/
    auth_service.py
    client_service.py
    viacep_service.py
    os_service.py          ← Entrega 2
  main.py
alembic/
  versions/
    202605260001_create_users_clients.py
    202605260002_create_revoked_tokens.py
    202605310001_create_ordens_servico.py  ← Entrega 2
```

A organização segue separação por responsabilidade:

- **Routers** recebem as requisições HTTP.
- **Schemas** validam entradas e formatam respostas.
- **Services** concentram regras de negócio.
- **Repositories** concentram acesso ao banco.
- **Models** representam as tabelas.
- **Dependencies** concentram autenticação, autorização e injeções reutilizáveis.

## Como executar

### 1. Ativar o ambiente virtual

```powershell
.\venv\Scripts\Activate.ps1
```

### 2. Instalar dependências

```powershell
pip install -r requirements.txt
```

### 3. Criar o arquivo de ambiente

```powershell
copy .env.example .env
```

### 4. Rodar migrations

```powershell
alembic upgrade head
```

### 5. Rodar seeds

```powershell
python -m app.database.seed
```

### 6. Iniciar a API

```powershell
uvicorn app.main:app --reload
```

A API ficará disponível em:

- API: `http://127.0.0.1:8000`
- Swagger: `http://127.0.0.1:8000/docs`

## Usuários seed

- administrador: admin@assistencia.com | senha: admin123
- tecnico: tecnico@assistencia.com | senha: tecnico123
- atendente: atendente@assistencia.com | senha: atendente123

## Autenticação

O projeto usa JWT Bearer Token.

### Login

Endpoint:

```http
POST /api/v1/auth/login
```

username = E-mail do usuário
password = Senha do usuário

Exemplo:

```text
username=admin@assistencia.com
password=admin123
```

Resposta esperada:

```json
{
  "access_token": "token.jwt.aqui",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "name": "Administrador",
    "email": "admin@assistencia.com",
    "role": "administrador",
    "is_active": true,
    "created_at": "2026-05-27T00:00:00"
  }
}
```

Use o token retornado no header:

```http
Authorization: Bearer token.jwt.aqui
```

### Logout

Endpoint:

```http
POST /api/v1/auth/logout
```

O logout registra o token atual na tabela `revoked_tokens`. Depois disso, o mesmo token passa a retornar `401 Token revogado`.

## Endpoints implementados

### Autenticação

- `POST` -> `/api/v1/auth/login` = Autentica usuário e retorna JWT 
- `POST` -> `/api/v1/auth/logout` = Revoga o token atual 
- `GET` -> `/api/v1/auth/me` = Retorna usuário autenticado 
- `POST` -> `/api/v1/auth/register` = Cadastra novo usuário 

### Clientes

Rotas permitidas para `administrador` e `atendente`.

- `POST` -> `/api/v1/clients` = Cadastra cliente
- `GET` -> `/api/v1/clients` = Lista clientes
- `GET` -> `/api/v1/clients?search=termo` = Busca por nome, CPF, e-mail ou telefone
- `GET` -> `/api/v1/clients/{client_id}` = Detalha cliente
- `PUT` -> `/api/v1/clients/{client_id}` = Atualiza cliente
- `DELETE` -> `/api/v1/clients/{client_id}` = Remove cliente

Exemplo de cadastro de cliente:

```json
{
  "name": "Maria Souza",
  "cpf": "12345678901",
  "phone": "81999998888",
  "email": "maria@email.com",
  "cep": "01001000",
  "number": "100",
  "complement": "Sala 2"
}
```

Quando `cep` for enviado, a API consulta o ViaCEP e preenche automaticamente:

- `street`
- `neighborhood`
- `city`
- `state`

Também é possível enviar esses campos manualmente. Se algum campo de endereço vier vazio e o CEP existir, o ViaCEP será usado para complementar.

## Integração externa

A integração obrigatória da Entrega 1 foi feita com o **ViaCEP**.

Serviço utilizado:

```text
https://viacep.com.br/ws/{cep}/json/
```

Arquivo responsável:

```text
app/services/viacep_service.py
```

Comportamento implementado:

- Consulta o CEP informado no cadastro ou atualização do cliente.
- Preenche endereço automaticamente quando possível.
- Retorna erro `404` quando o CEP não existe.
- Retorna erro `502` quando a API externa está indisponível.



