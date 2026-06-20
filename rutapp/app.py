# RUTAPP - APLICACIÓN DE GESTIÓN DE RUTAS ESCOLARES
# Desarrollada por: Cristina Salazar, Camilo Ocampo, Victor Velandia

#==================================================
# IMPORTACIÓN DE LIBRERÍAS 
#==================================================

from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector

from werkzeug.security import generate_password_hash, check_password_hash
import hashlib

#==========================================
# CONFIGURACIÓN DE LA APLICACIÓN FLASK
#==========================================

app = Flask(__name__)
app.secret_key = "rutapp_secreto"   # Clave secreta para manejar sesiones y flash messages en Flask

#==================================================
# CONFIGURACIÓN DE LA CONEXIÓN A LA BASE DE DATOS
#==================================================

conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Cristina+-2026",
    database="rutapp_bd"
)

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
        4: 'Padre de Familia'           
    }

    rol = session.get('rol') # Obtiene el rol del usuario desde la sesión

    return {
        'nombre_panel' : nombres_roles.get(rol, 'Usuario'), # Devuelve el nombre del panel según el rol, o 'Usuario' si no se encuentra
        'nombre_completo' : session.get('nombre_completo') # Devuelve el nombre completo del usuario desde la sesión
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

# ==========================================
# AUTENTICACIÓN
# ==========================================

# Ruta principal
@app.route('/')
def inicio():
    return render_template('mod_admin/login.html')


# Ruta login
@app.route('/login')
def login():
    return render_template('mod_admin/login.html')

# ==========================================
# VALIDACIÓN LOGIN
# ==========================================

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
            session['nombre_completo'] = usuario['nombres_y_apellidos']


            if usuario['id_rol'] == 1:
                return redirect(url_for('superadministrador'))
            elif usuario['id_rol'] == 2:
                return redirect(url_for('administrador'))
            elif usuario['id_rol'] == 3:
                return redirect(url_for('conductor'))
            elif usuario['id_rol'] == 4:
                return redirect(url_for('padres'))

    return "Usuario o contraseña incorrectos"

#===========================================
# RUTA PARA RECUPERAR CONTRASEÑA
#===========================================

@app.route('/recuperar_password')
def recuperar_password():
    return render_template('mod_admin/recuperar_password.html')

#============================================
#RUTA PARA BUSCAR SI EXISTE CORREO DE USUARIO
#============================================ 

@app.route('/buscar_correo', methods=['POST'])
def buscar_correo():
    
    correo = request.form['email']

    cursor = conexion.cursor(dictionary=True)

    consulta = """
    SELECT * FROM usuario WHERE correo = %s
    """

    cursor.execute(consulta, (correo,))
    correo_usuario =cursor.fetchone()
    cursor.close()

    if correo_usuario:
        session['correo_recuperacion'] = correo #GUARDA EL CORREO
        return redirect(url_for('nueva_password'))

    else: 
        return "Correo no registrado"
    
#===========================================
# RUTA PARA CREAR NUEVA CONTRASEÑA
#===========================================

@app.route('/nueva_password')
def nueva_password():
    return render_template('mod_admin/nueva_password.html')

#===========================================
# RUTA PARA ACTUALIZAR CONTRASEÑA
#===========================================

@app.route('/actualizar_password', methods=['POST'])
def actualizar_password():

    cursor = conexion.cursor(dictionary=True)

    correo = session['correo_recuperacion']

    nueva_password = request.form['password']
    confirmar_password = request.form['confirmar_password']


    if nueva_password == confirmar_password:
        hash_password = generate_password_hash(nueva_password)

       
        sql = """
        UPDATE usuario
        SET hash_password = %s
        WHERE correo = %s
        """

        valores = (hash_password, correo)

        cursor.execute(sql, valores)
        conexion.commit()

        session.pop('correo_recuperacion', None)

        cursor.close()

        flash('La contraseña fue actualizada correctamente', 'success')
        return redirect(url_for('login'))   
    
    else: 
        flash('Las contraseñas no coinciden', 'error')
        return redirect(url_for('nueva_password'))
        


# ==========================================
# LOGOUT
# ==========================================

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('inicio'))#retorna al home/pág inicio

