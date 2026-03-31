from flask import Flask, render_template, request, redirect, url_for,session
import mysql.connector

app = Flask(__name__)
app.secret_key = "rutapp_secreto"

#============================================
#Esta es la conexión a la base de datos MySQL
#============================================

conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="12345",
    database="rutapp_bd"
)

#============================================
#         RUTAS PROYECTO RUTAPP
#============================================

#============================================
# AUTENTICACIÓN - RESPONSABLE: CRISTINA SALAZAR
#============================================

#============================================
#   RUTA HOME
#============================================

@app.route('/') #Esta es la ruta principal
def inicio():
    return render_template('mod_admin/home.html')

@app.route('/login') #Esta es la ruta de login
def login():
    return render_template('mod_admin/login.html')

#=========Ruta Usuarios=========

@app.route('/usuarios') #Esta es la ruta Usuarios
def usuarios(): #Esta es la función de Usuarios

    if 'usuario' not in session: #Aqui se hace la verificación de sesión
        return redirect(url_for('mod_admin/home'))#Regresa al home
    
    if session['rol'] !=1:# Aqui se verifica el rol del usuario
        return "Acceso no autorizado"
    
    cursor = conexion.cursor(dictionary=True)#Cursor creado para interactualr con MySQL


    consulta = """ #Aquí estás guardando una consulta SQL dentro de una variable
    SELECT u.id_usuario,
       u.nombre_usuario,
       u.nombres_y_apellidos,
       u.correo,
       u.telefono,
       u.id_rol,
       r.nombre_rol
    FROM usuario u
    JOIN rol r ON u.id_rol = r.id_rol
    """

    cursor.execute(consulta)#Ejecuta la consulta SQL que guardamos en la variable consulta
    lista_usuarios = cursor.fetchall()#Aquí se traen todos los resultados de la consulta.

    cursor.close()

    return render_template('mod_admin/usuarios.html', usuarios = lista_usuarios)#Manda la lista a usuarios.html

#====== Ruta crear usuario======
@app.route('/crear_usuario')
def crear_usuario():
    return render_template('mod_admin/crear_usuarios.html')

#====== Ruta para guardar Usuario===
from werkzeug.security import generate_password_hash

@app.route('/guardar_usuario', methods=['POST'])
def guardar_usuario():
        
        id_usuario =request.form['id_usuario']
        nombre_usuario = request.form['nombre_usuario']
        nombres_y_apellidos = request.form['nombres_y_apellidos']
        correo = request.form['correo']
        telefono = request.form['telefono']
        password = generate_password_hash(request.form['password']) #Aqui se encripta la contraseña
        rol = request.form['rol']

        cursor = conexion.cursor()

        #validar cédula duplicada
        cursor.execute("SELECT * FROM usuario WHERE id_usuario =%s", (id_usuario,))
        if cursor.fetchone():
            return "Ya existe un usuario con este número de cédula"
        
        #Validar correo duplicado
        cursor.execute("SELECT * FROM usuario WHERE correo = %s", (correo,))
        if cursor.fetchone():
            return "El correo ingresado ya está registrado"
        
        sql= """
        INSERT INTO usuario
        (id_usuario, nombre_usuario, nombres_y_apellidos, correo, telefono, hash_password, id_rol)
        VALUES( %s, %s, %s, %s, %s, %s, %s)
        """

        valores = (id_usuario, nombre_usuario, nombres_y_apellidos, correo, telefono, password, rol)

        cursor.execute(sql, valores)
        conexion.commit()
        cursor.close()

        return redirect(url_for('mod_admin/usuarios'))
        

#====== Ruta para eliminar usuario=====

@app.route('/eliminar_usuario/<id_usuario>')
def eliminar_usuario(id_usuario):

    cursor = conexion.cursor()

    sql = "DELETE FROM usuario WHERE id_usuario = %s" 
    cursor.execute(sql, (id_usuario,))


    conexion.commit() #Guarda cambios
    cursor.close()

    return redirect(url_for('mod_admin/usuarios'))#Vuelve a la lista de usuarios

