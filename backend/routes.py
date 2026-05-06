# JSON RETURNS AND REQUEST HANDLING
from numpy import tile
import requests
from flask import Flask, jsonify, request, render_template, sessions
# CORS 
from flask_cors import CORS
# ENVIRONMENT VARIABLES AND CONEXION WITH DB TROUGH psycopg2 DRIVER
import os 

def register_routes(app,db):
    CORS(app, resources={
        r"/*": {
            "origins": ["http://localhost:3000", "http://localhost:5000"],
            "methods": ["GET", "POST", "OPTIONS"],
            "allow_headers": ["Content-Type"]
        }
    })

    '''
    {
    'muestra1': 
        {
        'varianza': '1', 
        'tamano': '1'
        }, 
    'muestra2': 
        {
        'varianza': '1', 
        'tamano': '1'
        }
    }
    '''

    @app.route('/data',methods=['POST'])
    def test():
        if request.method == 'POST':
            data = request.json
            print(data)
            return jsonify({'response':'ok'}),200
        print("No data")
        return 500

