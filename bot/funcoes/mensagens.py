
import discord


async def on_ready(cliente_discord,conector_discord,dados, alerta_checkpoint, verificar_checkpoints_nao_enviados):
    print(f'{cliente_discord.user} conectado ao Discord!')
    cliente_discord.loop.create_task(alerta_checkpoint(cliente_discord, conector_discord))
    cliente_discord.loop.create_task(verificar_checkpoints_nao_enviados(cliente_discord, conector_discord, dados))


async def on_message(mensagem, cliente_discord, conector_discord, envia_link_bot, processa_mensagem_canal_alvo, envia_planilha, envia_dm, comousar, offeveryone, oneveryone, offavisodm, onavisodm, idignore, readicionarids, idcheckpoint, idplanilha):
    """
    Função para lidar com mensagens recebidas.
    """
    if mensagem.author == cliente_discord.user:
        return

    if isinstance(mensagem.channel, discord.DMChannel):
        if mensagem.content.startswith('/linkbot'):
            await envia_link_bot(mensagem,cliente_discord)
        elif mensagem.content.startswith('/status'):
            await mensagem.channel.send(
                'Estou funcionando perfeitamente! Meu status é {0}'.format(
                    cliente_discord.status))
        elif mensagem.content.startswith('/dm'):
            await envia_dm(mensagem)
        elif mensagem.content.startswith('/comousar'):
            await comousar(mensagem)
        return

    if mensagem.content.startswith('/offeveryone'):
        await offeveryone(mensagem, conector_discord)
    elif mensagem.content.startswith('/oneveryone'):
        await oneveryone(mensagem, conector_discord)
    elif mensagem.content.startswith('/offavisodm'):
        await offavisodm(mensagem, conector_discord)
    elif mensagem.content.startswith('/onavisodm'):
        await onavisodm(mensagem, conector_discord)
    elif mensagem.content.startswith('/idignore'):
        await idignore(mensagem, conector_discord)
    elif mensagem.content.startswith('/readicionarids'):
        await readicionarids(mensagem, conector_discord)
    elif mensagem.content.startswith('/idcheckpoint'):
        await idcheckpoint(mensagem, conector_discord)
    elif mensagem.content.startswith('/idplanilha'):
        await idplanilha(mensagem, conector_discord)

    if mensagem.content.startswith('/linkbot'):
        await envia_link_bot(mensagem,cliente_discord)

    if mensagem.content.startswith('/status'):
        await mensagem.channel.send(
            'Estou funcionando perfeitamente! Meu status é {0}'.format(
                cliente_discord.status))
        
    if mensagem.channel.id == conector_discord.canal_checkpoint_id:
        await processa_mensagem_canal_alvo(mensagem)
    if mensagem.channel.id == conector_discord.canal_planilha_id and mensagem.content.strip() == '/checkpoint':
        await envia_planilha(mensagem)
