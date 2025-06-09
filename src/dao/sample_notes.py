from model import sample_notes

def get_all_sample_notes(connection):
    obj = connection.query(sample_notes.Sample_notes).all()
    data = []
    for row in obj:
        data.append({
            'id':row.id,
            'title': row.title,
            'content': row.content
        })
    return data