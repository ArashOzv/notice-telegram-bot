from telegram import Update
from telegram.ext import ContextTypes
from keybords.admin_keyboards import *


async def approve_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='هویت شما به عنوان ادمین تایید شد.',
        reply_markup=admin_auth_markup
    )


