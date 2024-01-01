import discord
import emoji
import pandas as pd
import asyncio
import datetime
import os
import time
from dotenv import load_dotenv
from config.conector_discord import ConectorDiscord

from config.config import get_settings

load_dotenv()

cliente_discord = discord.Client(intents=discord.Intents.all())
conector_discord = ConectorDiscord()

# df para armazenar os dados pegos pelo bot
dados = pd.DataFrame(columns=['ID do Usuário', 'Nome do Usuário', 'Emoji', 'Data de Envio','Ontem eu', 'Hoje eu pretendo', 'Preciso de ajuda com'])
dados2 = pd.DataFrame(columns=['ID do Usuário', 'Nome do Usuário', 'Emoji', 'Data de Envio','Ontem eu', 'Hoje eu pretendo', 'Preciso de ajuda com'])

def salvar_dados():
    """
    Função para salvar os dados em uma planilha Excel.
    """
    dados.to_excel('checkpoint.xlsx', index=False)

def salvar_dados_anteriores():
    """
    Função para salvar os dados em uma planilha Excel.
    """
    dados2.to_excel('checkpoint_anterior.xlsx', index=False)

async def alerta_checkpoint():
    """
    Função assíncrona para enviar um alerta de checkpoint no canal alvo de segunda a sexta-feira às 10h.
    """
    await cliente_discord.wait_until_ready()
    canal = cliente_discord.get_channel(conector_discord.canal_checkpoint_id)
    while not cliente_discord.is_closed():
        agora = datetime.datetime.now()
        # so dias de seg a sexta
        if agora.weekday() < 5 and agora.hour == 10 and agora.minute == 0:
            if conector_discord.enviar_everyone:  # Verifica se enviar_everyone é True antes de enviar a mensagem
                await canal.send("@everyone Lembre-se de responder ao #checkpoint!")
            await asyncio.sleep(60) # para ele não ficar spawnando a mensagem direto
        else:
            await asyncio.sleep(1)

async def verificar_checkpoints_nao_enviados():
    """
    Função assíncrona para verificar quem não enviou o checkpoint do dia e enviar uma mensagem privada (DM).
    """
    await cliente_discord.wait_until_ready()
    canal_alvo = cliente_discord.get_channel(conector_discord.canal_checkpoint_id)
    while not cliente_discord.is_closed():
        agora = datetime.datetime.now()
        if  agora.weekday() < 5 and agora.hour == 12 and agora.minute == 0:
            # Lista de usuários que já enviaram o checkpoint
            usuarios_enviaram = dados['ID do Usuário'].tolist()
            # Lista de membros do servidor
            membros = canal_alvo.guild.members
            for membro in membros:
                if membro.id not in usuarios_enviaram and membro.id not in conector_discord.ids_ignorados:
                    # Envia mensagem privada para usuários que não enviaram o checkpoint
                    if conector_discord.enviar_dm:
                        await membro.send("Você não enviou o checkpoint hoje! Por favor, envie o checkpoint.")
            await asyncio.sleep(60)  # para evitar mensagens repetidas
        else:
            await asyncio.sleep(1)
            
@cliente_discord.event
async def on_ready():
    """
    Função para imprimir uma mensagem quando o bot estiver pronto é gerenciar as tasks.
    """
    print('Logado como {0.user}'.format(cliente_discord))
    # criar a tarefa pro bot ficar executando:
    await processa_mensagens_anteriores()
    #FIXME: DESABILITADO POR ENQUANTO POIS SE NÃO ME ENGANO ESTÃO COM ERRO É NO MOMENTO MARLOS NÃO PEDIU ISSO TBM..
    # cliente_discord.loop.create_task(alerta_checkpoint())
    # cliente_discord.loop.create_task(verificar_checkpoints_nao_enviados())