#====== Ruta para editar usuario ======

@app.route('/editar_usuario/<id_usuario>')
def editar_usuario(id_usuario):

    cursor = conexion.cursor(dictionary=True)

    sql = "SELECT * FROM usuario WHERE id_usuario = %s"
    cursor.execute(sql, (id_usuario,))
    usuario = cursor.fetchone()

    cursor.close()

    if not usuario:
        return "Usuario no encontrado", 404

    return render_template('mod_admin/editar_usuario.html', usuario=usuario)

    

# ==========================================
# PANELES DEL SISTEMA
# ==========================================
#============= Panel Super Administrdor ===============

@app.route('/superadministrador')
def superadministrador():

    if 'usuario' not in session:
        return redirect(url_for('mod_admin/login'))#Si no hay sesión iniciada regresa al login
    if session['rol'] != 1:
        return 'Acceso no autorizado'
    
    return render_template('mod_admin/admin.html')#FALTA CREAR EL HTML DE SUPERADMIN


#============= Panel administrador ====================
@app.route('/admin')
def administrador():

    if 'usuario' not in session:
        return redirect(url_for('mod_admin/login')) #Si no hay sesión iniciada regresa al login
    
    if session['rol'] != 1:
        return "Acceso no autorizado"
    
    return render_template('mod_admin/admin.html')

#===============ALERTAS DEL SISTEMA=====================#
@app.route('/generar_alerta')
def generar_alerta():
    return "<h2>Módulo de alertas en construcción</h2>"

@app.route('/recibir_alerta')
def recibir_alertas():
    return "<h2>Módulo de alertas en construcción</h2>"



#=========== Panel conductor ==========================
@app.route('/conductor')
def conductor():

    if 'usuario' not in session:
        return redirect(url_for('mod_admin/login'))

    if session['rol'] != 3:
        return "Acceso no autorizado"
        
    return render_template('mod_conductor/conductor.html')


# panel Mis Rutas 
@app.route('/mi_ruta')
def mi_ruta():
    
    if 'usuario' not in session:
        return redirect(url_for('login'))

    
    if session['rol'] != 3:
        return "Acceso no autorizado"

    
    return render_template('mod_conductor/mi_ruta.html')



# panel Estudiantes_conductor

@app.route('/estudiantes_conductor')
def estudiantes_conductor():
 
    
    if 'usuario' not in session:
        return redirect(url_for('login'))

    
    if session['rol'] != 3:
        return "Acceso no autorizado"

    cursor = conexion.cursor(dictionary=True)
    consulta = """
    SELECT id_estudiante,nombre,grado,direccion,telefono,id_ruta,estado
    FROM estudiante;
    """
    cursor.execute(consulta)
    lista_estudiantes = cursor.fetchall()
    
    return render_template('mod_conductor/estudiantes_conductor.html', estudiantes_bd=lista_estudiantes)

@app.route('/abordar_estudiante/<int:id_estudiante>')
def abordar_estudiante(id_estudiante):
    if 'usuario' not in session or session['rol'] != 3:
        return redirect(url_for('login'))

    cursor = conexion.cursor()
    # Cambia el estado a 'Abordo' para ese ID específico
    consulta = "UPDATE estudiante SET estado = 'Abordo' WHERE id_estudiante = %s"
    cursor.execute(consulta, (id_estudiante,))
    conexion.commit() # ¡Importante! Guarda el cambio en la BD
    
    return redirect(url_for('estudiantes_conductor'))
#Panel alertas conductor
@app.route('/aler_conduc')
def aler_conduc():
    
    if 'usuario' not in session:
        return redirect(url_for('login'))

    
    if session['rol'] != 3:
        return "Acceso no autorizado"

    
    return render_template('mod_conductor/alertas_conductor.html')




