from peewee import Model, SqliteDatabase, CharField, IntegerField, ForeignKeyField, DateField, FloatField


db = SqliteDatabase('database/users.db')

class BaseModel(Model):
    class Meta:
        database = db

class User(BaseModel):
    name = CharField()
    user_id = IntegerField(unique=True)
    position = IntegerField(default=0)


class Search(BaseModel):
    user = ForeignKeyField(User, backref='searches')
    name = CharField(null=True)
    genre = CharField(null=True)
    limit = IntegerField()
    rating = CharField(null=True)
    

class Movie(BaseModel):
    search = ForeignKeyField(Search, backref='movies')
    name = CharField()
    description = CharField()
    rating = FloatField()
    year = IntegerField()
    genre = CharField()
    age = IntegerField()
    poster = CharField()
    

class History(BaseModel):
    search = ForeignKeyField(Search)
    date = DateField()


db.create_tables([User, Search, History])

users: dict[int, dict[str, str | int]] = {}