# JSON RETURNS AND REQUEST HANDLING
from numpy import tile
from flask import Flask, jsonify, request, render_template, sessions
# CORS 
from flask_cors import CORS
# ENVIRONMENT VARIABLES AND CONEXION WITH DB TROUGH psycopg2 DRIVER
import os 


def register_routes(app, db):
    CORS(app, resources={
        r"/*": {
            "origins": ["http://localhost:3000", "http://localhost:5000"],
            "methods": ["GET", "POST", "OPTIONS"],
            "allow_headers": ["Content-Type"]
        }
    })

