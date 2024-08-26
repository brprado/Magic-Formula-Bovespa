import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import tkinter as tk
from tkinter import messagebox
from atualizar_precos import search_stock_price


def salvar_dados(num_acoes=30):
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


def atualizar_precos_existente():
    # Especificar o nome do arquivo Excel
    excel_file = "dados_magic_formula.xlsx"

    # Verificar se o arquivo existe
    if os.path.exists(excel_file):
        # Ler o arquivo Excel
        df = pd.read_excel(excel_file)

        # Atualizar os preços das ações
        df = search_stock_price(df)

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
            salvar_dados()  # Executa o pipeline completo
        else:
            atualizar_precos_existente()  # Apenas atualiza os preços

    botao_salvar = tk.Button(root, text="Executar", command=escolher_opcao)
    botao_salvar.pack(pady=20)

    # Iniciar o loop da interface gráfica
    root.mainloop()