# ==========================================
# PANELES DEL SISTEMA
# ==========================================

# ==========================================
# PANEL SUPERADMINISTRADOR
# ==========================================

@app.route('/supadmin')
def superadministrador():

    estadisticas = obtener_estadisticas_dashboard() # Llama a la función para obtener las estadísticas del dashboard
    

    if 'usuario' not in session:
        return redirect(url_for('login'))

    if session['rol'] != 1:
        return 'Acceso no autorizado 1'
    
    return render_template(
        'mod_admin/supadmin.html',
        **estadisticas # Desempaqueta el diccionario de estadísticas para pasarlo a la plantilla
    )


# ==========================================
# PANEL ADMINISTRADOR
# ==========================================

@app.route('/admin')
def administrador():

    estadisticas = obtener_estadisticas_dashboard() # Llama a la función para obtener las estadísticas del dashboard

    if 'usuario' not in session:
        return redirect(url_for('login')) #Si no hay sesión iniciada regresa al login
    
    if session['rol'] != 2:
        return f"Acceso no autorizado 2 | {session['rol']} |"
    
    return render_template(
        'mod_admin/admin.html',
        **estadisticas # Desempaqueta el diccionario de estadísticas para pasarlo a la plantilla
    )

#===========================================
# RUTA PARA VALIDACION ROL EN DASHBOARD
#==========================================

@app.route('/dashboard')
def dashboard():

    if 'usuario' not in session:
        return redirect(url_for('login'))
    
    if session['rol'] == 1:
        return redirect(url_for('superadministrador'))
    
    if session['rol'] == 2:
        return redirect(url_for('administrador'))
    
    return redirect(url_for('login'))

# ==========================================
# FUNCION PARA ESTADISTICAS DASHBOARD
# ==========================================

def obtener_estadisticas_dashboard():

    cursor = conexion.cursor(dictionary=True)
# ==========================
# ESTADÍSTICAS GENERALES
# ==========================

    cursor.execute("""
    SELECT  COUNT(*) AS total_usuarios
    FROM usuario 
    """)
    total_usuarios = cursor.fetchone()['total_usuarios']

    cursor.execute("""
    SELECT COUNT(*) AS total_vehiculos
    FROM vehiculo
    """)
    total_vehiculos = cursor.fetchone()['total_vehiculos']

    cursor.execute("""
    SELECT COUNT(*) AS total_rutas
    FROM ruta
    """)
    total_rutas = cursor.fetchone()['total_rutas']

    cursor.execute("""
    SELECT COUNT(*) AS total_estudiantes
    FROM estudiante
    """)
    total_estudiantes = cursor.fetchone()['total_estudiantes']
# ==========================
# VEHICULOS
# ==========================

    cursor.execute("""
    SELECT COUNT(*) AS vehiculos_disponibles
    FROM vehiculo
    WHERE ESTADO = 'disponible'
    """)
    vehiculos_disponibles = cursor.fetchone()['vehiculos_disponibles']

# ==========================
# RUTAS
# ==========================

    cursor.execute("""
    SELECT COUNT(*) AS rutas_activas
    FROM ruta
    WHERE ESTADO = 'activa'
    """)
    rutas_activas = cursor.fetchone()['rutas_activas']

#=========================
# ALERTAS
#=========================

    cursor.execute("""
    SELECT COUNT(*) AS alertas_pendientes
    FROM alertas
    WHERE estado = 'nueva' OR estado = 'en proceso'
    """)
    alertas_pendientes = cursor.fetchone()['alertas_pendientes']

    cursor.close()

    return {
        'total_usuarios': total_usuarios,
        'total_vehiculos': total_vehiculos,
        'total_rutas': total_rutas,
        'total_estudiantes': total_estudiantes,
        'vehiculos_disponibles': vehiculos_disponibles,
        'rutas_activas': rutas_activas,
        'alertas_pendientes': alertas_pendientes
    }

# ==========================================
# MÓDULO USUARIOS
# ==========================================

