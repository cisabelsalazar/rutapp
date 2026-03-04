
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


-- INFORMACION BASE DE DATOS - PERMISOS DEL ROL
INSERT INTO `rutapp_bd`.`permiso` (`nombre_permiso`) VALUES ('Gestionar Estudiantes');
INSERT INTO `rutapp_bd`.`permiso` (`nombre_permiso`) VALUES ('Gestionar Vehículos');
INSERT INTO `rutapp_bd`.`permiso` (`nombre_permiso`) VALUES ('Gestionar Rutas');
INSERT INTO `rutapp_bd`.`permiso` (`nombre_permiso`) VALUES ('Generar Alertas');
INSERT INTO `rutapp_bd`.`permiso` (`nombre_permiso`) VALUES ('Recibir Alertas');
INSERT INTO `rutapp_bd`.`permiso` (`nombre_permiso`) VALUES ('Compartir Ruta');
INSERT INTO `rutapp_bd`.`permiso` (`nombre_permiso`) VALUES ('Monitorear Ruta');
INSERT INTO `rutapp_bd`.`permiso` (`nombre_permiso`) VALUES ('Crear Usuario');
INSERT INTO `rutapp_bd`.`permiso` (`nombre_permiso`) VALUES ('Modificar Usuario');
INSERT INTO `rutapp_bd`.`permiso` (`nombre_permiso`) VALUES ('Eliminar Usuario');

-- INFORMACION BASE DE DARTOS - ROLES
INSERT INTO `rutapp_bd`.`rol` (`nombre_rol`) VALUES ('Super Administrador');
INSERT INTO `rutapp_bd`.`rol` (`nombre_rol`) VALUES ('Administrador');
INSERT INTO `rutapp_bd`.`rol` (`nombre_rol`) VALUES ('Conductor');
INSERT INTO `rutapp_bd`.`rol` (`nombre_rol`) VALUES ('Padre de Familia');

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
INSERT INTO `rutapp_bd`.`rol_permiso` (`id_rol`, `id_permiso`) VALUES ('2', '1');
INSERT INTO `rutapp_bd`.`rol_permiso` (`id_rol`, `id_permiso`) VALUES ('2', '2');
INSERT INTO `rutapp_bd`.`rol_permiso` (`id_rol`, `id_permiso`) VALUES ('2', '3');
INSERT INTO `rutapp_bd`.`rol_permiso` (`id_rol`, `id_permiso`) VALUES ('2', '4');
INSERT INTO `rutapp_bd`.`rol_permiso` (`id_rol`, `id_permiso`) VALUES ('2', '5');
INSERT INTO `rutapp_bd`.`rol_permiso` (`id_rol`, `id_permiso`) VALUES ('2', '7');
INSERT INTO `rutapp_bd`.`rol_permiso` (`id_rol`, `id_permiso`) VALUES ('3', '4');
INSERT INTO `rutapp_bd`.`rol_permiso` (`id_rol`, `id_permiso`) VALUES ('3', '5');
INSERT INTO `rutapp_bd`.`rol_permiso` (`id_rol`, `id_permiso`) VALUES ('3', '6');
INSERT INTO `rutapp_bd`.`rol_permiso` (`id_rol`, `id_permiso`) VALUES ('4', '4');
INSERT INTO `rutapp_bd`.`rol_permiso` (`id_rol`, `id_permiso`) VALUES ('4', '5');
INSERT INTO `rutapp_bd`.`rol_permiso` (`id_rol`, `id_permiso`) VALUES ('4', '7');

-- select md5('12345') from dual;
INSERT INTO `rutapp_bd`.`usuario` (`id_usuario`, `nombre_usuario`, `hash_password`, `nombres_y_apellidos`, `correo`, `telefono`, `id_rol`) VALUES ('1', 'SUPERADMINISTRADOR', md5('12345'), 'Cristina Salazar', 'isabelsalazazar1589@gmial.com', '3164539219', '1');

