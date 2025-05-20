from models import db

class Users(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())

    def __repr__(self):
        return f"<User {self.email}>"

    def to_dict(self):
        return {
            "user_id": self.id,
            "user_name": self.name,
            "user_email": self.email,
            "user_created_at": self.created_at
        }
    
    def email_exists(email):
        return Users.query.filter_by(email=email).first() is not None