import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import tkinter as tk
from tkinter import messagebox, simpledialog
from atualizar_precos import search_stock_price


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


def salvar_dados(num_acoes=30, valor_investimento=None):
    # URL do site
    url = "https://quantbrasil.com.br/magic-formula/"

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
                colunas = [
                    "Posição",
                    "Ativo",
                    "EV/EBIT",
                    "ROIC",
                    "Segmento",
                    "Pontos",
                ]

                df = pd.DataFrame(data, columns=colunas)

                # Especificar o nome do arquivo Excel
                excel_file = f"dados_magic_formula.xlsx"

                # Salvar os dados no arquivo Excel
                df.to_excel(excel_file, index=False)

                # Atualizar os preços das ações
                df = search_stock_price(df)

                # Se um valor de investimento foi fornecido, distribuir o investimento
                if valor_investimento:
                    df = distribuir_investimento(df, valor_investimento)

                # Salvar os dados atualizados no arquivo Excel
                df.to_excel(excel_file, index=False)

                # Obter o caminho absoluto do arquivo salvo
                full_path = os.path.abspath(excel_file)

                # Mostrar mensagem de sucesso com o caminho do arquivo
                messagebox.showinfo(
                    "Sucesso", f"Dados salvos com sucesso em {full_path}"
                )
            else:
                messagebox.showerror("Erro", "Tag <tbody> não encontrada na tabela.")
        else:
            messagebox.showerror("Erro", "Tabela não encontrada na página.")
    else:
        messagebox.showerror(
            "Erro", f"Falha ao acessar a página. Status code: {response.status_code}"
        )
    return True


def atualizar_precos_existente(valor_investimento=None):
    # Especificar o nome do arquivo Excel
    excel_file = "dados_magic_formula.xlsx"

    # Verificar se o arquivo existe
    if os.path.exists(excel_file):
        # Ler o arquivo Excel
        df = pd.read_excel(excel_file)

        # Atualizar os preços das ações
        df = search_stock_price(df)

        # Se um valor de investimento foi fornecido, distribuir o investimento
        if valor_investimento:
            df = distribuir_investimento(df, valor_investimento)

        # Salvar o DataFrame atualizado no mesmo arquivo Excel
        df.to_excel(excel_file, index=False)

        # Obter o caminho absoluto do arquivo salvo
        full_path = os.path.abspath(excel_file)

        # Mostrar mensagem de sucesso com o caminho do arquivo
        messagebox.showinfo("Sucesso", f"Preços atualizados com sucesso em {full_path}")
    else:
        messagebox.showerror("Erro", f"O arquivo {excel_file} não foi encontrado.")


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Extrator de Dados - Magic Formula")

    # Criar e posicionar os widgets
    label_instrucao = tk.Label(root, text="Clique em Executar para escolher a ação.")
    label_instrucao.pack(pady=10)

    def escolher_opcao():
        resposta = messagebox.askyesno(
            "Escolha uma opção",
            "Deseja executar todo o código (scraping + atualização de preços)?\n"
            "Clique em 'Sim' para executar todo o código.\n"
            "Clique em 'Não' para apenas atualizar os preços de um arquivo existente.",
        )

        if resposta:
            valor_investimento = simpledialog.askstring(
                "Valor de Investimento",
                "Insira o valor que deseja investir:",
            )
            if valor_investimento:
                valor_investimento = float(valor_investimento)
            salvar_dados(
                valor_investimento=valor_investimento
            )  # Executa o pipeline completo
        else:
            valor_investimento = simpledialog.askstring(
                "Valor de Investimento",
                "Insira o valor que deseja investir:",
            )
            if valor_investimento:
                valor_investimento = float(valor_investimento)
            atualizar_precos_existente(
                valor_investimento=valor_investimento
            )  # Apenas atualiza os preços

    botao_salvar = tk.Button(root, text="Executar", command=escolher_opcao)
    botao_salvar.pack(pady=20)

    # Iniciar o loop da interface gráfica
    root.mainloop()
