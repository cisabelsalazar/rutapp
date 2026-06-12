CREATE DATABASE rutapp_bd;
USE rutapp_bd;

DROP TABLE IF EXISTS ROL;

CREATE TABLE ROL(
	id_rol INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nombre_rol VARCHAR(50) NOT NULL UNIQUE
);

DROP TABLE IF EXISTS PERMISO;

CREATE TABLE PERMISO(
	id_permiso INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nombre_permiso VARCHAR(50) NOT NULL UNIQUE
);

DROP TABLE IF EXISTS ROL_PERMISO;

CREATE TABLE ROL_PERMISO(
	id_rol INT NOT NULL,
    id_permiso INT NOT NULL,
    PRIMARY KEY(id_rol, id_permiso),
    FOREIGN KEY (id_rol) REFERENCES ROL(id_rol) ON DELETE CASCADE,
    FOREIGN KEY (id_permiso) REFERENCES PERMISO(id_permiso) ON DELETE CASCADE
);

DROP TABLE IF EXISTS USUARIO;

CREATE TABLE USUARIO(
	id_usuario VARCHAR(20) NOT NULL PRIMARY KEY,
    nombre_usuario VARCHAR(50) NOT NULL UNIQUE,
	hash_password VARCHAR(255) NOT NULL,
    nombres_y_apellidos VARCHAR(100) NOT NULL,
    correo VARCHAR(100) NOT NULL UNIQUE,
    telefono VARCHAR(20) NOT NULL,
    id_rol INT NOT NULL,
    FOREIGN KEY (id_rol) REFERENCES ROL(id_rol)
);

DROP TABLE IF EXISTS VEHICULO;

CREATE TABLE VEHICULO(
id_vehiculo INT AUTO_INCREMENT PRIMARY KEY,
placa VARCHAR(10) NOT NULL UNIQUE,
marca VARCHAR(50) NOT NULL,
modelo VARCHAR(50) NOT NULL,
capacidad INT NOT NULL,
id_conductor VARCHAR(20) NOT NULL,
FOREIGN KEY (id_conductor) REFERENCES USUARIO(id_usuario)
);

DROP TABLE IF EXISTS RUTA;

CREATE TABLE RUTA(
	id_ruta INT AUTO_INCREMENT PRIMARY KEY,
    nombre_ruta VARCHAR(50) NOT NULL UNIQUE,
    descripcion_ruta VARCHAR(100) NOT NULL,
    hora_salida TIME NOT NULL,
    hora_llegada TIME NOT NULL,
    id_conductor VARCHAR(20) NOT NULL,
    id_administrador VARCHAR(20) NOT NULL,
    FOREIGN KEY (id_conductor) REFERENCES USUARIO(id_usuario),
    FOREIGN KEY (id_administrador) REFERENCES USUARIO(id_usuario)
);

DROP TABLE IF EXISTS ESTUDIANTE;

CREATE TABLE ESTUDIANTE(
	id_estudiante INT PRIMARY KEY NOT NULL,
    nombre VARCHAR(80) NOT NULL,
    grado VARCHAR(20) NOT NULL,
    direccion VARCHAR(100) NOT NULL,
    telefono VARCHAR(20),
    id_ruta INT NULL,
    FOREIGN KEY (id_ruta) REFERENCES RUTA(id_ruta) ON DELETE SET NULL
);

DROP TABLE IF EXISTS PADRE_ESTUDIANTE;

CREATE TABLE PADRE_ESTUDIANTE(
    id_padre VARCHAR(20) NOT NULL,
    id_estudiante INT NOT NULL,

    PRIMARY KEY (id_padre, id_estudiante),

    FOREIGN KEY (id_padre)
        REFERENCES USUARIO(id_usuario)
        ON DELETE CASCADE,

    FOREIGN KEY (id_estudiante)
        REFERENCES ESTUDIANTE(id_estudiante)
        ON DELETE CASCADE
-- id_padre debe corresponder a un usuario con id_rol = 4
);

DROP TABLE IF EXISTS ALERTAS;

