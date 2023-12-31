
import discord
import emoji

from funcoes.dados import salvar_dados,dados #, salvar_dados_anteriores

async def on_ready(cliente_discord,conector_discord,dados, alerta_checkpoint, verificar_checkpoints_nao_enviados):
    print(f'{cliente_discord.user} conectado ao Discord!')
    cliente_discord.loop.create_task(alerta_checkpoint(cliente_discord, conector_discord))
    cliente_discord.loop.create_task(verificar_checkpoints_nao_enviados(cliente_discord, conector_discord, dados))


async def on_message(mensagem, cliente_discord, conector_discord, envia_link_bot, processa_mensagem_canal_alvo, envia_planilha, envia_dm, comousar, offeveryone, oneveryone, offavisodm, onavisodm, idignore, readicionarids, idcheckpoint, idplanilha):
    if mensagem.author == cliente_discord.user:
        return

    if isinstance(mensagem.channel, discord.DMChannel):
        if mensagem.content.startswith('/linkbot'):
            await envia_link_bot(mensagem, cliente_discord)
        elif mensagem.content.startswith('/status'):
            await mensagem.channel.send(
                'Estou funcionando perfeitamente! Meu status é {0}'.format(
                    cliente_discord.status))
        elif mensagem.content.startswith('/dm'):
            await envia_dm(mensagem, cliente_discord)
        elif mensagem.content.startswith('/comousar'):
            await comousar(mensagem, cliente_discord)
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

    #FIXME: A FUNÇAO PROCESSA_MENSAGEM_CANAL_ALVO ESTÁ FUNCIONANDO POREM NÃO ESTÁ ENVIANDO DE VOLTA A PLANILHA PARA O /idplanilha
    if mensagem.channel.id == conector_discord.canal_checkpoint_id:
        await processa_mensagem_canal_alvo(mensagem)
    elif mensagem.channel.id == conector_discord.canal_planilha_id and mensagem.content.strip() == '/checkpoint':
        await envia_planilha(mensagem)
        
    #TODO: PEGAR MENSAGENS ANTERIORES DO CANAL DE CHECKPOINT E SALVAR EM UMA PLANILHA DIFERNTE DA DO CHECKPOINT DO DIA
    '''
    if mensagem.channel.id == conector_discord.canal_checkpoint_id:
        await processa_mensagens_anteriores(cliente_discord, conector_discord)
    elif mensagem.channel.id == conector_discord.canal_planilha_id and mensagem.content.strip() == '/checkpoint_anteriores':
        await envia_planilha(mensagem)
    '''

async def envia_link_bot(mensagem, cliente_discord):
    link = "https://discord.com/api/oauth2/authorize?client_id={}&permissions=8&scope=bot".format(cliente_discord.user.id)
    await mensagem.channel.send(link)

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
                    salvar_dados(dados)
                else:
                    # Se não for um emoji reconhecido, registre como "emoji não reconhecido" na planilha
                    emoji_nao_reconhecido = "emoji não reconhecido"
                    await mensagem.channel.send(f'O usuário {nome_usuario} com ID {id_usuario} enviou um emoji não reconhecido: {emoji_nao_reconhecido}')
                    dados.loc[len(dados)] = [id_usuario, nome_usuario, emoji_nao_reconhecido, data_envio_sem_fuso_horario, ontem_eu, hj_pretendo, preciso_de_ajuda_com]
                    dados['Data de Envio'] = dados['Data de Envio'].astype(str)
                    salvar_dados(dados)

#TODO: PEGAR MENSAGENS ANTERIORES DO CANAL DE CHECKPOINT E SALVAR EM UMA PLANILHA DIFERNTE DA DO CHECKPOINT DO DIA
'''
async def processa_mensagens_anteriores(cliente_discord, conector_discord):
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
'''
