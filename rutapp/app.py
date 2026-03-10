from flask import Flask, render_template, request, redirect, url_for,session
import mysql.connector

app = Flask(__name__)
app.secret_key = "rutapp_secreto"

#Esta es la conexión a la base de datos MySQL

conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Cristina+-2026",
    database="rutapp_bd"
)

# Página de login
@app.route('/')
def login():
    return render_template('login.html')

#Usuario
@app.route('/usuarios')
def usuarios():

    if 'usuario' not in session:
        return redirect(url_for('login'))
    
    if session['rol'] !=1:
        return "Acceso no autorizado"
    
    cursor = conexion.cursor(dictionary=True)

    consulta = """ 
    SELECT id_usuario,
       nombre_usuario,
       nombres_y_apellidos,
       correo,
       telefono,
       id_rol
    FROM usuario
    """

    cursor.execute(consulta)
    lista_usuarios = cursor.fetchall()

    return render_template('usuarios.html', usuarios = lista_usuarios)
 

# Panel administrador
@app.route('/admin')
def administrador():

    if 'usuario' not in session:
        return redirect(url_for('login')) #Si no hay sesión iniciada regresa al login
    
    if session['rol'] != 1:
        return "Acceso no autorizado"
    
    return render_template('admin.html')

# Panel conductor
@app.route('/conductor')
def conductor():

    if 'usuario' not in session:
        return redirect(url_for('login'))

    if session['rol'] != 2:
        return "Acceso no autorizado"
        
    return render_template('conductor.html')

# Panel padres
@app.route('/padres')
def padres():

    if 'usuario' not in session:
        return redirect(url_for('login'))
    
    if session['rol'] != 3:
        return "Acceso no autorizado"
    
    return render_template('padres.html')

@app.route('/validar_login',methods=['POST'])
def valida_login():

    correo = request.form['correo']
    password = request.form['password']

    cursor = conexion.cursor(dictionary=True)

    consulta = """
    SELECT *
    FROM usuario
    WHERE correo=%s AND hash_password = md5(%s)
    """

    cursor.execute(consulta,(correo,password))
    usuario = cursor.fetchone()

    if usuario:
        id_rol = usuario[6] # Esta es la posición en donde esta el usuario en la tabla BD

        session['usuario'] = usuario[0]
        session['rol'] = id_rol

        if id_rol == 1:
            return redirect(url_for('administrador'))
        elif id_rol == 2:
            return redirect(url_for('conductor'))
        elif id_rol == 3:
            return redirect(url_for('padres'))
        else:
            return "Rol no reconocido"

    else:
        return "Usuario o contraseña incorrectos"
    
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
