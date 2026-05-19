import os
import pandas as pd
import plotly.express as px
import plotly.io as pio
from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for
from classes.corporation import Corporation
from classes.client import Client
from classes.broker import Broker
from classes.trade import Trade


app = Flask(__name__)

@app.template_filter('moeda')
def moeda_filter(value):
    return f"{value:,.2f} €".replace(',', 'X').replace('.', ',').replace('X', '.')

db_path = os.path.join(os.path.dirname(__file__), 'data/business.db')
Corporation.read(db_path)
Broker.read(db_path)
Client.read(db_path)  
Trade.read(db_path)

@app.route('/')
def home():
    return redirect(url_for('index'))

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/user_login')
def user_login():
    return render_template('login.html', user='', password='', resul='')

@app.route('/chklogin', methods=['POST'])
def chklogin():
    user = request.form.get('user')
    password = request.form.get('password')
    
    if user == 'admin' and password == 'admin':
        return redirect(url_for('login_simulado'))
    elif user == 'corp' and password == 'corp':
        # Assumiremos a primeira corporation da lista para efeitos de demonstração
        primeira_corp = Corporation.lst[0] if Corporation.lst else 1
        return redirect(url_for('corporation_dashboard', id=primeira_corp))
    elif user == 'broker' and password == 'broker':
        # Assumiremos o primeiro broker da lista
        primeiro_broker = Broker.lst[0] if Broker.lst else 1
        return redirect(url_for('broker_dashboard', id=primeiro_broker))
    elif user == 'client' and password == 'client':
        # Assumiremos o primeiro cliente da lista
        primeiro_cliente = Client.lst[0] if Client.lst else 1
        return redirect(url_for('cliente_dashboard', id=primeiro_cliente))
    else:
        return render_template('login.html', user=user, password=password, resul='Credenciais inválidas. Tente novamente!')

@app.route('/login')
def login_simulado():
    
    corps = [Corporation.obj[id] for id in Corporation.lst]
    brokers = [Broker.obj[id] for id in Broker.lst]
    clients = [Client.obj[id] for id in Client.lst]
    
    return render_template('login_simulado.html', 
                           lista_corps=corps, 
                           lista_brokers=brokers, 
                           lista_clients=clients)
    
@app.route('/corporation/<int:id>/dashboard')
def corporation_dashboard(id):
    if id not in Corporation.obj:
        return "Erro: Corporação não encontrada!", 404
    
    corp = Corporation.obj[id]
    
    corp_brokers = [Broker.obj[b_id] for b_id in Broker.lst if Broker.obj[b_id].corporation_id == id]
    
    broker_stats = []
    total_trades_list = []
    
    for b in corp_brokers:

        b_trades = [Trade.obj[t_id] for t_id in Trade.lst if Trade.obj[t_id].broker_id == b.id]
        
        if not b_trades:
            broker_stats.append({'obj': b, 'aum': 0, 'num_clients': 0, 'clients': [], 'risk_status': 'N/A', 'risk_color': '#95a5a6'})
            continue

        df_b = pd.DataFrame([{'client_id': t.client_id, 'amount': t.amount} for t in b_trades])
        b_aum = df_b['amount'].sum()
        
        max_conc_pct = (df_b.groupby('client_id')['amount'].sum().max() / b_aum) * 100
        
        if max_conc_pct > 10:
            status, color = 'ALTO', '#e74c3c'
        elif max_conc_pct > 7.5:
            status, color = 'MÉDIO', '#f1c40f'
        else:
            status, color = 'BAIXO', '#27ae60'
            
        clientes_info = []
        for c_id, group in df_b.groupby('client_id'):
            c_name = Client.obj[c_id].name if c_id in Client.obj else f"Cliente {c_id}"
            clientes_info.append({'name': c_name, 'amount': group['amount'].sum()})
            
        # Ordenar os clientes por amount descrescente para melhor visualização
        clientes_info = sorted(clientes_info, key=lambda x: x['amount'], reverse=True)
            
        broker_stats.append({
            'obj': b,
            'aum': b_aum,
            'num_clients': df_b['client_id'].nunique(),
            'clients': clientes_info,
            'risk_status': status,
            'risk_color': color
        })
        total_trades_list.extend([t.amount for t in b_trades])

    total_aum = sum(total_trades_list)
    avg_ticket = sum(total_trades_list) / len(total_trades_list) if total_trades_list else 0
    
    risk_series = pd.Series([s['risk_status'] for s in broker_stats])
    pct_alto = (risk_series == 'ALTO').mean() * 100
    
    if pct_alto > 30:
        corp_risk = {'nivel': 'CRÍTICO', 'cor': '#c0392b', 'msg': 'ALERTA: Mais de 30% da equipa está em risco de concentração!'}
    elif pct_alto > 10 or (risk_series == 'MÉDIO').sum() > (len(corp_brokers)/2):
        corp_risk = {'nivel': 'ATENÇÃO', 'cor': '#d35400', 'msg': 'Exposição moderada. Recomenda-se diversificar carteiras.'}
    else:
        corp_risk = {'nivel': 'ESTÁVEL', 'cor': '#27ae60', 'msg': 'A estrutura de brokers está saudável e diversificada.'}

    df_plot = pd.DataFrame([{'Broker': s['obj'].name, 'AUM': s['aum']} for s in broker_stats if s['aum'] > 0])
    if not df_plot.empty:
        fig = px.pie(df_plot, values='AUM', names='Broker', title='Distribuição de Volume por Broker', hole=0.4)
        graph_html = pio.to_html(fig, full_html=False)
    else:
        graph_html = "<p class='text-muted'>Nenhum dado de volume disponível para gerar o gráfico.</p>"

    return render_template('corporation_dashboard.html',
                           corp=corp,
                           aum=total_aum,
                           avg_ticket=avg_ticket,
                           num_brokers=len(corp_brokers),
                           risk=corp_risk,
                           graph_html=graph_html,
                           brokers=broker_stats)

