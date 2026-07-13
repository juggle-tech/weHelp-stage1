from sqlmodel import select
from models import Member, Message

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