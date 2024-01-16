# Bot de Checkpoint

## Introdução
Este bot foi desenvolvido em Python e possui diversas funcionalidades úteis para a gestão de checkpoints. 

## Comandos

### Configuração de Canais
Para o funcionamento adequado do bot, é necessário configurar os canais de checkpoint e de administração. Estes canais são onde o bot receberá as mensagens e enviará as planilhas. Utilize os comandos `/canalcheckpoint` e `/canalplanilha` para configurá-los.

### Link do Bot
Para adicionar o bot ao seu servidor, utilize o comando `/linkbot`.

### Verificação de Status
Para verificar se o bot está funcionando corretamente, utilize o comando `/status`.

### Checkpoint
Para receber a planilha do checkpoint do dia, vá ao canal de administração e digite `@checkpoint`. O bot enviará a planilha para o canal.

### Monitoramento de Checkpoint
O bot possui uma função de monitoramento para verificar quem enviou o checkpoint e avisar quem não enviou via DM. Esta função pode ser ativada ou desativada com os comandos `/offavisodm` e `/onavisodm`. O horário de envio é definido pelo comando `/horario_verificar` seguido pela hora e minuto (`/horario_verificar HH:MM`). Esta função é desativada automaticamente nos finais de semana.

### Mensagem @everyone
O bot pode enviar uma mensagem `@everyone` no canal do checkpoint em um horário determinado. Esta função pode ser ativada ou desativada com os comandos `/offeveryone` e `/oneveryone`. O horário de envio é definido pelo comando `/horario_alerta` seguido pela hora e minuto (`/horario_alerta HH:MM`). Esta função é desativada automaticamente nos finais de semana.

### Ignorar IDs
O bot possui uma função que permite ignorar IDs, ou seja, nenhuma mensagem será enviada para o ID ignorado (útil para períodos de férias). Utilize os comandos `/idignore` para remover e `/readicionarids` para adicioná-los novamente.

## Funções Extras

### Mensagem Privada
O bot pode enviar mensagens privadas através do comando `/dm`, onde enviará uma mensagem privada para o usuário fornecido.

### Ship
o bot tem uma função de shipagem tanto de amizade quanto de namoro basta usar o comando `/ship` é especificar se é namoro = TRUE ou amizade = false


Todos os comandos são autoexplicativos. Se o usuário tiver dúvidas sobre como utilizá-los, basta digitar o comando e o bot mostrará como ele espera a mensagem.

## Aviso
O bot possui um pequeno banco de dados para armazenar as configurações utilizadas pelo usuário.

## Autor
- [Jonathas Vinicius]
