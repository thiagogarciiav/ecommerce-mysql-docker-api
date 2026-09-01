<h1>
  Projeto MySQL + Docker
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/mysql/mysql-plain-wordmark.svg" width="40" height="40" align="center" />
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/docker/docker-plain-wordmark.svg" width="40" height="40" align="center" />
</h1>    

Projeto exemplo com Docker, MySQL e Flask, demonstrando boas práticas de desenvolvimento com banco de dados relacional.

## Funcionalidades

- **Banco de dados MySQL** com:
  - Tabelas normalizadas: `users`, `products`, `orders`, `order_items`
  - Índices em chaves estrangeiras e colunas de busca
  - Procedures armazenadas (ex: relatório de vendas)
  - Triggers (ex: atualização automática de estoque)
  - Views (ex: resumo de pedidos por cliente)
  - Eventos (ex: limpeza de logs antigos)

- **API REST (Flask)** com endpoints:
  - `GET /users` – lista todos os usuários
  - `POST /users` – cria novo usuário
  - `GET /products` – lista produtos (com filtro por nome)
  - `POST /orders` – cria um pedido (com validação de estoque via trigger)
  - `GET /reports/sales` – relatório de vendas (usa procedure)

- **Docker Compose** para subir todo o ambiente com um comando.

## Pré‑requisitos

- Docker e Docker Compose instalados
- Git (para clonar)

## Como executar

1. **Clone o repositório**
   ```bash
   git clone https://github.com/seu-usuario/meu-projeto-mysql-docker.git
   cd meu-projeto-mysql-docker