@app.route('/broker/<int:id>/dashboard')
def broker_dashboard(id):
    if id not in Broker.obj:
        return "Erro: Broker não encontrado!", 404
    
    broker = Broker.obj[id]
    empresa = Corporation.obj[broker.corporation_id].name if broker.corporation_id in Corporation.obj else "Independente"
    
    trades_list = []
    # Agrupar trades por cliente
    clientes_dict = {}
    
    for t in Trade.obj.values():
        if t.broker_id == id:
            c_name = Client.obj[t.client_id].name if t.client_id in Client.obj else f"Cliente {t.client_id}"
            trade_info = {
                'id': t.id,
                'client_name': c_name,
                'amount': t.amount,
                'date': t.date,
                'trade_name': t.name
            }
            trades_list.append(trade_info)
            
            if t.client_id not in clientes_dict:
                clientes_dict[t.client_id] = {'name': c_name, 'total': 0, 'trades': []}
            clientes_dict[t.client_id]['total'] += t.amount
            clientes_dict[t.client_id]['trades'].append(trade_info)
            
    df = pd.DataFrame(trades_list)
    
    # Passando a lista de clientes para a view
    lista_clientes = sorted(clientes_dict.values(), key=lambda x: x['total'], reverse=True)
    
    if df.empty:
        return render_template('broker_dashboard.html', broker=broker, empresa=empresa, total_investido=0, ticket_medio=0, num_clientes=0, risco={'nivel': 'N/A', 'cor': '#95a5a6', 'msg': 'Sem dados suficientes.'}, graph_html=None, negocios=[], lista_clientes=[])
    
    total_aum = df['amount'].sum()
    ticket_medio = df['amount'].mean()
    num_clientes = df['client_name'].nunique()
    
    df_clientes = df.groupby('client_name')['amount'].sum().reset_index()
    
    maior_fatia = df_clientes['amount'].max()
    percentagem_maior_cliente = (maior_fatia/total_aum)*100
    nome_maior_cliente = df_clientes.loc[df_clientes['amount'].idxmax(),'client_name']
    
    if percentagem_maior_cliente > 10:
        risco = {'nivel': 'ALTO', 'cor': '#e74c3c', 'msg': f'Cuidado! {nome_maior_cliente} detém {percentagem_maior_cliente:.1f}% da carteira.'}
    elif percentagem_maior_cliente > 7.5:
        risco = {'nivel': 'MÉDIO', 'cor': '#f1c40f', 'msg': 'Dependência moderada de um único cliente.'}
    else:
        risco = {'nivel': 'BAIXO', 'cor': '#27ae60', 'msg': 'Carteira bem diversificada.'}
        
    fig = px.bar(df_clientes.sort_values('amount',ascending=True).tail(5),
                 x = 'amount', y='client_name', orientation='h',
                 title= 'Top 5 Clientes por Volume',
                 labels= {'amount':'Volume(€)','client_name':'Cliente'},
                 color= 'amount', color_continuous_scale='Blues')
    
    graph_html = pio.to_html(fig, full_html=False)
    
    return render_template('broker_dashboard.html',
                           broker = broker,
                           empresa = empresa,
                           total_investido=total_aum,
                           ticket_medio=ticket_medio,
                           num_clientes=num_clientes,
                           risco=risco,
                           graph_html=graph_html,
                           negocios=trades_list,
                           lista_clientes=lista_clientes)

