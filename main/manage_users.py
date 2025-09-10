from manage_database import User
from main import db

def add_user(un, pswd, jsonfl):
    new_user = User(un=un, pswd=pswd, jsonfl=jsonfl)
    db.session.add(new_user)
    db.session.commit()

def delete_user(user_id):
        user_to_delete = User.query.get_or_404(user_id)
        try:
            db.session.delete(user_to_delete)
            db.session.commit()
        except Exception:
            db.session.rollback()