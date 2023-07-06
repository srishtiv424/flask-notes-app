from flask import Flask, Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
import json

views = Blueprint('views', __name__)


@views.route('/', methods = ['POST','GET'])
@login_required
def home():
    if request.method == 'POST':
        data = request.form.get('note')

        if len(data) < 1 :
            flash("The note is empty cannot submit", category= 'error')
        else:
            new_note = Note(data = data , user_id = current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash("Note successfully added" , category= 'success')
    
    return render_template("home.html" , user = current_user)


@views.route('/delete-note', methods=['POST'])
def delete_note():  
    note = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})
