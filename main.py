import discord

cliente_discord = discord.Client(intents=discord.Intents.all())

canal_alvo_id = 1158343397279543327

@cliente_discord.event
async def on_ready():
    print('Logado como {0.user}'.format(cliente_discord))

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
                    # FIXME: essa parte de remover o texto que vem com o emoji ta sem funcionar direito ACABA REMOVENDO O EMOJI É DEIXANDO A MENSAGEM EM BRANCO EM ALGUNS CASOS (CASO DE ISABELLE)
                    # if ' ' in emoji:
                    #     emoji = emoji.split(' ')[0]
                    await mensagem.channel.send(f'O emoji é {emoji}')
# Inicialização do cliente do Discord com o token de autenticação
cliente_discord.run('')


