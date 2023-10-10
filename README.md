# Projeto Bot Checkpoint

## Introdução
Este projeto consiste em um bot, desenvolvido em Python, que utiliza a API do Discord para capturar um template de mensagem específico e enviá-lo para uma planilha.

## Tecnologias Utilizadas
- [Python](https://www.python.org/)
- [API do Discord](https://discord.com/developers/docs/intro)

## Como Executar
1. No arquivo .env, forneça um token de acesso à API do Discord(discord.com/developers). Exemplo: (xxxxxxxxxxxxxxxxxxxxxxxxxx.GZxx-B.maJLyx_I_xxxxqrvQfY8yOCvNDghO7tQeECaQ)

2. Ainda no .env, forneça o ID do canal do checkpoint e o canal de administração para onde as planilhas serão enviadas. Por padrão, ele já vem com IDs predefinidos, mas você pode alterá-los para o ID que precisar. Basta ir a qualquer canal do servidor e digitar o comando /trocarid (FUNÇÃO AINDA EM TESTE POR FAVOR TROQUE O ID PELO .env).

3. O bot também possui um comando /status para verificar se está funcionando corretamente.

4. Para receber a planilha do checkpoint do dia, basta ir ao canal de administração e digitar /checkpoint.

5. O bot também possui uma função nativa de monitoramento para verificar quem enviou o checkpoint (e avisar para quem não enviou na dm).

6. O bot irá enviar uma mensagem @everyone no canal do checkpoint em um horário determinado.


Para executar o bot em um container Docker, use os seguintes comandos:
```bash
docker build -t botcheck .

docker run -d --name bot botcheck
```

## Autor
- [Jonathas Vinicius]