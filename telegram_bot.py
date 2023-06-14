from typing import Final

# pip install python-telegram-bot
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

print('Starting up bot...')

TOKEN: Final = '6153015218:AAG2EpB3kQoFEBbS4cenv7DByGNOJws3yCI'
BOT_USERNAME: Final = '@guess_the_n_bot'

     
async def start_command(update, context):
    await update.message.reply_text('Salve cria, seja bem-vindo!')
    await update.message.reply_text('Seguinte, funciona assim. Tem 5 digitos em uma certa ordem que voce tem que descobrir quais sao. Tipo assim: 5 8 2 0 1.')
    await update.message.reply_text('Ai voce me manda 5 digitos espacados, eu te digo quantos deles voce acertou e quantos deles estao na posicao correta!')

async def help_command(update, context):
    await update.message.reply_text(
        """
        /start -> Eu acordo e te explico como funciona o joguin
        /play -> Voce joga o joguin
        /help -> Printa isso tudo aqui
        /playlist -> Musica recomendada pra ouvir enquanto joga!
        """
    )

async def playlist_command(update, context):
    await update.message.reply_text('Escuta isso aqui namoral: \n https://www.youtube.com/watch?v=dQw4w9WgXcQ')


def handle_response(text: str) -> str:

    array = [7, 9, 2, 5, 0]
    # Create your own response logic
    resposta = text.split()
    if len(resposta) < 5:
        return "Sao 5 numeros amigao"
    resposta = [int(n) for n in resposta]

    n_corretos = 0
    pos_correta = 0

    for n in range(len(resposta)):
        if resposta[n] in array:
            n_corretos+=1
        
        if resposta[n] == array[n]:
            pos_correta+=1


    resposta = [str(n) for n in resposta]
    ret = "Sua resposta: " + " ".join(resposta) + "| Numeros corretos: " + str(n_corretos) + "| Posicao correta: " + str(pos_correta)

    if n_corretos == pos_correta == 5:
        return "Parabens, voce ganhou! \n" + ret

    return ret


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Get basic info of the incoming message
    message_type: str = update.message.chat.type
    text: str = update.message.text

    # Print a log for debugging
    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')

    # React to group messages only if users mention the bot directly
    if message_type == 'group':
        # Replace with your bot username
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            response: str = handle_response(new_text)
        else:
            return  # We don't want the bot respond if it's not mentioned in the group
    else:
        response: str = handle_response(text)

    # Reply normal if the message is in private
    print('Bot:', response)
    await update.message.reply_text(response)


# Log errors
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')


# Run the program
if __name__ == '__main__':
    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('playlist', playlist_command))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Log all errors
    app.add_error_handler(error)

    print('Polling...')
    # Run the bot
    app.run_polling(poll_interval=5)