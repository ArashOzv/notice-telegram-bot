import uuid
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, ContextTypes
from database.models import MainMessage, Payment, StatMesssage
from functions import expire_notice, extract_user_id_from_caption
from database.queries import get_approve_message_in_db, get_status_message, get_user_by_id, store_approve_message, store_stat_message, update_payment
from handlers.essensial_handlers import start
from migrations import session
from keybords.user_keyboards import channel_to_bot_markup
from decouple import config
amount = config('amount_per_notice_R')
bot_token = config('token')
channal_id = config('channal_id')
should_pay = config('pay')
main_channal = config('main_channal_link')

async def callback_query_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query

    if query.data == 'approved':
        user_id, caption, code = extract_user_id_from_caption(query.message.caption)
        file_id = query.message.photo[-1].file_id

        message = await context.bot.send_photo(
            chat_id=channal_id,
            photo=file_id,
            caption=caption,
            reply_markup=channel_to_bot_markup
        )

        store_approve_message(message_id=message.id, code=code, chat_id=message.chat.id, caption=query.message.caption)

        user_notice_keys = [
    [       InlineKeyboardButton('حذف آگهی من🚫', callback_data=f'delete_my_notice {code}'), InlineKeyboardButton('واگذار شد✅', callback_data=f'notice_done {code}')]
        ]

        user_notice_markup = InlineKeyboardMarkup(user_notice_keys)

        message = await context.bot.send_message(
            chat_id=user_id,
            text=f'🙂آگهی شما با متن زیر تایید شد\n\n{caption}\n\n\n{main_channal}{message.id}',
            reply_markup=user_notice_markup
        )
        store_stat_message(message_id=message.id, code=code, chat_id=message.chat.id)
        await query.edit_message_caption(
            caption=f'{query.message.caption}\n\n✅تایید شده توسط ادمین @{update.effective_user.username}'
        )

    if query.data == 'disapproved':
        user_id, caption, code = extract_user_id_from_caption(query.message.caption)
        payment = session.query(Payment).filter_by(message_code=code).first()
        stat_message = session.query(StatMesssage).filter_by(message_code=code).first()
        if should_pay == 'True':
            if payment.status == 'paid':
                see_wallet_key = [
                    [InlineKeyboardButton('💰مشاهده کیف پول', callback_data='my_wallet')],
                ]
                see_wallet_key_markup = InlineKeyboardMarkup(see_wallet_key)
                user = get_user_by_id(user_id)
                user.wallet = user.wallet + int(amount)
                session.add(user)
                session.commit()
                await context.bot.send_message(
                    chat_id=user_id,
                    text=f'❌😭 آگهی شما با متن زیر تایید نشد و مبلغ آن به کیف پول شما بازگشت داده شد\n\n{caption}',
                    reply_markup=see_wallet_key_markup
                )
                await context.bot.delete_message(
                    chat_id=user_id,
                    message_id=stat_message.message_id
                )
            else:
                await context.bot.send_message(
                    chat_id=user_id,
                    text=f'😑❌ آگهی شما با متن زیر تایید نشد\n\n{caption}'
                )
                await context.bot.delete_message(
                    chat_id=user_id,
                    message_id=payment.pay_message_id
                )
        else:
            await context.bot.send_message(
                    chat_id=user_id,
                    text=f'😑❌ آگهی شما با متن زیر تایید نشد\n\n{caption}'
                )
        await query.edit_message_caption(
            caption=f'{query.message.caption}\n\n❌تایید نشده توسط ادمین @{update.effective_user.username}'
        )


    if 'delete_my_notice' in query.data or 'notice_done' in query.data:
        q = query.data.split(' ')
        code = q[1:]
        for i in code:
            code = i
        message = get_approve_message_in_db(code)
        if message == 'message not in db':
            await query.answer('😉پس از تایید آگهی میتوانید اقدام به تغییر وضعیت آن کنید')
            return
        new_text, stat = expire_notice(message.caption, query.data)

        await context.bot.edit_message_caption(
            chat_id=message.chat_id,
            caption=new_text,
            message_id=message.message_id,
            reply_markup=channel_to_bot_markup
        )

        await query.edit_message_text(
            text=f'آگهی شما به وضعیت {stat} تغییر کرد'
        )

    if query.data == 'start':
        await query.delete_message()
        await start(update, context)

    if query.data == 'my_wallet':
        user = get_user_by_id(update.effective_chat.id)
        await query.answer(f'😌موجودی کیف پول شما مبلغ {user.wallet} تومان است')
            

    if 'pay' in query.data:
        payment_id = query.data.split(' ')[1]
        payment = session.query(Payment).filter_by(id=payment_id).first()
        ref_id = uuid.uuid4().hex
        update_payment(payment, ref_id, 'paid')
        message_code = payment.message_code
        user = payment.user
        user.wallet = user.wallet - int(payment.amount)
        session.add(user)
        session.commit()

        base_url = f"https://api.telegram.org/bot{bot_token}/editMessageText"
        message_text = f'✅پرداخت شما با شماره پیگیری {ref_id} کامل شد و آگهی شما پس از تایید ادمین در کانال قرار خواهد گرفت'
        params = {
            'chat_id': user.num_id,
            'message_id': payment.pay_message_id,
            'text': message_text,
        }
        requests.get(base_url, params=params)

        message = get_status_message(message_code)
        base_url = f"https://api.telegram.org/bot{bot_token}/editMessageText"
        message_text = f'✅وضعیت آگهی با #کد{message_code} پرداخت شده است.'
        params = {
            'chat_id': message.chat_id,
            'message_id': message.message_id,
            'text': message_text,
        }
        response = requests.get(base_url, params=params)

    if 'confirm' in query.data:
        message_code = query.data.split(' ')[1]
        user = get_user_by_id(update.effective_chat.id)
        message = session.query(StatMesssage).filter_by(message_code=message_code).first()
        base_url = f"https://api.telegram.org/bot{bot_token}/editMessageText"
        message_text = f'✅وضعیت آگهی با #کد{message_code} توسط کاربر پذیرفته شده است.'
        params = {
            'chat_id': message.chat_id,
            'message_id': message.message_id,
            'text': message_text,
        }
        response = requests.get(base_url, params=params)

        message = session.query(StatMesssage).filter_by(message_code=f'x{message_code}').first()
        base_url = f"https://api.telegram.org/bot{bot_token}/editMessageText"
        message_text = f'ممنون از ثبت آگهی شما\n\nتایید یا عدم تاییدش رو خودم خدمتت عرض میکنم جناب😎'
        params = {
            'chat_id': user.num_id,
            'message_id': message.message_id,
            'text': message_text,
        }
        requests.get(base_url, params=params)