# ==========================================
# LISTAR USUARIOS
# ==========================================

@app.route('/usuarios') #Esta es la ruta Usuarios
def usuarios(): #Esta es la función de Usuarios

    # Captura el rol seleccionado desde el filtro
    rol_actual = request.args.get("rol")


    if 'usuario' not in session: #Aqui se hace la verificación de sesión
        return redirect(url_for('mod_admin/login'))#Regresa al home
    
    if session['rol'] not in [1, 2, 3, 4]:# Aqui se verifica el rol del usuario
        return "Acceso no autorizado"
    
    botones = [
    {
        "texto": "Volver",
        "url": obtener_url_volver(),
        "class": "btn-secondary"
    },
    {
        "texto": "Nuevo usuario",
        "url": url_for("crear_usuario"),
        "class": "btn-primary"
    }
]
    
    cursor = conexion.cursor(dictionary=True)#Cursor creado para interactuar con MySQL

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

    return render_template(
        'mod_admin/usuarios.html',
        usuarios = lista_usuarios,
        botones=botones,
        rol_actual=rol_actual
    )#Manda la lista a usuarios.html

# ==========================================
# FORMULARIO CREAR USUARIO
# ==========================================

@app.route('/crear_usuario')
def crear_usuario():
    return render_template('mod_admin/crear_usuarios.html')

# ==========================================
# GUARDAR NUEVO USUARIO
# ==========================================

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

        flash('Usuario guardado correctamente', 'success')
        return redirect(url_for('usuarios'))
        


# ==========================================
# EDITAR USUARIO
# ==========================================

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


         # VALIDACIÓN LONGITUD DE CAMPOS
        if len(nombres) > 30:
            return "El nombre de usuario no puede superar 30 caracteres"

        if len(correo) > 50:
            return "El correo no puede superar 50 caracteres"

        if len(telefono) > 10:
            return "El teléfono no puede superar 10 caracteres"

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
# ELIMINAR USUARIO
# ==========================================

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

# ==========================================
# MODULO ESTUDIANTES
# ==========================================

#===========================================
# LISTAR ESTUDIANTES
#===========================================

@app.route('/gestion_estudiantes')
def gestion_estudiantes():

    ruta_actual = request.args.get("ruta")
    grado_actual = request.args.get("grado")
    conductor_actual = request.args.get("conductor")

    if 'usuario' not in session:
        return redirect(url_for('login'))
    
    if session['rol'] not in [1, 2]:
        return "Acceso no autorizado"
    
    botones = [
    {
        "texto": "Volver",
        "url": obtener_url_volver(),
        "class": "btn-secondary"
    },
    {
        "texto": "Crear estudiante",
        "url": url_for("crear_estudiante"),
        "class": "btn-primary"
    }
]
    
    cursor = conexion.cursor(dictionary=True)

    # ===== CONSULTA PARA OBTENER RUTAS ESCOLARES =====
    cursor.execute("SELECT nombre_ruta FROM ruta")

    rutas = cursor.fetchall()

    consulta = """
    SELECT e.id_estudiante,
           e.nombre,
           e.grado,
           e.direccion,
           e.telefono,
           e.id_ruta,
           r.nombre_ruta,
           p.nombres_y_apellidos AS padre_familia
    FROM estudiante e
    LEFT JOIN ruta r 
        ON e.id_ruta = r.id_ruta

    LEFT JOIN padre_estudiante pe   
        ON e.id_estudiante = pe.id_estudiante

    LEFT JOIN usuario p
        ON pe.id_padre = p.id_usuario
    WHERE 1=1
    """

    parametros = []

    if ruta_actual:
        consulta += " AND r.nombre_ruta = %s"
        parametros.append(ruta_actual)

    if grado_actual:
        consulta += " AND e.grado = %s"
        parametros.append(grado_actual)
    
    if conductor_actual:
        consulta += " AND r.id_conductor = %s"
        parametros.append(conductor_actual)

    consulta += " ORDER BY e.nombre DESC"

    cursor.execute(consulta, parametros)
    lista_estudiantes = cursor.fetchall()
    cursor.close()

    return render_template(
        'mod_admin/estudiantes.html',
        estudiantes = lista_estudiantes,
        botones = botones,
        rutas = rutas,
        ruta_actual = ruta_actual,
        grado_actual = grado_actual,
        conductor_actual = conductor_actual
    )