#============ Panel padres de familia==================
@app.route('/padres')
def padres():

    if 'usuario' not in session:
        return redirect(url_for('mod_admin/login'))
    
    if session['rol'] != 4:
        return "Acceso no autorizado"
    
    return render_template('mod_padres/padre.html')



@app.route('/ver_rutar')
def ver_rutar():
    return "<h2>Módulo de vehículos en construcción</h2>"

@app.route('/reportar_inansistencia')
def reportar_inansistencia():
    return "<h2>Módulo de vehículos en construcción</h2>"
#============ Panel informacion del conductor==================
@app.route('/informacion_conductor')
def informacion_conductor():

    if 'usuario' not in session:
        return redirect(url_for('mod_admin/login'))
    
    if session['rol'] != 4:
        return "Acceso no autorizado"
    
    return render_template('mod_padres/informacion_conductor.html')
#============ Panel estudiantes_padre==================

@app.route('/estudiantes_padre')
def estudiantes_padre():

    if 'usuario' not in session:
        return redirect(url_for('mod_admin/login'))
    
    if session['rol'] != 4:
        return "Acceso no autorizado"
    
    return render_template('mod_padres/estudiantes_padre.html')



#======= RUTA VALIDACION DE LOGIN====================== CRISTINA SALAZAR

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
        id_rol = usuario['id_rol'] # Esta es la posición en donde esta el usuario en la tabla BD

        session['usuario'] = usuario['id_rol']
        session['rol'] = usuario['id_rol']

        if id_rol == 1:
            return redirect(url_for('superadministrador'))
        elif id_rol == 2:
            return redirect(url_for('administrador'))
        elif id_rol == 3:
            return redirect(url_for('conductor'))
        elif id_rol == 4:
            return redirect(url_for('padres'))
        else:
            return "Rol no reconocido"

    else:
        return "Usuario o contraseña incorrectos"
    
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('inicio'))#retorna al home/pág inicio

# ==========================================
# GESTIÓN DE VEHÍCULOS Y RUTAS
# RESPONSABLE: CAMILO OCAMPO
# ==========================================
@app.route('/vehiculos')
def vehiculos():
    return "<h2>Módulo de vehículos en construcción</h2>"

@app.route('/monitorear_ruta')
def monitorear_ruta():
    return "<h2>Módulo de alertas en construcción</h2>"

# Aquí se desarrollarán las rutas relacionadas con:
# - Registro de vehículos
# - Listado de vehículos
# - Creación de rutas
# - Edición de rutas
# - Asignación de vehículo o conductor a la ruta


#==========================================
#GESTIÓN DE ESTUDIANTES Y ASIGNACIÓN A RUTA
#RESPONSABLE: VICTOR VELANDIA
#==========================================

@app.route('/rutas')
def rutas():
    return "<h2>Módulo de rutas en construcción</h2>"


#Aquí se desarrollarán las rutas relacionadas con:
#- Registro de estudiantes
#- Edición de estudiantes
#- Eliminación de estudiantes
#- Asignación de estudiantes a rutas
#- Consultar estudiantes por ruta
#- Listar estudiantes por conductor o ruta



# ==========================================
# INTERFAZ DE USUARIO Y VISUALIZACIÓN DEL SISTEMA
# RESPONSABLE: CAROLIA EPIAYU
# ==========================================
# Aquí se desarrollarán las rutas relacionadas con:
# - Diseño de formularios (usuarios, estudiantes, vehículos, rutas)
# - Dashboards por rol (Administrador, Conductor, Padres)
# - Integración visual con Flask (render_template)
# - Visualización de rutas, estudiantes y vehículos según rol
# - Mejora de experiencia de usuario (UX)


# ==========================================
# EJECUCIÓN DE LA APLICACIÓN
# ==========================================

if __name__ == '__main__':
    app.run(debug=True)
