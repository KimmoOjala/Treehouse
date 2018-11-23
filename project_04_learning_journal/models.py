import datetime

from flask_bcrypt import generate_password_hash
from flask_login import UserMixin
from peewee import *
from slugify import slugify

DATABASE = SqliteDatabase('learning_journal.db', threadlocals=True)


class BaseModel(UserMixin, Model):

    class Meta:
        database = DATABASE

class User(BaseModel):
    '''Class with user data and functionality to create a new user.'''
    user_name = CharField(unique=True)
    password = CharField(max_length=100)

    def get_entries(self):
        return Entry.select().where(Entry.user == self)

    @classmethod
    def create_user(cls, user_name, password):
        try:
            with DATABASE.transaction():
                cls.create(
                    user_name=user_name,
                    password=generate_password_hash(password)
                )
        except IntegrityError:
            raise ValueError("Username already exists")


class Entry(BaseModel):
    '''Class with Entry data.'''
    pk = PrimaryKeyField()
    user = ForeignKeyField(
        rel_model=User,
        related_name='entries'
    )
    title = CharField(max_length=50)
    date = DateTimeField()
    time_spent = IntegerField()
    what_i_learned = TextField()
    resources = TextField()

    @property
    def slugified_title(self):
        return slugify(self.title)


class Tag(BaseModel):
    '''Class with Tag data.'''
    tag = CharField(unique=True)

    @property
    def slugified_tag(self):
        return slugify(self.tag)


class EntryTag(BaseModel):
    '''Class used to create one or multiple tags per Entry.'''
    tagged_entry = ForeignKeyField(Entry, related_name='tagged_entries')
    tag = ForeignKeyField(Tag, related_name='tags')

    
def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Entry, Tag, EntryTag], safe=True)
    DATABASE.close()
