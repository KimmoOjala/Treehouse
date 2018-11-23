from flask_wtf import Form
from wtforms import (StringField, PasswordField, DateField, IntegerField,
                     TextField, RadioField, SelectField)
from wtforms.validators import (DataRequired, Regexp, ValidationError, 
                                Length, EqualTo)
from models import User, Entry, Tag, EntryTag


def name_exists(form, field):
    '''Checks if user name already exists.'''
    if User.select().where(User.user_name == field.data).exists():
        raise ValidationError('User with that name already exists.')

def tag_exists(form, field):
    '''Checks if tag already exists.'''
    if Tag.select().where(Tag.tag == field.data).exists():
        raise ValidationError('This tag already exists.')


class LoginForm(Form):
    user_name = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])


class EntryForm(Form):
    '''Form for adding a new Entry or editing an Entry.'''
    title = StringField('Title', validators=[DataRequired()])
    date = DateField('Date (yyyy-mm-dd)', validators=[DataRequired()], format='%Y-%m-%d')
    time_spent = IntegerField('Time spent (min.)', validators=[DataRequired()])
    what_i_learned = TextField('What I learned', validators=[DataRequired()])
    resources = TextField('Resources', validators=[DataRequired()])


class TagForm(Form):
    '''Form for adding a Tag to an Entry / removing a Tag from an Entry.'''
    selection_field = SelectField('', validators=[DataRequired()])

    def set_add_choices(self):
        '''Sets choices of tags (which can be added to entry)
        to selection_field. Needs to be called after form 
        is initialized and before add_tag.html is rendered.'''
        tag_list = Tag.select()
        tag_choices = []
        for tag in tag_list:
            tag_choices.append((tag.tag, tag.tag))
        self.selection_field.choices = tag_choices

    def set_remove_choices(self, entry_id):
        '''Sets choices of tags (which can be removed from an entry)
        to selection_field. Needs to be called after form 
        is initialized and before remove_tag.html is rendered.'''
        tag_list = Tag.select().join(EntryTag).join(Entry).where(Entry.pk == entry_id)
        tag_choices = []
        for tag in tag_list:
            tag_choices.append((tag.tag, tag.tag))
        self.selection_field.choices = tag_choices


class CreateTagForm(Form):
    '''Form for creating a new Tag.'''
    tag = StringField('Tag', validators=[DataRequired(), tag_exists])


class DeleteForm(Form):
    '''Form for deleting an Entry.'''
    confirm = RadioField('Label', choices=[('Yes','Yes'),('No', 'No')])
