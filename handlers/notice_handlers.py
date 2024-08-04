from telegram import Update
from telegram.ext import ContextTypes, CallbackContext, ConversationHandler
from handlers.essensial_handlers import start
from keybords.user_keyboards import *
from telegram import Update
from telegram.ext import ContextTypes
from handlers.gate_way_handlers import *
from database.queries import db_new_other_notice, get_user_by_id, store_main_message, store_stat_message, store_status_message
from functions import save_image
from handlers.gate_way_handlers import *


from decouple import config
approve_kanal_id = config('approve_kanal_id')
admin_password = config('admin_password')
admins_number_list = config('admins_number_list')
main_username = config('main_username')
np_jozve_img_path = config('default_jozve_img_path')
np_sq_img_path = config('default_sq_img_path')
default_other_img_path = config('default_other_img_path')
should_pay = config('pay')

NOTICE_ENTRY, PROSSESS_NOTICE, SELECT_NOTICE_TYPE, NOTICE_DONE = range(4)


async def new_notice_success(update: Update, context: ContextTypes.DEFAULT_TYPE, message_id):
    user_notice_keys = [
    [InlineKeyboardButton('حذف آگهی من🚫', callback_data=f'delete_my_notice {message_id}'), InlineKeyboardButton('واگذار شد✅', callback_data=f'notice_done {message_id}')]
    ]

    user_notice_markup = InlineKeyboardMarkup(user_notice_keys)
    message_success = await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='🥰آگهی شما با موفقیت ثبت شد و پس از پرداخت و تایید ادمین درکانال قرار خواهد گرفت✅',
        reply_markup=user_notice_markup
    )
    return message_success
async def delete_message(update: Update, context: ContextTypes.DEFAULT_TYPE, chat_id, message_id):
    await context.bot.delete_message(
        chat_id = chat_id,
        message_id = message_id,
    )


async def new_other_notice(update: Update, context:ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='🤔آیا آگهی شما عکس دار است؟\nنکته مهم: اگر متن آگهی شما طولانی است بدون عکس ارسال کنید🎯',
        reply_markup=other_notice_keys_markup
    )

    return SELECT_NOTICE_TYPE



async def new_other_channal_approve_admin(update: Update, context: ContextTypes.DEFAULT_TYPE, other, user, channal_id,  main_username):
    message = await context.bot.send_photo(
        chat_id=channal_id,
        photo= open(other.other_photo_path, 'rb'),
        caption=f'#متفرقه\n#کد{update.message.id}\n{other.notice}\n\nارتباط با آگهی دهنده: {user.tel_id}\nایدی عددی کاربر: {user.num_id}\n\n\n🆔🌐{main_username}',
        reply_markup=approve_notice_markup
    )
    if should_pay == 'True':
        text=f'❌وضعیت آگهی با #کد{update.message.id} پرداخت نشده است.'
    else:
        text=f'❌وضعیت آگهی با #کد{update.message.id} توسط کاربر پذیرفته نشده است.'
    confirm_message = await context.bot.send_message(
        chat_id=channal_id,
        text=text  
    )
    return update.message.id, message, confirm_message

async def select_notice_type(update: Update, context: CallbackContext):
    if update.effective_message.text == 'عکس دارم':
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='🤗لطفا متن آگهی خودرا در کپشن عکس موردنظر قرار داده و ارسال کنید'
        )
        return PROSSESS_NOTICE
    elif update.effective_message.text == 'عکس ندارم':
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='الان لطفا متن آگهیت رو برام بفرست🤭'
        )
        return PROSSESS_NOTICE
    elif update.effective_message.text == 'بازگشت':
        await start(update, context)
        return ConversationHandler.END
    else:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='لطفا نوع آگهی خود را انتخاب کنید.',
            reply_markup=other_notice_keys_markup
        )


async def prossess_notice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == 'عکس دارم':
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='لطفا متن مورد نظرت رو کپشن عکست قرار بده و بفرست🤓'
        )
        return PROSSESS_NOTICE
    elif update.message.text == 'عکس ندارم':
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='لطفا متن آگهی خود را ارسال کنید.'
        )
        return PROSSESS_NOTICE
    elif update.effective_message.text == 'بازگشت':
        await start(update, context)
        return ConversationHandler.END


    user = get_user_by_id(update.effective_chat.id)
    if update.message.photo:
        photo_file = update.message.photo[-1]
        photo_file_id = photo_file.file_id
        file = await context.bot.get_file(photo_file_id)
        file_path = await save_image('other', user.name, file)
        caption = update.effective_message.caption
        other = db_new_other_notice(caption, user, file_path)
    else:
        file_path = default_other_img_path
        caption = update.effective_message.text
        other = db_new_other_notice(caption, user, file_path)
    message_code, message, confirm_message = await new_other_channal_approve_admin(update, context, other, user, approve_kanal_id, main_username)
    if should_pay == 'True':
        await pay(update, context, user, message_code, 'متفرقه')
    else:
        confirm = [
            [InlineKeyboardButton('موافقت با قوانین و ثبت آگهی', callback_data=f'confirm {message_code}')],
        ]
        confirm_markup = InlineKeyboardMarkup(confirm)
        message = await context.bot.send_message(
            chat_id=user.num_id,
            text=f'کاربر گرامی لطفا قبل از اقدام به ثبت آگهی حتما موارد کانال قوانین را مطالعه کنید و چنانچه با هریک موافق نیستید آگهی ثبت نکنید\n{rules}',
            reply_markup=confirm_markup
        )
        print(message.id)
        store_stat_message(message_id=message.id, code=f'x{message_code}', chat_id=user.num_id)
        store_stat_message(message_id=confirm_message.id, code=message_code, chat_id=approve_kanal_id)
    store_status_message(message_id=message.id+1, message_code=message_code, chat_id=approve_kanal_id)
    store_main_message(message_id=message.id, code=message_code, chat_id=message.chat.id)
    return ConversationHandler.END


