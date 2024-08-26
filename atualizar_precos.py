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


def distribuir_investimento(df, valor_investimento):
    # Certifique-se de que o DataFrame contém uma coluna chamada 'Preco'
    if "Preco" not in df.columns:
        raise ValueError(
            "O DataFrame deve conter uma coluna chamada 'Preco' com os preços das ações."
        )

    # Inicializa uma nova coluna para armazenar o valor investido em cada ação
    df["Recomendação Investimento"] = 0.0

    # Calcula o valor mínimo a ser investido em cada ação (3,33% do valor total)
    valor_minimo_por_acao = valor_investimento * 0.0333

    # Inicializa o valor restante para ser distribuído
    valor_restante = valor_investimento

    # Itera sobre as ações para garantir que cada uma receba pelo menos 3,33% do valor total
    for i, row in df.iterrows():
        preco_acao = row["Preco"]

        # Determina o número de ações que pode ser comprado com o valor mínimo
        max_acoes = int(valor_minimo_por_acao // preco_acao)

        # Calcula o valor a ser investido na ação atual
        valor_investido = max_acoes * preco_acao

        # Assegura que pelo menos o valor mínimo é investido
        if valor_investido >= valor_minimo_por_acao:
            df.at[i, "Recomendação Investimento"] = valor_investido
            valor_restante -= valor_investido

    # Se ainda houver valor restante, distribua-o iterativamente
    while valor_restante > 0:
        for i, row in df.iterrows():
            preco_acao = row["Preco"]
            valor_investido_atual = df.at[i, "Recomendação Investimento"]

            if valor_restante >= preco_acao:
                df.at[i, "Recomendação Investimento"] += preco_acao
                valor_restante -= preco_acao

            # Para o loop se o valor restante for insuficiente para comprar mais uma ação
            if valor_restante < df["Preco"].min():
                valor_restante = 0
                break

    return df
