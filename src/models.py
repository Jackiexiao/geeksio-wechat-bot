from enum import Enum

from sqlmodel import Field, Session, SQLModel, create_engine


class MessageType(int, Enum):
    Unknown = 0  # Unknown = 0
    Attachment = 1  # Attach(6)
    Audio = 2  # Audio(1), Voice(34)
    Contact = 3  # ShareCard(42)
    ChatHistory = 4  # ChatHistory(19)
    Emoticon = 5  # Sticker: Emoticon(15), Emoticon(47)
    Image = 6  # Img(2), Image(3)
    Text = 7  # Text(1)
    Location = 8  # Location(48)
    MiniProgram = 9  # MiniProgram(33)
    GroupNote = 10  # GroupNote(53)
    Transfer = 11  # Transfers(2000)
    RedEnvelope = 12  # RedEnvelopes(2001)
    Recalled = 13  # Recalled(10002)
    Url = 14  # Url(5)
    Video = 15  # Video(4), Video(43)
    Post = 16  # Moment, Channel, Tweet, etc


# 创建一个新的SQLModel模型，用于存储消息
class Message(SQLModel, table=True):
    id: str = Field(primary_key=True)
    timestamp: int
    type: int  # MessageType
    text: str
    filePath: str
    talkerId: str
    talkerName: str
    token: str
    quoteId: str


# 创建数据库引擎
engine = create_engine("sqlite:///database.db")


def get_session():
    with Session(engine) as session:
        yield session


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


if __name__ == "__main__":
    create_db_and_tables()
