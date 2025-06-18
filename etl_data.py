import pandas as pd

def load_and_transform_data(acidentes_path, frotas_path):
    # Carregar os dados
    df_acidentes = pd.read_csv(acidentes_path)
    df_frotas = pd.read_csv(frotas_path)

    # Tratamento de dados de acidentes
    df_acidentes['data'] = pd.to_datetime(df_acidentes['data'])
    df_acidentes['dia_semana'] = df_acidentes['data'].dt.day_name()
    df_acidentes['hora'] = pd.to_datetime(df_acidentes['hora'], format='%H:%M').dt.time

    # Criar faixa de horário
    def get_faixa_horario(hora):
        if hora >= pd.to_datetime('05:00').time() and hora < pd.to_datetime('12:00').time():
            return 'Manhã'
        elif hora >= pd.to_datetime('12:00').time() and hora < pd.to_datetime('18:00').time():
            return 'Tarde'
        elif hora >= pd.to_datetime('18:00').time() and hora < pd.to_datetime('23:00').time():
            return 'Noite'
        else:
            return 'Madrugada'

    df_acidentes['faixa_horario'] = df_acidentes['hora'].apply(get_faixa_horario)

    # Combinar rodovia e km para identificar trechos
    df_acidentes['trecho'] = df_acidentes['rodovia'] + '-' + df_acidentes['km'].astype(str)

    return df_acidentes, df_frotas

if __name__ == '__main__':
    df_acidentes, df_frotas = load_and_transform_data('acidentes2025_estruturado.csv', 'frotas_veiculos_2023.csv')
    print('DataFrame de Acidentes (primeiras 5 linhas):')
    print(df_acidentes.head())
    print('\nDataFrame de Frotas (primeiras 5 linhas):')
    print(df_frotas.head())




    df_acidentes.to_pickle('df_acidentes.pkl')
    df_frotas.to_pickle('df_frotas.pkl')

