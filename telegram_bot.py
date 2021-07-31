from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
from apis import common, request_function

token = "token"
room = '디알씨 모빌리티 (DRC) 커뮤니티'

# updater
updater = Updater(token=token, use_context=True)
dispatcher = updater.dispatcher


# command hander
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="DRC_TELEGRAM_BOT START")


def message(update, context):
    sender = update.message.from_user['first_name']
    chat_id = update.effective_chat.id
    message = update.message.text
    print(update.message)

    # hide or kick
    if common.get_forbidden_words(room, message):
        context.bot.delete_message(chat_id=chat_id, message_id=update.message.message_id)  # hide
        # context.bot.ban_chat_member(chat_id=chat_id, user_id=update.message.from_user['id']) # kick

    # command
    if common.get_command_list(room, message) == '':
        if message[0] == "/":
            command = message.split('/')[1]

            try:
                command = command.lower()
            except:
                command = message.split('/')[1]

            if command == "drc":
                context.bot.send_message(chat_id=chat_id, text=request_function.get_drc(sender))
            elif command == "슈퍼카":
                context.bot.send_message(chat_id=chat_id, text=request_function.get_drc(sender))
            elif command[0:2] == "날씨":
                if len(command) == 2:
                    context.bot.send_message(chat_id=chat_id,
                                             text=common.get_weather('', sender)
                                             )
                else:
                    context.bot.send_message(chat_id=chat_id,
                                             text=common.get_weather(message.split('/')[1].split(' ')[1], sender)
                                             )
            elif command == "코로나":
                context.bot.send_message(chat_id=chat_id,
                                         text=common.get_covid()
                                         )
        if message.split(' ')[0] == "옥희야":
            context.bot.send_message(chat_id=chat_id,
                                     text=common.get_okhee(message.split(' ')[1])
                                     )
    else:
        context.bot.send_message(chat_id=chat_id,
                                 text=common.get_command_list(room, message)
                                 )


message_handler = MessageHandler(Filters.text, message)
updater.dispatcher.add_handler(message_handler)

command = [CommandHandler('start', start)]

for i in command:
    dispatcher.add_handler(i)

updater.start_polling()
updater.idle()
