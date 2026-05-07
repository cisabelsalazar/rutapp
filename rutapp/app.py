# RUTAPP - APLICACIÓN DE GESTIÓN DE RUTAS ESCOLARES
# Desarrollada por: Cristina Salazar, Camilo Ocampo, Victor Velandia

#==========================================
# IMPORTACIÓN DE LIBRERÍAS Y CONFIGURACIÓN INICIAL
#==========================================

from flask import Flask, render_template, request, redirect, url_for,session, flash
import mysql.connector

#==========================================
# CONFIGURACIÓN DE LA APLICACIÓN FLASK
#==========================================

app = Flask(__name__)
app.secret_key = "rutapp_secreto"   #   Clave secreta para manejar sesiones y flash messages en Flask

#==========================================
# CONFIGURACIÓN DE LA CONEXIÓN A LA BASE DE DATOS
#==========================================

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



#============================================
#         RUTAS PROYECTO RUTAPP
#============================================

#============================================
# AUTENTICACIÓN - RESPONSABLE: CRISTINA SALAZAR
#============================================

#============================================
#   RUTA HOME
#============================================

@app.route('/') #Esta es la ruta principal o index del proyecto
def inicio():
    return render_template('mod_admin/login.html')

@app.route('/login') #Esta es la ruta de login
def login():
    return render_template('mod_admin/login.html')

#=========   RUTA USUARIOS   =========

@app.route('/usuarios') #Esta es la ruta Usuarios
def usuarios(): #Esta es la función de Usuarios


    if 'usuario' not in session: #Aqui se hace la verificación de sesión
        return redirect(url_for('mod_admin/login'))#Regresa al home
    
    if session['rol'] not in [1, 2, 3, 4]:# Aqui se verifica el rol del usuario
        return "Acceso no autorizado"
    
    botones = [
    {
        "texto": "← Volver",
        "url": url_for("usuarios"),
        "class": "btn-secondary"
    },
    {
        "texto": "+ Nuevo usuario",
        "url": url_for("crear_usuario"),
        "class": "btn-primary"
    }
]
    
    cursor = conexion.cursor(dictionary=True)#Cursor creado para interactuar con MySQL


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

    return render_template('mod_admin/usuarios.html', usuarios = lista_usuarios, botones=botones)#Manda la lista a usuarios.html

#====== Ruta crear usuario======
@app.route('/crear_usuario')
def crear_usuario():
    return render_template('mod_admin/crear_usuarios.html')

#====== RUTA GUARDAR USUARIO===
from werkzeug.security import generate_password_hash #Importa la función para encriptar contraseñas

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

        flash('Usuario guardado correctamente', 'success')
        return redirect(url_for('usuarios'))
        

#====== RUTA ELIMINAR USUARIO =====

# - Elimina un usuario de la base de datos
# - Se ejecuta únicamente mediante método POST por seguridad
@app.route('/eliminar_usuario/<id_usuario>', methods=['POST'])
def eliminar_usuario(id_usuario):

    cursor = conexion.cursor() # Crear cursor
    sql = "DELETE FROM usuario WHERE id_usuario = %s"# Consulta SQL para eliminar el usuario
    cursor.execute(sql, (id_usuario,))# Ejecutar la consulta
    conexion.commit() # Guardar cambios en la base de datos
    cursor.close() # Cerrar cursor
    flash('Usuario eliminado correctamente', 'success')

    return redirect(url_for('usuarios')) # Redirigir a la lista de usuarios

#====== RUTA EDITAR USUARIO ======

