from unittest.mock import AsyncMock, MagicMock,patch, mock_open

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

# FIXME: Não consigo fazer ele encontrar o arquivo comomeusar.md
# @patch('builtins.open', new_callable=mock_open, read_data="conteúdo do arquivo")
# @pytest.mark.asyncio
# async def test_comousar(basic_commands, interaction):
#     await basic_commands.comousar(interaction)
#     interaction.response.send_message.assert_called_once()
#     interaction.user.create_dm.assert_called_once()


def test_load_basic_commands(basic_commands):
    tree = MagicMock()
    basic_commands.load_basic_commands(tree)
    assert tree.command.call_count == 3
