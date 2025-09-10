from main import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    un = db.Column(db.String(30), nullable=False, primary_key=False)
    pswd = db.Column(db.String(50), nullable=False, primary_key=False)
    jsonfl = db.Column(db.String(75), nullable=False, primary_key=False)
