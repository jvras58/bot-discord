import time

import discord
from config.conector_discord import ConectorDiscord
from config.config import get_settings


cliente_discord = ConectorDiscord()
tree = cliente_discord.tree



# ------------------- Comandos basicos INICIO ------------------- #
@tree.command(name='status', description='Envia o status do bot na dm')
async def status(interaction: discord.Interaction):
    # Responda à interação primeiro
    """
    send_message tem um parâmetro ephemeral que, quando definido como True, faz com que a mensagem seja visível apenas para o usuário que iniciou a interação
    """
    await interaction.response.send_message(
        'Enviando status na DM...', ephemeral=True
    )
    dm_channel = await interaction.user.create_dm()
    await dm_channel.send(f'Status é {cliente_discord.status}')


@tree.command(name='linkbot', description='Envia o link do bot na dm')
async def linkbot(interaction: discord.Interaction):
    # Responda à interação primeiro
    await interaction.response.send_message(
        'Enviando link do bot na DM...', ephemeral=True
    )
    link = 'https://discord.com/api/oauth2/authorize?client_id={}&permissions=8&scope=bot'.format(
        interaction.client.user.id
    )
    dm_channel = await interaction.user.create_dm()
    await dm_channel.send(link)

@tree.command(name='comousar', description='Envia instruções de como usar o bot')
async def comousar(interaction: discord.Interaction):
    # Responda à interação primeiro
    await interaction.response.send_message(
        'Enviando como usar na DM...', ephemeral=True
    )
    dm_channel = await interaction.user.create_dm()
    with open('comomeusar.md', 'rb') as file:
        await dm_channel.send(file=discord.File(file, 'comousar.md'))
# ------------------- Comandos basicos FIM ------------------- #


# ------------------- Comandos de enviar everyone no canal INICIO ------------------- #
#TODO: NECESSARIO TESTAR
@tree.command(name='horario_alerta', description='Define o horário do alerta')
async def definir_alerta(interaction: discord.Interaction, horario: str):
    # Responda à interação primeiro
    await interaction.response.send_message(
        'Definindo alerta...', ephemeral=True
    )
    cliente_discord.alerta_checkpoint_horario = horario
    dm_channel = await interaction.user.create_dm()
    await dm_channel.send(f'Alerta definido para {cliente_discord.alerta_checkpoint_horario}.')

@tree.command(name='offeveryone', description='Desativa menções a todos')
async def offeveryone(interaction: discord.Interaction):
    # Responda à interação primeiro
    await interaction.response.send_message(
        'Desativando menções a todos...', ephemeral=True
    )
    cliente_discord.enviar_everyone = False
    dm_channel = await interaction.user.create_dm()
    await dm_channel.send('Desativado menções a todos.')

@tree.command(name='oneveryone', description='Ativa menções a todos')
async def oneveryone(interaction: discord.Interaction):
    # Responda à interação primeiro
    await interaction.response.send_message(
        'Ativando menções a todos...', ephemeral=True
    )
    cliente_discord.enviar_everyone = True
    dm_channel = await interaction.user.create_dm()
    await dm_channel.send('Ativado menções a todos.')
# ------------------- Comandos de enviar everyone no canal FIM ------------------- #











# ------------------- Comandos de enviar dm no canal INICIO ------------------- #
#TODO: NECESSARIO TESTAR
@tree.command(name='horario_verificar', description='Define o horário do verficar checkpoint')
async def alerta_dm_horario(interaction: discord.Interaction, horario: str):
    # Responda à interação primeiro
    await interaction.response.send_message(
        'Horario do alerta no horário sendo definido...', ephemeral=True
    )
    cliente_discord.verificar_checkpoint_horario = horario
    dm_channel = await interaction.user.create_dm()
    await dm_channel.send(f'Alerta definido para {cliente_discord.verificar_checkpoint_horario}.')
    
@tree.command(name='offavisodm', description='Desativa aviso de mensagem direta')
async def offavisodm(interaction: discord.Interaction):
    # Responda à interação primeiro
    await interaction.response.send_message(
        'Desativando aviso de mensagem direta...', ephemeral=True
    )
    cliente_discord.enviar_dm = False
    dm_channel = await interaction.user.create_dm()
    await dm_channel.send('Desativado aviso de mensagem direta.')

@tree.command(name='onavisodm', description='Ativa aviso de mensagem direta')
async def onavisodm(interaction: discord.Interaction):
    # Responda à interação primeiro
    await interaction.response.send_message(
        'Ativando aviso de mensagem direta...', ephemeral=True
    )
    cliente_discord.enviar_dm = True
    dm_channel = await interaction.user.create_dm()
    await dm_channel.send('Ativado aviso de mensagem direta.')