#===========================================
# FORMULARIO CREAR ESTUDIANTE
#===========================================

@app.route('/crear_estudiante')
def crear_estudiante():

    cursor = conexion.cursor(dictionary=True)

    cursor.execute("SELECT * FROM ruta") # Selecciona ruta escolar para asignar
    rutas = cursor.fetchall()

    cursor.execute("""
        SELECT id_usuario, nombres_y_apellidos
        FROM usuario
        WHERE id_rol = 4
        ORDER BY nombres_y_apellidos
    """) # Selecciona padres de familia para asignar

    padres = cursor.fetchall()

    cursor.close()
    
    return render_template(
        'mod_admin/crear_estudiante.html',
        rutas = rutas,
        padres = padres
    )



#===========================================
# GUARDAR ESTUDIANTE
#===========================================

@app.route('/guardar_estudiante', methods=['POST'])
def guardar_estudiante():

        id_estudiante = request.form['id_estudiante']
        nombre= request.form['nombre']
        grado= request.form['grado']
        direccion= request.form['direccion']
        telefono= request.form['telefono']
        id_ruta= request.form['id_ruta']
        id_padre = request.form['id_padre']


        if len(id_estudiante) > 10:
            return "El número de identificación no puede superar 10 caracteres"
        if len(nombre) > 30:
            return "El nombre de estudiante no puede superar los 30 caracteres"
        if len(grado) > 5:
            return "El grado no puede superar 5 caracteres"
        if len(direccion) > 30:
            return "La dirección no puede superar los 30 caracteres"
        if len(telefono) > 10:
            return "El teléfono no puede superar los 10 caracteres"
        

        #CONEXION Y VALIDACION EN BASE DE DATOS
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

        sql_padre= """
        INSERT INTO padre_estudiante
        (id_padre, id_estudiante)
        VALUES (%s, %s)
        """
    
        cursor.execute(sql_padre, (id_padre, id_estudiante))

        conexion.commit()
        cursor.close()
        flash('Estudiante guardado correctamente', 'success')

        return redirect(url_for('gestion_estudiantes')) 

#===========================================
# EDITAR ESTUDIANTE
#===========================================

