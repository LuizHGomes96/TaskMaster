from app import * #type: ignore
from datetime import datetime

class Tasks(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    task = db.Column(db.String(200), nullable = False)
    description = db.Column(db.String(2000))
    status = db.Column(db.Boolean, default = False)
    date_added = db.Column(db.DateTime, default = datetime.utcnow)
    order = db.Column(db.Integer, nullable = False, unique = True)