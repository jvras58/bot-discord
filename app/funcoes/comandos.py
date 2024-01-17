import asyncio
import io

import discord
import emoji
from config.config import get_settings
from funcoes.dados import dados, dados_anteriores, salvar_dados
from PIL import Image, ImageDraw, ImageFont


async def processa_mensagem_canal_alvo(mensagem):
    """
    Função para processar mensagens recebidas no canal alvo.

    Parâmetros:
        mensagem (discord.Message): A mensagem a ser processada.

    """
    linhas = mensagem.content.split('\n')
    if len(linhas) == 4:
        id_usuario = mensagem.author.id
        nome_usuario = mensagem.author.name
        # FIXME: AJUSTES NO FUSO HORARIO AINDA SÃO NECESSARIOS
        data_envio = mensagem.created_at
        data_envio_sem_fuso_horario = data_envio.replace(tzinfo=None)

        hj_estou = linhas[0]
        ontem_eu = ':'.join(linhas[1].split(':')[1:]).strip()
        hj_pretendo = ':'.join(linhas[2].split(':')[1:]).strip()
        preciso_de_ajuda_com = ':'.join(linhas[3].split(':')[1:]).strip()

        if (
            preciso_de_ajuda_com
            and preciso_de_ajuda_com != '-'
            and preciso_de_ajuda_com != 'nada'
            and preciso_de_ajuda_com != 'Nada'
            and preciso_de_ajuda_com != 'nada;'
            and preciso_de_ajuda_com != 'por enquanto nada'
            and preciso_de_ajuda_com != 'não'
            and preciso_de_ajuda_com != 'não por enquanto'
            and preciso_de_ajuda_com != 'nda'
            and preciso_de_ajuda_com != 'nd'
            and preciso_de_ajuda_com != 'Por enquanto, nada.'
        ):
            preciso_de_ajuda_com = preciso_de_ajuda_com
        else:
            preciso_de_ajuda_com = None

        if (
            hj_estou.startswith('- **Hj estou')
            or hj_estou.startswith('Hj estou:')
            or hj_estou.startswith('- Hj estou:')
        ):
            partes = hj_estou.split(':')
            if len(partes) > 1:
                texto = partes[1].strip()
                if texto.startswith('**'):
                    texto = texto[2:]
                emojis = [char for char in texto if emoji.emoji_count(char)]
                if emojis:
                    # Se um emoji for reconhecido
                    await mensagem.channel.send(
                        f'O usuário {mensagem.author.mention} enviou um checkpoint com o emoji: {emojis[0]}'
                    )

                    # Se for um emoji reconhecido
                    dados.loc[len(dados)] = [
                        id_usuario,
                        nome_usuario,
                        emojis[0],
                        data_envio_sem_fuso_horario,
                        ontem_eu,
                        hj_pretendo,
                        preciso_de_ajuda_com,
                    ]
                    dados['Data de Envio'] = dados['Data de Envio'].astype(str)
                    salvar_dados(dados, 'checkpoint.xlsx')
                else:
                    # Se não for um emoji reconhecido, registre como "emoji não reconhecido" na planilha
                    emoji_nao_reconhecido = 'emoji não reconhecido'
                    await mensagem.channel.send(
                        f'O usuário {mensagem.author.mention} enviou um checkpoint com um emoji não reconhecido'
                    )
                    dados.loc[len(dados)] = [
                        id_usuario,
                        nome_usuario,
                        emoji_nao_reconhecido,
                        data_envio_sem_fuso_horario,
                        ontem_eu,
                        hj_pretendo,
                        preciso_de_ajuda_com,
                    ]
                    dados['Data de Envio'] = dados['Data de Envio'].astype(str)
                    salvar_dados(dados, 'checkpoint.xlsx')


