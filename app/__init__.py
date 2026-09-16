from flask import Flask

def create_app():
    
    app = Flask(__name__)

    from app.routes import bp as bp_routes
    app.register_blueprint(bp_routes)

    return app