CREATE TABLE ALERTAS(
    id_alerta INT AUTO_INCREMENT PRIMARY KEY,

    id_usuario_emisor VARCHAR(20) NOT NULL,
    id_usuario_receptor VARCHAR(20) NULL,

    id_estudiante INT NULL,
    id_ruta INT NULL,

    tipo_alerta VARCHAR(50) NOT NULL,
    mensaje TEXT NOT NULL,

    fecha_hora DATETIME DEFAULT CURRENT_TIMESTAMP,

    estado ENUM('nueva','leida','en_proceso','resuelta') DEFAULT 'nueva',
    prioridad ENUM('alta','media','baja') DEFAULT 'media',

    observacion_admin TEXT NULL,

    FOREIGN KEY (id_usuario_emisor) REFERENCES USUARIO(id_usuario),
    FOREIGN KEY (id_usuario_receptor) REFERENCES USUARIO(id_usuario),
    FOREIGN KEY (id_estudiante) REFERENCES ESTUDIANTE(id_estudiante),
    FOREIGN KEY (id_ruta) REFERENCES RUTA(id_ruta)
);

--- QUERY 
SELECT * FROM rol ORDER BY id_rol;
SELECT * FROM permiso ORDER BY id_permiso;
SELECT * FROM rol_permiso ORDER BY id_rol;
SELECT * FROM usuario ORDER BY id_usuario;
SELECT * FROM ruta ORDER BY id_ruta;
SELECT * FROM estudiante ORDER BY id_estudiante;
SELECT * FROM alertas ORDER BY id_alerta;
SELECT * FROM vehiculo ORDER BY id_vehiculo;


-- INFORMACION BASE DE DATOS - ROL
INSERT INTO `rutapp_bd`.`rol` (`id_rol`, `nombre_rol`) VALUES ('1', 'Super Administrador');
INSERT INTO `rutapp_bd`.`rol` (`id_rol`, `nombre_rol`) VALUES ('2', 'Administrador');
INSERT INTO `rutapp_bd`.`rol` (`id_rol`, `nombre_rol`) VALUES ('3', 'Conductor');
INSERT INTO `rutapp_bd`.`rol` (`id_rol`, `nombre_rol`) VALUES ('4', 'Padre de Familia');


-- INFORMACION BASE DE DATOS - PERMISOS DEL ROL
INSERT INTO `rutapp_bd`.`permiso` (`id_permiso`, `nombre_permiso`) VALUES ('1', 'Registro de Usuario');
INSERT INTO `rutapp_bd`.`permiso` (`id_permiso`, `nombre_permiso`) VALUES ('2', 'Inicio de Sesión');
INSERT INTO `rutapp_bd`.`permiso` (`id_permiso`, `nombre_permiso`) VALUES ('3', 'Gestionar Usuarios');
INSERT INTO `rutapp_bd`.`permiso` (`id_permiso`, `nombre_permiso`) VALUES ('4', 'Gestionar Estudiantes');
INSERT INTO `rutapp_bd`.`permiso` (`id_permiso`, `nombre_permiso`) VALUES ('5', 'Gestionar Vehículos');
INSERT INTO `rutapp_bd`.`permiso` (`id_permiso`, `nombre_permiso`) VALUES ('6', 'Gestionar Rutas');
INSERT INTO `rutapp_bd`.`permiso` (`id_permiso`, `nombre_permiso`) VALUES ('7', 'Compartir Ubicación');
INSERT INTO `rutapp_bd`.`permiso` (`id_permiso`, `nombre_permiso`) VALUES ('8', 'Visualizar Rutas');
INSERT INTO `rutapp_bd`.`permiso` (`id_permiso`, `nombre_permiso`) VALUES ('9', 'Monitorear Ruta en Tiempo Real');
INSERT INTO `rutapp_bd`.`permiso` (`id_permiso`, `nombre_permiso`) VALUES ('10', 'Gestión de Alertas');
INSERT INTO `rutapp_bd`.`permiso` (`id_permiso`, `nombre_permiso`) VALUES ('11', 'Visualizar Información de Ruta');
INSERT INTO `rutapp_bd`.`permiso` (`id_permiso`, `nombre_permiso`) VALUES ('12', 'Reportar Inasistencia');