# - GET  -> muestra el formulario con los datos actuales
# - POST -> guarda los cambios realizados en la BD
@app.route('/editar_usuario/<id_usuario>', methods=['GET', 'POST'])
def editar_usuario(id_usuario):

    cursor = conexion.cursor(dictionary=True) # Crear cursor en formato diccionario para acceder por nombre de campo

    # POST guardar cambios
    if request.method == 'POST': # POST: cuando el usuario da clic en "Guardar cambios"

        # Captura los datos enviados desde el formulario HTML
        nombres = request.form['nombres_y_apellidos']
        correo = request.form['correo']
        telefono = request.form['telefono']
        rol = request.form['rol'] #para actualizar el rol cuando se edita usuario

        # Consulta SQL para actualizar la información del usuario
        sql = """
        UPDATE usuario
        SET nombres_y_apellidos = %s,
            correo = %s,
            telefono = %s,
            id_rol = %s
        WHERE id_usuario = %s
        """

        valores = (nombres, correo, telefono, rol, id_usuario)

        cursor.execute(sql, valores)
        conexion.commit()
        cursor.close()

        flash('Informacion actualizada correctamente', 'success')
        return redirect(url_for('usuarios'))

    #GET: Cargar formulario
    sql = "SELECT * FROM usuario WHERE id_usuario = %s" # Consulta para obtener los datos actuales del usuario
    cursor.execute(sql, (id_usuario,))
    usuario_data = cursor.fetchone()

    cursor.close() #Cierra el cursor

    if not usuario_data: #validacion por si no existe el usuario
        return "Usuario no encontrado", 404

    return render_template('mod_admin/editar_usuario.html', usuario=usuario_data) # Envía los datos al formulario editar_usuario.html
  

# ==========================================
#          PANELES DEL SISTEMA
# ==========================================
#============= PANEL SUPER ADMINISTRADOR ===============

@app.route('/supadmin')
def superadministrador():

    if 'usuario' not in session:
        return redirect(url_for('login'))

    if session['rol'] != 1:
        return 'Acceso no autorizado 1'
    
    return render_template('mod_admin/supadmin.html')


#============= PANEL ADMINISTRADOR====================
@app.route('/admin')
def administrador():

    if 'usuario' not in session:
        return redirect(url_for('login')) #Si no hay sesión iniciada regresa al login
    
    if session['rol'] != 2:
        return f"Acceso no autorizado 2 | {session['rol']} |"
    
    return render_template('mod_admin/admin.html')

#============================================================================================
#===============ALERTAS DEL SISTEMA (mod admin)=====================
#=============================================================================================
@app.route('/gestion_alerta')#Rura gestion de alertas Modulo admin y supadmin
def gestion_alerta():#función para mostrar las alertas en el panel del admin y supadmin

    if 'usuario' not in session:
        return redirect(url_for('login'))

    if session['rol'] not in [1, 2]:
        return "Acceso no autorizado"

    cursor = conexion.cursor(dictionary=True)# Crear cursor para interactuar con la base de datos

    # Consulta para traer alertas con datos del conductor, estudiante y ruta
    consulta = """
    SELECT 
        a.*,
        u.nombres_y_apellidos AS conductor_nombre,
        e.nombre AS estudiante_nombre,
        r.nombre_ruta
    FROM ALERTAS a
    LEFT JOIN USUARIO u 
        ON a.id_usuario_emisor = u.id_usuario
    LEFT JOIN ESTUDIANTE e 
        ON a.id_estudiante = e.id_estudiante
    LEFT JOIN RUTA r 
        ON a.id_ruta = r.id_ruta
    ORDER BY a.fecha_hora DESC
    """

    cursor.execute(consulta) #Ejecuta la consulta SQL
    alertas = cursor.fetchall() #Trae todas las alertas obtenidas de la consulta
    cursor.close() #Cierra el cursor

    return render_template(
        'mod_admin/alertas.html', 
        alertas=alertas
    ) #Renderiza la plantilla gestion_alerta.html y le pasa la lista de alertas obtenida de la consulta


#===============================================================
#========Ruta para editar alerta (mod admin y supadmin)=========
#===============================================================

