from telegram import KeyboardButton, KeyboardButton, KeyboardButtonRequestChat, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from decouple import config
bot_link = config('bot_link')
channal = config('main_username')
channal = channal.strip().strip("'")

channals_keys = [
    [InlineKeyboardButton('عضویت در کانال', url=f"https://t.me/{channal.lstrip('@')}")],
    [InlineKeyboardButton('عضو شدم', callback_data='start')]
]

channals_keys_markup = InlineKeyboardMarkup(channals_keys)


wallet_keys = [
    [InlineKeyboardButton('کیف پول من', callback_data='my_wallet')],
]

wallet_keys_markup = InlineKeyboardMarkup(wallet_keys)




user_start_keys = [
    [KeyboardButton('راهنما',), KeyboardButton('آگهی جدید',)],
]

user_start_keys_markup = ReplyKeyboardMarkup(user_start_keys, resize_keyboard=True)

signup_keys = [
    [KeyboardButton('ثبت نام', request_contact=True)]
]
signup_keys_markup = ReplyKeyboardMarkup(signup_keys, resize_keyboard=True)



approve_notice_keys = [
    [InlineKeyboardButton('تایید آگهی', callback_data='approved'), InlineKeyboardButton('عدم تایید آگهی', callback_data='disapproved')]
]

approve_notice_markup = InlineKeyboardMarkup(approve_notice_keys)




channel_to_bot_keys = [
    [InlineKeyboardButton('ثبت آگهی', url=bot_link)]
]
channel_to_bot_markup = InlineKeyboardMarkup(channel_to_bot_keys)





other_notice_keys = [
    [KeyboardButton('عکس دارم'), KeyboardButton('عکس ندارم')],
    [KeyboardButton('بازگشت')]
]

other_notice_keys_markup = ReplyKeyboardMarkup(other_notice_keys, resize_keyboard=True)

