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
#===========================================
# VARIABLES GLOBALES PARA HTML
#===========================================

# Aquí se definen variables globales que estarán disponibles en todas las plantillas HTML del proyecto.
@app.context_processor # Decorador para inyectar variables globales en todas las plantillas HTML
def inyectar_datos_globales(): # Función que devuelve un diccionario con datos globales disponibles en todas las plantillas
    nombres_roles = {
        1: 'Superadministrador',
        2: 'Administrador',
        3: 'Conductor',
        4: 'Padre de familia'           
    }

    rol = session.get('rol') # Obtiene el rol del usuario desde la sesión

    return {
        'nombre_panel' : nombres_roles.get(rol, 'Usuario') # Devuelve el nombre del panel según el rol, o 'Usuario' si no se encuentra
    }
#Ruta global para regreso al panel
@app.route('/volver_panel')
def volver_panel():

    if 'usuario' not in session:
        return redirect(url_for('login'))
    
    rol = session.get('rol')

    if rol == 1:
        return redirect(url_for('superadministrador'))
    elif rol == 2:
        return redirect(url_for('administrador'))
    elif rol == 3:
        return redirect(url_for('conductor'))
    elif rol == 4:
        return redirect(url_for('padre de familia'))
    return redirect(url_for('login'))



#===========================================
#FUNCIONES AUXILIARES Y VARIABLES GLOBALES PARA HTML
#===========================================

# Variables globales disponibles en todas las vistas HTML
@app.context_processor # Decorador para inyectar variables globales en todas las plantillas HTML
def inyectar_datos_globales(): # Función que devuelve un diccionario con datos globales disponibles en todas las plantillas
    nombres_roles = {
        1: 'Superadministrador',
        2: 'Administrador',
        3: 'Conductor',
        4: 'Padre de familia'           
    }

    rol = session.get('rol') # Obtiene el rol del usuario desde la sesión

    return {
        'nombre_panel' : nombres_roles.get(rol, 'Usuario') # Devuelve el nombre del panel según el rol, o 'Usuario' si no se encuentra
    }

#=============================================
# FUNCION PARA BOTON VOLVER 
#=============================================

def obtener_url_volver():
    if session ['rol'] == 1:
        return url_for('superadministrador')
    elif session ['rol'] == 2:
        return url_for('administrador')
    elif session ['rol'] == 3:
        return url_for('conductor')
    elif session ['rol'] == 4:
        return url_for('padre de familia')
    else:
        return url_for('login')

# ==========================================
# RUTA GLOBAL VOLVER AL PANEL
# ==========================================

@app.route('/') #Esta es la ruta principal
def inicio():
    return render_template('mod_admin/home.html')

# Ruta login
@app.route('/login')
def login():
    return render_template('mod_admin/login.html')

#=========Ruta Usuarios=========

@app.route('/usuarios') #Esta es la ruta Usuarios
def usuarios(): #Esta es la función de Usuarios

    if 'usuario' not in session: #Aqui se hace la verificación de sesión
        return redirect(url_for('mod_admin/login'))#Regresa al home
    
    if session['rol'] not in [1, 2, 3, 4]:# Aqui se verifica el rol del usuario
        return "Acceso no autorizado"
    
    cursor = conexion.cursor(dictionary=True)#Cursor creado para interactualr con MySQL

