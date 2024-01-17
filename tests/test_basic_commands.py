from unittest.mock import MagicMock, mock_open, patch

import pytest


@pytest.mark.asyncio
async def test_status(basic_commands, interaction):
    await basic_commands.status(interaction)
    interaction.response.send_message.assert_called_once()


# FIXME: CORREÇÃO NO TESTE DO ENVIO DE LINK
# @pytest.mark.asyncio
# async def test_linkbot(basic_commands, interaction):
#     # Cria um objeto AsyncMock para substituir 'avatar.read'
#     read_mock = AsyncMock(return_value="Imagem")

#     # Usa 'patch' para substituir 'avatar.read' em todos os lugares onde ele é chamado
#     with patch('discord.User.avatar.read', new=read_mock):
#         await basic_commands.linkbot(interaction)
#         interaction.response.send_message.assert_called_once()
#         interaction.user.create_dm.assert_called_once()


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


def test_load_basic_commands(basic_commands):
    tree = MagicMock()
    basic_commands.load_basic_commands(tree)
    assert tree.command.call_count == 3
