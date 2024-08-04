from decouple import config
from sms_ir import SmsIr

api_key = config('smsir_api')
linenumber = config('smsir_linenumber')

sms_ir = SmsIr(
    api_key,
    linenumber,
)



def admin_verify_sms(admin_number, code):
    number = admin_number[1:]
    number = '+98' + number
    sms_ir.send_verify_code(
    number=number,
    template_id=100000,
    parameters=[
        {
            "name" : "CODE",
            "value": code,
        },
    ])