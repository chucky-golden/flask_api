from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils import mongo
from bson import ObjectId
from models import create_businesses, get_all_business, get_business_by_id, update_a_business, delete_a_business

# create the flask app blueprint so you can use it elsewhere. just like here
business_bp = Blueprint("business", __name__)


# create business route
@business_bp.route("/businesses", methods=["POST"])
@jwt_required()
def create_business():
    data = request.json
    name = data.get("name")
    location = data.get("location")
    category = data.get("category")
    phone = data.get("phone")
    description = data.get("description")
    owner = get_jwt_identity()

    try:
        busines = create_businesses(
            name,
            owner,
            location,
            category,
            phone,
            description,
        )

        return jsonify({"message": "Business created", "data": busines}), 201
    except:
        return jsonify({"message": "Cannot create business at this moment"}), 500


# get all businesses
@business_bp.route("/businesses", methods=["GET"])
def get_all_businesses():
    businesses = get_all_business()
    return jsonify(businesses), 200


# get a specific business using its id 
@business_bp.route("/businesses/<business_id>", methods=["GET"])
def get_business(business_id):
    business = get_business_by_id(business_id)
    if not business:
        return jsonify({"error": "Business not found"}), 404

    return jsonify(business), 200


# edit a specific business
@business_bp.route("/businesses/<business_id>", methods=["PUT"])
@jwt_required()
def update_business(business_id):
    data = request.json
    updated_data = {key: value for key, value in data.items() if value}

    try:
        result = update_a_business(business_id, updated_data)

        return jsonify({"message": "Business updated successfully", "data": result}), 200
    except:
        return jsonify({"message": "Error updating business"}), 500


# delete business
@business_bp.route("/businesses/<business_id>", methods=["DELETE"])
@jwt_required()
def delete_business(business_id):
    try:
        result = delete_a_business(business_id)
        if result.deleted_count == 0:
            return jsonify({"error": "Business not found"}), 404

        return jsonify({"message": "Business deleted successfully"}), 200
    except:
        return jsonify({"message": "Error processing request"}), 500