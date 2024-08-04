from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from database.queries import add_user
from handlers.essensial_handlers import register_success, start, help
from keybords.user_keyboards import *
from decouple import config
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_message.text == 'بازگشت':
        ConversationHandler.END
        return await start(update, context)

    elif update.effective_message.contact:
        chat_id = config('main_username')
        channel1_join_status = await context.bot.get_chat_member(chat_id=chat_id, user_id=update.effective_chat.id)

        if not channel1_join_status.status in ['member', 'administrator', 'creator']:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='برای استفاده از ربات ابتدا در کانال های زیر عضو شوید',
                reply_markup=channals_keys_markup
            )
        else:
            name = update.effective_message.contact.first_name
            tel_id = f'@{update.effective_user.username}'
            num_id = update.effective_message.contact.user_id
            phone = update.effective_message.contact.phone_number
            if not update.effective_user.username:
                await context.bot.send_message(
                    chat_id=num_id,
                    text='😒لطفا برای اکانت خود آیدی ثبت کنید راه ارتباط آگهی شما با آیدی است.'
                )
                return
            new_user = add_user(name, tel_id, num_id, phone)
            await register_success(update, context, new_user)

    elif update.message.text == 'راهنما':
        ConversationHandler.END
        return await help(update, context)