#Aquí se esta guardando una consulta SQL dentro de una variable
    consulta = """ 
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

    parametros = []

    if rol_actual:# Agrega condición SQL solo si el usuario seleccionó un rol
        consulta += " WHERE r.nombre_rol = %s"
        parametros.append(rol_actual)

    consulta += " ORDER BY u.id_rol DESC"

    cursor.execute(consulta,parametros)#Ejecuta la consulta SQL que guardamos en la variable consulta
    lista_usuarios = cursor.fetchall()#Aquí se traen todos los resultados de la consulta.
    cursor.close()

    return render_template('mod_admin/usuarios.html', usuarios = lista_usuarios)#Manda la lista a usuarios.html

# ==========================================
# FORMULARIO CREAR USUARIO
# ==========================================

@app.route('/crear_usuario')
def crear_usuario():
    return render_template('mod_admin/crear_usuarios.html')

#====== Ruta para guardar Usuario===
from werkzeug.security import generate_password_hash

@app.route('/guardar_usuario', methods=['POST'])
def guardar_usuario():
        
        #CAPTURA DE DATOS DEL FORMULARIO
        id_usuario =request.form['id_usuario']
        nombre_usuario = request.form['nombre_usuario']
        nombres_y_apellidos = request.form['nombres_y_apellidos']
        correo = request.form['correo']
        telefono = request.form['telefono']
        password = generate_password_hash(request.form['password']) #Aqui se encripta la contraseña
        rol = request.form['rol']

         # VALIDACIÓN LONGITUD DE CAMPOS
        if len(id_usuario) > 10:
            return "El número de identificación no puede superar 10 caracteres"

        if len(nombre_usuario) > 30:
            return "El nombre de usuario no puede superar 30 caracteres"

        if len(nombres_y_apellidos) > 50:
            return "El nombre completo no puede superar 50 caracteres"

        if len(correo) > 50:
            return "El correo no puede superar 50 caracteres"

        if len(telefono) > 10:
            return "El teléfono no puede superar 10 caracteres"
        
        # CONEXIÓN Y VALIDACIONES EN BASE DE DATOS
        cursor = conexion.cursor()

        #validar cédula duplicada
        cursor.execute("SELECT * FROM usuario WHERE id_usuario =%s", (id_usuario,))
        if cursor.fetchone():
            return "Ya existe un usuario con este número de cédula"
        
        #Validar correo duplicado
        cursor.execute("SELECT * FROM usuario WHERE correo = %s", (correo,))
        if cursor.fetchone():
            return "El correo ingresado ya está registrado"
        
        # INSERTAR USUARIO
        sql= """
        INSERT INTO usuario
        (
        id_usuario,
        nombre_usuario, 
        nombres_y_apellidos, 
        correo, telefono, 
        hash_password, 
        id_rol
        )
        VALUES( %s, %s, %s, %s, %s, %s, %s)
        """

        valores = (
            id_usuario, 
            nombre_usuario, 
            nombres_y_apellidos, 
            correo, telefono, 
            password, 
            rol
        )

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

    cursor = conexion.cursor(dictionary=True) # Crear cursor en formato diccionario para acceder por nombre de campo

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

    if session['rol'] != 2:
        return "Acceso no autorizado"
        
    return render_template('conductor.html')

#============ Panel padres de familia==================
@app.route('/padres')
def padres():

    # if 'usuario' not in session:
    #     return redirect(url_for('login'))
    
    # if session['rol'] != 4:
    #     return "Acceso no autorizado"
    
    return render_template('mod_padres/padre.html')

#======== Ruta para gestion de alertas (padres)=========

@app.route('/padres/alertas')
def alertas_padres():
    cursor = conexion.cursor(dictionary=True)

     #Temporal: para luego conectamos con sesión del padre
    id_estudiante = 7895462

    consulta = """
    SELECT *
    FROM ALERTAS
    WHERE id_estudiante = %s
    ORDER BY fecha_hora DESC
    """
    cursor.execute(consulta, (id_estudiante,))
    alertas = cursor.fetchall()
    cursor.close()

    return render_template(
        'mod_padres/alertas_padres.html', 
        alertas=alertas
    )

#======== Ruta para reporte de inasistencia (padres)=========
@app.route('/reportar_inasistencia', methods=['GET', 'POST'])
def reportar_inasistencia():
    cursor = conexion.cursor(dictionary=True)

    #Temporal: luego conectamos con sesión del padre
    id_padre = session.get('usuario')

    if request.method == 'POST':
        estudiante = request.form.get('estudiante')
        fecha = request.form.get('fecha')
        motivo = request.form.get('motivo')
        observacion = request.form.get('observacion')

        mensaje = f"Inasistencia reportada para{estudiante} el día {fecha}. Motivo: {motivo}. Observación{observacion}"

        consulta_insert = """
        INSERT INTO ALERTAS(
            id_usuario_emisor,
            tipo_alerta,
             mensaje
        )
        VALUES (%s, %s, %s)
        """
        cursor.execute(consulta_insert, (
            id_padre,
            'inasistencia',
            mensaje
        ))

        conexion.commit()
        cursor.close()

        flash('Inasistencia reportada correctamente', 'success')
        return redirect(url_for('alertas_padres'))
    cursor.close()
    return render_template('mod_padres/reportar_inasistencia.html')

#======== Ruta para información conductor (padres)=========

@app.route('/padres/informacion_conductor')
def informacion_conductor():
    cursor = conexion.cursor(dictionary=True)

    # Consulta SQL para obtener la información del conductor
    consulta = """
    SELECT u.nombres_y_apellidos AS nombre,
       u.telefono,
       u.correo,
       v.id_vehiculo AS vehiculo,
       v.placa,
       r.nombre_ruta AS ruta
     FROM ESTUDIANTE e
     INNER JOIN RUTA r 
      ON e.id_ruta = r.id_ruta
     INNER JOIN USUARIO u 
      ON r.id_conductor = u.id_usuario
     INNER JOIN VEHICULO v 
      ON u.id_usuario = v.id_conductor
     WHERE e.id_ruta = 301;
    """

    cursor.execute(consulta)
    conductor = cursor.fetchone()  # Trae un solo registro

    # Renderiza el HTML y pasa los datos
    return render_template(
        'mod_padres/informacion_conductor.html',
        conductor=conductor
    )


@app.route('/estudiantes_padre')
def estudiantes_padre():
    return "<h2>Módulo de rutas en construcción</h2>"


@app.route('/padres/ver_ruta')
def ver_ruta():
    return render_template('mod_padres/ver_ruta.html')



#===============================================================================
#==========GESTIONAR ESTUDIANTES (mod_admin mod_supadmin) ==========
#==================================================================================

@app.route('/gestion_estudiantes')
def gestion_estudiantes():

    if 'usuario' not in session:
        return redirect(url_for('mod_admin/login'))
    
    if session['rol'] != 3:
        return "Acceso no autorizado"
    
    return render_template('padre.html')

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
# MODULO VEHÍCULOS Y RUTAS
# RESPONSABLE: CAMILO OCAMPO
# ==========================================
@app.route('/gestion_vehiculos')
def gestion_vehiculos():
    return "<h2>Módulo de vehículos en construcción</h2>"

@app.route('/monitorear_ruta')
def monitorear_ruta():
    return "<h2>Módulo de alertas en construcción</h2>"

# Aquí se desarrollarán las rutas relacionadas con:
# - gestionar_rutas
# - crear_ruta
# - editar_ruta
# - eliminar_ruta

# - gestionar_vehiculos
# - crear_vehiculo
# - editar_vehiculo
# - eliminar_vehiculo

# - asignar conductor
# - asignar estudiantes
# - asignar vehículo


#==========================================
#GESTIÓN DE ESTUDIANTES Y ASIGNACIÓN A RUTA
#RESPONSABLE: VICTOR VELANDIA
#==========================================

@app.route('/gestion_rutas')
def gestion_rutas():
    return "<h2>Módulo de rutas en construcción</h2>"


#Aquí se desarrollarán las rutas relacionadas con:
# - ver su ruta
# - reportar alertas
# - compartir ubicación
# - marcar estudiantes recogidos
# - modificar recorrido temporalmente


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
