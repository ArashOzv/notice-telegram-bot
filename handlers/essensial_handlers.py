from telegram import Update
from telegram.ext import ContextTypes, CallbackContext
from keybords.user_keyboards import *
from database.models import User
from migrations import session
from decouple import config



async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_num_id = update.effective_chat.id
    user = session.query(User).filter_by(num_id=user_num_id).first()
    chat_id = config('main_username')
    channel1_join_status = await context.bot.get_chat_member(chat_id=chat_id, user_id=user_num_id)
    if not channel1_join_status.status in ['member', 'administrator', 'creator']:
        await context.bot.send_message(
            chat_id=user_num_id,
            text='برای استفاده از ربات ابتدا در کانال(ها) زیر عضو شوید',
            reply_markup=channals_keys_markup
        )
    else:
        if user is None:
            recive_contact = True
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='لطفا ابتدا ثبت نام کنید🗒😃',
                reply_markup=signup_keys_markup,
            )
        else:
            name = update.effective_sender.first_name
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f'سلام {name} عزیز\nمن ربات ثبت آگهی های خرید و فروش جزوه، کتاب، نمونه سوال، آگهی های نیازمندی و و هرچیز دیگه که تو بخوای هستم\nبرای ثبت آگهی فقط کافیه از دکمه های قرار داده شده استفاده کنی❤️😘\n\ndeveloped by: @Arashtz',
                reply_markup=user_start_keys_markup,
            )







async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = update.effective_sender.first_name
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f'سلام {name} عزیز\nمن ربات ثبت آگهی های خرید و فروش جزوه، کتاب، نمونه سوال، آگهی های نیازمندی و و هرچیز دیگه که تو بخوای هستم\nبرای ثبت آگهی فقط کافیه از دکمه های قرار داده شده استفاده کنی❤️😘\n\ndeveloped by: @Arashtz',
        reply_markup=user_start_keys_markup,
    )




async def register_success(update: Update, context: ContextTypes.DEFAULT_TYPE, user: User):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f' ثبت نام شما با موفقیت انجام شد💥👍\n\nمشخصات شما:\nنام: {user.name}\nشماره تلفن: {user.phone}\nآیدی عددی: {user.num_id}\nیوزرنیم: {user.tel_id}',
        reply_markup=user_start_keys_markup,
    )
    await help(update, context)