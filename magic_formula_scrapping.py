import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

# URL do site
url = "https://quantbrasil.com.br/magic-formula/"

# Solicitar ao usuário o número de ações desejado
while True:
    try:
        num_acoes = int(input("Quantas ações você deseja salvar? (Máximo de 100): "))
        if 1 <= num_acoes <= 100:
            break
        else:
            print("Por favor, insira um número entre 1 e 100.")
    except ValueError:
        print("Entrada inválida. Por favor, insira um número inteiro.")

# Fazer a requisição GET para o site
response = requests.get(url)

# Verificar se a requisição foi bem-sucedida
if response.status_code == 200:
    # Analisar o conteúdo HTML da página
    soup = BeautifulSoup(response.text, "html.parser")

    # Encontrar a primeira tabela na página
    table = soup.find("table")

    # Verificar se a tabela foi encontrada
    if table:
        # Encontrar o tbody dentro da tabela
        tbody = table.find("tbody")

        # Verificar se o tbody foi encontrado
        if tbody:
            # Extrair todas as linhas (tr) dentro do tbody
            rows = tbody.find_all("tr")

            # Criar uma lista para armazenar os dados
            data = []

            # Iterar sobre cada linha, até o número máximo solicitado
            for i, row in enumerate(rows[:num_acoes], start=1):
                # Extrair todas as células (td) dentro da linha
                cols = row.find_all("td")
                # Armazenar os textos das células em uma lista
                cols = [col.text.strip() for col in cols]
                # Adicionar a lista de células à lista de dados
                data.append(cols)

            # Criar um DataFrame com os dados extraídos
            df = pd.DataFrame(
                data,
                columns=["Posição", "Ativo", "EV/EBIT", "ROIC", "Segmento", "Pontos"],
            )

            # Especificar o nome do arquivo Excel
            excel_file = f"dados_magic_formula.xlsx"

            # Salvar os dados no arquivo Excel
            df.to_excel(excel_file, index=False)
            full_path = os.path.abspath(excel_file)
            print(f"Dados salvos com sucesso em {full_path}")
        else:
            print("Tag <tbody> não encontrada na tabela.")
    else:
        print("Tabela não encontrada na página.")
else:
    print(f"Falha ao acessar a página. Status code: {response.status_code}")
