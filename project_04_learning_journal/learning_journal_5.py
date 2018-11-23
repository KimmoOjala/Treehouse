from flask import (Flask, g, render_template, flash, redirect, url_for)
from flask_bcrypt import check_password_hash
from flask_login import (LoginManager, login_user, logout_user,
                             login_required, current_user) 
import forms
import models
from flask_login.utils import current_user

DEBUG = True
PORT = 8000
HOST = '127.0.0.1'

app = Flask(__name__)
app.secret_key = 'ssee456/&SDFV&/12sgffSCÖ=(/H'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(userid):
    try:
        return models.User.get(models.User.id == userid)
    except models.DoesNotExist:
        return None

@app.before_request
def before_request():
    '''Connect to the database before each request.'''
    g.db = models.DATABASE
    g.db.connect()
    g.user = current_user

@app.after_request
def after_request(response):
    """Close the database connection after each request."""
    g.db.close()
    return response

@app.route('/login', methods=('GET', 'POST'))
def log_in():
    form = forms.LoginForm()
    if form.validate_on_submit():
        try:
            user = models.User.get(models.User.user_name == form.user_name.data)
        except models.DoesNotExist:
            flash("Your username or password doesn't match!,", "error")
        else:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                flash("You have been logged in!", "sucess")
                return redirect(url_for('index'))
            else:
                flash("Your username or password doesn't match!", "error")
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def log_out():
    logout_user()
    flash("You've been logged out! Come back soon!", "success")
    return redirect(url_for('index'))

@app.route('/entries/add', methods=('GET', 'POST'))
@login_required
def new():
    '''View for adding a new entry.'''
    form = forms.EntryForm()
    if form.validate_on_submit():
        models.Entry.create(user=g.user.id,
                title=form.title.data.strip(),
                date=form.date.data,
                time_spent=form.time_spent.data,
                what_i_learned=form.what_i_learned.data.strip(),
                resources=form.resources.data.strip(),
        )
        flash("Entry posted!", "success")
        return redirect(url_for('entries'))
    return render_template('new.html', form=form)

@app.route('/entries/edit/<int:entry_id>/<slug>' , methods=('GET', 'POST'))
@login_required
def edit(entry_id, slug):
    '''View for editing an entry.'''
    entry = models.Entry.get(models.Entry.pk == entry_id)
    form = forms.EntryForm(obj=entry)
    form.populate_obj(entry)
    if form.validate_on_submit():
        entry.user=g.user.id
        entry.title=form.title.data.strip()
        entry.date=form.date.data
        entry.time_spent=form.time_spent.data
        entry.what_i_learned=form.what_i_learned.data.strip()
        entry.resources=form.resources.data.strip()
        entry.save()
        flash("Entry updated!", "success")
        return redirect(url_for('entries'))
    return render_template('edit.html', form=form)

@app.route('/entries/delete/<int:entry_id>/<slug>', methods=('GET', 'POST'))
@login_required
def delete(entry_id, slug):
    '''View for deleting an entry.'''
    entry = models.Entry.get(models.Entry.pk == entry_id)
    form = forms.DeleteForm()
    if form.validate_on_submit():
        if "Yes" in form.confirm.data:
            entry.delete_instance()
            flash("Entry deleted!", "success")
        else:
            flash("Entry was not deleted", "success")
        return redirect(url_for('entries'))
    return render_template('delete.html', form=form)

@app.route('/entries/details/<int:entry_id>/<slug>', strict_slashes=False)
def detail(entry_id, slug):
    '''View for showing the details of an entry.'''
    entry = models.Entry.get(models.Entry.pk == entry_id)
    try:
        entry_tags = (models.Tag.select()
                .join(models.EntryTag)
                .where(models.EntryTag.tagged_entry == entry.pk)
                .order_by(models.Tag.tag))
    except models.DoesNotExist:
        entry_tags = []
    return render_template('detail.html', entry=entry, entry_tags=entry_tags)    
    
