# Projeto Bot Checkpoint

## Introdução
O Projeto Bot Checkpoint é um aplicativo desenvolvido em Python que utiliza a API do Discord para capturar um template de mensagem específico e enviá-lo para uma planilha.

## Tecnologias Utilizadas
- [Python](https://www.python.org/)
- [Poetry](https://python-poetry.org/)
- [API do Discord](https://discord.com/developers/docs/intro)

## Como Executar
1. No arquivo `.env`, insira um token de acesso à API do Discord ([discord.com/developers](https://discord.com/developers)). Exemplo: `xxxxxxxxxxxxxxxxxxxxxxxxxx.GZxx-B.maJLyx_I_xxxxqrvQfY8yOCvNDghO7tQeECaQ`

2. Use o comando `/linkbot` para receber o link de adição do bot ao servidor. (funcional na DM do bot)

3. Use o comando `/comousar` para receber instruções dos comandos que o bot possui. (funcional na DM do bot)

4. O bot também possui um comando `/status` para verificar se está funcionando corretamente. (funcional na DM do bot)


Para executar o bot em um container Docker, utilize os seguintes comandos:
```bash
docker build -t botcheck .

docker run -d --name bot botcheck
```

## Autor
- [Jonathas Vinicius]
