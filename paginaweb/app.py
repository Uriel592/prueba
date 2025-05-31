from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Configuración de la base de datos
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Ghost592'
app.config['MYSQL_DB'] = 'flaskcontacts'
mysql = MySQL(app)

app.secret_key = 'Ghost592'

# Ruta principal
@app.route('/')
def home():
    if 'usuario' in session:
        email = session['usuario']
        if email == 'admin@cesba.com':
            # Admin ve lista de contactos
            cur = mysql.connection.cursor()
            cur.execute('SELECT * FROM contacts')
            data = cur.fetchall()
            return render_template('index.html', contacts=data)
        else:
            return render_template('bienvenida.html', email=email)
    else:
        return redirect(url_for('login'))

# Agregar contacto
@app.route('/add_contact', methods=['POST'])
def add_contact():
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO contacts (fullname, phone, email, password) VALUES (%s, %s, %s, %s)",
                    (fullname, phone, email, password))
        mysql.connection.commit()
        flash('Contacto agregado correctamente', 'success')
        return redirect(url_for('home'))

# Editar contacto
@app.route('/edit/<id>')
def get_contact(id):
    if 'usuario' not in session:
        return redirect(url_for('login'))
    
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts WHERE id = %s', (id,))
    data = cur.fetchall()
    return render_template('edit-contact.html', contact=data[0])

# Actualizar contacto (con cambio opcional de contraseña)
@app.route('/update/<id>', methods=['POST'])
def update_contact(id):
    if 'usuario' not in session:
        return redirect(url_for('login'))

    fullname = request.form['fullname']
    phone = request.form['phone']
    email = request.form['email']
    password = request.form['password']

    cur = mysql.connection.cursor()

    if password:
        hashed_password = generate_password_hash(password)
        cur.execute("""
            UPDATE contacts
            SET fullname = %s,
                email = %s,
                phone = %s,
                password = %s
            WHERE id = %s
        """, (fullname, email, phone, hashed_password, id))
    else:
        cur.execute("""
            UPDATE contacts
            SET fullname = %s,
                email = %s,
                phone = %s
            WHERE id = %s
        """, (fullname, email, phone, id))

    mysql.connection.commit()
    flash('Contacto actualizado correctamente', 'info')
    return redirect(url_for('home'))

# Eliminar contacto
@app.route('/delete/<string:id>')
def delete_contact(id):
    if 'usuario' not in session:
        return redirect(url_for('login'))

    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM contacts WHERE id = %s', (id,))
    mysql.connection.commit()
    flash('Contacto eliminado exitosamente', 'warning')
    return redirect(url_for('home'))

# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['usuario']
        password = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute('SELECT email, password FROM contacts WHERE email = %s', (email,))
        user = cur.fetchone()

        if user and check_password_hash(user[1], password):
            session['usuario'] = user[0]
            flash('Inicio de sesión exitoso', 'success')
            return redirect(url_for('home'))
        else:
            flash('Credenciales incorrectas', 'danger')
            return redirect(url_for('login'))

    return render_template('login.html')

# Logout
@app.route('/logout')
def logout():
    session.pop('usuario', None)
    flash('Sesión cerrada correctamente', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=3000, debug=True)
