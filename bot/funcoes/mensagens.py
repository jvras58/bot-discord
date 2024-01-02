import discord

from funcoes.comandos import processa_mensagens_anteriores


async def on_ready(
    cliente_discord,
    conector_discord,
    dados,
    alerta_checkpoint,
    verificar_checkpoints_nao_enviados,
):
    print(f'{cliente_discord.user} conectado ao Discord!')
    await processa_mensagens_anteriores(conector_discord, cliente_discord)
    
    # TODO: DESATIVADO POIS POR ENQUANTO MARLOS NÃO PEDIU
    # cliente_discord.loop.create_task(
    #     alerta_checkpoint(cliente_discord, conector_discord)
    # )
    
    # cliente_discord.loop.create_task(
    #     verificar_checkpoints_nao_enviados(
    #         cliente_discord, conector_discord, dados
    #     )
    # )


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
    idignore,
    readicionarids,
    idcheckpoint,
    idplanilha,
):
    """
    Função para lidar com mensagens recebidas.
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
