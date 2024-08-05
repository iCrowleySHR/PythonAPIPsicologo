# Usar uma imagem base do Python
FROM python:3.9-slim

# Instalar dependências
RUN apt-get update && \
    apt-get install -y \
    wget \
    unzip \
    libnss3 \
    libgconf-2-4 \
    libfontconfig1 \
    libx11-xcb1 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libxtst6 \
    libnss3-dev \
    libappindicator3-1 \
    && rm -rf /var/lib/apt/lists/*

# Instalar o Google Chrome
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    dpkg -i google-chrome-stable_current_amd64.deb && \
    apt-get -f install -y && \
    rm google-chrome-stable_current_amd64.deb

# Instalar o ChromeDriver
RUN wget https://chromedriver.storage.googleapis.com/2.46/chromedriver_linux64.zip && \
    unzip chromedriver_linux64.zip && \
    mv chromedriver /usr/local/bin/chromedriver && \
    chmod +x /usr/local/bin/chromedriver && \
    rm chromedriver_linux64.zip

# Definir o diretório de trabalho
WORKDIR /app

# Copiar o arquivo de requisitos e instalar dependências
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copiar o código da aplicação
COPY . .

# Expor a porta que a aplicação Flask usará
EXPOSE 5000

# Comando para iniciar a aplicação
CMD ["python", "main.py"]
