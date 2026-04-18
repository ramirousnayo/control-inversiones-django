from django.shortcuts import render
from .models import DepositoPlazo
from datetime import date, timedelta
from decimal import Decimal
import pandas as pd
import io
import base64

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def dashboard(request):
    depositos = DepositoPlazo.objects.all()

    hoy = date.today()
    prox_30 = hoy + timedelta(days=30)

    capital_total = Decimal(0)
    interes_total = Decimal(0)
    monto_30_dias = Decimal(0)

    datos_flujo = []
    datos_bancos = {}

    for d in depositos:
        interes = d.interes_ganado()
        monto = d.monto_final()

        capital_total += d.capital
        interes_total += interes

        if hoy <= d.fecha_vencimiento <= prox_30:
            monto_30_dias += monto

        datos_flujo.append({
            'fecha': d.fecha_vencimiento,
            'monto': float(monto)
        })

        # Acumulado por banco (capital)
        datos_bancos[d.banco.nombre] = datos_bancos.get(d.banco.nombre, 0) + float(d.capital)

    # -------- Gráfica flujo mensual --------
    grafico_flujo = None
    tabla = []

    if datos_flujo:
        df = pd.DataFrame(datos_flujo)
        df['fecha'] = pd.to_datetime(df['fecha'])
        df['mes'] = df['fecha'].dt.to_period('M')

        df_mensual = df.groupby('mes')['monto'].sum().reset_index()
        df_mensual['mes'] = df_mensual['mes'].astype(str)

        fig, ax = plt.subplots()
        ax.bar(df_mensual['mes'], df_mensual['monto'])
        ax.set_title('Flujo de Caja Mensual por Vencimientos')
        ax.set_xlabel('Mes')
        ax.set_ylabel('Monto')

        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        grafico_flujo = base64.b64encode(buffer.getvalue()).decode('utf-8')
        buffer.close()
        plt.close(fig)

        tabla = df_mensual.to_dict('records')

    # -------- Gráfica torta por banco --------
    grafico_bancos = None

    if datos_bancos:
        fig2, ax2 = plt.subplots()
        ax2.pie(datos_bancos.values(), labels=datos_bancos.keys(), autopct='%1.1f%%')
        ax2.set_title('Distribución de Capital por Banco')

        buffer2 = io.BytesIO()
        plt.savefig(buffer2, format='png')
        buffer2.seek(0)
        grafico_bancos = base64.b64encode(buffer2.getvalue()).decode('utf-8')
        buffer2.close()
        plt.close(fig2)

    context = {
        'capital_total': f"{capital_total:,.0f}",
        'interes_total': f"{interes_total:,.0f}",
        'monto_30_dias': f"{monto_30_dias:,.0f}",
        'grafico_flujo': grafico_flujo,
        'grafico_bancos': grafico_bancos,
        'tabla': tabla
    }

    return render(request, 'depositos/dashboard.html', context)
