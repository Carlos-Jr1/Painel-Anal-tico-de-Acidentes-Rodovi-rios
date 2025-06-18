import pandas as pd

def perform_statistical_analysis():
    # Carregar os dataframes processados
    df_acidentes = pd.read_pickle("df_acidentes.pkl")
    df_frotas = pd.read_pickle("df_frotas.pkl")

    print("\n--- Análises Estatísticas ---")

    # 1. Total de acidentes por rodovia, trecho e município
    print("\nTotal de acidentes por Rodovia:")
    print(df_acidentes["rodovia"].value_counts().reset_index(name="Total Acidentes"))

    print("\nTotal de acidentes por Trecho (Rodovia-KM):")
    print(df_acidentes["trecho"].value_counts().reset_index(name="Total Acidentes"))

    print("\nTotal de acidentes por Município:")
    print(df_acidentes["municipio"].value_counts().reset_index(name="Total Acidentes"))

    # 2. Acidentes por dia da semana e horário
    print("\nAcidentes por Dia da Semana:")
    print(df_acidentes["dia_semana"].value_counts().reindex(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']).reset_index(name="Total Acidentes"))

    print("\nAcidentes por Faixa de Horário:")
    print(df_acidentes["faixa_horario"].value_counts().reindex(['Madrugada', 'Manhã', 'Tarde', 'Noite']).reset_index(name="Total Acidentes"))

    # 3. Distribuição por tipo de acidente
    print("\nDistribuição por Tipo de Acidente:")
    print(df_acidentes["tipo_acidente"].value_counts().reset_index(name="Total Acidentes"))

    # 4. Correlação entre frota de veículos e número de acidentes
    # Agrupar acidentes por município
    acidentes_por_municipio = df_acidentes.groupby("municipio").size().reset_index(name="total_acidentes")

    # Agrupar frota por município (somar todos os tipos de veículos para simplificar)
    frota_por_municipio = df_frotas.groupby("municipio")["quantidade"].sum().reset_index(name="total_frota")

    # Juntar os dois dataframes
    df_correlacao = pd.merge(acidentes_por_municipio, frota_por_municipio, on="municipio", how="inner")

    print("\nCorrelação entre Frota de Veículos e Número de Acidentes por Município:")
    print(df_correlacao)
    print("\nCoeficiente de Correlação (Frota vs Acidentes):", df_correlacao["total_frota"].corr(df_correlacao["total_acidentes"]))

if __name__ == "__main__":
    perform_statistical_analysis()


