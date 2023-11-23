
import discord


async def envia_dm(mensagem, cliente_discord):
    partes = mensagem.content.split()
    if len(partes) >= 3:
        id_usuario = int(partes[1])
        texto = ' '.join(partes[2:])
        usuario = cliente_discord.get_user(id_usuario)
        if usuario:
            await usuario.send(texto)
            await mensagem.channel.send(f"Mensagem enviada para o usuário com ID {id_usuario}.")
        else:
            await mensagem.channel.send(f"Não foi possível encontrar o usuário com ID {id_usuario}.")
    else:
        await mensagem.channel.send("Por favor, forneça um ID de usuário e uma mensagem. Exemplo: /dm 11111111111111111 Olá!")

async def comousar(mensagem):
    with open('comomeusar.md', 'rb') as file:
        await mensagem.channel.send("Aqui está:", file=discord.File(file, 'comomeusar.md'))

async def offeveryone(mensagem, conector_discord):
    conector_discord.enviar_everyone = False
    await mensagem.channel.send("O envio de mensagens @everyone foi desativado.")

async def oneveryone(mensagem, conector_discord):
    conector_discord.enviar_everyone = True
    await mensagem.channel.send("O envio de mensagens @everyone foi reativado.")

async def offavisodm(mensagem, conector_discord):
    conector_discord.enviar_dm = False
    await mensagem.channel.send("O envio de avisos por DM foi desativado.")

async def onavisodm(mensagem, conector_discord):
    conector_discord.enviar_dm = True
    await mensagem.channel.send("O envio de avisos por DM foi reativado.")

async def idignore(mensagem, conector_discord):
    ids_para_ignorar = mensagem.content.split()[1:]  # Pega todos os IDs após o comando /idignore
    if ids_para_ignorar:
        conector_discord.ids_ignorados.extend(ids_para_ignorar)
        await mensagem.channel.send(f"Os seguintes IDs foram adicionados à lista de ignorados: {', '.join(ids_para_ignorar)}")
    else:
        await mensagem.channel.send("Por favor, forneça pelo menos um ID para ignorar. Exemplo: /idignore 11111111111111111")

#testeme: parece a mesma função, mas não é pois essa adiciona um ID por vez e a de cima adiciona vários IDs de uma vez
# async def idignore(mensagem, conector_discord):
#     partes = mensagem.content.split()
#     if len(partes) >= 2:
#         id_usuario = int(partes[1])
#         conector_discord.ids_ignorados.add(id_usuario)
#         await mensagem.channel.send(f"O usuário com ID {id_usuario} foi adicionado à lista de IDs ignorados.")
#     else:
#         await mensagem.channel.send("Por favor, forneça um ID de usuário. Exemplo: /idignore 11111111111111111")


async def readicionarids(mensagem, conector_discord):
    ids_para_readicionar = mensagem.content.split()[1:]  # Pega todos os IDs após o comando /readicionarids
    if ids_para_readicionar:
        conector_discord.ids_ignorados = [id for id in conector_discord.ids_ignorados if id not in ids_para_readicionar]
        await mensagem.channel.send(f"Os seguintes IDs foram removidos da lista de ignorados: {', '.join(ids_para_readicionar)}")
    else:
        await mensagem.channel.send("Por favor, forneça pelo menos um ID para readicionar. Exemplo: /readicionarids 11111111111111111")

async def idcheckpoint(mensagem, conector_discord):
    id_canal_checkpoint = mensagem.content.split()[1:]  # Pega o ID após o comando /idcheckpoint
    if id_canal_checkpoint:
        conector_discord.canal_checkpoint_id = int(id_canal_checkpoint[0])
        await mensagem.channel.send(f"O ID do canal de checkpoint foi definido como: {conector_discord.canal_checkpoint_id}")
    else:
        await mensagem.channel.send("Por favor, forneça um ID para o canal de checkpoint. Exemplo: /idcheckpoint 1158343397279543327")

async def idplanilha(mensagem, conector_discord):
    id_planilha = mensagem.content.split()[1:]  # Pega o ID após o comando /idplanilha
    if id_planilha:
        conector_discord.id_planilha = int(id_planilha[0])
        await mensagem.channel.send(f"O ID da planilha foi definido como: {conector_discord.id_planilha}")
    else:
        await mensagem.channel.send("Por favor, forneça um ID para a planilha. Exemplo: /idplanilha 123456789")
