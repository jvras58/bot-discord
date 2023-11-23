
import discord
import emoji

from funcoes.dados import salvar_dados,dados

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
        await processa_mensagem_canal_alvo(mensagem, dados, salvar_dados)
    elif mensagem.channel.id == conector_discord.canal_planilha_id and mensagem.content.strip() == '/checkpoint':
        await envia_planilha(mensagem)


async def envia_link_bot(mensagem, cliente_discord):
    link = "https://discord.com/api/oauth2/authorize?client_id={}&permissions=8&scope=bot".format(cliente_discord.user.id)
    await mensagem.channel.send(link)

async def processa_mensagem_canal_alvo(mensagem, dados, salvar_dados):
    """
    Função para processar mensagens recebidas no canal alvo.
    """
    linhas = mensagem.content.split('\n')
    if len(linhas) == 4:
        primeira_linha = linhas[0]
        if primeira_linha.startswith('- **Hj estou') or primeira_linha.startswith('Hj estou:') or primeira_linha.startswith('- Hj estou:'):
            partes = primeira_linha.split(':')
            if len(partes) > 1:
                texto = partes[1].strip()
                if texto.startswith('**'):
                    texto = texto[2:]
                emojis = [char for char in texto if emoji.emoji_count(char)]
                if emojis:
                    id_usuario = mensagem.author.id
                    nome_usuario = mensagem.author.name
                    data_envio = mensagem.created_at
                    data_envio_sem_fuso_horario = data_envio.replace(tzinfo=None)
                    # print com a mensagem capturada para testes
                    await mensagem.channel.send(f'O usuário {nome_usuario} com ID {id_usuario} enviou um emoji: {emojis[0]}')
                    
                    # O .loc é usado para acessar linhas e colunas por rótulo len(dados) retorna o número de linhas no DataFrame (então Adiciona uma nova linha ao DataFrame 'dados')
                    dados.loc[len(dados)] = [id_usuario, nome_usuario, emojis[0], data_envio_sem_fuso_horario]

                    # Converte a coluna 'Data de Envio' do DataFrame para string.
                    dados['Data de Envio'] = dados['Data de Envio'].astype(str)
                    salvar_dados(dados)
