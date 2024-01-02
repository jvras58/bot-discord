
import discord
import emoji

from funcoes.dados import salvar_dados,dados

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

#TODO: parece a mesma função, mas não é pois essa adiciona um ID por vez e a de cima adiciona vários IDs de uma vez
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
        conector_discord.canal_planilha_id = int(id_planilha[0])
        await mensagem.channel.send(f"O ID do canal da planilha foi definido como: {conector_discord.canal_planilha_id}")
    else:
        await mensagem.channel.send("Por favor, forneça um ID para o canal da planilha. Exemplo: /idplanilha 123456789")

async def envia_link_bot(mensagem, cliente_discord):
    link = "https://discord.com/api/oauth2/authorize?client_id={}&permissions=8&scope=bot".format(cliente_discord.user.id)
    await mensagem.channel.send(link)
    
# FIXME: UMA MENSAGEM DE ISABELLE ELE NÃO PEGOU POR INTEIRO 
'''
A MENSAGEM QUE ELE PEGOU: 32] Otrs está online, consegui instalar a VPN, mas o Gitlab/staging/homolog ainda está fora do ar

A MENSAGEM COMPLETA: Site da UFPE ta fora do ar, não vou conseguir baixar a VPN até normalizar + [Atualização às 12:32] Otrs está online, consegui instalar a VPN, mas o Gitlab/staging/homolog ainda fora do ar + [Atualização às 13:08] Gitlab e frontend homolog online, backend ainda pendente. Já consegui clonar o rep

'''
async def processa_mensagem_canal_alvo(mensagem):
    """
    Função para processar mensagens recebidas no canal alvo.
    """
    linhas = mensagem.content.split('\n')
    if len(linhas) == 4:
        id_usuario = mensagem.author.id
        nome_usuario = mensagem.author.name
        #FIXME: AJUSTES NO FUSO HORARIO AINDA SÃO NECESSARIOS
        data_envio = mensagem.created_at
        data_envio_sem_fuso_horario = data_envio.replace(tzinfo=None)
        
        #FIXME: AJUSTES NO METODO DE PEGAR AS MENSAGENS PARA EVITAR ERROS DE MENSAGENS QUE TEM MAIS DE UM :
        hj_estou = linhas[0]
        ontem_eu = linhas[1].split(':')[-1].strip()
        hj_pretendo = linhas[2].split(':')[-1].strip()
        preciso_de_ajuda_com = linhas[3].split(':')[-1].strip()

        if preciso_de_ajuda_com and preciso_de_ajuda_com != '-' and preciso_de_ajuda_com != 'nada' and preciso_de_ajuda_com != 'por enquanto nada':
            preciso_de_ajuda_com = preciso_de_ajuda_com
        else:
            preciso_de_ajuda_com = None 


        if hj_estou.startswith('- **Hj estou') or hj_estou.startswith('Hj estou:') or hj_estou.startswith('- Hj estou:'):
            partes = hj_estou.split(':')
            if len(partes) > 1:
                texto = partes[1].strip()
                if texto.startswith('**'):
                    texto = texto[2:]
                emojis = [char for char in texto if emoji.emoji_count(char)]
                if emojis:
                    # Se um emoji for reconhecido
                    await mensagem.channel.send(f'O usuário {nome_usuario} com ID {id_usuario} enviou um emoji: {emojis[0]}')
                    
                    # Se for um emoji reconhecido
                    dados.loc[len(dados)] = [id_usuario, nome_usuario, emojis[0], data_envio_sem_fuso_horario, ontem_eu, hj_pretendo, preciso_de_ajuda_com]
                    dados['Data de Envio'] = dados['Data de Envio'].astype(str)
                    salvar_dados(dados)
                else:
                    # Se não for um emoji reconhecido, registre como "emoji não reconhecido" na planilha
                    emoji_nao_reconhecido = "emoji não reconhecido"
                    await mensagem.channel.send(f'O usuário {nome_usuario} com ID {id_usuario} enviou um emoji não reconhecido: {emoji_nao_reconhecido}')
                    dados.loc[len(dados)] = [id_usuario, nome_usuario, emoji_nao_reconhecido, data_envio_sem_fuso_horario, ontem_eu, hj_pretendo, preciso_de_ajuda_com]
                    dados['Data de Envio'] = dados['Data de Envio'].astype(str)
                    salvar_dados(dados)
