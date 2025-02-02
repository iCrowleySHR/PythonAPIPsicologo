# Search Psychologist API

Este projeto é uma API Flask que utiliza Selenium e BeautifulSoup para buscar informações de psicólogos no site do **Cadastro Nacional de Psicólogos**.

## 🚀 Tecnologias Utilizadas
- Python
- Flask
- Selenium
- BeautifulSoup
- WebDriver Manager

## 📦 Instalação e Configuração

### 1️⃣ Instalar as Dependências
```sh
pip install -r requirements.txt
```

### 2️⃣ Executar a API
```sh
python app.py
```

A API estará rodando em `http://127.0.0.1:5000/`

## 🔍 Como Usar
### **Rota: `/search_psychologist`**
- **Método:** `POST`
- **Requisição:**
  ```json
  {
    "nome": "Nome do Psicólogo",
    "cpf": "000.000.000-00"
  }
  ```
  - **Observações:**
    - Se **apenas o nome** for informado, a busca será feita apenas pelo nome.
    - Se **apenas o CPF** for informado, a busca será feita apenas pelo CPF.
    - Se **nenhum dos dois** for informado, a API retornará erro `400`.

- **Resposta Sucesso (`200`)**:
  ```json
  {
    "status": "success",
    "resultados": [
      {
        "Status": "Ativo",
        "Nome": "Psicólogo Exemplo",
        "Região": "CRP 06",
        "Número do Registro": "12345/06",
        "Data de Registro": "01/01/2020"
      }
    ]
  }
  ```
- **Resposta Erro (`404`)**:
  ```json
  {
    "status": "error",
    "message": "Nenhum resultado encontrado."
  }
  ```
- **Resposta Erro (`400`) - Nome e CPF ausentes:**
  ```json
  {
    "status": "error",
    "message": "É necessário informar pelo menos um dos campos: nome ou CPF."
  }
  ```

## 🛠 Dependências
Caso precise instalar manualmente:
```sh
pip install flask selenium webdriver-manager beautifulsoup4 lxml
```

## 📌 Observações
- Certifique-se de ter o **Google Chrome** instalado para o Selenium funcionar corretamente.
- O WebDriver será gerenciado automaticamente pelo `webdriver-manager`.
- O tempo de espera para carregar os elementos pode ser ajustado no código (`WebDriverWait`).

---

Desenvolvido por 🚀 [Seu Nome]
