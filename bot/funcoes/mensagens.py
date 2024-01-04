import discord
from funcoes.comandos import processa_mensagens_anteriores


async def on_ready(
    cliente_discord,
    conector_discord,
    dados,
    alerta_checkpoint,
    verificar_checkpoints_nao_enviados,
):
    """
    Função assíncrona que é chamada quando o bot está pronto para ser usado.
    Realiza a impressão de uma mensagem informando que o bot está conectado ao Discord.
    Em seguida, chama as funções para processar mensagens anteriores, alertar checkpoints e verificar checkpoints não enviados.

    Parâmetros:
    - cliente_discord: objeto cliente do Discord
    - conector_discord: objeto conector do Discord
    - dados: dados necessários para o processamento das mensagens
    - alerta_checkpoint: função para alertar sobre checkpoints
    - verificar_checkpoints_nao_enviados: função para verificar checkpoints não enviados

    processa_mensagens_anteriores: função para processar mensagens anteriores do canal de checkpoint
    """
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


# TODO: versão 1 com adminstração de tags (alguns comandos liberados para todos) [em fase de teste]
'''
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

    # Adicione aqui as tags que você quer permitir:
    tags_permitidas = ['Admin', 'Labs Leaders' , 'System call']

    for comando, funcao in comandos.items():
        if mensagem.content.startswith(comando):
            if isinstance(mensagem.channel, discord.DMChannel):
                if comando not in comandos_servidor_exclusivo:
                    await funcao(mensagem, cliente_discord)
            else:
                # Verifica se o autor da mensagem tem a tag permitida ou é o dono do servidor
                if (
                    comando == '/linkbot'
                    or comando == '/status'
                    or comando == '/dm'
                    or comando == '/comousar'
                ):
                    await funcao(mensagem, cliente_discord)
                elif any(tag.name in tags_permitidas for tag in mensagem.author.roles) or mensagem.author == mensagem.guild.owner:
                    await funcao(mensagem, conector_discord)
                else:
                    await mensagem.channel.send('Você não tem permissão para usar este comando.')
            break

    if mensagem.channel.id == conector_discord.canal_checkpoint_id:
        await processa_mensagem_canal_alvo(mensagem)
    if (
        mensagem.channel.id == conector_discord.canal_planilha_id
        and mensagem.content.strip() == '/checkpoint'
    ):
        await envia_planilha(mensagem)
'''

# TODO: versão 2 com adminstração de todos os comandos bloqueados [em fase de teste]
"""
for comando, funcao in comandos.items():
    if mensagem.content.startswith(comando):
        if isinstance(mensagem.channel, discord.DMChannel):
            if comando not in comandos_servidor_exclusivo:
                await funcao(mensagem, cliente_discord)
        else:
            # Verifica se o autor da mensagem tem a tag permitida ou é o dono do servidor
            if any(tag.name in tags_permitidas for tag in mensagem.author.roles) or mensagem.author == mensagem.guild.owner:
                if (
                    comando == '/linkbot'
                    or comando == '/status'
                    or comando == '/dm'
                    or comando == '/comousar'
                ):
                    await funcao(mensagem, cliente_discord)
                else:
                    await funcao(mensagem, conector_discord)
            else:
                await mensagem.channel.send('Você não tem permissão para usar este comando.')
        break
"""
