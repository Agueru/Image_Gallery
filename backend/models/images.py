from models import db

class Images(db.Model):
    __tablename__ = "images"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    url = db.Column(db.String(255), nullable=False)
    uploaded_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())

    def __repr__(self):
        return f"<Image {self.name}>"

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.name,
            "url": f"http://localhost:5000/static/{self.url}",
            "uploaded_at": self.uploaded_at
        }