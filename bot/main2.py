from datetime import datetime
import time
import discord
from discord import app_commands

from config.config import get_settings
from funcoes.alertas import alerta_checkpoint #, verificar_checkpoints_nao_enviados
# from funcoes.comandos import processa_mensagens_anteriores


class client(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.synced = False # para o bot não sincronizar os comandos mais de uma vez
        self.enviar_everyone: bool = True
        self.alerta_checkpoint_horario: datetime = None
        self.canal_checkpoint_id: str = None
        self.canal_planilha_id: str = None
        
        
    
    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:  #checa se os comandos slash já foram sincronizados
            await tree.sync() # sincroniza os comandos slash (se não passar o parametro guild_id, os comandos demoram de 1~24 hrs para sincronizar)
            self.synced = True
        print(f'{self.user} conectado ao Discord!')
        #await processa_mensagens_anteriores(self, self)

        self.loop.create_task(alerta_checkpoint(self, self))

        #self.loop.create_task(verificar_checkpoints_nao_enviados(self, self, self.dados))

aclient = client()
tree = app_commands.CommandTree(aclient)


@tree.command(name='ping', description='Responde com pong!')
async def ping(interaction: discord.Interaction):
    await interaction.channel.send_message('pong!', ephemeral=True)

# -------------------COMANDOS BASICOS INICIO ------------------- #
@tree.command(name='status', description='Envia o status do bot na dm')
async def status(interaction: discord.Interaction):
    # Responda à interação primeiro

    await interaction.response.send_message(f'Status é {aclient.status}')

@tree.command(name='linkbot', description='Envia o link do bot na dm')
async def linkbot(interaction: discord.Interaction):
    # Responda à interação primeiro
    link = 'https://discord.com/api/oauth2/authorize?client_id={}&permissions=8&scope=bot'.format(
        interaction.client.user.id
    )
    await interaction.response.send_message(link)

@tree.command(name='comousar', description='Envia instruções de como usar o bot')
async def comousar(interaction: discord.Interaction):
    # Responda à interação primeiro
    """
    send_message tem um parâmetro ephemeral que, quando definido como True, faz com que a mensagem seja visível apenas para o usuário que iniciou a interação
    """
    await interaction.response.send_message(
        'Enviando como usar na DM...', ephemeral=True
    )
    dm_channel = await interaction.user.create_dm()
    with open('comomeusar.md', 'rb') as file:
        await dm_channel.send(file=discord.File(file, 'comousar.md'))

# -------------------COMANDOS BASICOS FIM ------------------- #


# -------------------COMANDOS DE CONFIGURAÇÃO DE CANAL INICIO ------------------- #
#TODO: NECESSARIO TESTAR (importante)
@tree.command(name='idcheckpoint', description='Define o ID do canal de checkpoint')
async def idcheckpoint(interaction: discord.Interaction, id: str):
    # Responda à interação primeiro
    await interaction.response.send_message(
        'Definindo ID do canal de checkpoint...', ephemeral=True
    )
    aclient.canal_checkpoint_id = id 
    dm_channel = await interaction.user.create_dm()
    await dm_channel.send(f'ID do canal de checkpoint definido para {aclient.canal_checkpoint_id}.')

#TODO: NECESSARIO TESTAR (importante)
@tree.command(name='idplanilha', description='Define o ID do canal da planilha')
async def idplanilha(interaction: discord.Interaction, id: str):
    # Responda à interação primeiro
    await interaction.response.send_message(
        'Definindo ID do canal da planilha...', ephemeral=True
    )
    aclient.canal_planilha_id = id
    dm_channel = await interaction.user.create_dm()
    await dm_channel.send(f'ID do canal da planilha definido para {aclient.canal_planilha_id}.')

# -------------------COMANDOS DE CONFIGURAÇÃO DE CANAL FIM ------------------- #


# ------------------- Comandos de enviar everyone no canal INICIO ------------------- #
@tree.command(name='alerta', description='Define o horário do alerta')
async def definir_alerta(interaction: discord.Interaction, horario: str ):
    # Responda à interação primeiro
    await interaction.response.send_message(
        'Definindo alerta...', ephemeral=True
    )
    if horario:
        aclient.alerta_checkpoint_horario = horario
        dm_channel = await interaction.user.create_dm()
        await dm_channel.send(f'Alerta definido para {aclient.alerta_checkpoint_horario}.')
    else:
        # Use followup.send para mensagens subsequentes
        await interaction.followup.send(
            'Nenhuma opção fornecida.', ephemeral=True
        )

@tree.command(name='offeveryone', description='Desativa menções a todos')
async def offeveryone(interaction: discord.Interaction):
    # Responda à interação primeiro
    await interaction.response.send_message(
        'Desativando menções a todos...', ephemeral=True
    )
    aclient.enviar_everyone = False
    dm_channel = await interaction.user.create_dm()
    await dm_channel.send('Desativado menções a todos.')

@tree.command(name='oneveryone', description='Ativa menções a todos')
async def oneveryone(interaction: discord.Interaction):
    # Responda à interação primeiro
    await interaction.response.send_message(
        'Ativando menções a todos...', ephemeral=True
    )
    aclient.enviar_everyone = True
    dm_channel = await interaction.user.create_dm()
    await dm_channel.send('Ativado menções a todos.')
# ------------------- Comandos de enviar everyone no canal FIM ------------------- #

while True:
    try:
        # Inicialização do cliente do Discord
        aclient.run(get_settings().DISCORD_TOKEN)
    except Exception as e:
        print(f'Erro: {e}. Reiniciando o bot.')
        time.sleep(5)  # Pausa por 5s