@app.route('/editar_alerta/<id_alerta>', methods=['GET', 'POST'])
def editar_alerta(id_alerta):
    cursor = conexion.cursor(dictionary=True)

    # POST: Guardar cambios en la alerta
    if request.method == 'POST':
        estado = request.form.get('estado')
        observacion = request.form.get('observacion_admin')

        consulta_update = """
        UPDATE ALERTAS
        SET estado = %s,
            observacion_admin = %s
        WHERE id_alerta = %s
        """

        cursor.execute(consulta_update, (
            estado, 
            observacion, 
            id_alerta
        ))
        conexion.commit()
        cursor.close()

        flash('Alerta gestionada correctamente', 'success')#nO ESTA FUNCIONANDO REVISAR
        return redirect(url_for('editar_alerta', id_alerta=id_alerta))

    
    # GET: Cargar datos actuales de la alerta para mostrar en el formulario
    consulta = """ SELECT * FROM ALERTAS WHERE id_alerta = %s """
    cursor.execute(consulta, (id_alerta,))
    alerta = cursor.fetchone()
    cursor.close()

    return render_template(# Return de la consulta
        'mod_admin/editar_alerta.html', 
        alerta=alerta
    )
    
#============================================================================================
#============================ PANEL CONDUCTOR==========================
#============================================================================================
@app.route('/conductor')
def conductor():

    # if 'usuario' not in session:
    #     return redirect(url_for('login'))

    # if session['rol'] != 3:
    #     return "Acceso no autorizado"
        
    return render_template('mod_conductor/conductor.html')

@app.route('/conductor/mi_ruta')#Revisado por Cristina OK#
def mi_ruta():
    # if 'usuario' not in session:
    #     return redirect(url_for('login'))
    # if session['rol'] != 3:
    #     return "Acceso no autorizado"
    return render_template('mod_conductor/mi_ruta.html')

#======== Ruta para visualisar estudiantes en el panel conductor=========#
@app.route('/conductor/estudiantes')
def estudiantes_conductor():
    cursor = conexion.cursor(dictionary=True) # Importante: dictionary=True
    consulta = "SELECT  nombre, grado, direccion, telefono, id_ruta, estado FROM estudiante"
    cursor.execute(consulta)
    
    # Obtenemos los datos
    estudiantes_bd = cursor.fetchall()
    
    
    
    # Pasamos la variable al HTML
    return render_template('mod_conductor/estudiantes_conductor.html', estudiantes_bd=estudiantes_bd)



#==========================================================
# ======== Ruta para gestionar alertas (conductor)=========
#=========================================================

@app.route('/conductor/alertas', methods=['GET', 'POST'])#Revisado por Cristina OK#
def alertas_conductor():
    cursor = conexion.cursor(dictionary=True)# Crear cursor para interactuar con la base de datos

    id_conductor = session.get('usuario') # Obtener el ID del conductor desde la sesión

    #Crear alerta
    if request.method == 'POST':
        id_estudiante = request.form.get('id_estudiante')
        id_ruta = request.form.get('id_ruta')
        tipo_alerta = request.form.get('tipo_alerta')
        mensaje = request.form.get('mensaje')

        consulta_insert = """
        INSERT INTO ALERTAS(
        id_usuario_emisor,
        id_estudiante,
        id_ruta,
        tipo_alerta,
        mensaje
        )
        VALUES (%s, %s, %s, %s, %s)
        """

        cursor.execute(consulta_insert,(
            id_conductor,
            id_estudiante,
            id_ruta,
            tipo_alerta,
            mensaje
        ))

        conexion.commit()
        cursor.close()
        flash('Alerta creada correctamente', 'success')
        return redirect(url_for('alertas_conductor'))
    
    #Mostrar alertas enviadas por el conductor
    consulta="""
    SELECT *
    FROM ALERTAS
    WHERE id_usuario_emisor = %s
    ORDER BY fecha_hora DESC
    """

    cursor.execute(consulta, (id_conductor,))
    alertas = cursor.fetchall()

    cursor.close()

    return render_template('mod_conductor/alertas_conductor.html', alertas=alertas)


@app.route('/conductor/compartir_ubicacion')
def compartir_ubicacion():  
    return "<h2>Módulo en construcción</h2>"
