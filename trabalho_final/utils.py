import csv

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from lxml import html


def get_table_from_site():
    # 1. Configura navegador headless
    options = Options()
    # options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)


    # 2. Vai para a página
    url = "https://www.cs.princeton.edu/courses/archive/spring20/cos320/LL1/"
    driver.get(url)

    with open('gramatica.txt', 'r', encoding='utf-8') as f:
        grammar = f.read()
    
    textarea = driver.find_element(By.XPATH, '//*[@id="grammar"]')
    textarea.clear()
    textarea.send_keys(grammar)

    # 4. Clica no botão para gerar a tabela
    botao = driver.find_element(By.XPATH, '/html/body/div[2]/a')
    botao.click()

    # 5. Espera a tabela aparecer
    driver.implicitly_wait(3)
    tabela = driver.find_element(By.XPATH, '/html/body/div[2]/table/tbody/tr/td[2]/table')
    
    # 6. Converte o HTML da tabela em CSV
    html_str = tabela.get_attribute("outerHTML")
    tree = html.fromstring(html_str)

    # Cabeçalhos
    headers = [th.text_content().strip() for th in tree.xpath('.//thead/tr/th')]

    # Linhas
    rows = []
    for tr in tree.xpath('.//tbody/tr'):
        cells = [td.text_content().strip() for td in tr.xpath('./td')]
        rows.append(cells)

    # 7. Salva como CSV
    with open("ll1_gerada.csv", "w", newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)

    print("Tabela LL(1) salva como 'll1_gerada.csv' com sucesso.")

    driver.quit()


def load_ll1_table_from_csv(caminho_csv):
    with open(caminho_csv, newline='', encoding='utf-8') as f:
        leitor = csv.reader(f)
        linhas = [linha for linha in leitor if any(c.strip() for c in linha)]  # remove linhas totalmente vazias

    terminais = [token.strip() for token in linhas[0][1:]]
    tabela = {}

    for linha in linhas[1:]:  # agora não há mais necessidade de pular 2 em 2
        nao_terminal = linha[0].strip()
        if not nao_terminal:
            continue  # só por segurança: ignora se o primeiro campo estiver vazio

        tabela[nao_terminal] = {}

        for i, producao in enumerate(linha[1:]):
            producao = producao.strip()
            if producao:
                simbolos = producao.split()[2:] if "::=" in producao else producao.split()
                tabela[nao_terminal][terminais[i]] = simbolos

    return tabela


get_table_from_site()
print(load_ll1_table_from_csv("ll1_gerada.csv"))