# Projeto Bot Checkpoint

## Introdução
O Projeto Bot Checkpoint é um aplicativo desenvolvido em Python que utiliza a API do Discord para capturar um template de mensagem específico e enviá-lo para uma planilha.

## Tecnologias Utilizadas
- [Python](https://www.python.org/)
- [Poetry](https://python-poetry.org/)
- [API do Discord](https://discord.com/developers/docs/intro)

## Como Executar
1. No arquivo `.env`, insira um token de acesso à API do Discord ([discord.com/developers](https://discord.com/developers)). Exemplo: `xxxxxxxxxxxxxxxxxxxxxxxxxx.GZxx-B.maJLyx_I_xxxxqrvQfY8yOCvNDghO7tQeECaQ`

2. Forneça o ID do canal do checkpoint e o canal de administração para onde as planilhas serão enviadas.
   (comandos: `/idcheckpoint` & `/idplanilha`)

3. Use o comando `/linkbot` para receber o link de adição do bot ao servidor. (funcional na DM do bot)

4. O bot também possui um comando `/status` para verificar se está funcionando corretamente. (funcional na DM do bot)

5. Para receber a planilha do checkpoint do dia, basta ir ao canal de administração e digitar `/checkpoint`.

6. O bot possui uma função de monitoramento para verificar quem enviou o checkpoint (e avisar quem não enviou na DM). Essa função pode ser ativada/desativada com os comandos `/offavisodm` & `/onavisodm`. (Horário de envio: 12h; nos finais de semana essa função é desativada automaticamente).

7. O bot enviará uma mensagem `@everyone` no canal do checkpoint em um horário determinado. Essa função pode ser ativada/desativada com os comandos `/offeveryone` & `/oneveryone`. (Horário de envio: 10h; nos finais de semana essa função é desativada automaticamente).

8. Função extra: é possível ignorar IDs, ou seja, nenhuma mensagem será enviada para o ID ignorado (útil para períodos de férias). Use os comandos `/idignore` para remover e `/readicionarids` para adiciona-los novamente.

Para executar o bot em um container Docker, utilize os seguintes comandos:
```bash
docker build -t botcheck .

docker run -d --name bot botcheck
```

# obs: caso a saida do container seja: The virtual environment found in /app/.venv seems to be broken favor apagar a pasta .venv e gerar o build novamente

## Autor
- [Jonathas Vinicius]