# - GET  -> muestra el formulario con los datos actuales
# - POST -> guarda los cambios realizados en la BD
@app.route('/editar_estudiante/<id_estudiante>', methods=['GET', 'POST'])
def editar_estudiante(id_estudiante):


    cursor = conexion.cursor(dictionary=True) # Crear cursor en formato diccionario para acceder por nombre de campo
    
    cursor.execute("SELECT * FROM ruta") # Selecciona ruta escolar para asignar
    rutas = cursor.fetchall()
    
    cursor.execute("""
        SELECT id_usuario, nombres_y_apellidos
        FROM usuario
        WHERE id_rol = 4
        ORDER BY nombres_y_apellidos
    """) # Selecciona padres de familia para asignar

    padres = cursor.fetchall()

    # POST guardar cambios
    if request.method == 'POST': # POST: cuando el usuario da clic en "Guardar cambios"

        # Captura los datos enviados desde el formulario HTML
        nombre = request.form['nombre']
        grado = request.form['grado']
        direccion = request.form['direccion']
        telefono = request.form['telefono']
        id_ruta = request.form['id_ruta']
        id_padre = request.form['id_padre']

        #VALIDACION LONGITUD DE CAMPOS
        if len(nombre) > 30:
            return "El nombre de estudiante no puede superar los 30 caracteres"
        if len(grado) > 5:
            return "El grado no puede superar 5 caracteres"
        if len(direccion) > 30:
            return "La dirección no puede superar los 30 caracteres"
        if len(telefono) > 10:
            return "El teléfono no puede superar los 10 caracteres"

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

        cursor.execute(sql, valores, rutas)

        # Verificar si ya existe relación padre-estudiante
        cursor.execute("""
            SELECT *
            FROM padre_estudiante
            WHERE id_estudiante = %s
        """, (id_estudiante,))

        relacion = cursor.fetchone()

        if relacion:

            # Actualiza la relación existente
            sql_padre = """
            UPDATE padre_estudiante
            SET id_padre = %s
            WHERE id_estudiante = %s
            """

            cursor.execute(sql_padre, (id_padre, id_estudiante))

        else:

            # Crea la relación si no existe
            sql_padre = """
            INSERT INTO padre_estudiante
            (id_padre, id_estudiante)
            VALUES (%s, %s)
            """

        cursor.execute(sql_padre, (id_padre, id_estudiante))

        conexion.commit()
        cursor.close()

        flash('Informacion actualizada correctamente', 'success')
        return redirect(url_for('gestion_estudiantes'))

    #GET: Cargar formulario
    sql = "SELECT * FROM estudiante WHERE id_estudiante = %s" # Consulta para obtener los datos actuales del estudiante
    cursor.execute(sql, (id_estudiante,))
    estudiante = cursor.fetchone()

    cursor.execute("""
        SELECT id_padre
        FROM padre_estudiante
        WHERE id_estudiante = %s
    """, (id_estudiante,))

    relacion = cursor.fetchone()

    padre_actual = None

    if relacion:
        padre_actual = relacion['id_padre']

    cursor.close() #Cierra el cursor

    if not estudiante: #validacion por si no existe el estudiante
        return "Estudiante no encontrado", 404
    
    ruta_volver = {
        1: 'superadministrador',
        2: 'administrador'
    }.get(session['rol'])

    return render_template(
        'mod_admin/editar_estudiante.html', # Renderiza el formulario de edición con los datos actuales del estudiante
        ruta_volver=ruta_volver, 
        estudiante=estudiante,
        rutas = rutas,
        padres = padres,
        padre_actual = padre_actual
    ) # Envía los datos al formulario editar_estudiante.html

#===========================================
# ELIMINAR ESTUDIANTES
#===========================================

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

#===========================================
# MODULO ALERTAS
#===========================================

#===========================================
# GESTION DE ALERTAS
#===========================================

