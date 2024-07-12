from peewee import Model, SqliteDatabase, CharField, IntegerField, ForeignKeyField, DateField, FloatField


db = SqliteDatabase('database/users.db')


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    name = CharField()
    user_id = IntegerField(unique=True)
    position = IntegerField(default=1)


class History(BaseModel):
    user = ForeignKeyField(User, backref='history')
    date = DateField()


class Search(BaseModel):
    history = ForeignKeyField(History, backref='searches')
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
    genres = CharField()
    age = IntegerField()
    poster = CharField()
    
    def __str__(self):
       return '<b>{name}</b>\n<i>{description}</i>\nРейтинг: <b>{rating}</b>\
            \nГод: {year}\n{genres}\n<u>{age}+</u>'.format(
            name=self.name,
            description=self.description,
            rating=self.rating,
            year=self.year,
            genres=self.genres,
            age=self.age
        )
    

db.create_tables(BaseModel.__subclasses__())

users: dict[int, dict[str, str | int]] = {}
