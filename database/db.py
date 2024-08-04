from peewee import Model, SqliteDatabase, CharField, IntegerField, ForeignKeyField, FloatField, DateTimeField


db = SqliteDatabase('database/users.db')


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    name = CharField()
    user_id = IntegerField(unique=True)
    pg_position = IntegerField(default=0)


class History(BaseModel):
    user = ForeignKeyField(User, backref='histories')
    date = DateTimeField()
    command = CharField()
    limit = IntegerField(default=1)


class Movie(BaseModel):
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
    

class HistoryMovie(BaseModel):
    history = ForeignKeyField(History)
    movie = ForeignKeyField(Movie)


db.create_tables(BaseModel.__subclasses__())
