import os
import secrets
from dotenv import load_dotenv
from sqlalchemy import text
from sqlmodel import create_engine
from sqlmodel import select
from models import Member, Message
import hashlib
import time


## Database setup
load_dotenv()  # Retrieve DB variables in .env

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

# Connect to MySQL server (no database specified) to check/create the database
def create_database_if_not_exists():
    server_url = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/"
    temp_engine = create_engine(server_url)
    with temp_engine.connect() as conn:
        conn.execute(text(f"CREATE DATABASE IF NOT EXISTS `{DB_NAME}` CHARACTER SET utf8mb4"))
        conn.commit()
    temp_engine.dispose()

create_database_if_not_exists()

# Connect to MySQL
mysql_url = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(mysql_url, echo=True)


def validate_login(session, email, pwd):
    stat = select(Member).where(
        Member.email == email,
        Member.password == pwd
    )
    return session.exec(stat).first()


def check_email(session, email):
    stat = select(Member).where(Member.email == email)
    return session.exec(stat).first()


def create_member(session, member):
    session.add(member)
    session.commit()
    session.refresh(member)
    return member


def get_all_messages(session, user_id):
    stat = (
        select(Message, Member.name)
        .join(Member, Message.member_id == Member.id)
        .order_by(Message.time.desc())
    )

    results = session.exec(stat).all()

    return [{
            "id": message.id,
            "name": name,
            "content": message.content,
            "self": message.member_id == user_id
        }
        for message, name in results
    ]


def create_message(session, message):
    session.add(message)
    session.commit()
    session.refresh(message)
    return message


def delete_message(session, id):
    message = session.get(Message, id)
    session.delete(message)
    session.commit()
    return message


def get_author_id(session, id):
    return session.get(Message, id).member_id


def get_member_by_id(session, id):
    return session.get(Member, id)


def update_token(session, id):
    # Get member data
    member = get_member_by_id(session, id)
    salt = secrets.token_hex(8)
    
    # Create token using sha256
    token = hashlib.sha256(f"{member.email}|{salt}|{time.time()}".encode()).hexdigest()
    member.token = token
    session.commit()
    return token


def get_member_by_token(session, token):
    stat = select(Member).where(Member.token == token)
    return session.exec(stat).first()