#======================================================================================
#======================= PANEL ESTUDIANTES_CONDUCTOR==================
#======================================================================================
@app.route('/abordar_estudiante')
def abordar_estudiante(id_estudiante):
    cursor = conexion.cursor()
    actualizar = """
        UPDATE estudiante
        SET estado = 'Abordo'
        WHERE id_estudiante = %s
    """
    cursor.execute(actualizar, (id_estudiante,))
    conexion.commit()
    cursor.close()
    # Redirigimos de nuevo a la lista
    return redirect(url_for('estudiantes_conductor'))




#======================================================================================
#======================= PANEL PADRES DE FAMILIA==================
#======================================================================================
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
        return redirect(url_for('login'))
    
    if session['rol'] not in [1, 2]:
        return "Acceso no autorizado"
    
    cursor = conexion.cursor(dictionary=True)

    consulta = """
    SELECT e.id_estudiante,
           e.nombre,
           e.grado,
           e.direccion,
           e.telefono,
           r.nombre_ruta
    FROM estudiante e
    LEFT JOIN ruta r ON e.id_ruta = r.id_ruta
    """

    cursor.execute(consulta)
    lista_estudiantes = cursor.fetchall()
    cursor.close()
    
    # ruta_volver = {
    #     1: 'superadministrador',
    #     2: 'administrador'
    # }.get(session['rol'])

    return render_template(
        'mod_admin/estudiantes.html',
        # ruta_volver=ruta_volver,
        estudiantes=lista_estudiantes
    )
#==== Ruta Crear Estudiante ====

@app.route('/crear_estudiante')
def crear_estudiante():
    return render_template('mod_admin/crear_estudiante.html')

#================================================================
#=============RUTA GUARDA ESTUDIANTE=======

