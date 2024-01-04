import asyncio
import emoji
from funcoes.dados import (
    dados,
    dados_anteriores,
    salvar_dados,
    salvar_dados_anteriores,
)


async def envia_dm(mensagem, cliente_discord):
    """
    Envia uma mensagem direta para um usuário no Discord.

    Parâmetros:
    - mensagem: O objeto de mensagem que acionou o comando.
    - cliente_discord: O cliente do Discord.
    """
    partes = mensagem.content.split()
    if len(partes) >= 3:
        id_usuario = int(partes[1])
        texto = ' '.join(partes[2:])
        usuario = cliente_discord.get_user(id_usuario)
        if usuario:
            await usuario.send(texto)
            await mensagem.channel.send(
                f'Mensagem enviada para o usuário com ID {id_usuario}.'
            )
        else:
            await mensagem.channel.send(
                f'Não foi possível encontrar o usuário com ID {id_usuario}.'
            )
    else:
        await mensagem.channel.send(
            'Por favor, forneça um ID de usuário e uma mensagem. Exemplo: /dm 11111111111111111 Olá!'
        )


# TODO: _ é um argumento que não será usado, mas é necessário para que o bot funcione
async def comousar(mensagem, _):
    """
    Envia seções do arquivo com instruções de como usar o bot.

    Parâmetros:
    - mensagem: a mensagem recebida pelo bot.
    - _: um parâmetro não utilizado.
    """
    with open('comomeusar.md', 'r', encoding='utf-8') as file:
        content = file.read()

        sections = content.split('\n## ')
        for section in sections:
            if section.strip():  # Verifica se a seção não está em branco
                section = (
                    '## ' + section
                )  # Adiciona '## ' de volta ao início de cada seção
                await mensagem.channel.send(section)


async def offeveryone(mensagem, conector_discord):
    """
    Desativa o envio de mensagens @everyone.

    Parâmetros:
        - mensagem: a mensagem recebida pelo bot.
        - cliente_discord: O cliente do Discord.
    """
    conector_discord.enviar_everyone = False
    await mensagem.channel.send(
        'O envio de mensagens @everyone foi desativado.'
    )


async def oneveryone(mensagem, conector_discord):
    """
    Ativa o envio de mensagens @everyone e envia uma mensagem de confirmação.

    Parâmetros:
    - mensagem: a mensagem recebida pelo bot.
    - cliente_discord: O cliente do Discord.
    """
    conector_discord.enviar_everyone = True
    await mensagem.channel.send(
        'O envio de mensagens @everyone foi reativado.'
    )


async def offavisodm(mensagem, conector_discord):
    """
    Desativa o envio de avisos por DM.

    Parâmetros:
    - mensagem: a mensagem recebida pelo bot.
    - conector_discord: O conector do Discord.
    """
    conector_discord.enviar_dm = False
    await mensagem.channel.send('O envio de avisos por DM foi desativado.')


async def onavisodm(mensagem, conector_discord):
    """
    ativa o envio de avisos por DM.

    Parâmetros:
    - mensagem: a mensagem recebida pelo bot.
    - conector_discord: O conector do Discord.
    """
    conector_discord.enviar_dm = True
    await mensagem.channel.send('O envio de avisos por DM foi reativado.')


async def idignore(mensagem, conector_discord):
    """
    Função que adiciona IDs à lista de ignorados.

    Parâmetros:
    - mensagem: O objeto de mensagem recebida pelo bot.
    - conector_discord: O conector do Discord.

    """
    ids_para_ignorar = mensagem.content.split()[
        1:
    ]  # Pega todos os IDs após o comando /idignore
    if ids_para_ignorar:
        conector_discord.ids_ignorados.extend(ids_para_ignorar)
        await mensagem.channel.send(
            f"Os seguintes IDs foram adicionados à lista de ignorados: {', '.join(ids_para_ignorar)}"
        )
    else:
        await mensagem.channel.send(
            'Por favor, forneça pelo menos um ID para ignorar. Exemplo: /idignore 11111111111111111'
        )


