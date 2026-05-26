import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

def main():
    """
    Gera uma imagem (.png) com um gráfico (plot) da
    temperatura nos últimos 7 dias em Guarulhos, com
    máxima e mínima.
    """
    daily_data, start_date, end_date = requestdata()
    frame = dframe(daily_data)
    graph = mathgraph(frame, start_date, end_date)

def requestdata():
    """Função responsável por obter o Weather report
    de Guarulhos nos últimos 7 dias.

    Returns:
        tuple: Uma tupla que contém um 
        dicionário com informações de temp e dias, 
        e duas strings referentes ao
        intervalo de tempo (dias)
    """
    # Uso do requests e API meteo

    today = datetime.now()
    week_ago = today - timedelta(days=7)

    # Formata as datas para a API
    # no modelo esperado (YYYY-MM-DD)
    start_date = week_ago.strftime("%Y-%m-%d")
    end_date = today.strftime("%Y-%m-%d")

    # Guarulhos
    latitude = -23.4628
    longitude = -46.5333

    # Temperatura de Guarulhos na última semana
    url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&start_date={start_date}&end_date={end_date}&daily=temperature_2m_max,temperature_2m_min"

    response = requests.get(url)
    data = response.json()

    # Dados do dia
    daily_data = data['daily']
    return daily_data, start_date, end_date

def dframe(daily_data):
    """ Retorna um dataframe a partir de um dicionário

    Args:
        daily_data (dict): dicionário que contém informações de temperatura e dias.

    Returns:
        df (pandas.DataFrame): dataframe que contém as informações
        de {daily_data}.
    """
    # Uso do pandas por meio de um alias (pd)

    # Cria uma tabela com as temperaturas (dataframe)
    df = pd.DataFrame({
    'date': daily_data['time'],
    'max_temp': daily_data['temperature_2m_max'],
    'min_temp': daily_data['temperature_2m_min']
    })

    # Muda o tipo de string para horário (datetime64[us])
    df['date'] = pd.to_datetime(df['date'])
    return df

def mathgraph(df, start_date, end_date):
    """ Gera uma imagem .png e a salva a partir de
    um dataframe.

    Args:
        df (pandas.DataFrame): dataframe que contém temperatura (min e max) nos últimos 7 dias.
        start_date (string): Começo do intervalo.
        end_date (string): Fim do intervalo.
    """
    # Uso da matplotlib por meio de um alias (plt)

    # Cria o gráfico de linha (plot)
    plt.figure(figsize=(10, 6))
    plt.plot(df['date'], df['max_temp'], marker='o', label='Max Temp')
    plt.plot(df['date'], df['min_temp'], marker='o', label='Min Temp')

    # Adição de título e descrições dos eixos (x e y)
    plt.xlabel('Data')
    plt.ylabel('Temperatura (°C)')
    plt.title('Temperatura em Guarulhos - ultimos 7 dias')
    plt.legend()

    # Rotaciona o eixo das abscissas (x)
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Salva o gráfico em .png
    plt.savefig(f'{start_date} até {end_date} .png')
    # Abre uma janela "pop up" mostrando o gráfico
    plt.show()

if __name__ == "__main__":
    main()