#TODO: NECESSARIO TESTAR
@tree.command(name='idignore', description='Adiciona um ID de usuário à lista de ignorados')
async def idignore(interaction: discord.Interaction, id: str):
    # Responda à interação primeiro
    await interaction.response.send_message(
        'Adicionando ID de usuário à lista de ignorados...', ephemeral=True
    )
    cliente_discord.ids_ignorados = id
    dm_channel = await interaction.user.create_dm()
    await dm_channel.send(f'ID de usuário {cliente_discord.ids_ignorados} adicionado à lista de ignorados.')

#TODO: NECESSARIO TESTAR
@tree.command(name='readicionarids', description='Remove um ID de usuário da lista de ignorados')
async def readicionarids(interaction: discord.Interaction, id: str):
    # Responda à interação primeiro
    await interaction.response.send_message(
        'Removendo ID de usuário da lista de ignorados...', ephemeral=True
    )
    cliente_discord.ids_ignorados.remove(id)
    dm_channel = await interaction.user.create_dm()
    await dm_channel.send(f'ID de usuário {id} removido da lista de ignorados.')
# ------------------- Comandos de enviar dm no canal FIM ------------------- #














# ------------------- Comandos de configurações de canais INICIO ------------------- #

#TODO: NECESSARIO TESTAR (importante)
@tree.command(name='idcheckpoint', description='Define o ID do canal de checkpoint')
async def idcheckpoint(interaction: discord.Interaction, id: str):
    # Responda à interação primeiro
    await interaction.response.send_message(
        'Definindo ID do canal de checkpoint...', ephemeral=True
    )
    cliente_discord.canal_checkpoint_id = id 
    dm_channel = await interaction.user.create_dm()
    await dm_channel.send(f'ID do canal de checkpoint definido para {cliente_discord.canal_checkpoint_id}.')

#TODO: NECESSARIO TESTAR (importante)
@tree.command(name='idplanilha', description='Define o ID do canal da planilha')
async def idplanilha(interaction: discord.Interaction, id: str):
    # Responda à interação primeiro
    await interaction.response.send_message(
        'Definindo ID do canal da planilha...', ephemeral=True
    )
    cliente_discord.canal_planilha_id = id
    dm_channel = await interaction.user.create_dm()
    await dm_channel.send(f'ID do canal da planilha definido para {cliente_discord.canal_planilha_id}.')
# ------------------- Comandos de configurações de canais FIM ------------------- #


while True:
    try:
        # Inicialização do cliente do Discord
        cliente_discord.run(get_settings().DISCORD_TOKEN)
    except Exception as e:
        print(f'Erro: {e}. Reiniciando o bot.')
        time.sleep(5)  # Pausa por 5s












# ------------------- Comandos em fase de ajustes INICIO ------------------- #
'''
@tree.command(name='dm', description='Envia uma mensagem direta para o usuário')
async def dm(interaction: discord.Interaction):
    await interaction.response.send_message(
        'Enviando mensagem direta...', ephemeral=True
    )
    if 'options' in interaction.data and len(interaction.data['options']) > 0:
        partes = interaction.data['options'][0]['value'].split()
        if len(partes) >= 2:
            id_usuario = int(partes[0])
            texto = ' '.join(partes[1:])
            usuario = interaction.client.get_user(id_usuario)
            if usuario:
                dm_channel = await usuario.create_dm()
                await dm_channel.send(texto)
                await interaction.followup.send(
                    f'Mensagem enviada para o usuário com ID {id_usuario}.'
                )
            else:
                await interaction.followup.send(
                    f'Não foi possível encontrar o usuário com ID {id_usuario}.'
                )
        else:
            await interaction.followup.send(
                'Por favor, forneça um ID de usuário e uma mensagem. Exemplo: /dm 11111111111111111 Olá!'
            )
    else:
        await interaction.followup.send(
            'Por favor, forneça um ID de usuário e uma mensagem. Exemplo: /dm 11111111111111111 Olá!'
        )

@tree.command(name='dm1', description='Envia o dm pelo bot')
async def dm1(ctx, id_usuario: int, *, mensagem: str):
    usuario = cliente_discord.get_user(id_usuario)
    if usuario:
        dm_channel = await usuario.create_dm()
        await dm_channel.send(mensagem)
        await ctx.send(f'Mensagem enviada para o usuário com ID {id_usuario}.')
    else:
        await ctx.send(f'Não foi possível encontrar o usuário com ID {id_usuario}.')
'''       
# ------------------- Comandos em fase de ajustes FIM ------------------- #