-- INFORMACION BASE DE DATOS - ROL_PERMISO
INSERT INTO `rutapp_bd`.`rol_permiso` (`id_rol`, `id_permiso`) VALUES ('1', '1');
INSERT INTO `rutapp_bd`.`rol_permiso` (`id_rol`, `id_permiso`) VALUES ('1', '2');
INSERT INTO `rutapp_bd`.`rol_permiso` (`id_rol`, `id_permiso`) VALUES ('1', '3');
INSERT INTO `rutapp_bd`.`rol_permiso` (`id_rol`, `id_permiso`) VALUES ('1', '4');
INSERT INTO `rutapp_bd`.`rol_permiso` (`id_rol`, `id_permiso`) VALUES ('1', '5');
INSERT INTO `rutapp_bd`.`rol_permiso` (`id_rol`, `id_permiso`) VALUES ('1', '6');
INSERT INTO `rutapp_bd`.`rol_permiso` (`id_rol`, `id_permiso`) VALUES ('1', '7');
INSERT INTO `rutapp_bd`.`rol_permiso` (`id_rol`, `id_permiso`) VALUES ('1', '8');
INSERT INTO `rutapp_bd`.`rol_permiso` (`id_rol`, `id_permiso`) VALUES ('1', '9');
INSERT INTO `rutapp_bd`.`rol_permiso` (`id_rol`, `id_permiso`) VALUES ('1', '10');
INSERT INTO `rutapp_bd`.`rol_permiso` (`id_rol`, `id_permiso`) VALUES ('1', '11');
INSERT INTO `rutapp_bd`.`rol_permiso` (`id_rol`, `id_permiso`) VALUES ('1', '12');
INSERT INTO `rutapp_bd`.`rol_permiso` (`id_rol`, `id_permiso`) VALUES ('2', '1');
INSERT INTO `rutapp_bd`.`rol_permiso` (`id_rol`, `id_permiso`) VALUES ('2', '2');
INSERT INTO `rutapp_bd`.`rol_permiso` (`id_rol`, `id_permiso`) VALUES ('2', '3');
INSERT INTO `rutapp_bd`.`rol_permiso` (`id_rol`, `id_permiso`) VALUES ('2', '4');
INSERT INTO `rutapp_bd`.`rol_permiso` (`id_rol`, `id_permiso`) VALUES ('2', '5');
INSERT INTO `rutapp_bd`.`rol_permiso` (`id_rol`, `id_permiso`) VALUES ('2', '6');
INSERT INTO `rutapp_bd`.`rol_permiso` (`id_rol`, `id_permiso`) VALUES ('2', '8');
INSERT INTO `rutapp_bd`.`rol_permiso` (`id_rol`, `id_permiso`) VALUES ('2', '9');
INSERT INTO `rutapp_bd`.`rol_permiso` (`id_rol`, `id_permiso`) VALUES ('2', '10');
INSERT INTO `rutapp_bd`.`rol_permiso` (`id_rol`, `id_permiso`) VALUES ('2', '11');
INSERT INTO `rutapp_bd`.`rol_permiso` (`id_rol`, `id_permiso`) VALUES ('3', '2');
INSERT INTO `rutapp_bd`.`rol_permiso` (`id_rol`, `id_permiso`) VALUES ('3', '7');
INSERT INTO `rutapp_bd`.`rol_permiso` (`id_rol`, `id_permiso`) VALUES ('3', '9');
INSERT INTO `rutapp_bd`.`rol_permiso` (`id_rol`, `id_permiso`) VALUES ('3', '10');
INSERT INTO `rutapp_bd`.`rol_permiso` (`id_rol`, `id_permiso`) VALUES ('4', '2');
INSERT INTO `rutapp_bd`.`rol_permiso` (`id_rol`, `id_permiso`) VALUES ('4', '9');
INSERT INTO `rutapp_bd`.`rol_permiso` (`id_rol`, `id_permiso`) VALUES ('4', '10');
INSERT INTO `rutapp_bd`.`rol_permiso` (`id_rol`, `id_permiso`) VALUES ('4', '11');
INSERT INTO `rutapp_bd`.`rol_permiso` (`id_rol`, `id_permiso`) VALUES ('4', '12');


-- select md5('12345') from dual;
INSERT INTO `rutapp_bd`.`usuario` (`id_usuario`, `nombre_usuario`, `hash_password`, `nombres_y_apellidos`, `correo`, `telefono`, `id_rol`) VALUES ('1', 'SuperAdministrador', md5('12345'), 'Cristina Salazar', 'isabelsalazar1589@gmail.com', '3164539219', '1');
