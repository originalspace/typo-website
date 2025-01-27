from flask import Blueprint, render_template, url_for, redirect, flash, request, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
import json

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("webapp.html")

@views.route('/homepage')
@login_required
def homepage():
    return render_template("homepage.html", user=current_user)

@views.route('/my_posts')
def myposts():
    return render_template("myposts.html", user=current_user)

@views.route('/new_paper', methods=['GET', 'POST'])
def newpaper():
    if request.method == 'POST':
        title = request.form.get('title')
        note = request.form.get('paper')

        if len(title) < 1:
            flash('Title is too short!', category='error')
        if len(note) < 1:
            flash('Paper is too short!', category='error')
        else:
            new_paper = Note(title=title, data=note, user_id=current_user.id)
            db.session.add(new_paper)
            db.session.commit()
            flash('Paper published!', category='success')
            return redirect(url_for('views.myposts'))

    return render_template('pages.html')

@views.route('/read')
def read():
    return render_template("read.html", user=current_user)

@views.route('/read_user')
def readuser():
    return render_template("readuser.html", user=current_user)

@views.route('/about_us')
def aboutus():
    return render_template("aboutus.html")

@views.route('/about_us_user')
def aboutususer():
    return render_template("aboutususer.html")

@views.route('/contact_us')
def contactus():
    return render_template("contact.html")

@views.route('/contact_us_user')
def contactususer():
    return render_template("contactuser.html")

@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
    
    return jsonify({})


