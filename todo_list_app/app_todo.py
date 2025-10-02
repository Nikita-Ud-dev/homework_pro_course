from flask import Flask
from db_config import db
from routes import app as app_routes

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "not_event_good_key"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"
    db.init_app(app)
    app.register_blueprint(app_routes)

    with app.app_context():
        db.create_all()

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)