import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import database

class ModelUser:
    @staticmethod
    def login(username, password):
        conn = database.get_connection()
        cursor = conn.cursor()
        
        # Menggunakan kolom 'nama' sesuai database mentor
        cursor.execute("""
            SELECT id, username, role, nama 
            FROM users 
            WHERE username = ? AND password = ?
        """, (username, password))
        
        user = cursor.fetchone()
        conn.close()
        if user:
            return dict(user)
        return None
