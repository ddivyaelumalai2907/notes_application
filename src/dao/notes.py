from operator import and_
from sqlalchemy import func
from operator import and_
from model import notes

def get_notes(connection):
    obj = connection.query(notes.Notes).all()
    data = []
    for row in obj:
        data.append({
            'title': row.note_title,
            'content': row.note_content
        })
    return data if data else "No data"


def add_notes(title,content,user_id,connection):

    obj = notes.Notes(note_title = title,note_content=content,user_id=user_id)
    connection.add(obj)
    connection.commit()

    return {
        'id': obj.note_id
    }


def update_note(note_id,connection,new_title = None,new_content = None):
    data = False
    obj = connection.query(notes.Notes).filter(notes.Notes.note_id == note_id).first()
    if obj is not None:
        if new_title is not None and new_title != obj.note_title :
            obj.note_title = new_title
            data = True
        if  new_content is not None and new_content != obj.note_content:
            obj.note_content = new_content
            data = True
        connection.commit()
    return data

def get_all_user_notes(user_id,connection):
    all_notes = []
    table_notes = connection.query(notes.Notes).filter(notes.Notes.user_id == user_id).all()
    for note in table_notes:
        all_notes.append({
            'note_id':note.note_id,
            'note_title':note.note_title,
            'note_content':note.note_content,
            'last_update':str(note.last_update)
        })
    return all_notes

def delete_note(note_id,connection):
    note = connection.query(notes.Notes).filter(note_id == note_id).first()
    if note:
        connection.delete(note)
        connection.commit()