import os

import discord
import pandas as pd

cliente_discord = discord.Client(intents=discord.Intents.all())
# df para armazenar os dados pegos pelo bot
dados = pd.DataFrame(
    columns=[
        'id_usuario',
        'nome_usuario',
        'emojis',
        'Data de Envio',
        'ontem_eu',
        'hj_pretendo',
        'preciso_de_ajuda_com',
    ]
)

dados_anteriores = pd.DataFrame(
    columns=[
        'id_usuario',
        'nome_usuario',
        'emojis',
        'Data de Envio',
        'ontem_eu',
        'hj_pretendo',
        'preciso_de_ajuda_com',
    ]
)


def salvar_dados(dados):
    """
    Função para salvar os dados em uma planilha Excel.
    """
    dados.to_excel('checkpoint.xlsx', index=False)


def salvar_dados_anteriores():
    """
    Função para salvar os dados em uma planilha Excel.
    """
    dados_anteriores.to_excel('checkpoint_anteriores.xlsx', index=False)


async def envia_planilha(mensagem):
    """
    Função para enviar as planilhas quando o comando /checkpoint é recebido.
    """
    # Verifica se existe o checkpoint atual
    if not os.path.exists('checkpoint.xlsx'):
        await mensagem.channel.send(
            'Nenhum checkpoint identificado. Por favor, gere um no canal de #checkpoint!'
        )
    else:
        # Envia o checkpoint atual
        with open('checkpoint.xlsx', 'rb') as f:
            await mensagem.channel.send(
                'Aqui está o checkpoint de hoje:',
                file=discord.File(f, 'checkpoint.xlsx'),
            )
        os.remove(
            'checkpoint.xlsx'
        )  # Remove o arquivo localmente após o envio

    # Verifica se existe o checkpoint anterior
    if not os.path.exists('checkpoint_anteriores.xlsx'):
        return  # Ignora se o checkpoint anterior não existir

    # Envia o checkpoint anterior
    with open('checkpoint_anteriores.xlsx', 'rb') as f:
        await mensagem.channel.send(
            'Aqui está os checkpoint antigos:',
            file=discord.File(f, 'checkpoint_anteriores.xlsx'),
        )
    os.remove(
        'checkpoint_anteriores.xlsx'
    )  # Remove o arquivo localmente após o envio