@app.route('/guardar_estudiante', methods=['POST'])
def guardar_estudiante():

        id_estudiante = request.form['id_estudiante']
        nombre= request.form['nombre']
        grado= request.form['grado']
        direccion= request.form['direccion']
        telefono= request.form['telefono']
        id_ruta= request.form['id_ruta']

        cursor =conexion.cursor()



        # Valida Id dubplicado
        cursor.execute ("SELECT * FROM estudiante WHERE id_estudiante = %s", (id_estudiante,))
        if cursor.fetchone():
            return "Ya existe un estudiante con este número de identificación"
            
        sql = """
        INSERT INTO estudiante
        (id_estudiante, nombre, grado, direccion, telefono, id_ruta)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        valores = (id_estudiante, nombre, grado, direccion, telefono, id_ruta)

        cursor.execute(sql, valores)
        conexion.commit()
        cursor.close()
        flash('Estudiante guardado correctamente', 'success')

        return redirect(url_for('gestion_estudiantes')) 

#====== RUTA ELIMINAR ESTUDIANTE =====

# - Elimina un estudiante de la base de datos
# - Se ejecuta únicamente mediante método POST por seguridad
@app.route('/eliminar_estudiante/<id_estudiante>', methods=['POST'])
def eliminar_estudiante(id_estudiante):

    cursor = conexion.cursor() # Crear cursor

    if request.method == 'POST':

        sql = "DELETE FROM estudiante WHERE id_estudiante = %s"# Consulta SQL para eliminar el estudiante
        cursor.execute(sql, (id_estudiante,))# Ejecutar la consulta
        conexion.commit() # Guardar cambios en la base de datos
        cursor.close() # Cerrar cursor
        flash('Estudiante eliminado correctamente', 'success')

    return redirect(url_for('gestion_estudiantes')) # Redirigir a la lista de estudiantes

#====== RUTA EDITAR ESTUDIANTE ======

# - GET  -> muestra el formulario con los datos actuales
# - POST -> guarda los cambios realizados en la BD
@app.route('/editar_estudiante/<id_estudiante>', methods=['GET', 'POST'])
def editar_estudiante(id_estudiante):

    cursor = conexion.cursor(dictionary=True) # Crear cursor en formato diccionario para acceder por nombre de campo

    # POST guardar cambios
    if request.method == 'POST': # POST: cuando el usuario da clic en "Guardar cambios"

        # Captura los datos enviados desde el formulario HTML
        nombre = request.form['nombre']
        grado = request.form['grado']
        direccion = request.form['direccion']
        telefono = request.form['telefono']
        id_ruta = request.form['id_ruta']

        # Consulta SQL para actualizar la información del estudiante        
        sql = """
        UPDATE estudiante
        SET nombre = %s,
            grado = %s,
            direccion = %s,
            telefono = %s,
            id_ruta = %s
        WHERE id_estudiante = %s
        """

        valores = (nombre, grado, direccion, telefono, id_ruta, id_estudiante)

        cursor.execute(sql, valores)
        conexion.commit()
        cursor.close()

        flash('Informacion actualizada correctamente', 'success')
        return redirect(url_for('gestion_estudiantes'))

    #GET: Cargar formulario
    sql = "SELECT * FROM estudiante WHERE id_estudiante = %s" # Consulta para obtener los datos actuales del estudiante
    cursor.execute(sql, (id_estudiante,))
    estudiante = cursor.fetchone()

    cursor.close() #Cierra el cursor

    if not estudiante: #validacion por si no existe el estudiante
        return "Estudiante no encontrado", 404
    
    ruta_volver = {
        1: 'superadministrador',
        2: 'administrador'
    }.get(session['rol'])

    return render_template('mod_admin/editar_estudiante.html', # Renderiza el formulario de edición con los datos actuales del estudiante
                           ruta_volver=ruta_volver, 
                           estudiante=estudiante  ) # Envía los datos al formulario editar_estudiante.html




#============== RUTA VALIDACION DE LOGIN====================== CRISTINA SALAZAR

from werkzeug.security import check_password_hash # Importa la función para verificar contraseñas encriptadas
import hashlib # Importa la librería para manejar hash MD5 (usuarios antiguos)

@app.route('/validar_login', methods=['POST'])
def valida_login():
    correo = request.form['correo'].strip()
    password = request.form['password'].strip()

    cursor = conexion.cursor(dictionary=True)

    cursor.execute("""
        SELECT * 
        FROM usuario
        WHERE correo = %s
    """, (correo,))

    usuario = cursor.fetchone()

    if usuario:
        hash_guardado = usuario['hash_password']

        acceso = False

        # Usuarios nuevos (scrypt)
        if hash_guardado.startswith("scrypt:"):
            acceso = check_password_hash(hash_guardado, password)

        # Usuarios viejos (MD5)
        else:
            acceso = hashlib.md5(password.encode()).hexdigest() == hash_guardado

        if acceso:
            session['usuario'] = usuario['id_usuario']
            session['rol'] = usuario['id_rol']

            if usuario['id_rol'] == 1:
                return redirect(url_for('superadministrador'))
            elif usuario['id_rol'] == 2:
                return redirect(url_for('administrador'))
            elif usuario['id_rol'] == 3:
                return redirect(url_for('conductor'))
            elif usuario['id_rol'] == 4:
                return redirect(url_for('padres'))

    return "Usuario o contraseña incorrectos"
    
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('inicio'))#retorna al home/pág inicio

# ==========================================
# GESTIÓN DE VEHÍCULOS Y RUTAS
# RESPONSABLE: CAMILO OCAMPO
# ==========================================
@app.route('/gestion_vehiculos')
def gestion_vehiculos():
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

@app.route('/gestion_rutas')
def gestion_rutas():
    return "<h2>Módulo de rutas en construcción</h2>"


#Aquí se desarrollarán las rutas relacionadas con:
#- Registro de estudiantes
#- Edición de estudiantes
#- Eliminación de estudiantes
#- Asignación de estudiantes a rutas
#- Consultar estudiantes por ruta
#- Listar estudiantes por conductor o ruta






# ==========================================
# EJECUCIÓN DE LA APLICACIÓN
# ==========================================

if __name__ == '__main__':
    app.run(debug=True)
