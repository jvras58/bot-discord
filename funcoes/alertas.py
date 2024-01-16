import asyncio
from datetime import datetime

import discord


def is_time_to_check_alerta_checkpoint(conector_discord):
    """
    Verifica se é hora de verificar o alerta do checkpoint.

    Retorna True se for um dia útil (segunda a sexta-feira), no horário definido pelo comando definir_alerta.
    Caso contrário, retorna False.
    """
    horario_alerta_str = conector_discord.alerta_checkpoint_horario
    if horario_alerta_str is None:
        return False

    # Converta a string de volta para um objeto time
    horario_alerta = datetime.strptime(horario_alerta_str, '%H:%M').time()

    agora = datetime.now()
    # print(f'Horário do alerta: {horario_alerta}')
    # print(agora.time())  # Imprime apenas a hora atual, sem a data

    return (
        agora.weekday() < 5
        and agora.time().hour == horario_alerta.hour
        and agora.time().minute == horario_alerta.minute
    )


async def alerta_checkpoint(cliente_discord, conector_discord):
    """
    Envia um alerta para o canal de checkpoint no Discord.

    Parâmetros:
    - cliente_discord: o cliente do Discord.
    - conector_discord: o conector do Discord.
    """
    await cliente_discord.wait_until_ready()
    while not cliente_discord.is_closed():

        if is_time_to_check_alerta_checkpoint(conector_discord):
            canal = cliente_discord.get_channel(
                conector_discord.canal_checkpoint_id
            )

            if canal is not None:
                if (
                    conector_discord.enviar_everyone
                ):  # Verifica se enviar_everyone é True antes de enviar a mensagem
                    await canal.send(
                        '@everyone Lembre-se de responder ao #checkpoint!'
                    )
            await asyncio.sleep(
                60
            )   # para ele não ficar spawnando a mensagem direto
        else:
            await asyncio.sleep(1)


async def verificar_checkpoints_nao_enviados(
    cliente_discord, conector_discord, dados
):
    """
    Verifica checkpoints não enviados e alerta os membros do canal alvo.

    Args:
        cliente_discord (discord.Client): O cliente Discord.
        conector_discord (ConectorDiscord): O conector Discord.
        dados (dict): Os dados contendo informações sobre os checkpoints.
    """
    await cliente_discord.wait_until_ready()
    while not cliente_discord.is_closed():
        canal_alvo = cliente_discord.get_channel(
            conector_discord.canal_checkpoint_id
        )
        # print(f'Canal alvo: {canal_alvo}')

        if not is_time_to_check(conector_discord):
            await asyncio.sleep(1)
            continue

        if canal_alvo is None:
            await asyncio.sleep(60)
            continue

        # print('O canal alvo existe')
        usuarios_enviaram = dados['id_usuario'].tolist()
        # print('IDs dos usuários que já enviaram o checkpoint:', usuarios_enviaram)

        membros = canal_alvo.guild.members
        membros_para_alertar = filter_members(
            membros, usuarios_enviaram, conector_discord.ids_ignorados
        )

        await send_messages(
            membros_para_alertar, cliente_discord, conector_discord, canal_alvo
        )

        await asyncio.sleep(60)  # para evitar mensagens repetidas


def is_time_to_check(conector_discord):
    """
    Verifica se é hora de verificar o checkpoints não enviados.

    Retorna True se for um dia útil (segunda a sexta-feira), às 18:00 da tarde.
    Caso contrário, retorna False.
    """
    horario_alerta_str = conector_discord.verificar_checkpoint_horario
    if horario_alerta_str is None:
        return False

    # Converta a string de volta para um objeto time
    horario_alerta = datetime.strptime(horario_alerta_str, '%H:%M').time()

    agora = datetime.now()

    return (
        agora.weekday() < 5
        and agora.time().hour == horario_alerta.hour
        and agora.time().minute == horario_alerta.minute
    )


def filter_members(membros, usuarios_enviaram, ids_ignorados):
    """
    Filtra uma lista de membros com base em usuários que já enviaram mensagens e IDs ignorados.

    Args:
        membros (list): Lista de membros a serem filtrados.
        usuarios_enviaram (list): Lista de IDs de usuários que já enviaram mensagens.
        ids_ignorados (list): Lista de IDs a serem ignorados.

    Returns:
        list: Lista filtrada de membros.
    """
    return [
        membro
        for membro in membros
        if membro.id not in usuarios_enviaram
        and membro.id not in ids_ignorados
    ]


async def send_messages(
    membros, cliente_discord, conector_discord, canal_alvo
):
    """
    Envia mensagens para os membros especificados.

    Args:
        membros (list): Lista de membros para os quais as mensagens devem ser enviadas.
        cliente_discord (discord.Client): Cliente do Discord.
        conector_discord (ConectorDiscord): Conector do Discord.
        canal_alvo (discord.TextChannel): Canal de texto onde obtem a lista para enviar as mensagens.

    """
    for membro in membros:
        if not canal_alvo.permissions_for(membro).read_messages or membro.bot:
            continue
        # # Verifica se enviar_dm é True antes de enviar a mensagem
        if conector_discord.enviar_dm and membro != cliente_discord.user:
            try:
                await membro.send(
                    'Você não enviou o checkpoint hoje! Por favor, envie o checkpoint.'
                )
            except discord.errors.HTTPException as e:
                print(
                    f'Erro ao enviar mensagem para o usuário {membro.id}: {e}'
                )
