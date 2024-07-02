from peewee import Model, SqliteDatabase, CharField, IntegerField, ForeignKeyField


db = SqliteDatabase('database/users.db')

class User(Model):
    name = CharField()
    user_id = IntegerField(primary_key=True)

    class Meta:
        database = db


class Search(Model):
    id_user = ForeignKeyField(User, backref='search')
    name = CharField()
    genre = CharField()
    limit = IntegerField()
    position = IntegerField()
    poster = CharField()
    rating = CharField()
    
    class Meta:
        database = db


class History(Model):
    search_id = ForeignKeyField(Search)

    class Meta:
        database = db
        

db.create_tables([User, Search, History])

users: dict[int, dict[str, str | int]] = {}