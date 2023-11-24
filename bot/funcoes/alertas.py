import datetime
import asyncio
import discord


async def alerta_checkpoint(cliente_discord, conector_discord):
    await cliente_discord.wait_until_ready()
    while not cliente_discord.is_closed():
        agora = datetime.datetime.now()
        # so dias de seg a sexta
        if agora.weekday() < 5 and agora.hour == 13 and agora.minute == 15:
            canal = cliente_discord.get_channel(conector_discord.canal_checkpoint_id)
            if canal is not None:  # Check if the channel exists
                if conector_discord.enviar_everyone:  # Verifica se enviar_everyone é True antes de enviar a mensagem
                    await canal.send("@everyone Lembre-se de responder ao #checkpoint!")
            await asyncio.sleep(60) # para ele não ficar spawnando a mensagem direto
        else:
            await asyncio.sleep(1)

# FIXME: o codigo deveria estar restrito a so membros que conseguem ver o canal de checkpoint e que não estão na lista de ignorados
async def verificar_checkpoints_nao_enviados(cliente_discord, conector_discord, dados):
    await cliente_discord.wait_until_ready()
    canal_alvo = cliente_discord.get_channel(1158343397279543327)
    while not cliente_discord.is_closed():
        agora = datetime.datetime.now()
        if agora.weekday() < 5 and agora.hour == 15 and agora.minute == 18:
            if canal_alvo is not None:
                print("O canal alvo existe")
                # Lista de usuários que já enviaram o checkpoint
                usuarios_enviaram = dados['ID do Usuário'].tolist()
                print("IDs dos usuários que já enviaram o checkpoint:", usuarios_enviaram)
                # Lista de membros do servidor
                membros = canal_alvo.guild.members
                for membro in membros:
                    if membro.id not in usuarios_enviaram and membro.id not in conector_discord.ids_ignorados:
                        # Envia mensagem privada para usuários que não enviaram o checkpoint
                        if conector_discord.enviar_dm:
                            try:
                                await membro.send("Você não enviou o checkpoint hoje! Por favor, envie o checkpoint.")
                            except discord.errors.HTTPException as e:
                                print(f"Erro ao enviar mensagem para o usuário {membro.id}: {e}")
            await asyncio.sleep(60)  # para evitar mensagens repetidas
        else:
            await asyncio.sleep(1)
