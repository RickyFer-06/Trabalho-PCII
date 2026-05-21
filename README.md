# G53 – Brokers and Clients' Transactions

Aplicação web de gestão de corretores, clientes e transações financeiras,
desenvolvida no âmbito da unidade curricular de PCII.

## Credenciais de Acesso

| Utilizador | Password | Acesso                          |
|------------|----------|---------------------------------|
| admin      | admin    | Portal de administração completo |
| corp       | corp     | Dashboard da primeira corporação |
| broker     | broker   | Dashboard do primeiro broker     |
| client     | client   | Dashboard do primeiro cliente    |

## Funcionalidades

- **Portal de acesso** com pesquisa por Corporação, Broker ou Cliente
- **Portal de administração** com pesquisa, filtros de risco e ordenação por métricas (clientes ativos, ticket médio, nº transações)
- **Dashboard de Corporação** — visão geral dos brokers, volume total (AUM), ticket médio e risco corporativo (ESTÁVEL / ATENÇÃO / CRÍTICO)
- **Dashboard de Broker** — carteira de clientes, top 5 por volume e nível de risco de concentração (BAIXO / MÉDIO / ALTO, thresholds: >10% e >7.5%)
- **Dashboard de Cliente** — histórico de investimentos, distribuição por corretor e operações de depósito/levantamento em tempo real com validação de saldo
- **Estatísticas globais** — top 10 corporações e top 5 brokers por volume, KPIs gerais do sistema
- **Análise de risco automática** com Pandas — classifica carteiras em BAIXO, MÉDIO ou ALTO com base na concentração por cliente; risco corporativo agrega o estado de todos os brokers
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