from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()


#region secondary models

class Payment_User(Base):
    __tablename__ = 'payment_user'
    id = Column(Integer, primary_key=True)
    user_id = user_id = Column(Integer, ForeignKey('users.id'))
    payment_id = Column(Integer, ForeignKey('payments.id'))


class Other_Notice_User(Base):
    __tablename__ = 'other_notice_user'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    other_notice_id = Column(Integer, ForeignKey('others.id'))
#endregion




class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    tel_id = Column(String(100))
    num_id = Column(String(50))
    phone = Column(String(20))
    wallet = Column(Integer, default=0)
    verify_code = Column(Integer)
    is_admin = Column(Boolean, default=False)
    others = relationship("OtherNotice", back_populates='user', secondary='other_notice_user')
    payments = relationship("Payment", back_populates='user', secondary='payment_user')


class MainMessage(Base):
    __tablename__ = 'messages_main'
    id = Column(Integer, primary_key=True)
    message_id = Column(String(50))
    message_code = Column(String(50))
    chat_id = Column(String(50))

class StatMesssage(Base):
    __tablename__ = 'messages_stat'
    id = Column(Integer, primary_key=True)
    message_id = Column(String(50))
    message_code = Column(String(50))
    chat_id = Column(String(50))


class ApproveMessage(Base):
    __tablename__ = 'messages_approve'
    id = Column(Integer, primary_key=True)
    message_id = Column(String(50))
    message_code = Column(String(50))
    chat_id = Column(String(50))
    caption = Column(String(300))



class Payment(Base):
    __tablename__ = 'payments'
    id = Column(Integer, primary_key=True)
    status = Column(String(50), default='not paid')
    authority = Column(String(50), default='')
    ref_id = Column(String(1024), default='')
    pay_message_id = Column(String(50), default='')
    amount = Column(Integer)
    message_code = Column(String(50))
    date_paid = Column(DateTime)
    user = relationship("User", back_populates="payments", secondary='payment_user', uselist=False)




class OtherNotice(Base):
    __tablename__ = 'others'
    id = Column(Integer, primary_key=True)
    notice = Column(String(1024))
    other_photo_path = Column(String(300))
    user = relationship("User", back_populates="others", secondary='other_notice_user', uselist=False)



class StatusMessage(Base):
    __tablename__ = 'satus_messages'
    id = Column(Integer, primary_key=True)
    message_id = Column(Integer)
    message_code = Column(Integer)
    chat_id = Column(String(50))