from models import db

class UsersImages(db.Model):
    __tablename__ = "users_images"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    image_id = db.Column(db.Integer, db.ForeignKey("images.id"))

    def __repr__(self):
        return f"<UsersImages {self.user_id} {self.image_id}>"

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "image_id": self.image_id
        }