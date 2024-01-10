from unittest import mock
from unittest.mock import AsyncMock, MagicMock, mock_open, patch


import pytest

from config.conector_discord import ConectorDiscord
from funcoes.comandos_basicos import BasicCommands


@pytest.fixture
def cliente_discord():
    return ConectorDiscord()


@pytest.fixture
def basic_commands(cliente_discord):
    return BasicCommands(cliente_discord)


@pytest.fixture
def interaction():
    interaction = MagicMock()
    interaction.response.send_message = AsyncMock()
    interaction.user.create_dm = AsyncMock()
    return interaction


@pytest.mark.asyncio
async def test_status(basic_commands, interaction):
    await basic_commands.status(interaction)
    interaction.response.send_message.assert_called_once()


@pytest.mark.asyncio
async def test_linkbot(basic_commands, interaction):
    await basic_commands.linkbot(interaction)
    interaction.response.send_message.assert_called_once()
    interaction.user.create_dm.assert_called_once()



@pytest.mark.asyncio
async def test_comousar(basic_commands, interaction):
    with patch(
        'builtins.open',
        new_callable=mock_open,
        read_data='conteúdo do arquivo',
    ) as mock_file:
        await basic_commands.comousar(interaction)
        interaction.response.send_message.assert_called_once_with(
            'Enviando como usar...', ephemeral=True
        )
        interaction.user.create_dm.assert_called_once()
        mock_file.assert_any_call('comomeusar.md', 'rb')
        dm_channel = await interaction.user.create_dm()
        #TODO: discord.File NÃO É O MESMO QUE EU ESTARIA TESTANDO AQUI NO TEST ENTÃO UMA MANEIRA DE CONTORNAR ISSO É O MOCK.ANY QUE PASSA A VERIFICAÇÃO PARA QUALQUER VALOR..
        dm_channel.send.assert_called_once_with(
            file=mock.ANY
        )

def test_load_basic_commands(basic_commands):
    tree = MagicMock()
    basic_commands.load_basic_commands(tree)
    assert tree.command.call_count == 3
