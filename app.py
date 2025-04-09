from flask import Flask
from config import Config
from utils import mongo, jwt
from routes.auth import auth_bp
from routes.business import business_bp

app = Flask(__name__)
app.config.from_object(Config)

# Initialize utilities
mongo.init_app(app)
jwt.init_app(app)

# Register blueprints
app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(business_bp, url_prefix="/api")

if __name__ == "__main__":
    app.run(debug=True)