# TODO: parece a mesma função, mas não é pois essa adiciona um ID por vez e a de cima adiciona vários IDs de uma vez
# async def idignore(mensagem, conector_discord):
#     partes = mensagem.content.split()
#     if len(partes) >= 2:
#         id_usuario = int(partes[1])
#         conector_discord.ids_ignorados.add(id_usuario)
#         await mensagem.channel.send(f"O usuário com ID {id_usuario} foi adicionado à lista de IDs ignorados.")
#     else:
#         await mensagem.channel.send("Por favor, forneça um ID de usuário. Exemplo: /idignore 11111111111111111")


async def readicionarids(mensagem, conector_discord):
    """
    Função que readiciona IDs para a função verificar checkpoint não enviados.

    Parâmetros:
    - mensagem: O objeto de mensagem recebida pelo bot.
    - conector_discord: O conector do Discord.

    """
    ids_para_readicionar = mensagem.content.split()[
        1:
    ]  # Pega todos os IDs após o comando /readicionarids
    if ids_para_readicionar:
        conector_discord.ids_ignorados = [
            id
            for id in conector_discord.ids_ignorados
            if id not in ids_para_readicionar
        ]
        await mensagem.channel.send(
            f"Os seguintes IDs foram removidos da lista de ignorados: {', '.join(ids_para_readicionar)}"
        )
    else:
        await mensagem.channel.send(
            'Por favor, forneça pelo menos um ID para readicionar. Exemplo: /readicionarids 11111111111111111'
        )


async def idcheckpoint(mensagem, conector_discord):
    """
    Define o ID do canal de checkpoint.

    Parâmetros:
    - mensagem: O objeto da mensagem recebida.
    - conector_discord: O objeto do conector do Discord.
    """
    id_canal_checkpoint = mensagem.content.split()[
        1:
    ]  # Pega o ID após o comando /idcheckpoint
    if id_canal_checkpoint:
        conector_discord.canal_checkpoint_id = int(id_canal_checkpoint[0])
        await mensagem.channel.send(
            f'O ID do canal de checkpoint foi definido como: {conector_discord.canal_checkpoint_id}'
        )
    else:
        await mensagem.channel.send(
            'Por favor, forneça um ID para o canal de checkpoint. Exemplo: /idcheckpoint 1158343397279543327'
        )


async def idplanilha(mensagem, conector_discord):
    """
    Define o ID do canal para receber as planilhas.

    Parâmetros:
    - mensagem: O objeto da mensagem recebida.
    - conector_discord: O objeto do conector do Discord.
    """
    id_planilha = mensagem.content.split()[
        1:
    ]  # Pega o ID após o comando /idplanilha
    if id_planilha:
        conector_discord.canal_planilha_id = int(id_planilha[0])
        await mensagem.channel.send(
            f'O ID do canal da planilha foi definido como: {conector_discord.canal_planilha_id}'
        )
    else:
        await mensagem.channel.send(
            'Por favor, forneça um ID para o canal da planilha. Exemplo: /idplanilha 123456789'
        )


async def envia_link_bot(mensagem, cliente_discord):
    """
    Envia o link de convite do bot para o canal da mensagem.

    Parâmetros:
    - mensagem: A mensagem recebida pelo bot.
    - cliente_discord: O cliente Discord do bot.
    """
    link = 'https://discord.com/api/oauth2/authorize?client_id={}&permissions=8&scope=bot'.format(
        cliente_discord.user.id
    )
    await mensagem.channel.send(link)


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
                    salvar_dados(dados)
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
                    salvar_dados(dados)


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

    canal_alvo = cliente_discord.get_channel(
        conector_discord.canal_checkpoint_id
    )
    if canal_alvo is None:
        print(
            f'Não foi possível encontrar o canal com ID {conector_discord.canal_checkpoint_id}'
        )
        return
    # FIXME: CUIDADO COM O LIMIT DE MENSAGENS ANTERIORES ESTA DEFINIDO PARA 2500
    mensagens_anteriores = canal_alvo.history(
        limit=2500
    )  # Obtem as últimas 100 mensagens do canal
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
                salvar_dados_anteriores()
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
                salvar_dados_anteriores()
