# Use a imagem base do Python
FROM python:3.11

# Define o diretório de trabalho no contêiner
WORKDIR /app

# Copia os arquivos do projeto para o contêiner
COPY . .

# Instala as dependências do projeto
RUN pip install discord 
RUN pip install emoji
RUN pip install pandas
RUN pip install asyncio
RUN pip install datetime
RUN pip install python-dotenv

# Comando para executar o bot
CMD ["python", "main.py"]


