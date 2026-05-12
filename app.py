#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  7 17:58:52 2026

@author: goncalotavares
"""
import pandas as pd
import plotly.express as px
import plotly.io as pio

from flask import Flask, render_template, request, redirect
from classes.corporation import Corporation
from classes.client import Client
from classes.broker import Broker
from classes.trade import Trade


app = Flask(__name__)


db_path = 'data/business.db'
Corporation.read(db_path)
Broker.read(db_path)
Client.read(db_path)  
Trade.read(db_path)


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
            broker_stats.append({'obj': b, 'aum': 0, 'risk_status': 'N/A', 'risk_color': '#95a5a6'})
            continue

        df_b = pd.DataFrame([{'client_id': t.client_id, 'amount': t.amount} for t in b_trades])
        b_aum = df_b['amount'].sum()
        
        max_conc_pct = (df_b.groupby('client_id')['amount'].sum().max() / b_aum) * 100
        
        if max_conc_pct > 50:
            status, color = 'ALTO', '#e74c3c'
        elif max_conc_pct > 25:
            status, color = 'MÉDIO', '#f1c40f'
        else:
            status, color = 'BAIXO', '#27ae60'
            
        broker_stats.append({
            'obj': b,
            'aum': b_aum,
            'num_clients': df_b['client_id'].nunique(),
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
        return "Erro: Broker não encontrado!"
    
    broker = Broker.obj[id]
    empresa = Corporation.obj[broker.corporation_id].name if broker.corporation_id in Corporation.obj else "Independente"
    
    trades_list = []
    for t in Trade.obj.values():
        if t.broker_id == id:
            c_name = Client.obj[t.client_id].name if t.client_id in Client.obj else f"Cliente {t.client_id}"
            trades_list.append({
                'client_name': c_name,
                'amount': t.amount,
                'date': t.date,
                'trade_name': t.name})
    
    df = pd.DataFrame(trades_list)
    if df.empty:
        return render_template('broker_dashboard.html', broker=broker, empresa=empresa, total_investido=0, risco={'nivel': 'N/A'}, graph_html=None)
    
    total_aum = df['amount'].sum()
    ticket_medio = df['amount'].mean()
    num_clientes = df['client_name'].nunique()
    
    df_clientes = df.groupby('client_name')['amount'].sum().reset_index()
    
    maior_fatia = df_clientes['amount'].max()
    percentagem_maior_cliente = (maior_fatia/total_aum)*100
    nome_maior_cliente = df_clientes.loc[df_clientes['amount'].idxmax(),'client_name']
    
    if percentagem_maior_cliente > 50:
        risco = {'nivel': 'ALTO', 'cor': '#e74c3c', 'msg': f'Cuidado! {nome_maior_cliente} detém {percentagem_maior_cliente:.1f}% da carteira.'}
    elif percentagem_maior_cliente > 25:
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
                           negocios=df.to_dict('records'))

@app.route('/cliente/<int:id>/dashboard')
def cliente_dashboard(id):
    if id not in Client.obj:
        return "Erro: Cliente não encontrado!", 404

    cliente = Client.obj[id]
    
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
    df_cliente = df_all[df_all['client_id']==id]
    
    if df_cliente.empty:
        return render_template('cliente_dashboard.html', cliente=cliente, negocios = [], total_investido=0, graph_html=None)
    
    total_investido = df_cliente['amount'].sum()
    total_negocios = len(df_cliente)
    
    df_grouped = df_cliente.groupby('broker_name')['amount'].sum().reset_index()
    
    fig = px.pie(df_grouped, values='amount', names='broker_name',
                 title='Distribuição de Investimento por Corretor',
                 hole=0.4,
                 color_discrete_sequence=px.colors.sequential.RdBu)
    
    graph_html = pio.to_html(fig, full_html=False)
    
    return render_template('cliente_dashboard.html', 
                           cliente=cliente, 
                           negocios=df_cliente.to_dict('records'),
                           total_investido=total_investido,
                           total_negocios=total_negocios,
                           graph_html=graph_html)
    

if __name__ == '__main__':
    app.run(debug=True) 
    