@app.route('/cliente/<int:id>/dashboard')
def cliente_dashboard(id):
    if id not in Client.obj:
        return "Erro: Cliente não encontrado!", 404

    cliente = Client.obj[id]
    todos_brokers = [Broker.obj[bid] for bid in Broker.lst]
    
    trades_data = []
    for t in Trade.obj.values():
        if t.client_id == id:
            b_name = Broker.obj[t.broker_id].name if t.broker_id in Broker.obj else "Desconhecido"
            
            trades_data.append({
                'id': t.id,
                'broker_name': b_name, 
                'client_id': t.client_id, 
                'amount': t.amount,
                'name': t.name,
                'date': t.date
            })
    
    df_all = pd.DataFrame(trades_data)
    if df_all.empty:
        return render_template('cliente_dashboard.html', cliente=cliente, brokers=todos_brokers, negocios=[], total_investido=0, total_negocios=0, graph_html=None)
    
    if df_all.empty:
        return render_template('cliente_dashboard.html', cliente=cliente, negocios = [], total_investido=0, graph_html=None)
    
    total_investido = df_all['amount'].sum()
    total_negocios = len(df_all)
    
    df_grouped = df_all.groupby('broker_name')['amount'].sum().reset_index()
    df_grouped = df_grouped[df_grouped['amount'] > 0]
    
    if not df_grouped.empty:
        fig = px.pie(df_grouped, values='amount', names='broker_name',
                     title='Distribuição de Investimento por Corretor',
                     hole=0.4,
                     color_discrete_sequence=px.colors.sequential.RdBu)
        
        graph_html = pio.to_html(fig, full_html=False)
    else:
        graph_html = "<p style='text-align:center; color:#7f8c8d;'>Sem investimentos ativos no momento.</p>"
    
    return render_template('cliente_dashboard.html', 
                           cliente=cliente, 
                           brokers=todos_brokers,
                           negocios=df_all.to_dict('records'),
                           total_investido=total_investido,
                           total_negocios=total_negocios,
                           graph_html=graph_html)
    
@app.route('/trade/new', methods=['POST'])
def new_trade():
    client_id = int(request.form.get('client_id'))
    broker_id = int(request.form.get('broker_id'))
    amount = float(request.form.get('amount'))
    tipo = request.form.get('tipo')
        
        # 1. Gerar a data atual no momento do clique
    data_atual = datetime.now().strftime("%Y-%m-%d") # Podes ajustar o formato (ex: "%d/%m/%Y")
        
        # 2. Definir o t.name e ajustar o sinal do amount
    if tipo == 'investir':
        trade_name = "Novo Investimento"
        amount = abs(amount)
    else:
        saldo_neste_broker = sum(t.amount for t in Trade.obj.values() if t.client_id == client_id and t.broker_id == broker_id)
        
        # 2. A "Parede de Segurança": Se tentar levantar mais do que tem...
        if amount > saldo_neste_broker:
            # Retorna uma mensagem de erro simples (no futuro podes fazer isto aparecer num Pop-up bonito)
            return f"<h1>Operação Recusada!</h1><p>Tentou levantar {amount}€, mas o seu saldo no Broker selecionado é de apenas {saldo_neste_broker}€.</p><a href='/cliente/{client_id}/dashboard'>Voltar à Dashboard</a>", 400
        trade_name = "Levantamento"
        amount = -abs(amount)
        
        # 3. Gerar ID e criar o objeto
    new_id = max(Trade.lst) + 1 if Trade.lst else 1
        
        # Substitui pela ordem EXATA dos argumentos do teu __init__ da classe Trade
        # Assumi que a tua ordem é (id, client_id, broker_id, amount, date, name)
    Trade(new_id, broker_id, client_id, trade_name, data_atual, amount)
    
    query = f"INSERT INTO Trade (id, broker_id, client_id, name, date, amount) VALUES ({new_id}, {broker_id}, {client_id}, '{trade_name}', '{data_atual}', {amount})"
    
    # Executamos o comando através da classe Trade (que herdou sqlexe do Gclass)
    Trade.sqlexe(query)
        
    return redirect(url_for('cliente_dashboard', id=client_id))

@app.route('/stats')
def stats():
    all_trades = list(Trade.obj.values())
    total_trades = len(all_trades)
    total_aum = sum(t.amount for t in all_trades)

    corp_volumes = {}
    for t in all_trades:
        broker = Broker.obj.get(t.broker_id)
        if broker:
            corp = Corporation.obj.get(broker.corporation_id)
            if corp:
                corp_volumes[corp.name] = corp_volumes.get(corp.name, 0) + t.amount

    df_corp = pd.DataFrame(list(corp_volumes.items()), columns=['Corporação', 'Volume'])
    df_corp = df_corp.sort_values('Volume', ascending=True).tail(10)
    fig_corp = px.bar(df_corp, x='Volume', y='Corporação', orientation='h',
        title='Top 10 Corporações por Volume',
        color='Volume', color_continuous_scale='Blues')
    graph_corp = pio.to_html(fig_corp, full_html=False)

    broker_volumes = {}
    for t in all_trades:
        broker = Broker.obj.get(t.broker_id)
        if broker:
            broker_volumes[broker.name] = broker_volumes.get(broker.name, 0) + t.amount

    df_broker = pd.DataFrame(list(broker_volumes.items()), columns=['Broker', 'Volume'])
    df_broker = df_broker.sort_values('Volume', ascending=True).tail(5)
    fig_broker = px.bar(df_broker, x='Volume', y='Broker', orientation='h',
                        title='Top 5 Brokers por Volume',
                        color='Volume', color_continuous_scale='Blues')
    graph_broker = pio.to_html(fig_broker, full_html=False)

    return render_template('stats.html',
                           total_trades=total_trades,
                           total_aum=total_aum,
                           num_clients=len(Client.lst),
                           num_brokers=len(Broker.lst),
                           num_corps=len(Corporation.lst),
                           graph_corp=graph_corp,
                           graph_broker=graph_broker)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
    
