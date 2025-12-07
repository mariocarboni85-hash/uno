"""
User Management API Service

Generated: 2025-11-26 09:00:17
"""

from flask import Flask, request, jsonify
from typing import Dict, List, Optional
import sqlite3
from datetime import datetime

class UserDatabase:
    """
    Database operations for user management.
    
    Attributes:
        db_path (str): Database file path
    """
    
    def __init__(self, db_path: str):
        """Initialize UserDatabase."""
        self.db_path = db_path


    def create_user(self: , username: str, email: str) -> int:
        """
        Create new user.
        
        Args:
            self (): 
            username (str): 
            email (str): 
        
        Returns:
            int
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO users (username, email, created_at) VALUES (?, ?, ?)',
            (username, email, datetime.now().isoformat())
        )
        user_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return user_id

    def get_user(self: , user_id: int) -> Optional[Dict]:
        """
        Get user by ID.
        
        Args:
            self (): 
            user_id (int): 
        
        Returns:
            Optional[Dict]
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return {'id': row[0], 'username': row[1], 'email': row[2]}
        return None



if __name__ == '__main__':

    # Initialize Flask app
    app = Flask(__name__)
    db = UserDatabase('users.db')

    @app.route('/users', methods=['POST'])
    def create_user():
        data = request.json
        user_id = db.create_user(data['username'], data['email'])
        return jsonify({'id': user_id, 'status': 'created'}), 201

    @app.route('/users/<int:user_id>', methods=['GET'])
    def get_user(user_id):
        user = db.get_user(user_id)
        if user:
            return jsonify(user)
        return jsonify({'error': 'User not found'}), 404

    # Run server
    app.run(host='0.0.0.0', port=5000, debug=True)