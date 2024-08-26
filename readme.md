
# Extrator de Dados - Magic Formula

Este é um projeto de automação para extrair dados de ações usando a fórmula mágica do site [QuantBrasil](https://quantbrasil.com.br/magic-formula/), salvá-los em um arquivo Excel e, opcionalmente, atualizar os preços das ações posteriormente. A interface gráfica é criada usando Tkinter, e o script permite ao usuário escolher entre executar o pipeline completo ou apenas atualizar os preços dos dados existentes.

## Funcionalidades

* **Extração de Dados** : Realiza o scraping de dados do site QuantBrasil e salva as informações das 30 principais ações recomendadas pela fórmula mágica.
* **Atualização de Preços** : Atualiza os preços das ações já salvas em um arquivo Excel.
* **Interface Gráfica** : Interface simples e intuitiva feita com Tkinter, permitindo ao usuário escolher entre executar todo o pipeline ou apenas atualizar os preços.
* **Recomendação de Aporte** : Baseado na quantia a ser investida ele faz uma recomendação levando em conta que deve comprar todas as acoes (3.3% de aporte no minimo)

## Requisitos

* Python 3.x
* Bibliotecas Python:
  * `requests`
  * `BeautifulSoup4`
  * `pandas`
  * `openpyxl`
  * `tkinter` (incluído no Python por padrão)

## Instalação

1. Clone o repositório para a sua máquina local:
   <pre><div class="dark bg-gray-950 rounded-md border-[0.5px] border-token-border-medium"><div class="flex items-center relative text-token-text-secondary bg-token-main-surface-secondary px-4 py-2 text-xs font-sans justify-between rounded-t-md"><span>bash</span><div class="flex items-center"><span class="" data-state="closed"><button class="flex gap-1 items-center"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" viewBox="0 0 24 24" class="icon-sm"><path fill="currentColor" fill-rule="evenodd" d="M7 5a3 3 0 0 1 3-3h9a3 3 0 0 1 3 3v9a3 3 0 0 1-3 3h-2v2a3 3 0 0 1-3 3H5a3 3 0 0 1-3-3v-9a3 3 0 0 1 3-3h2zm2 2h5a3 3 0 0 1 3 3v5h2a1 1 0 0 0 1-1V5a1 1 0 0 0-1-1h-9a1 1 0 0 0-1 1zM5 9a1 1 0 0 0-1 1v9a1 1 0 0 0 1 1h9a1 1 0 0 0 1-1v-9a1 1 0 0 0-1-1z" clip-rule="evenodd"></path></svg>Copiar código</button></span></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="!whitespace-pre hljs language-bash">git clone https://github.com/brprado/Magic-Formula-Bovespa.git
   </code></div></div></pre>
2. Navegue até o diretório do projeto:
   <pre><div class="dark bg-gray-950 rounded-md border-[0.5px] border-token-border-medium"><div class="flex items-center relative text-token-text-secondary bg-token-main-surface-secondary px-4 py-2 text-xs font-sans justify-between rounded-t-md"><span>bash</span><div class="flex items-center"><span class="" data-state="closed"><button class="flex gap-1 items-center"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" viewBox="0 0 24 24" class="icon-sm"><path fill="currentColor" fill-rule="evenodd" d="M7 5a3 3 0 0 1 3-3h9a3 3 0 0 1 3 3v9a3 3 0 0 1-3 3h-2v2a3 3 0 0 1-3 3H5a3 3 0 0 1-3-3v-9a3 3 0 0 1 3-3h2zm2 2h5a3 3 0 0 1 3 3v5h2a1 1 0 0 0 1-1V5a1 1 0 0 0-1-1h-9a1 1 0 0 0-1 1zM5 9a1 1 0 0 0-1 1v9a1 1 0 0 0 1 1h9a1 1 0 0 0 1-1v-9a1 1 0 0 0-1-1z" clip-rule="evenodd"></path></svg>Copiar código</button></span></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="!whitespace-pre hljs language-bash">cd Magic-Formula-Bovespa
   </code></div></div></pre>
3. Instale as dependências necessárias:
   <pre><div class="dark bg-gray-950 rounded-md border-[0.5px] border-token-border-medium"><div class="flex items-center relative text-token-text-secondary bg-token-main-surface-secondary px-4 py-2 text-xs font-sans justify-between rounded-t-md"><span>bash</span><div class="flex items-center"><span class="" data-state="closed"><button class="flex gap-1 items-center"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" viewBox="0 0 24 24" class="icon-sm"><path fill="currentColor" fill-rule="evenodd" d="M7 5a3 3 0 0 1 3-3h9a3 3 0 0 1 3 3v9a3 3 0 0 1-3 3h-2v2a3 3 0 0 1-3 3H5a3 3 0 0 1-3-3v-9a3 3 0 0 1 3-3h2zm2 2h5a3 3 0 0 1 3 3v5h2a1 1 0 0 0 1-1V5a1 1 0 0 0-1-1h-9a1 1 0 0 0-1 1zM5 9a1 1 0 0 0-1 1v9a1 1 0 0 0 1 1h9a1 1 0 0 0 1-1v-9a1 1 0 0 0-1-1z" clip-rule="evenodd"></path></svg>Copiar código</button></span></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="!whitespace-pre hljs language-bash">pip install -r requirements.txt
   </code></div></div></pre>

## Como Usar

1. **Executar o Script** :

* Para iniciar a aplicação, execute o script principal:

<pre><div class="dark bg-gray-950 rounded-md border-[0.5px] border-token-border-medium"><div class="flex items-center relative text-token-text-secondary bg-token-main-surface-secondary px-4 py-2 text-xs font-sans justify-between rounded-t-md"><span>bash</span><div class="flex items-center"><span class="" data-state="closed"><button class="flex gap-1 items-center"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" viewBox="0 0 24 24" class="icon-sm"><path fill="currentColor" fill-rule="evenodd" d="M7 5a3 3 0 0 1 3-3h9a3 3 0 0 1 3 3v9a3 3 0 0 1-3 3h-2v2a3 3 0 0 1-3 3H5a3 3 0 0 1-3-3v-9a3 3 0 0 1 3-3h2zm2 2h5a3 3 0 0 1 3 3v5h2a1 1 0 0 0 1-1V5a1 1 0 0 0-1-1h-9a1 1 0 0 0-1 1zM5 9a1 1 0 0 0-1 1v9a1 1 0 0 0 1 1h9a1 1 0 0 0 1-1v-9a1 1 0 0 0-1-1z" clip-rule="evenodd"></path></svg>Copiar código</button></span></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="!whitespace-pre hljs language-bash">python gui.py
   </code></div></div></pre>

1. **Escolher a Ação** :

* Ao iniciar, você verá uma janela com um botão "Executar".
* Clique em "Executar" para escolher entre:
  * Executar o pipeline completo (scraping + atualização de preços).
  * Apenas atualizar os preços dos dados existentes.

1. **Salvamento dos Dados** :

* Os dados são salvos em um arquivo Excel chamado `dados_magic_formula.xlsx` na mesma pasta do script.
* Se escolher a atualização de preços, os valores do arquivo existente serão atualizados e salvos no mesmo arquivo.

## Estrutura do Projeto

<pre><div class="dark bg-gray-950 rounded-md border-[0.5px] border-token-border-medium"><div class="flex items-center relative text-token-text-secondary bg-token-main-surface-secondary px-4 py-2 text-xs font-sans justify-between rounded-t-md"><span>plaintext</span><div class="flex items-center"><span class="" data-state="closed"><button class="flex gap-1 items-center"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" viewBox="0 0 24 24" class="icon-sm"><path fill="currentColor" fill-rule="evenodd" d="M7 5a3 3 0 0 1 3-3h9a3 3 0 0 1 3 3v9a3 3 0 0 1-3 3h-2v2a3 3 0 0 1-3 3H5a3 3 0 0 1-3-3v-9a3 3 0 0 1 3-3h2zm2 2h5a3 3 0 0 1 3 3v5h2a1 1 0 0 0 1-1V5a1 1 0 0 0-1-1h-9a1 1 0 0 0-1 1zM5 9a1 1 0 0 0-1 1v9a1 1 0 0 0 1 1h9a1 1 0 0 0 1-1v-9a1 1 0 0 0-1-1z" clip-rule="evenodd"></path></svg>Copiar código</button></span></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="!whitespace-pre hljs language-plaintext">extrator-magic-formula/
│
├── atualizar_precos.py        # Função que realiza a atualização dos preços das ações
├── gui.py                    # Script principal que executa a interface gráfica e o pipeline
├── requirements.txt           # Arquivo com as dependências do projeto
└── README.md                  # Documentação do projeto
</code></div></div></pre>

## Notas

* Certifique-se de ter uma conexão de internet ativa, pois o script realiza solicitações ao site QuantBrasil para extrair os dados.
* A quantidade de ações é fixada em 30 para simplificação do processo.

## Contribuição

Se quiser contribuir para o projeto, sinta-se à vontade para enviar pull requests ou abrir issues no repositório.

## Licença

Este projeto está licenciado sob a [MIT License]().
