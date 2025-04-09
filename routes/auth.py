from flask import Blueprint, request, jsonify
from utils import mongo
from flask_jwt_extended import create_access_token
import bcrypt
from models import get_user_by_email, create_user

# create the flask app blueprint so you can use it elsewhere. just like here
auth_bp = Blueprint("auth", __name__)

# register user
@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.json
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    try:
        # check if user with email exists
        if get_user_by_email(email):
            return jsonify({"message": "User already exists"}), 400

        # hash the password using bycrypt package
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        user = create_user(username, email, hashed_password)

        # Convert ObjectId to string for JSON serialization
        user["_id"] = str(user["_id"])

        return jsonify({"message": "User registered successfully", "data": user}), 201
    
    except:

        return jsonify({"message": "Cannot register user at the moment"}), 500


# login user
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    try:
        user = get_user_by_email(email)
        if not user or not bcrypt.checkpw(password.encode("utf-8"), user["password"]):
            return jsonify({"error": "Invalid credentials"}), 401

        # create authentication using jwt
        access_token = create_access_token(identity=email)
        return jsonify({"message": "Login Successful", "data": user, "access_token": access_token}), 200
    
    except:
        return jsonify({"message": "error processing request"}), 200