async def processa_mensagens_anteriores(conector_discord, cliente_discord):
    """
    Processa as mensagens anteriores de um canal do Discord.

    Args:
        conector_discord: O conector do Discord.
        cliente_discord: O cliente do Discord.
    """

    while conector_discord.canal_checkpoint_id is None:
        await asyncio.sleep(
            1
        )  # aguarda 1 segundo antes de verificar novamente

    canal_alvo = await cliente_discord.fetch_channel(
        conector_discord.canal_checkpoint_id
    )
    if canal_alvo is None:
        print(
            f'Não foi possível encontrar o canal com ID {conector_discord.canal_checkpoint_id}'
        )
        return
    # FIXME: CUIDADO COM O LIMIT DE MENSAGENS ANTERIORES ESTA DEFINIDO PARA 2500
    mensagens_anteriores = canal_alvo.history(
        limit=50000
    )  # Obtem as últimas mensagens do canal
    async for mensagem in mensagens_anteriores:
        linhas = mensagem.content.split('\n')
        if len(linhas) == 4:
            id_usuario = mensagem.author.id
            nome_usuario = mensagem.author.name
            data_envio = mensagem.created_at
            data_envio_sem_fuso_horario = data_envio.replace(tzinfo=None)

            hj_estou = linhas[0]
            ontem_eu = ':'.join(linhas[1].split(':')[1:]).strip()
            hj_pretendo = ':'.join(linhas[2].split(':')[1:]).strip()
            preciso_de_ajuda_com = ':'.join(linhas[3].split(':')[1:]).strip()

            if (
                preciso_de_ajuda_com
                and preciso_de_ajuda_com != '-'
                and preciso_de_ajuda_com != 'nada'
                and preciso_de_ajuda_com != 'Nada'
                and preciso_de_ajuda_com != 'nada;'
                and preciso_de_ajuda_com != 'por enquanto nada'
                and preciso_de_ajuda_com != 'não'
                and preciso_de_ajuda_com != 'não por enquanto'
                and preciso_de_ajuda_com != 'nda'
                and preciso_de_ajuda_com != 'nd'
                and preciso_de_ajuda_com != 'Por enquanto, nada.'
            ):
                preciso_de_ajuda_com = preciso_de_ajuda_com
            else:
                preciso_de_ajuda_com = None

            if hj_estou.startswith('**'):
                hj_estou = hj_estou[2:]
            emojis = [char for char in hj_estou if emoji.emoji_count(char)]
            if emojis:
                # Se um emoji for reconhecido
                await mensagem.channel.send(
                    f'O usuário {mensagem.author.mention} tem checkpoint antigo contendo o emoji:{emojis[0]}'
                )

                # Se for um emoji reconhecido
                dados_anteriores.loc[len(dados_anteriores)] = [
                    id_usuario,
                    nome_usuario,
                    emojis[0],
                    data_envio_sem_fuso_horario,
                    ontem_eu,
                    hj_pretendo,
                    preciso_de_ajuda_com,
                ]
                dados_anteriores['Data de Envio'] = dados_anteriores[
                    'Data de Envio'
                ].astype(str)
                salvar_dados(dados_anteriores, 'checkpoint_anteriores.xlsx')
            else:
                # Se não for um emoji reconhecido, registre como "emoji não reconhecido" na planilha
                emoji_nao_reconhecido = 'emoji não reconhecido'
                await mensagem.channel.send(
                    f'O usuário {mensagem.author.mention} tem checkpoint antigo mas o emoji não foi reconhecido'
                )
                dados_anteriores.loc[len(dados_anteriores)] = [
                    id_usuario,
                    nome_usuario,
                    emoji_nao_reconhecido,
                    data_envio_sem_fuso_horario,
                    ontem_eu,
                    hj_pretendo,
                    preciso_de_ajuda_com,
                ]
                dados_anteriores['Data de Envio'] = dados_anteriores[
                    'Data de Envio'
                ].astype(str)
                salvar_dados(dados_anteriores, 'checkpoint_anteriores.xlsx')


async def create_image(
    usuario1: discord.User,
    usuario2: discord.User = None,
    porcentagem: int = None,
):
    imagem1 = await usuario1.avatar.read()
    avatar1 = Image.open(io.BytesIO(imagem1)).resize(
        get_settings().AVATAR_SIZE
    )

    if usuario2:
        planodefundo = Image.new(
            'RGB',
            get_settings().BACKGROUND_SIZE,
            get_settings().BACKGROUND_COLOR,
        )
        planodefundo.paste(avatar1, (0, 0))

        imagem2 = await usuario2.avatar.read()
        avatar2 = Image.open(io.BytesIO(imagem2)).resize(
            get_settings().AVATAR_SIZE
        )
        planodefundo.paste(avatar2, (get_settings().AVATAR_SIZE[0], 0))
    else:
        planodefundo = Image.new(
            'RGB', get_settings().AVATAR_SIZE, get_settings().BACKGROUND_COLOR
        )
        planodefundo.paste(avatar1, (0, 0))

    if porcentagem is not None:
        fundodraw = ImageDraw.Draw(planodefundo)
        fundodraw.rounded_rectangle(
            (
                (0, get_settings().AVATAR_SIZE[1]),
                (
                    get_settings().BACKGROUND_SIZE[0] * (porcentagem / 100),
                    get_settings().BACKGROUND_SIZE[1] + 9,
                ),
            ),
            fill=get_settings().RECTANGLE_COLOR,
            radius=get_settings().RECTANGLE_RADIUS,
        )

        fonte = ImageFont.truetype(
            'RobotoMono-Bold.ttf', get_settings().FONT_SIZE
        )
        fundodraw.text(
            (230, get_settings().AVATAR_SIZE[1]), f'{porcentagem}%', font=fonte
        )

    buffer = io.BytesIO()
    planodefundo.save(buffer, format='PNG')
    buffer.seek(0)

    return buffer
