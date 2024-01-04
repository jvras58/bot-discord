import os
import discord
import pandas as pd

# DataFrames para armazenar os dados pegos pelo bot
colunas = [
    'id_usuario',
    'nome_usuario',
    'emojis',
    'Data de Envio',
    'ontem_eu',
    'hj_pretendo',
    'preciso_de_ajuda_com',
]

dados = pd.DataFrame(columns=colunas)
dados_anteriores = pd.DataFrame(columns=colunas)

# Função para salvar os dados em uma planilha Excel
def salvar_dados(dados, nome_arquivo):
    """
    Salva os dados em uma planilha Excel.

    Args:
    dados: DataFrame - Os dados a serem salvos.
    nome_arquivo: str - Nome do arquivo a ser criado.
    """
    try:
        dados.to_excel(nome_arquivo, index=False)
    except Exception as e:
        print(f"Erro ao salvar os dados: {e}")

# Função para enviar as planilhas quando o comando /checkpoint é recebido
async def envia_planilha(mensagem):
    """
    Envia as planilhas quando o comando /checkpoint é recebido.

    Args:
    mensagem: discord.Message - A mensagem recebida que desencadeou o comando.
    """
    # Verifica e envia o checkpoint atual
    checkpoint_atual = 'checkpoint.xlsx'
    if not os.path.exists(checkpoint_atual):
        await mensagem.channel.send('Nenhum checkpoint identificado. Por favor, gere um no canal de #checkpoint!')
    else:
        try:
            with open(checkpoint_atual, 'rb') as f:
                await mensagem.channel.send('Aqui está o checkpoint de hoje:', file=discord.File(f, checkpoint_atual))
            os.remove(checkpoint_atual)
        except Exception as e:
            print(f"Erro ao enviar o checkpoint atual: {e}")

    # Verifica e envia o checkpoint anterior
    checkpoint_anterior = 'checkpoint_anteriores.xlsx'
    if not os.path.exists(checkpoint_anterior):
        return  # Ignora se o checkpoint anterior não existir
    
    try:
        with open(checkpoint_anterior, 'rb') as f:
            await mensagem.channel.send('Aqui estão os checkpoints antigos:', file=discord.File(f, checkpoint_anterior))
        os.remove(checkpoint_anterior)
    except Exception as e:
        print(f"Erro ao enviar o checkpoint anterior: {e}")
