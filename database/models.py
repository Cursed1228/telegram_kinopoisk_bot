from peewee import (
    AutoField,
    BooleanField,
    CharField,
    DateField,
    ForeignKeyField,
    IntegerField,
    Model,
    SqliteDatabase,
)
from config_data.config import DB_PATH, DATE_FORMAT

db = SqliteDatabase(DB_PATH)


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    user_id = IntegerField(primary_key=True)
    username = CharField()
    first_name = CharField()
    last_name = CharField(null=True)


class History(BaseModel):
    movie_id = AutoField()
    user_id = ForeignKeyField(User, backref="history")
    result = CharField()
    date = DateField()
    is_watching = BooleanField(default=False)


def create_models():
    db.create_tables(BaseModel.__subclasses__())

