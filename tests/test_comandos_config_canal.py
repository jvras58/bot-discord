from unittest.mock import MagicMock

import pytest


@pytest.mark.asyncio
async def test_canalcheckpoint(canal_commands, interaction, mock_canal):
    await canal_commands.canalcheckpoint(interaction, mock_canal)
    interaction.response.send_message.assert_called_once_with(
        f'ID do canal de checkpoint definido para {mock_canal}.'
    )
    assert canal_commands.cliente_discord.canal_checkpoint_id == mock_canal.id


@pytest.mark.asyncio
async def test_canalplanilha(canal_commands, interaction, mock_canal):
    await canal_commands.canalplanilha(interaction, mock_canal)
    interaction.response.send_message.assert_called_once_with(
        f'ID do canal da planilha definido para {mock_canal}.'
    )
    assert canal_commands.cliente_discord.canal_planilha_id == mock_canal.id


def test_load_channel_commands(canal_commands):
    tree = MagicMock()
    canal_commands.load_channel_commands(tree)
    assert tree.command.call_count == 2
