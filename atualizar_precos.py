import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta


def search_stock_price(df):
    # Calcula a data de 3 dias atrás
    end_date = datetime.now().date()  # Data atual
    start_date = end_date - timedelta(days=3)  # Data de 3 dias atrás

    # Ajusta o ticker para o mercado brasileiro
    carteira = (df["Ativo"] + ".SA").tolist()
    print(carteira)

    # Baixa os preços ajustados
    dt = yf.download(carteira, start=start_date, end=end_date)["Adj Close"]

    # Coleta o preço do primeiro dia no intervalo
    prices = []
    for ativo in carteira:
        prices.append(dt[ativo].iloc[0])

    df["Preco"] = prices
    return df
