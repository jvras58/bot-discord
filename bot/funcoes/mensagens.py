
import discord
import emoji

from funcoes.dados import salvar_dados,dados

async def on_ready(cliente_discord,conector_discord,dados, alerta_checkpoint, verificar_checkpoints_nao_enviados):
    print(f'{cliente_discord.user} conectado ao Discord!')
    cliente_discord.loop.create_task(alerta_checkpoint(cliente_discord, conector_discord))
    cliente_discord.loop.create_task(verificar_checkpoints_nao_enviados(cliente_discord, conector_discord, dados))

#função 'modularizada porém não pegando 100%'
async def on_message(mensagem, cliente_discord, conector_discord, envia_link_bot, processa_mensagem_canal_alvo, envia_planilha, envia_dm, comousar, offeveryone, oneveryone, offavisodm, onavisodm, idignore, readicionarids, idcheckpoint, idplanilha):
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
        await envia_link_bot(mensagem)

    if mensagem.content.startswith('/status'):
        await mensagem.channel.send(
            'Estou funcionando perfeitamente! Meu status é {0}'.format(
                cliente_discord.status))
    #FIXME: A FUNÇAO PROCESSA_MENSAGEM_CANAL_ALVO ESTÁ FUNCIONANDO POREM NÃO ESTÁ ENVIANDO DE VOLTA A PLANILHA PARA O /idplanilha com /checkpoint
    #TODO: O QUE ESTA FALTANDO ENTRE ESSA on_message1 PARA A MODULARIZADA FUNCIONAR??
    if mensagem.channel.id == conector_discord.canal_checkpoint_id:
        await processa_mensagem_canal_alvo(mensagem)
    elif mensagem.channel.id == conector_discord.canal_planilha_id and mensagem.content.strip() == '/checkpoint':
        await envia_planilha(mensagem)



#TODO: O QUE ESTA FALTANDO ENTRE ESSA on_message1 PARA A MODULARIZADA (on_message) FUNCIONAR??
'''
async def on_message1(mensagem, cliente_discord, conector_discord, envia_link_bot, processa_mensagem_canal_alvo, envia_planilha, envia_dm, comousar, offeveryone, oneveryone, offavisodm, onavisodm, idignore, readicionarids, idcheckpoint, idplanilha):
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
