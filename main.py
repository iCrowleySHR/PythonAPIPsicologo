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

    if not nome or not cpf:
        return jsonify({'error': 'Nome e CPF são obrigatórios.'}), 400

    # Configurando o WebDriver
    options = Options()
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        # Acessando o site
        url = 'https://cadastro.cfp.org.br/'
        driver.get(url)

        # Espera até que o campo de input 'nomepsi' esteja presente
        input_nome = WebDriverWait(driver, 40).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="nomepsi"]'))
        )

        # Espera até que o botão 'btn_busca_avancada' esteja presente
        btn_busca_avancada = WebDriverWait(driver, 40).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/article/div/div/div[2]/form/div[3]/button[2]'))
        )
        
        # Espera até que o campo de input 'cpf' esteja presente
        input_cpf = WebDriverWait(driver, 40).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="cpf"]'))
        )
        
        # Espera até que o botão 'btn_buscar' esteja presente
        btn_buscar = WebDriverWait(driver, 40).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/article/div/div/div[2]/form/div[3]/button[1]'))
        )
        
        # Preenchendo e enviando os dados
        input_nome.send_keys(nome)
        btn_busca_avancada.click()
        
        # Espera até que o campo de CPF esteja visível e disponível para inserção
        WebDriverWait(driver, 40).until(
            EC.visibility_of(input_cpf)
        )
        input_cpf.send_keys(cpf)
        time.sleep(2)
        btn_buscar.click()

        # Espera até que o resultado esteja presente
        resultado_html = WebDriverWait(driver, 550).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/article/div/div/div[2]/div/div/table'))
        ).get_attribute('outerHTML')

        # Usando BeautifulSoup para analisar o HTML
        soup = BeautifulSoup(resultado_html, 'lxml')
        tabela = soup.find('table')
        linhas = tabela.find('tbody').find_all('tr')

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

        return jsonify({'status': 'success', 'resultados': resultados})

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

    finally:
        # Fechando o navegador
        driver.quit()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
