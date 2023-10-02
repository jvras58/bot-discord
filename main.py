import discord

cliente_discord = discord.Client(intents=discord.Intents.all())

canal_alvo_id = 1158343397279543327

@cliente_discord.event
async def on_ready():
    print('Logado como {0.user}'.format(cliente_discord))

#versão mais estavel ate agora (que consegue tratar mais ou menos o caso de isabelle)
@cliente_discord.event
async def on_message(mensagem):
    if mensagem.channel.id == canal_alvo_id:
        linhas = mensagem.content.split('\n')
        if len(linhas) == 4:
            primeira_linha = linhas[0]
            if primeira_linha.startswith('- **Hj estou') or primeira_linha.startswith('Hj estou:') or primeira_linha.startswith('- Hj estou:'):
                emoji = primeira_linha.split(':')[-1].strip()
                if emoji.startswith('**'):
                    emoji = emoji[2:]
                await mensagem.channel.send(f'O emoji é {emoji}')
                
# melhor versão porem não consigo tratar o erro de quando a mensagem começa assim: - **Hj estou:** :woman_detective:  (o caso de isabelle)
@cliente_discord.event
async def on_message(mensagem):
    if mensagem.channel.id == canal_alvo_id:
        linhas = mensagem.content.split('\n')
        if len(linhas) == 4:
            primeira_linha = linhas[0]
            if primeira_linha.startswith('- **Hj estou') or primeira_linha.startswith('Hj estou:') or primeira_linha.startswith('- Hj estou:'):
                partes = primeira_linha.split(':')
                if len(partes) > 1:
                    emoji = partes[1].strip()
                    if emoji.startswith('**'):
                        emoji = emoji[2:]
                    if ' ' in emoji:
                        emoji = emoji.split(' ')[0]
                    await mensagem.channel.send(f'O emoji é {emoji}')
# Inicialização do cliente do Discord com o token de autenticação
cliente_discord.run('')