@app.route('/gestion_alerta')#Rura gestion de alertas Modulo admin y supadmin
def gestion_alerta():#función para mostrar las alertas en el panel del admin y supadmin

    estado_actual = request.args.get("estado")

    if 'usuario' not in session:
        return redirect(url_for('login'))

    if session['rol'] not in [1, 2]:
        return "Acceso no autorizado"
    
    # estado = request.args.get('estado') #Captura el estado
    
    botones = [
    {
        "texto": "Volver",
        "url": obtener_url_volver(),
        "class": "btn-secondary"
    },

]

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
    """

    parametros = []

    if estado_actual:
        consulta += " WHERE a.estado = %s"
        parametros.append(estado_actual)

    consulta += " ORDER BY a.fecha_hora DESC"


    cursor.execute(consulta, parametros) #Ejecuta la consulta SQL
    alertas = cursor.fetchall() #Trae todas las alertas obtenidas de la consulta
    cursor.close() #Cierra el cursor

    return render_template(
        'mod_admin/alertas.html', 
        alertas = alertas,
        botones = botones,
        estado_actual = estado_actual
    ) #Renderiza la plantilla gestion_alerta.html y le pasa la lista de alertas obtenida de la consulta


#===========================================
# EDITAR ALERTAS (mod admin y supadmin)
#===========================================

@app.route('/editar_alerta/<id_alerta>', methods=['POST'])
def editar_alerta(id_alerta):
    cursor = conexion.cursor()

    estado = request.form.get('estado')
    observacion = request.form.get('observacion_admin')

    consulta_update = """
        UPDATE ALERTAS
        SET estado = %s,
            observacion_admin = %s
        WHERE id_alerta = %s
    """

    cursor.execute(consulta_update, (estado, observacion, id_alerta))
    conexion.commit()
    cursor.close()

    flash('Alerta gestionada correctamente', 'success')

    return redirect(url_for('gestion_alerta'))
    


#===========================================
# GESTIONAR ALERTAS (Panel conductor)
#===========================================

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



#===========================================
# GESTIONAR  ALERTAS (Panel padres)
#===========================================

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


# ==========================================
# MODULO CONDUCTOR
# ==========================================

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

#============================================
# Ruta para visualisar estudiantes en el panel conductor
#=============================================

@app.route('/conductor/estudiantes')
def estudiantes_conductor():
    
    cursor = conexion.cursor(dictionary=True) # Importante: dictionary=True
    # Consulta para traer alertas con datos de los estudiantes y rutas
    
    consulta = """
    SELECT 
      nombre,
      grado,
      direccion,
      telefono,
      id_ruta,
      estado
      FROM estudiante
    """
    cursor.execute(consulta)
    
    # Obtenemos los datos
    estudiantes_bd = cursor.fetchall()
    

    # Pasamos la variable al HTML
    return render_template(
        'mod_conductor/estudiantes_conductor.html', 
        estudiantes_bd=estudiantes_bd)

#==============================================
#======== Ruta para abordar estudiante=========#
#==============================================

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
    # Redirige de nuevo a la lista
    return redirect(url_for('estudiantes_conductor'))

# ==========================================
# MODULO PADRES DE FAMILIA
# ==========================================
@app.route('/padres')
def padres():

    # if 'usuario' not in session:
    #     return redirect(url_for('login'))
    
    # if session['rol'] != 4:
    #     return "Acceso no autorizado"
    
    return render_template('mod_padres/padre.html')


# ==========================================
# GESTIONAR REPORTE INASISTENCIA
# ==========================================

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

# ==========================================
# VER INFORMACION CONDUCTOR
# ==========================================

#=========================================
#======== Ruta para información conductor (padres)=========
#=========================================

@app.route('/padres/informacion_conductor')
def informacion_conductor():

    cursor = conexion.cursor(dictionary=True, buffered=True)
    
# Consulta SQL para obtener la información del conductor
    consulta = """
    SELECT
        u.nombres_y_apellidos AS nombre,
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
    WHERE e.id_ruta = 7;
    """

    
    cursor.execute(consulta)
    conductor = cursor.fetchone()
    cursor.close()

        # Renderiza el HTML y pasa los datos
    return render_template(
        'mod_padres/informacion_conductor.html',
        conductor=conductor
    )



# ==========================================
# VER ESTUDIANTE
# ==========================================

@app.route('/estudiantes_padre')
def estudiantes_padre():
    return "<h2>Módulo de rutas en construcción</h2>"
# ==========================================
# VER RECORRIDO RUTA ESCOLAR
# ==========================================

@app.route('/padres/ver_ruta')
def ver_ruta():
    return render_template('mod_padres/ver_ruta.html')


# ==========================================
# MODULO VEHÍCULOS Y RUTAS
# RESPONSABLE: Desarrollo CRISTINA SALAZAR
# ==========================================
@app.route('/gestion_vehiculos')
def gestion_vehiculos():

    placa_actual = request.args.get("placa")
    conductor_actual = request.args.get("conductor")
    estado_actual = request.args.get("estado")

    if 'usuario' not in session:
        return redirect(url_for('login'))
    
    if session['rol'] not in [1, 2]:
        return "Acceso no autorizado"
    
    botones = [
    {
        "texto": "Volver",
        "url": obtener_url_volver(),
        "class": "btn-secondary"
    },
    {
        "texto": "Crear vehículo",
        "url": url_for("crear_vehiculo"),
        "class": "btn-primary"
    }
]
    
    cursor = conexion.cursor(dictionary=True)

    # ===== CONSULTA PARA OBTENER INFO VEHICULOS =====

    consulta = """
    SELECT v.id_vehiculo,
           v.placa,
           v.marca,
           v.modelo,
           v.capacidad,
           v.id_conductor,
           v.estado,
           c.nombres_y_apellidos AS conductor_nombre,
           r.nombre_ruta AS nombre_ruta
    FROM vehiculo v
    LEFT JOIN usuario c
        ON v.id_conductor = c.id_usuario
    LEFT JOIN ruta r
        ON v.id_vehiculo = r.id_vehiculo

    WHERE 1=1
    """

    parametros = []

    if placa_actual:
        consulta += " AND v.placa = %s"
        parametros.append(placa_actual)

    
    if conductor_actual:
        consulta += " AND c.nombres_y_apellidos = %s"
        parametros.append(conductor_actual)

    if estado_actual:
        consulta += " AND v.estado = %s"
        parametros.append(estado_actual)

    consulta += " ORDER BY v.id_vehiculo DESC"

    cursor.execute(consulta, parametros)
    lista_vehiculos = cursor.fetchall()
    cursor.close()


    return render_template(
        'mod_admin/vehiculos.html',
        vehiculos = lista_vehiculos,
        botones = botones,
        placa_actual = placa_actual,
        conductor_actual = conductor_actual,
        estado_actual = estado_actual
    )

#===========================================
# FORMULARIO CREAR VEHICULO
#===========================================

@app.route('/crear_vehiculo')
def crear_vehiculo():

    cursor = conexion.cursor(dictionary=True)

    cursor.execute("""
        SELECT id_usuario, nombres_y_apellidos
        FROM usuario
        WHERE id_rol = 3
        ORDER BY nombres_y_apellidos
    """)  #Selecciona conductor para asignar

    conductores = cursor.fetchall()
    
    cursor.execute("""
        SELECT estado
        FROM vehiculo
    """)  #Selecciona estados para asignar

    estados = cursor.fetchall()

    cursor.close()

    return render_template(
        'mod_admin/crear_vehiculo.html',
        conductores=conductores,
        estados=estados
    )


#===========================================
# GUARDAR VEHICULO
#===========================================

@app.route('/guardar_vehiculo', methods=['POST'])
def guardar_vehiculo():

        placa= request.form['placa']
        marca= request.form['marca']
        modelo= request.form['modelo']
        capacidad= request.form['capacidad'] 
        id_conductor= request.form['id_conductor']
        estado= request.form['estado']



        if len(placa) > 8:
            return "La placa del vehículo no puede superar los 8 caracteres"
        if len(marca) > 20:
            return "La marca del vehículo no puede superar 20 caracteres"
        if len(modelo) > 30:
            return "El modelo del vehículo no puede superar los 30 caracteres"
        if len(capacidad) > 10:
            return "La capacidad del vehículo no puede superar los 10 caracteres"
        if len(id_conductor) > 10:
            return "El número de identificacion no puede superar los 10 caracteres"
        if len(estado) > 20:
            return "El estado del vehículo no puede superar los 20 caracteres"
        

        #CONEXION Y VALIDACION EN BASE DE DATOS
        cursor =conexion.cursor()

        # Valida placa dubplicado
        cursor.execute ("SELECT * FROM vehiculo WHERE placa = %s", (placa,))
        if cursor.fetchone():
            return "Ya existe un vehículo con este número de placa"
            
        sql = """
        INSERT INTO vehiculo
        (placa, marca, modelo, capacidad, id_conductor, estado)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        valores = (placa, marca, modelo, capacidad, id_conductor, estado)

        cursor.execute(sql, valores)

        conexion.commit()
        cursor.close()
        flash('Vehículo guardado correctamente', 'success')

        return redirect(url_for('gestion_vehiculos')) 