@cliente_discord.event
async def on_message(mensagem):
    """
    Função para lidar com mensagens recebidas.
    """
    if mensagem.author == cliente_discord.user:
        return
    
    if isinstance(mensagem.channel, discord.DMChannel):
        if mensagem.content.startswith('/linkbot'):
            await envia_link_bot(mensagem)
        elif mensagem.content.startswith('/status'):
            await mensagem.channel.send(
                'Estou funcionando perfeitamente! Meu status é {0}'.format(
                    cliente_discord.status))
            
        elif mensagem.content.startswith('/dm'):
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

        elif mensagem.content.startswith('/comousar'):
            with open('comomeusar.md', 'rb') as file:
                await mensagem.channel.send("Aqui está:", file=discord.File(file, 'comomeusar.md'))
        return
    
    if mensagem.content.startswith('/offeveryone'):
        conector_discord.enviar_everyone = False
        await mensagem.channel.send("O envio de mensagens @everyone foi desativado.")
        
    elif mensagem.content.startswith('/oneveryone'):
        conector_discord.enviar_everyone = True
        await mensagem.channel.send("O envio de mensagens @everyone foi reativado.")
    
    elif mensagem.content.startswith('/offavisodm'):
        conector_discord.enviar_dm = False
        await mensagem.channel.send("O envio de avisos por DM foi desativado.")
        
    elif mensagem.content.startswith('/onavisodm'):
        conector_discord.enviar_dm = True
        await mensagem.channel.send("O envio de avisos por DM foi reativado.")
    
    elif mensagem.content.startswith('/idignore'):
        ids_para_ignorar = mensagem.content.split()[1:]  # Pega todos os IDs após o comando /idignore
        if ids_para_ignorar:
            conector_discord.ids_ignorados.extend(ids_para_ignorar)
            await mensagem.channel.send(f"Os seguintes IDs foram adicionados à lista de ignorados: {', '.join(ids_para_ignorar)}")
        else:
            await mensagem.channel.send("Por favor, forneça pelo menos um ID para ignorar. Exemplo: /idignore 11111111111111111")
    
    elif mensagem.content.startswith('/readicionarids'):
        ids_para_readicionar = mensagem.content.split()[1:]  # Pega todos os IDs após o comando /readicionarids
        if ids_para_readicionar:
            conector_discord.ids_ignorados = [id for id in conector_discord.ids_ignorados if id not in ids_para_readicionar]
            await mensagem.channel.send(f"Os seguintes IDs foram removidos da lista de ignorados: {', '.join(ids_para_readicionar)}")
        else:
            await mensagem.channel.send("Por favor, forneça pelo menos um ID para readicionar. Exemplo: /readicionarids 11111111111111111")
    
    elif mensagem.content.startswith('/idcheckpoint'):
        id_canal_checkpoint = mensagem.content.split()[1:]  # Pega o ID após o comando /idcheckpoint
        if id_canal_checkpoint:
            conector_discord.canal_checkpoint_id = int(id_canal_checkpoint[0])
            await mensagem.channel.send(f"O ID do canal de checkpoint foi definido como: {conector_discord.canal_checkpoint_id}")
        else:
            await mensagem.channel.send("Por favor, forneça um ID para o canal de checkpoint. Exemplo: /idcheckpoint 1158343397279543327")
    
    elif mensagem.content.startswith('/idplanilha'):
        id_canal_planilha = mensagem.content.split()[1:]  # Pega o ID após o comando /idplanilha
        if id_canal_planilha:
            conector_discord.canal_planilha_id = int(id_canal_planilha[0])
            await mensagem.channel.send(f"O ID do canal da planilha foi definido como: {conector_discord.canal_planilha_id}")
        else:
            await mensagem.channel.send("Por favor, forneça um ID para o canal da planilha. Exemplo: /idplanilha 1158543934021173258")
    
    if mensagem.content.startswith('/linkbot'):
        await envia_link_bot(mensagem)

    if mensagem.content.startswith('/status'):
        await mensagem.channel.send(
            'Estou funcionando perfeitamente! Meu status é {0}'.format(
                cliente_discord.status))
        
    if mensagem.channel.id == conector_discord.canal_checkpoint_id:
        await processa_mensagem_canal_alvo(mensagem)
    elif mensagem.channel.id == conector_discord.canal_planilha_id and mensagem.content.strip() == '/checkpoint':
        await envia_planilha(mensagem)



async def envia_link_bot(mensagem):
    """
    Função para enviar o link do bot quando o comando /linkbot é recebido.
    """
    link = f"https://discord.com/api/oauth2/authorize?client_id={cliente_discord.user.id}&permissions=0&scope=bot"
    await mensagem.channel.send(f"Me adicione ao seu servidor: {link}")


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
                    salvar_dados()
                else:
                    # Se não for um emoji reconhecido, registre como "emoji não reconhecido" na planilha
                    emoji_nao_reconhecido = "emoji não reconhecido"
                    await mensagem.channel.send(f'O usuário {nome_usuario} com ID {id_usuario} enviou um emoji não reconhecido: {emoji_nao_reconhecido}')
                    dados.loc[len(dados)] = [id_usuario, nome_usuario, emoji_nao_reconhecido, data_envio_sem_fuso_horario, ontem_eu, hj_pretendo, preciso_de_ajuda_com]
                    dados['Data de Envio'] = dados['Data de Envio'].astype(str)
                    salvar_dados()

