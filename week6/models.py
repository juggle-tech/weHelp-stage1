from datetime import datetime
from sqlalchemy import Column, Text, DateTime, ForeignKey, text
from sqlalchemy.dialects.mysql import INTEGER as MySQLInteger
from sqlmodel import SQLModel, Field

class Member(SQLModel, table=True):
    __tablename__ = "member"

    id: int | None = Field(
        default=None,
        sa_column=Column(MySQLInteger(unsigned=True), primary_key=True, autoincrement=True)
    )
    name: str = Field(max_length=254, nullable=False)
    email: str = Field(max_length=254, nullable=False)
    password: str = Field(max_length=254, nullable=False)
    follower_count: int| None = Field(
        default=None,
        sa_column=Column(MySQLInteger(unsigned=True), nullable=False, server_default="0")
    )
    time: datetime = Field(
        default=None,
        sa_column=Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    )


class Message(SQLModel, table=True):
    __tablename__ = "message"

    id: int | None = Field(
        default=None,
        sa_column=Column(MySQLInteger(unsigned=True), primary_key=True, autoincrement=True)
    )
    member_id: int = Field(
        sa_column=Column(MySQLInteger(unsigned=True), ForeignKey("member.id"), nullable=False)
    )
    content: str = Field(sa_column=Column(Text, nullable=False))
    like_count: int | None = Field(
        default=None,
        sa_column=Column(MySQLInteger(unsigned=True), nullable=False, server_default="0")
    )
    time: datetime = Field(
        default=None,
        sa_column=Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    )