#===========================================
# EDITAR VEHICULO
#===========================================

# - GET  -> muestra el formulario con los datos actuales
# - POST -> guarda los cambios realizados en la BD
@app.route('/editar_vehiculo/<int:id_vehiculo>', methods=['GET', 'POST'])
def editar_vehiculo(id_vehiculo):

    cursor = conexion.cursor(dictionary=True) # Crear cursor en formato diccionario para acceder por nombre de campo
    
    # =========================
    # GET: datos del vehículo
    # =========================

    #Buscar el vehículo a editar
    cursor.execute("""
        SELECT *
        FROM vehiculo
        WHERE id_vehiculo = %s
    """, (id_vehiculo,))

    vehiculo = cursor.fetchone()

    if not vehiculo: #validacion por si no existe el vehículo
        cursor.close()
        return "Vehículo no encontrado", 404

    # Buscar conductores para asignar
    cursor.execute("""
        SELECT id_usuario, nombres_y_apellidos
        FROM usuario
        WHERE id_rol = 3
        ORDER BY nombres_y_apellidos
    """)  #Selecciona conductor para asignar

    conductores = cursor.fetchall()

    # =========================
    # POST: actualizar
    # =========================

    if request.method == 'POST': # POST: cuando el usuario da clic en "Guardar cambios"


        placa = request.form['placa']
        marca = request.form['marca']
        modelo = request.form['modelo']
        capacidad = request.form['capacidad']
        id_conductor = request.form['id_conductor']
        estado = request.form['estado']

                #VALIDACION LONGITUD DE CAMPOS
        if len(placa)>8:
            return "La placa del vehículo no puede superar 8 caracteres"
        if len(marca)>20:
            return "La marca del vehículo no puede superar los 8 caracteres"
        if len(modelo)>20:
            return "El modelo del vehículo no puede superar los 20 caracteres"
        if len(capacidad)>2:
            return "La capacidad del vehículo no puede superar los 2 caracteres"
        if len(id_conductor)>10:
            return "El id del conductor no puede superar 10 caracteres"
        if len(estado)>20:
            return "El estado no puede superar 20 caracteres"
            

        # validar si el conductor ya está asignado a otro vehículo
        cursor.execute("""
            SELECT id_vehiculo
            FROM vehiculo
            WHERE id_conductor = %s
            AND id_vehiculo != %s
        """, (id_conductor, id_vehiculo))

        vehiculo_existente = cursor.fetchone()

        if vehiculo_existente:
            flash("Este conductor ya está asignado a otro vehículo", "error")
            return redirect(url_for('editar_vehiculo', id_vehiculo=id_vehiculo))
            
        #Consulta SQL para actualizar la información del vehículo.

        sql = """
        UPDATE vehiculo
        SET placa = %s,
            marca = %s,
            modelo = %s,
            capacidad = %s,
            id_conductor = %s,
            estado = %s
        WHERE id_vehiculo = %s
        """

        valores = (placa, marca, modelo, capacidad, id_conductor, estado, id_vehiculo)

        cursor.execute(sql, valores)

        conexion.commit()

        flash('Informacion actualizada correctamente', 'success')
        return redirect(url_for('gestion_vehiculos'))


    # =========================
    # GET render
    # =========================

    ruta_volver = {
        1: 'superadministrador',
        2: 'administrador'
    }.get(session['rol'])


    cursor.close() #Cierra el cursor

    return render_template(
        'mod_admin/editar_vehiculo.html', # Renderiza el formulario de edición con los datos actuales del vehículo
        vehiculo=vehiculo,
        conductores = conductores,
        ruta_volver=ruta_volver
    ) # Envía los datos al formulario editar_vehiculo.html

#===========================================
# ELIMINAR VEHICULO
#===========================================

# - Elimina un estudiante de la base de datos
# - Se ejecuta únicamente mediante método POST por seguridad
@app.route('/eliminar_vehiculo/<id_vehiculo>', methods=['POST'])
def eliminar_vehiculo(id_vehiculo):

    cursor = conexion.cursor() # Crear cursor

    if request.method == 'POST':

        sql = "DELETE FROM vehiculo WHERE id_vehiculo = %s"# Consulta SQL para eliminar vehículo
        cursor.execute(sql, (id_vehiculo,))# Ejecutar la consulta
        conexion.commit() # Guardar cambios en la base de datos
        cursor.close() # Cerrar cursor
        flash('Vehículo eliminado correctamente', 'success')

    return redirect(url_for('gestion_vehiculos')) # Redirigir a la lista de estudiantes


#===========================================
# MONITOREAR RUTA
#===========================================

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
# EJECUCIÓN DE LA APLICACIÓN
# ==========================================

if __name__ == '__main__':
    app.run(debug=True)