async def processa_mensagens_anteriores():
    """
    Função para processar mensagens anteriores no canal alvo.
    """
    while conector_discord.canal_checkpoint_id is None:
        await asyncio.sleep(1)  # aguarda 1 segundo antes de verificar novamente

    canal_alvo = cliente_discord.get_channel(conector_discord.canal_checkpoint_id)
    if canal_alvo is None:
        print(f"Não foi possível encontrar o canal com ID {conector_discord.canal_checkpoint_id}")
        return

    mensagens_anteriores = canal_alvo.history(limit=100)  # Obtem as últimas 100 mensagens do canal
    async for mensagem in mensagens_anteriores:
        linhas = mensagem.content.split('\n')
        if len(linhas) == 4:
            id_usuario = mensagem.author.id
            nome_usuario = mensagem.author.name
            data_envio = mensagem.created_at
            data_envio_sem_fuso_horario = data_envio.replace(tzinfo=None)

            hj_estou = linhas[0]
            ontem_eu = linhas[1].split(':')[-1].strip()
            hj_pretendo = linhas[2].split(':')[-1].strip()
            preciso_de_ajuda_com = linhas[3].split(':')[-1].strip()

            if preciso_de_ajuda_com and preciso_de_ajuda_com != '-' and preciso_de_ajuda_com != 'nada' and preciso_de_ajuda_com != 'por enquanto nada':
                preciso_de_ajuda_com = preciso_de_ajuda_com
            else:
                preciso_de_ajuda_com = None 

            if hj_estou.startswith('**'):
                hj_estou = hj_estou[2:]
            emojis = [char for char in hj_estou if emoji.emoji_count(char)]
            if emojis:
                # Se um emoji for reconhecido
                await mensagem.channel.send(f'O usuário {nome_usuario} com ID {id_usuario} tem checkpoint antigo: {emojis[0]}')
                
                # Se for um emoji reconhecido
                dados2.loc[len(dados2)] = [id_usuario, nome_usuario, emojis[0], data_envio_sem_fuso_horario, ontem_eu, hj_pretendo, preciso_de_ajuda_com]
                dados2['Data de Envio'] = dados2['Data de Envio'].astype(str)
                salvar_dados_anteriores()
            else:
                # Se não for um emoji reconhecido, registre como "emoji não reconhecido" na planilha
                emoji_nao_reconhecido = "emoji não reconhecido"
                await mensagem.channel.send(f'O usuário {nome_usuario} com ID {id_usuario} tem checkpoint antigo mas o emoji não foi reconhecido: {emoji_nao_reconhecido}')
                dados2.loc[len(dados2)] = [id_usuario, nome_usuario, emoji_nao_reconhecido, data_envio_sem_fuso_horario, ontem_eu, hj_pretendo, preciso_de_ajuda_com]
                dados2['Data de Envio'] = dados2['Data de Envio'].astype(str)
                salvar_dados_anteriores()


async def envia_planilha(mensagem):
    """
    Função para enviar as planilhas quando o comando /checkpoint é recebido.
    """
    # Verifica se existe o checkpoint atual
    if not os.path.exists('checkpoint.xlsx'):
        await mensagem.channel.send("Nenhum checkpoint identificado. Por favor, gere um no canal de #checkpoint!")
    else:
        # Envia o checkpoint atual
        with open('checkpoint.xlsx', 'rb') as f:
            await mensagem.channel.send("Aqui está o checkpoint de hoje:", file=discord.File(f, 'checkpoint.xlsx'))
        os.remove('checkpoint.xlsx')  # Remove o arquivo localmente após o envio

    # Verifica se existe o checkpoint anterior
    if not os.path.exists('checkpoint_anterior.xlsx'):
        return  # Ignora se o checkpoint anterior não existir

    # Envia o checkpoint anterior
    with open('checkpoint_anterior.xlsx', 'rb') as f:
        await mensagem.channel.send("Aqui está o checkpoint anterior:", file=discord.File(f, 'checkpoint_anterior.xlsx'))
    os.remove('checkpoint_anterior.xlsx')  # Remove o arquivo localmente após o envio

        
while True:
    try:
        # Inicialização do cliente do Discord
        cliente_discord.run(get_settings().DISCORD_TOKEN)
    except Exception as e:
        print(f"Erro: {e}. Reiniciando o bot.")
        time.sleep(5)  # Pausa por 5s
