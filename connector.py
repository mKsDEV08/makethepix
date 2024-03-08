from sqlalchemy import create_engine, Column, String, Integer, Double, Text
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from configparser import ConfigParser

Base = declarative_base()

try:
    cfg_obj = ConfigParser()
    cfg_obj.read(f"{os.getcwd()}/config.cfg")

    database = cfg_obj["database-config"]

except KeyError:
    cfg_obj = ConfigParser()
    cfg_obj.read(f"{os.getcwd()}/../config.cfg")

    database = cfg_obj["database-config"]

class User(Base):
    __tablename__ = "users"

    uid = Column("id", Integer, primary_key=True, autoincrement=True)
    username = Column("username", String, nullable=False)
    password_hash = Column("password_hash", String, nullable=False)
    alert_id = Column("alert_id", String, nullable=False)
    balance = Column("balance", Double, nullable=False)
    lang_choose = Column("lang_choose", String, default='com.br')
    pix_key = Column("pix_key", Text, nullable=False)
    pitch_choose = Column("pitch_choose", Double, nullable=False)

    def __init__(self, username, password_hash, alert_id, balance, pix_key, pitch_choose):
        self.username = username
        self.password_hash = password_hash
        self.alert_id = alert_id
        self.balance = balance
        self.pix_key = pix_key
        self.pitch_choose = pitch_choose

    def __repr__(self):
        return f"({self.uid}) {self.username} | {self.alert_id}"
    

class Message(Base):
    __tablename__ = "messages"

    uid = Column("id", Integer, primary_key=True, autoincrement=True)
    message = Column("message", String, nullable=False)
    sender_name = Column("sender_name", String, nullable=False)
    status = Column("status", String, default='pending')
    value = Column("value", Double, nullable=False)
    receiver_alert_id = Column("receiver_alert_id", String, nullable=False)

    def __init__(self, message, sender_name, value, receiver_alert_id):

        self.message = message
        self.sender_name = sender_name
        self.value = value
        self.receiver_alert_id = receiver_alert_id

    def __repr__(self):
        return f"({self.uid}) {self.message} | {self.sender_name} | {self.value}"

engine = create_engine(f'mysql+mysqlconnector://{database["username"]}:{database["password"]}@{database["host"]}/{database["name"]}')
Base.metadata.create_all(bind=engine)

Database = sessionmaker(bind=engine)
db = Database()