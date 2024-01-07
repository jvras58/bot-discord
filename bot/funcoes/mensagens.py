import discord
from discord import app_commands

cliente_discord = discord.Client(intents=discord.Intents.all())
tree = app_commands.CommandTree(cliente_discord)



async def on_message(
    mensagem,
    cliente_discord,
    conector_discord,
    envia_link_bot,
    processa_mensagem_canal_alvo,
    envia_planilha,
    envia_dm,
    comousar,
    offeveryone,
    oneveryone,
    offavisodm,
    onavisodm,
    definir_alerta,
    alerta_dm_horario,
    idignore,
    readicionarids,
    idcheckpoint,
    idplanilha,
):
    """
    Função para lidar com mensagens recebidas pelo bot.

    Parâmetros:
    - mensagem: A mensagem recebida.
    - cliente_discord: O cliente Discord.
    - conector_discord: O conector Discord.
    - envia_link_bot: Função para enviar o link do bot.
    - processa_mensagem_canal_alvo: Função para processar a mensagem do canal alvo.
    - envia_planilha: Função para enviar a planilha.
    - envia_dm: Função para enviar uma mensagem direta.
    - comousar: Função para exibir informações de como usar o bot.
    - offeveryone: Função para desativar menções a todos.
    - oneveryone: Função para ativar menções a todos.
    - offavisodm: Função para desativar aviso de mensagem direta.
    - onavisodm: Função para ativar aviso de mensagem direta.
    - definir_alerta: Função para definir o horário do alerta.
    - alerta_dm_horario: Função para enviar o alerta de mensagem direta no horário definido.
    - idignore: Função para adicionar um ID de usuarios à lista de ignorados(para quem não deve ser enviado os avisos do verificar_checkpoint_não_enviados).
    - readicionarids: Função para remover ids da lista de ignorados.
    - idcheckpoint: Função para definir o ID do canal de checkpoint.
    - idplanilha: Função para definir o ID do canal da planilha.
    """
    if mensagem.author == cliente_discord.user:
        return

    comandos = {
        '/linkbot': envia_link_bot,
        '/status': lambda mensagem, _: mensagem.channel.send(
            'Status é {0}'.format(cliente_discord.status)
        ),
        '/dm': envia_dm,
        '/comousar': comousar,
        '/offeveryone': offeveryone,
        '/oneveryone': oneveryone,
        '/offavisodm': offavisodm,
        '/onavisodm': onavisodm,
        '/horacheckpoint': definir_alerta,
        '/alertadm': alerta_dm_horario,
        '/idignore': idignore,
        '/readicionarids': readicionarids,
        '/idcheckpoint': idcheckpoint,
        '/idplanilha': idplanilha,
    }

    comandos_servidor_exclusivo = [
        '/offeveryone',
        '/oneveryone',
        '/offavisodm',
        '/onavisodm',
        '/horacheckpoint',
        '/alertadm',
        '/idignore',
        '/readicionarids',
        '/idcheckpoint',
        '/idplanilha',
    ]

    for comando, funcao in comandos.items():
        if mensagem.content.startswith(comando):
            if isinstance(mensagem.channel, discord.DMChannel):
                if comando not in comandos_servidor_exclusivo:
                    await funcao(mensagem, cliente_discord)
            else:
                if (
                    comando == '/linkbot'
                    or comando == '/status'
                    or comando == '/dm'
                    or comando == '/comousar'
                ):
                    await funcao(mensagem, cliente_discord)
                else:
                    await funcao(mensagem, conector_discord)
            break

    if mensagem.channel.id == conector_discord.canal_checkpoint_id:
        await processa_mensagem_canal_alvo(mensagem)
    if (
        mensagem.channel.id == conector_discord.canal_planilha_id
        and mensagem.content.strip() == '/checkpoint'
    ):
        await envia_planilha(mensagem)
