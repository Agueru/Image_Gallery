from flask import Flask, request, jsonify, send_file
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, Users, UsersImages, Images, TokenBlocklist

from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity, get_jwt
from flask_cors import CORS

from datetime import timedelta, datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///sqlite3.db"
ACCESS_EXPIRES = timedelta(days=1)
app.config["JWT_SECRET_KEY"] = "super-secret"  
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = ACCESS_EXPIRES
jwt = JWTManager(app)
db.init_app(app)


CORS(app, resources=r'/api/*', origins='*')

def validate_response(fields, form):
    """
    Validate the response from the client.
    :param fields: list of fields to validate
    :param form: the form to validate
    :return: a dictionary of errors
    """
    errors = {}
    for field in fields:
        if not form.get(field):
            errors[field] = f"{field} is required."
    return errors

def hash_password(password):
    """
    Hash the password.
    :param password: the password to hash
    :return: a hashed password
    """
    return generate_password_hash(password)

def is_password_valid(password, hash):
    """
    Verify the password.
    :param password: the password to verify
    :param hash: the hash to verify
    :return: a boolean
    """
    return check_password_hash(hash, password)

@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload: dict) -> bool:
    jti = jwt_payload["jti"]
    token = db.session.query(TokenBlocklist.id).filter_by(jti=jti).scalar()

    return token is not None

@app.route("/api/v1/login", methods=["POST"])
def login():
    """
    Login route.
    :return: a json response
    """
    if request.method == "POST":
        errors = validate_response(("email", "password"), request.form)

        if errors:
            return jsonify(errors), 400

        email = request.form.get("email")
        password = request.form.get("password")

        user = Users.query.filter_by(email=email).first()

        if not user or not is_password_valid(password, user.password):
            return jsonify({"error": "Invalid username or password"}), 404

        access_token = create_access_token(identity=email)

        return jsonify({
            "user_id": user.id,
            "email": email,
            "name": user.name,
            "access_token": access_token
        }), 200


@app.route("/api/v1/signup", methods=["POST"])
def signup():
    """
    Signup route.
    :return: a json response
    """
    if request.method == "POST":
        errors = validate_response(
            ("email", "password", "name"), request.form)

        if errors:
            return jsonify(errors), 400

        email = request.form.get("email")

        if Users.email_exists(email):
            return jsonify({"error": "Email already exists"}), 400

        password = request.form.get("password")
        if len(password) < 5:
            return jsonify({"error": "Password must be at least 5 characters"}), 400
        
        name = request.form.get("name")

        password = hash_password(password)

        user = Users(email=email, password=password, name=name)
        db.session.add(user)
        db.session.commit()

        return jsonify({"user_id": user.id ,"email": email, "name": name}), 201


@app.route("/api/v1/logout", methods=["POST"])
@jwt_required()
def logout():
    """
    Logout route.
    :return: a json response
    """
    if request.method == "POST":
        jti = get_jwt()["jti"]
        now = datetime.now()
        db.session.add(TokenBlocklist(jti=jti, created_at=now))
        db.session.commit()
        return jsonify({"message": "Successfully logged out"}), 200


@app.route("/api/v1/users/<int:user_id>/images", methods=["GET"])
def get_images(user_id):
    """
    Get images route.
    :param user_id: the user id
    :return: a json response
    """
    if request.method == "GET":
        user = Users.query.filter_by(id=user_id).first()

        if not user:
            return jsonify({"error": "User not found"}), 404

        images = UsersImages.query.filter_by(user_id=user_id).all()

        fetched_images = [Images.query.get(image.image_id) for image in images]

        return jsonify([{**image.to_dict(), "user_id":user.id} for image in fetched_images]), 200

@app.route("/api/v1/images", methods=["GET"])
def get_all_images():
    """
    Get images route.
    :param user_id: the user id
    :return: a json response
    """
    if request.method == "GET":
        images_mapping = UsersImages.query.all()

        fetched_images = [{**Images.query.get(image.image_id).to_dict(), **Users.query.get(image.user_id).to_dict()} for image in images_mapping]

        return jsonify(fetched_images), 200

@app.route("/api/v1/images/upload", methods=["POST"])
@jwt_required()
def upload_images():
    """
    Upload images route.
    :return: a json response
    """
    if request.method == "POST":
        current_user = get_jwt_identity()

        if not current_user:
            return jsonify({"error": "Unauthorized"}), 401

        user = Users.query.filter_by(email=current_user).first()
        if not user:
            return jsonify({"error": "User not found"}), 404

        image = request.files.get("image")
        if not image:
            return jsonify({"error": "Image is required"}), 400
        
        title = request.form.get("title")
        if not title:
            return jsonify({"error": "Title is required"}), 400
        
        image_name = title
        image_url = f"images/{image.filename}"
        image.save(image_url)

        image_entry = Images(name=image_name, url=image_url)
        db.session.add(image_entry)
        db.session.commit()


        user_image = UsersImages(user_id=user.id, image_id=image_entry.id)
        db.session.add(user_image)
        db.session.commit()


        return jsonify({"message": "Image uploaded successfully"}), 201


@app.route('/static/images/<path:filename>', methods=['GET'])
def serve_image(filename):
    
    image_directory = 'images/'

    
    return send_file(image_directory + filename, mimetype='image/*')

@app.route("/api/v1/users/<int:user_id>/images/<int:image_id>", methods=["DELETE"])
@jwt_required()
def delete_images(user_id, image_id):
    """
    Upload images route.
    :return: a json response
    """
    if request.method == "DELETE":
        current_user = get_jwt_identity()

        if not current_user:
            return jsonify({"error": "Unauthorized"}), 401

        user = Users.query.filter_by(email=current_user).first()
        if not user:
            return jsonify({"error": "User not found"}), 404

        
        image = Images.query.get(image_id)
        if not image:
            return jsonify({"error": "Image not found"}), 404

        db.session.delete(image)
        db.session.commit()

        user_image_mapping = UsersImages.query.filter_by(user_id=user_id, image_id=image_id).first()
        if user_image_mapping:
            db.session.delete(user_image_mapping)
            db.session.commit()

        return jsonify({"message": "Image deleted successfully"}), 204
