import re
import threading
from telegram.ext import CommandHandler, CallbackQueryHandler, Application, MessageHandler, filters, ConversationHandler
from handlers.essensial_handlers import start, help
from handlers.notice_handlers import new_other_notice, PROSSESS_NOTICE, SELECT_NOTICE_TYPE, prossess_notice, select_notice_type
from handlers.callback_query_handlers import callback_query_handler
from handlers.message_handlers import handle_message
from decouple import config




tk = config('token')
bot_link = config('bot_link')



from functions import verify
from handlers.gate_way_handlers import pay_failed, pay_sucsess
from flask import Flask, render_template, request





flask_app = Flask(__name__)


@flask_app.route('/callback', methods=['GET'])
def callback():
    authority = request.args.get('Authority')
    status = request.args.get('Status')
    if status == 'OK':
        result = verify(authority)
        pay_sucsess(authority, result["RefID"])
        return render_template('callback.html', ref_id=result["RefID"], status=status)
    else:
        ref_id = pay_failed(authority)
        return render_template('callback.html', ref_id=ref_id, status=status)

@flask_app.route('/', methods=['GET'])
def index():
    return render_template('home.html')


# if __name__ == "__main__":
#     flask_app.run()


def main():
    app= Application.builder().token(tk).build()
    thread = threading.Thread(target=flask_app.run)
    thread.start()
    conv_handler = ConversationHandler(
        entry_points=[
            MessageHandler(filters.Regex(re.compile(r'^آگهی جدید$', re.IGNORECASE)), new_other_notice)
        ],
        states={
            SELECT_NOTICE_TYPE: [MessageHandler(filters.TEXT & ~filters.COMMAND, select_notice_type)],
            PROSSESS_NOTICE: [MessageHandler(filters.ALL, prossess_notice)],
        },
        fallbacks=[],
    )
    app.add_handlers([
        CommandHandler('start', start),
        CommandHandler('help', help),

        conv_handler,

        CallbackQueryHandler(callback_query_handler),
        
        MessageHandler(~filters.COMMAND, handle_message),
    ])

    
    
    app.run_polling()

if __name__ == "__main__":
    main()







