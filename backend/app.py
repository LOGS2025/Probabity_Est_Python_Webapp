# app.py
from flask import Flask, render_template

def create_app():
    app = Flask(__name__)
    
    from routes import register_routes
    register_routes(app,None)

    return app

