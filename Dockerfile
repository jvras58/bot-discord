# Use a imagem base do Python com suporte ao Poetry
FROM python:3.11

# Instala o Poetry
RUN pip install poetry

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia os arquivos de configuração do Poetry (pyproject.toml e poetry.lock) para o diretório de trabalho
COPY pyproject.toml poetry.lock ./

# Copia os arquivos de configuração do Poetry (pyproject.toml e requirements.txt) para o diretório de trabalho para exportas as dependencias do poetry para o requeriment.txt este é o comando: ( poetry export -f requirements.txt --output requirements.txt )
# COPY pyproject.toml requirements.txt ./

# Instala as dependências usando o Poetry
RUN poetry install

# Instala as dependências usando o requirements.txt
#RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante dos arquivos para o diretório de trabalho
COPY . .

# Define o comando padrão para executar o bot
CMD ["poetry", "run", "python", "main.py"]

