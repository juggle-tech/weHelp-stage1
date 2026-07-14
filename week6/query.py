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