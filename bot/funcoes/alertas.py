import datetime
import asyncio

async def alerta_checkpoint(cliente_discord, conector_discord):
    while True:
        if cliente_discord.is_ready() and conector_discord.canal_checkpoint_id is not None:
            if datetime.datetime.now().hour == 10 and datetime.datetime.now().weekday() < 5:
                if conector_discord.enviar_everyone:
                    await conector_discord.canal_checkpoint_id.send("@everyone")
                await conector_discord.canal_checkpoint_id.send("Hora do checkpoint!")
                await asyncio.sleep(60)
        await asyncio.sleep(1)

async def verificar_checkpoints_nao_enviados(cliente_discord, conector_discord, dados):
    while True:
        if cliente_discord.is_ready() and conector_discord.canal_checkpoint_id is not None:
            if datetime.datetime.now().hour == 11 and datetime.datetime.now().weekday() < 5:
                membros_servidor = [membro.id for membro in conector_discord.canal_checkpoint_id.guild.members]
                membros_que_enviaram_checkpoint = dados['ID do Usuário'].unique()
                membros_que_nao_enviaram_checkpoint = [membro for membro in membros_servidor if membro not in membros_que_enviaram_checkpoint and membro not in conector_discord.ids_ignorados]
                
                for membro in membros_que_nao_enviaram_checkpoint:
                    usuario = cliente_discord.get_user(membro)
                    if usuario is not None:
                        await usuario.send("Você não enviou o checkpoint hoje!")
                await asyncio.sleep(60)
        await asyncio.sleep(1)
