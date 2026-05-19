# G53 – Brokers and Clients' Transactions

Aplicação web de gestão de corretores, clientes e transações financeiras,
desenvolvida no âmbito da unidade curricular de PCII.

## Funcionalidades

- **Portal de acesso** com pesquisa por Corporação, Broker ou Cliente
- **Dashboard de Corporação** — visão geral dos brokers, volume total (AUM),
  ticket médio e análise de risco de concentração por broker
- **Dashboard de Broker** — carteira de clientes, top 5 por volume e nível de risco
- **Dashboard de Cliente** — histórico de investimentos, distribuição por corretor
  e operações de depósito/levantamento em tempo real
- **Análise de risco automática** com Pandas — classifica carteiras em BAIXO,
  MÉDIO ou ALTO risco com base na concentração por cliente
- **Gráficos interativos** com Plotly (pie charts e bar charts)

## Estrutura do projeto

    g53_project/
      app.py              # servidor Flask e rotas
      classes/            # modelo de classes (Gclass, Corporation, Broker, Client, Trade)
      data/business.db    # base de dados SQLite
      templates/          # páginas HTML
      migracao.ipynb      # migração dos dados CSV para a BD
      main_teste.py       # testes das classes no terminal

## Como correr localmente

    python app.py

Abrir em: http://127.0.0.1:5001

## Tecnologias

- Python 3 / Flask
- SQLite (via DB Browser)
- Pandas
- Plotly

## Publicação

Disponível em: https://up202504207.pythonanywhere.com