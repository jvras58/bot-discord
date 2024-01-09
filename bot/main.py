
import time
from config.conector_discord import ConectorDiscord
from config.config import get_settings

from funcoes.comandos_basicos import status, linkbot, comousar
from funcoes.comandos_mencoes import definir_alerta, offeveryone, oneveryone
from funcoes.comandos_dm import alerta_dm_horario, offavisodm, onavisodm, idignore, readicionarids, dm
from funcoes.comandos_config_canal import idcheckpoint, idplanilha

cliente_discord = ConectorDiscord()
tree = cliente_discord.tree



cliente_discord.tree.command(name='status', description='Envia o status do bot na dm')(status)
cliente_discord.tree.command(name='linkbot', description='Envia o link do bot na dm')(linkbot)
cliente_discord.tree.command(name='comousar', description='Envia instruções de como usar o bot')(comousar)

cliente_discord.tree.command(name='horario_alerta', description='Define o horário do alerta')(definir_alerta)
cliente_discord.tree.command(name='offeveryone', description='Desativa menções a todos')(offeveryone)
cliente_discord.tree.command(name='oneveryone', description='Ativa menções a todos')(oneveryone)

cliente_discord.tree.command(name='horario_verificar', description='Define o horário do verficar checkpoint')(alerta_dm_horario)
cliente_discord.tree.command(name='offavisodm', description='Desativa aviso de mensagem direta')(offavisodm)
cliente_discord.tree.command(name='onavisodm', description='Ativa aviso de mensagem direta')(onavisodm)
#TODO: NECESSARIO TESTAR
cliente_discord.tree.command(name='idignore', description='Adiciona um ID de usuário à lista de ignorados')(idignore)
#TODO: NECESSARIO TESTAR
cliente_discord.tree.command(name='readicionarids', description='Remove um ID de usuário da lista de ignorados')(readicionarids)
cliente_discord.tree.command(name='dm', description='Envia o dm pelo bot')(dm)

cliente_discord.tree.command(name='idcheckpoint', description='Define o ID do canal de checkpoint')(idcheckpoint)
cliente_discord.tree.command(name='idplanilha', description='Define o ID do canal da planilha')(idplanilha)


while True:
    try:
        # Inicialização do cliente do Discord
        cliente_discord.run(get_settings().DISCORD_TOKEN)
    except Exception as e:
        print(f'Erro: {e}. Reiniciando o bot.')
        time.sleep(5)  # Pausa por 5s
