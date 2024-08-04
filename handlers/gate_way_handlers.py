import uuid
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from database.queries import db_new_payment, get_payment_by_id, get_status_message, update_payment
from migrations import session
from functions import send_request

from decouple import config
bot_token = config('token')
amount = config('amount_per_notice_R')
approve_kanal_id = config('approve_kanal_id')
rules = config('rules')

async def pay(update: Update, context: ContextTypes.DEFAULT_TYPE, user, message_code, notice_type):
    description = f'جهت ثبت آگهی برای کاربر {user.name}'
    req_result = send_request(user.phone, description)
    new_payment = db_new_payment(user, amount, req_result['authority'], message_code)
    
    pay_keys = [
        [InlineKeyboardButton('💰پرداخت', url=req_result['url'])]
    ]
    pay_keys_markup = InlineKeyboardMarkup(pay_keys)

    wallet_pay_keys = [
        [InlineKeyboardButton('💰پرداخت', callback_data=f'pay {new_payment.id}')],
    ]
    wallet_pay_keys_markup = InlineKeyboardMarkup(wallet_pay_keys)

    if user.wallet >= int(amount):
        message= await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f'کاربر گرامی لطفا قبل از اقدام به پرداخت و ثبت آگهی حتما موارد کانال قوانین را مطالعه کنید و چنانچه با هریک موافق نیستید آگهی ثبت نکنید\n{rules}\nهزینه ثبت آگهی مبلغ 10ت است، شما میتوانید از کیف پول خود این مبلغ را پرداخت کنید❤️🙏\n\nموجودی کیف پول شما: {user.wallet} 🤯تومان',
            reply_markup=wallet_pay_keys_markup
        )
        new_payment.pay_message_id = message.id
        session.add(new_payment)
        session.commit()
    else:
        message= await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f'کاربر گرامی لطفا قبل از اقدام به پرداخت و ثبت آگهی حتما موارد کانال قوانین را مطالعه کنید و چنانچه با هریک موافق نیستید آگهی ثبت نکنید\n{rules}\nهزینه ثبت آگهی مبلغ 10ت میباشد لطفا ابتدا نسبت به پرداخت اقدام کنید❤️🙏',
            reply_markup=pay_keys_markup
        )
        new_payment.pay_message_id = message.id
        session.add(new_payment)
        session.commit()


def pay_sucsess(authority, ref_id):

    payment = get_payment_by_id(authority)
    update_payment(payment, ref_id, 'paid')
    message_code = payment.message_code
    user = payment.user

    base_url = f"https://api.telegram.org/bot{bot_token}/editMessageText"
    message_text = f'✅پرداخت شما با شماره پیگیری {ref_id} کامل شد و آگهی شما پس از تایید ادمین در کانال قرار خواهد گرفت\n\nتایید یا عدم تاییدش رو خودم خدمتت عرض میکنم جناب😎'
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

    
def pay_failed(authority):
    fail_ref_id = uuid.uuid4().variant
    payment = get_payment_by_id(authority)
    status = update_payment(payment, fail_ref_id, 'not paid')
    user = payment.user

    if status == 'payment already paid':
        base_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        message_text = f'پرداخت شما با شماره پیگیری {payment.ref_id} قبلا انجام شده است'
        params = {
            'chat_id': user.num_id,
            'text': message_text,
        }
        requests.get(base_url, params=params)
        return payment.ref_id
    if status == 'payment updated':
        base_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        message_text = f'پرداخت شما با شماره پیگیری زیر با خطا مواجه شد درصورت کسر وجه تا 72 ساعت وجه به حساب شما بازگشت داده خواهد شد در غیر این صورت با پشتیبانی تماس بگیرید\n\n{fail_ref_id}\n\n@Arashtz'
        params = {
            'chat_id': user.num_id,
            'text': message_text,
        }
        requests.get(base_url, params=params)
        return fail_ref_id




