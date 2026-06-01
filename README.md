# G53 – Brokers and Clients' Transactions

Aplicação web de gestão de corretores, clientes e transações financeiras,
desenvolvida no âmbito da unidade curricular de PCII.

## Credenciais de Acesso

| Utilizador | Password | Acesso                          |
|------------|----------|---------------------------------|
| admin      | admin    | Portal de administração completo |
| corp       | corp     | Dashboard da primeira corporação |
| broker     | broker   | Dashboard do primeiro corretor   |
| client     | client   | Dashboard do primeiro cliente    |

## Funcionalidades

### Portal de Administração
- Pesquisa, filtros de risco e ordenação por métricas (clientes ativos, ticket médio, nº transações)
- **Adicionar e remover** corporações, corretores e clientes com confirmação e cascade automático (remover uma corporação apaga os seus corretores e respetivas transações)

### Dashboard de Corporação
- Visão geral dos corretores, volume total (AUM), ticket médio e risco corporativo (ESTÁVEL / ATENÇÃO / CRÍTICO)
- **Gestão de corretores** diretamente na dashboard: adicionar novo corretor ou remover existente
- **Encerrar corporação** — apaga a corporação, todos os seus corretores e transações associadas

### Dashboard de Corretor
- Carteira de clientes, top 5 por volume e nível de risco de concentração (BAIXO / MÉDIO / ALTO, thresholds: >10% e >7.5%)
- **Associar e remover clientes** da carteira com aviso do valor em risco antes de confirmar
- **Encerrar corretor** — liquida automaticamente os saldos dos clientes e remove o corretor do sistema

### Dashboard de Cliente
- Histórico de investimentos, distribuição por corretor e gráfico de alocação
- **Depositar e levantar fundos** em tempo real com validação de saldo (não permite levantar mais do que o saldo disponível no corretor selecionado)
- **Encerrar conta** — liquida o saldo em todos os corretores e remove o cliente do sistema

### Estatísticas Globais
- Top 10 corporações e top 5 corretores por volume
- KPIs gerais: total de transações, volume total (AUM), nº de corporações, corretores e clientes

### Análise de Risco Automática
- Classifica carteiras de corretores em BAIXO, MÉDIO ou ALTO com base na concentração por cliente
- Risco corporativo agrega o estado de todos os corretores associados
- Gráficos interativos com Plotly (pie charts e bar charts com tooltips formatados)

## Estrutura do Projeto

    g53_project/
      app.py                  # servidor Flask e rotas
      classes/                # modelo de classes (Gclass, Corporation, Broker, Client, Trade)
      data/business.db        # base de dados SQLite
      templates/              # páginas HTML (Jinja2)
      static/
        css/                  # folhas de estilo por página
        js/                   # scripts por página
        images/               # ícones e logo
      G53_data (1).csv        # dados originais (57 corretores, 100 corporações, 100 clientes, 5000 transações)
      migracao.ipynb          # migração dos dados CSV para a BD
      main_teste.py           # testes das classes no terminal

## Como Correr Localmente

    python app.py

Abrir em: http://127.0.0.1:5001

## Tecnologias

- Python 3 / Flask
- SQLite
- Pandas
- Plotly

## Publicação

Disponível em: https://up202504207.pythonanywhere.com
