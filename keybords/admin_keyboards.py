from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from decouple import config
admin_channal_url = config('approve_link')


admin_auth_keys = [
    [InlineKeyboardButton('ورود به کانال بررسی آگهی', url=admin_channal_url)]
]

admin_auth_markup = InlineKeyboardMarkup(admin_auth_keys)