import asyncio
import datetime

import discord


async def alerta_checkpoint(cliente_discord, conector_discord):
    await cliente_discord.wait_until_ready()
    while not cliente_discord.is_closed():
        agora = datetime.datetime.now()
        # so dias de seg a sexta
        if agora.weekday() < 5 and agora.hour == 15 and agora.minute == 35:
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
    await cliente_discord.wait_until_ready()
    while not cliente_discord.is_closed():
        canal_alvo = cliente_discord.get_channel(
            conector_discord.canal_checkpoint_id
        )
        # print(f'Canal alvo: {canal_alvo}')

        if not is_time_to_check():
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


def is_time_to_check():
    agora = datetime.datetime.now()
    return agora.weekday() < 5 and agora.hour == 16 and agora.minute == 22


def filter_members(membros, usuarios_enviaram, ids_ignorados):
    return [
        membro
        for membro in membros
        if membro.id not in usuarios_enviaram
        and membro.id not in ids_ignorados
    ]


async def send_messages(
    membros, cliente_discord, conector_discord, canal_alvo
):
    for membro in membros:
        if not canal_alvo.permissions_for(membro).read_messages or membro.bot:
            continue

        if conector_discord.enviar_dm and membro != cliente_discord.user:
            try:
                await membro.send(
                    'Você não enviou o checkpoint hoje! Por favor, envie o checkpoint.'
                )
            except discord.errors.HTTPException as e:
                print(
                    f'Erro ao enviar mensagem para o usuário {membro.id}: {e}'
                )
