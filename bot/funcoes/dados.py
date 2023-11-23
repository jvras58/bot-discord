
import os
import discord
import pandas as pd
cliente_discord = discord.Client(intents=discord.Intents.all())
# df para armazenar os dados pegos pelo bot
dados = pd.DataFrame(columns=['ID do Usuário', 'Nome do Usuário', 'Emoji', 'Data de Envio'])

def salvar_dados(dados):
    """
    Função para salvar os dados em uma planilha Excel.
    """
    dados.to_excel('checkpoint.xlsx', index=False)

async def envia_planilha(mensagem):
    """
    Função para enviar a planilha quando o comando /checkpoint é recebido.
    """
    # Verifica se existe usando o os 
    if not os.path.exists('checkpoint.xlsx'):
        # se não existir avisa que não existe
        await mensagem.channel.send("Nenhum checkpoint identificado Por favor Gere um no Canal de #checkpoint! .")
    else:
        # se existir ele envia 
        # rb modo leitura / f arquivo aberto 
        with open('checkpoint.xlsx', 'rb') as f:
            await mensagem.channel.send("Aqui está o checkpoint de hoje:", file=discord.File(f, 'checkpoint.xlsx'))
        # apaga do arquivo local depois de enviado para não encher 
        os.remove('checkpoint.xlsx')
