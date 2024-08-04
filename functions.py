import os
import re

async def save_image(category, filename, file):
    parent_dir = 'images'
    if not os.path.exists(parent_dir):
        os.mkdir(parent_dir)
    if not os.path.exists(f'{parent_dir}\{category}'):
        os.mkdir(f'{parent_dir}\{category}')
    file_path = os.path.join(f'{parent_dir}\{category}', f"{filename}.jpg")
    await file.download_to_drive(file_path)
    return file_path



def extract_user_id_from_caption(caption):
    pattern = None
    if 'متفرقه' in caption:
        pattern = (
            r"#متفرقه\s*\n"
            r"#کد(?P<code>\d+)\s*\n"
            r"(?:.*\n)*?"  # Non-capturing group to match any text including new lines
            r"ارتباط با آگهی دهنده\s*:\s*(?P<username>.*?)\s*\n"
            r"ایدی عددی کاربر\s*:\s*(?P<num_id>\d+)\s*\n\s*\n\s*\n"
            r"🆔🌐@farhangiwall"
        )
    if not pattern:
        return None

    match = re.match(pattern, caption, re.DOTALL)
    if not match:
        return None

    user_id = match.group('num_id')
    code = match.group('code')
    updated_caption = re.sub(r"ایدی عددی کاربر\s*:\s*.*?\s*\n\s*\n\s*\n", '\n\n\n', caption)

    return user_id, updated_caption, code


def change_other_notice_caption(caption):
    pattern = r"(.*?)(\s*?555\s*)$"

    match = re.match(pattern, caption, re.DOTALL)
    if match:
        # Extract the part of the caption before the code
        updated_caption = match.group(1).strip()
        return updated_caption
    else:
        pattern = r"(.*?)(\s*?444\s*)$"

        match = re.match(pattern, caption, re.DOTALL)
        if match:
            # Extract the part of the caption before the code
            updated_caption = match.group(1).strip()
            return updated_caption
        else:
            return None


def expire_notice(caption, status):
    if 'notice_done' in status:
        stat = 'واگذار شد✅'
    if 'delete_my_notice' in status:
        stat = 'منقضی شده⛔️'

    new_text = re.sub(r"ارتباط با آگهی دهنده:(?P<username>.*?)\n", f'ارتباط با آگهی دهنده: {stat}', caption)
    new_text = re.sub(r"ایدی عددی کاربر:(?P<num_id>.*?)\n\n\n",'\n\n\n', new_text)
    return new_text, stat

#payments:
from decouple import config
import json
import requests

amount = config('amount_per_notice_R')
SANDBOX = config('SANDBOX')
MERCHANT = config('MERCHANT')


if SANDBOX:
    sandbox = 'sandbox'
else:
    sandbox = 'www'


ZP_API_REQUEST = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
ZP_API_VERIFY = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
ZP_API_STARTPAY = f"https://{sandbox}.zarinpal.com/pg/StartPay/"

# amount = 1000  # Rial / Required
# description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"  # Required
# phone = '09022668233'  # Optional
# Important: need to edit for realy server.
CallbackURL = config('CallbackURL')

def send_request(phone, description):
    data = {
        "MerchantID": MERCHANT,
        "Amount": amount,
        "Description": description,
        "Phone": phone,
        "CallbackURL": CallbackURL,
    }
    data = json.dumps(data)
    headers = {'content-type': 'application/json', 'content-length': str(len(data))}
    try:
        response = requests.post(ZP_API_REQUEST, data=data, headers=headers, timeout=10)

        if response.status_code == 200:
            response = response.json()
            if response['Status'] == 100:
                return {'status': True, 'url': ZP_API_STARTPAY + str(response['Authority']), 'authority': response['Authority']}
            else:
                return {'status': False, 'code': str(response['Status'])}
        return {'status': False, 'code': 'error'}
    
    except requests.exceptions.Timeout:
        return {'status': False, 'code': 'timeout'}
    except requests.exceptions.ConnectionError:
        return {'status': False, 'code': 'connection error'}

def verify(authority):
    data = {
        "MerchantID": MERCHANT,
        "Amount": amount,
        "Authority": authority,
    }
    data = json.dumps(data)
    # set content length by data
    headers = {'content-type': 'application/json', 'content-length': str(len(data)) }
    response = requests.post(ZP_API_VERIFY, data=data,headers=headers)

    if response.status_code == 200:
        response = response.json()
        if response['Status'] == 100:
            return {'status': True, 'RefID': response['RefID']}
        else:
            return {'status': False, 'code': str(response['Status'])}
    return response

