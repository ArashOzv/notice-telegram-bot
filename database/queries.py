from database.models import MainMessage, ApproveMessage, OtherNotice, Payment, StatMesssage, StatusMessage, User
from migrations import session
import random



def add_user(name, tel_id, num_id, phone):
        new_user = User(
            name = name,
            tel_id = tel_id,
            num_id = num_id,
            phone = phone,
        )
        session.add(new_user)
        session.commit()
        return new_user


def db_new_other_notice(notice, user, photo_path):
    
    new_other = OtherNotice(
        notice=notice,
        user=user,
        other_photo_path=photo_path
    )
    session.add(new_other)
    session.commit()
    return new_other



def db_new_payment(user, amount, authority, message_code):
    new_payment = Payment(
        amount = amount,
        user=user,
        authority = authority,
        message_code = message_code,
        status='not paid'
    )
    session.add(new_payment)
    session.commit()
    return new_payment

def get_payment_by_id(authority):
    payment = session.query(Payment).filter_by(authority=authority).first()
    return payment

def update_payment(payment, ref_id, status):
    if payment.status == 'paid':
        return 'payment already paid'
    payment.status = status
    payment.ref_id = ref_id
    session.add(payment)
    session.commit()
    return 'payment updated'

def get_user_by_id(num_id):
    user = session.query(User).filter_by(num_id=num_id).first()
    return user

def create_update_verify_code(user_num_id):
    user = session.query(User).filter_by(num_id=user_num_id).first()
    new_verify_code = random.randint(10000,99999)

    user.verify_code = new_verify_code
    session.add(user)
    session.commit()
    return new_verify_code

def set_admin(user: User):
    user.is_admin = True

    session.add(user)
    session.commit()

def store_main_message(message_id, code, chat_id):
    new_message = MainMessage(
        message_id = message_id,
        message_code = code,
        chat_id = chat_id,
    )
    session.add(new_message)
    session.commit()

def store_stat_message(message_id, code, chat_id):
    new_message = StatMesssage(
        message_id = message_id,
        message_code = code,
        chat_id = chat_id,
    )
    session.add(new_message)
    session.commit()

def store_approve_message(message_id, code, chat_id, caption):
    new_message = ApproveMessage(
        message_id = message_id,
        message_code = code,
        chat_id = chat_id,
        caption = caption
    )
    session.add(new_message)
    session.commit()


def store_status_message(message_id, message_code, chat_id):
    new_message = StatusMessage(
        message_code=message_code,
        message_id=message_id,
        chat_id=chat_id
    )
    session.add(new_message)
    session.commit()
    return new_message

def get_main_message_in_db(code):
    message = session.query(MainMessage).filter_by(message_code=code).first()
    if not message:
        return 'message not in db'
    else:
        return message
    
def get_approve_message_in_db(code):
    message = session.query(ApproveMessage).filter_by(message_code=code).first()
    if not message:
        return 'message not in db'
    else:
        return message

def get_status_message(code):
    message = session.query(StatusMessage).filter_by(message_code=code).first()
    if not message:
        return 'message not in db'
    else:
        return message
