from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from database.models import User
from database.models import Base




# engine = create_engine('sqlite:///database/database.db')



engine = create_engine(
    url='DATABASE_URL',
)

session = sessionmaker(bind=engine)
session = session()

Base.metadata.create_all(engine)
session.commit()
print('databese created/updated !!')
# this file is migrations.py

