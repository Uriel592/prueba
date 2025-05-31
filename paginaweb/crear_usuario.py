from flask import Flask
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash

app = Flask(__name__)

#  conexión a MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Ghost592'  
app.config['MYSQL_DB'] = 'flaskcontacts'

mysql = MySQL(app)

@app.route('/')
def crear_admin():
    try:
        cur = mysql.connection.cursor()
        
        cur.execute("SELECT * FROM contacts WHERE email = %s", ('admin@cesba.com',))
        if cur.fetchone():
            return 'El usuario admin@cesba.com ya existe.'

        password_hash = generate_password_hash('admin123')
        cur.execute(
            'INSERT INTO contacts (fullname, email, phone, password) VALUES (%s, %s, %s, %s)',
            ('Admin', 'admin@cesba.com', '0000000000', password_hash)
        )
        mysql.connection.commit()
        return 'Usuario administrador creado con éxito.'
    except Exception as e:
        return f'Error: {e}'

if __name__ == '__main__':
    app.run(debug=True, port=5001)  