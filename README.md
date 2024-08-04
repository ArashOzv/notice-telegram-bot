# notice-telegram-bot
telegram bot that stores and share notices to a telegram channal

# configuring .env file:
1) get http token from @botfather
2) get your main telegram channal id and username
3) get sms.ir apikey and linenumber 
4) get a domain for callback url or just add localhost
5) set pay=True for paid notice submitting or pay=False
6) set amount to pay per notice
7) set SANDBOX=False and obtain MERCHANT from zarinpal.com or set SANDBOX=True and MERCHANT=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx for free notice submitting


# configuring migrations.py
 add database url to create_engine method or unhash line 9 for local sqlite database
 example for mysql: mysql://USERNAME:PASSWORD@DATABASE_HOST:PORT(DEFAULT=3306)/DATABASE_NAME