@app.route('/entries/add_tag/<int:entry_id>/<slug>', methods=('GET', 'POST'))
@login_required
def add_tag(entry_id, slug):
    '''View for adding a tag to an entry.'''
    form = forms.TagForm()
    form.set_add_choices()
    entry = models.Entry.get(models.Entry.pk == entry_id)
    if form.validate_on_submit():
        chosen_tag = models.Tag.get(models.Tag.tag == form.selection_field.data)
        if models.EntryTag.select().where(
                                          (models.EntryTag.tagged_entry == entry.pk) & 
                                          (models.EntryTag.tag == chosen_tag.id)).exists():
            flash("Entry was already tagged with this tag. No tag added.", "error")
        else:
            models.EntryTag.create(tagged_entry=entry.pk, tag=chosen_tag.id)
            flash("Yay, Tag added!", "success")
        return redirect(url_for('detail', entry_id=entry_id, slug=slug))
    return render_template('add_tag.html', form=form)

@app.route('/entries/remove_tag/<int:entry_id>/<slug>', methods=('GET', 'POST'))
@login_required
def remove_tag(entry_id, slug):
    '''View for removing a from an entry.'''
    form = forms.TagForm()
    form.set_remove_choices(entry_id)
    entry = models.Entry.get(models.Entry.pk == entry_id)
    if form.validate_on_submit():
        chosen_tag = models.Tag.get(models.Tag.tag == form.selection_field.data)
        try:
            models.EntryTag.get(tagged_entry=entry.pk, tag=chosen_tag.id).delete_instance()
            flash("Tag removed!", "success")
        except models.IntegrityError:
            pass
        return redirect(url_for('detail', entry_id=entry_id, slug=slug))
    return render_template('remove_tag.html', form=form)

@app.route('/entries/create_tag', methods=('GET', 'POST'))
@login_required
def create_tag():
    '''View for creating a new tag.'''
    form = forms.CreateTagForm()
    if form.validate_on_submit():
        models.Tag.create(tag=form.tag.data)
        flash("Tag created!", "success")
        return redirect(url_for('entries'))
    return render_template('create_tag.html', form=form)

@app.route('/entries/edit_tag/<int:tag_id>/<slug>', methods=('GET', 'POST'))
@login_required
def edit_tag(tag_id, slug):
    '''View for editing a tag.'''   
    tag = models.Tag.get(models.Tag.id == tag_id)
    tag_name = tag.tag
    tag = (models.Tag.select().where(models.Tag.tag==tag_name)
                .join(models.EntryTag)
                .join(models.Entry)
                .get())
    form = forms.CreateTagForm(obj=tag)
    form.populate_obj(tag)
    if form.validate_on_submit():
        tag.tag = form.tag.data.strip()
        tag.save()
        flash("Tag updated!", "success")
        return redirect(url_for('entries'))
    return render_template('edit_tag.html', form=form)

@app.route('/entries/tags')
def all_tags():
    '''View for listing used tags.'''
    try:
        tag_list = (models.Tag.select()
                .join(models.EntryTag)
                .join(models.Entry)
                .order_by(models.Tag.tag))
    except models.Tag.DoesNotExist:
        tag_list = []   
    return render_template('all_tags.html', tag_list=tag_list)    

@app.route('/entries/tags/<tag_id>/<slug>')
def entries_same_tag(tag_id, slug):
    '''View for querying entries with the same tag.'''
    tag = models.Tag.get(models.Tag.id == tag_id)
    tag_name = tag.tag
    tagged_entries = (models.Entry.select()
                      .join(models.EntryTag)
                      .join(models.Tag)
                      .where(models.Tag.tag == tag_name)
                      .order_by(models.Entry.date.desc())
                      )
    return render_template('entries_same_tag.html', tag_name=tag_name, tagged_entries=tagged_entries)  

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/entries')
def entries():
    '''View for listing entries.'''
    entries= models.Entry.select()
    return render_template('entries.html', entries=entries)

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


if __name__ == '__main__':
    models.initialize()
    try:
        models.User.create_user(
            user_name='test_user',
            password='password'
        ) 
    except ValueError:
        pass       
    app.run(debug=DEBUG, host=HOST, port=PORT)
