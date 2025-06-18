import plotly.io as pio
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
import os

def export_graphs_to_png():
    """Exporta gráficos para PNG"""
    # Carregar os dados
    df_acidentes = pd.read_pickle("df_acidentes.pkl")
    df_frotas = pd.read_pickle("df_frotas.pkl")
    
    # Preparar dados para análises
    acidentes_por_municipio = df_acidentes.groupby("municipio").size().reset_index(name="total_acidentes")
    frota_por_municipio = df_frotas.groupby("municipio")["quantidade"].sum().reset_index(name="total_frota")
    df_correlacao = pd.merge(acidentes_por_municipio, frota_por_municipio, on="municipio", how="inner")
    
    # Criar diretório para exportações
    os.makedirs("exports", exist_ok=True)
    
    # Gráfico de tipos de acidente
    import plotly.express as px
    tipo_counts = df_acidentes['tipo_acidente'].value_counts()
    fig_tipo = px.pie(
        values=tipo_counts.values,
        names=tipo_counts.index,
        title="Distribuição por Tipo de Acidente"
    )
    fig_tipo.write_image("exports/grafico_tipos_acidente.png", width=800, height=600)
    
    # Gráfico por dia da semana
    dia_counts = df_acidentes['dia_semana'].value_counts()
    fig_dia = px.bar(
        x=dia_counts.index,
        y=dia_counts.values,
        title="Acidentes por Dia da Semana",
        labels={'x': 'Dia da Semana', 'y': 'Número de Acidentes'}
    )
    fig_dia.write_image("exports/grafico_dia_semana.png", width=800, height=600)
    
    # Gráfico por faixa de horário
    horario_counts = df_acidentes['faixa_horario'].value_counts()
    fig_horario = px.bar(
        x=horario_counts.index,
        y=horario_counts.values,
        title="Acidentes por Faixa de Horário",
        labels={'x': 'Faixa de Horário', 'y': 'Número de Acidentes'}
    )
    fig_horario.write_image("exports/grafico_faixa_horario.png", width=800, height=600)
    
    # Gráfico de correlação
    fig_correlacao = px.scatter(
        df_correlacao,
        x="total_frota",
        y="total_acidentes",
        hover_name="municipio",
        title="Correlação: Frota de Veículos vs Acidentes",
        labels={'total_frota': 'Total da Frota', 'total_acidentes': 'Total de Acidentes'}
    )
    fig_correlacao.write_image("exports/grafico_correlacao.png", width=800, height=600)
    
    print("Gráficos exportados para a pasta 'exports' em formato PNG")

def export_table_to_pdf():
    """Exporta tabela de trechos críticos para PDF"""
    # Carregar os dados
    df_acidentes = pd.read_pickle("df_acidentes.pkl")
    
    # Criar ranking dos trechos mais críticos
    trechos_criticos = df_acidentes.groupby(['trecho', 'rodovia', 'municipio', 'uf']).size().reset_index(name='total_acidentes').sort_values('total_acidentes', ascending=False).head(50)
    
    # Criar PDF
    doc = SimpleDocTemplate("exports/ranking_trechos_criticos.pdf", pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    
    # Título
    title = Paragraph("Ranking dos Trechos Mais Críticos", styles['Title'])
    story.append(title)
    story.append(Spacer(1, 12))
    
    # Preparar dados da tabela
    data = [['Trecho', 'Rodovia', 'Município', 'UF', 'Total Acidentes']]
    for _, row in trechos_criticos.iterrows():
        data.append([row['trecho'], row['rodovia'], row['municipio'], row['uf'], str(row['total_acidentes'])])
    
    # Criar tabela
    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    story.append(table)
    doc.build(story)
    
    print("Tabela de trechos críticos exportada para 'exports/ranking_trechos_criticos.pdf'")

if __name__ == "__main__":
    export_graphs_to_png()
    export_table_to_pdf()

