from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

app = Flask(__name__)

@app.route('/search_psychologist', methods=['POST'])
def search_psychologist():
    data = request.json
    nome = data.get('nome')
    cpf = data.get('cpf')

    if not nome and not cpf:
        return jsonify({'status': 'error', 'message': 'É necessário informar pelo menos um dos campos: nome ou CPF.'}), 400

    # Configurando o WebDriver
    options = Options()
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        # Acessando o site
        url = 'https://cadastro.cfp.org.br/'
        driver.get(url)

        # Se nome foi enviado, preenche o campo correspondente
        if nome:
            input_nome = WebDriverWait(driver, 40).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="nomepsi"]'))
            )
            input_nome.send_keys(nome)

        # Se CPF foi enviado, clica na busca avançada e preenche o campo correspondente
        if cpf:
            btn_busca_avancada = WebDriverWait(driver, 40).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/article/div/div/div[2]/form/div[3]/button[2]'))
            )
            btn_busca_avancada.click()

            input_cpf = WebDriverWait(driver, 40).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="cpf"]'))
            )

            WebDriverWait(driver, 40).until(EC.visibility_of(input_cpf))
            input_cpf.send_keys(cpf)

        # Clicar no botão de busca
        btn_buscar = WebDriverWait(driver, 40).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/article/div/div/div[2]/form/div[3]/button[1]'))
        )
        time.sleep(5)
        btn_buscar.click()
        btn_buscar.click()
        btn_buscar.click()

        # Espera até que os resultados apareçam
        resultado_html = WebDriverWait(driver, 50).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/article/div/div/div[2]/div/div/table'))
        ).get_attribute('outerHTML')

        # Usando BeautifulSoup para analisar o HTML
        soup = BeautifulSoup(resultado_html, 'lxml')
        tabela = soup.find('table')

        if not tabela:
            return jsonify({'status': 'error', 'message': 'Nenhuma tabela encontrada.'}), 404

        tbody = tabela.find('tbody')
        if not tbody:
            return jsonify({'status': 'error', 'message': 'Nenhum dado na tabela.'}), 404

        linhas = tbody.find_all('tr')

        resultados = []
        for linha in linhas:
            colunas = linha.find_all('td')
            resultado = {
                'Status': colunas[0].text.strip() if len(colunas) > 0 else '',
                'Nome': colunas[1].text.strip() if len(colunas) > 1 else '',
                'Região': colunas[2].text.strip() if len(colunas) > 2 else '',
                'Número do Registro': colunas[3].text.strip() if len(colunas) > 3 else '',
                'Data de Registro': colunas[4].text.strip() if len(colunas) > 4 else ''
            }
            resultados.append(resultado)
            
        if not resultados:
            return jsonify({'status': 'error', 'message': 'Nenhum resultado encontrado.'}), 404

        return jsonify({'status': 'success', 'resultados': resultados})

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

    finally:
        driver.quit()

if __name__ == '__main__':
    app.run(debug=True)