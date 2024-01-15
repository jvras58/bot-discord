import time

from config.conector_discord import ConectorDiscord
from config.config import get_settings
from funcoes.comandos_basicos import BasicCommands
from funcoes.comandos_config_canal import CanalCommands
from funcoes.comandos_dm import DmCommands
from funcoes.comandos_extras import ExtrasCommands
from funcoes.comandos_mencoes import MentionsCommands


#TODO: problema de ordem de chamada de função task format foi desabilitado

cliente_discord = ConectorDiscord()
tree = cliente_discord.tree


BasicCommands = BasicCommands(cliente_discord)
BasicCommands.load_basic_commands(tree)


MentionsCommands = MentionsCommands(cliente_discord)
MentionsCommands.load_mentions_commands(tree)


dm_commands = DmCommands(cliente_discord)
dm_commands.load_dm_commands(tree)


canal_commands = CanalCommands(cliente_discord)
canal_commands.load_channel_commands(tree)

Extras_Commands = ExtrasCommands(cliente_discord)
Extras_Commands.load_extras_commands(tree)


while True:
    try:
        # Inicialização do cliente do Discord
        cliente_discord.run(get_settings().DISCORD_TOKEN)
    except Exception as e:
        print(f'Erro: {e}. Reiniciando o bot.')
        time.sleep(5)  # Pausa por 5s


#TODO: PROBLEMA: IDS_IGNORADOS É UMA LISTA E NO MOMENTO POR FALTA DE CONHECIMENTO ESTOU COLOCANDO COMO STRING DEPOIS AVERIGUAR COMO FAZER DE FATO ISSO...
