from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from study_timer import create_app

app = create_app()

if __name__ == "__main__":
    app.run()


