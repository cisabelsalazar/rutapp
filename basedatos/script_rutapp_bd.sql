
CREATE DATABASE rutapp_bd;
USE rutapp_bd;

CREATE TABLE ROL(
	id_rol INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nombre_rol VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE PERMISO(
	id_permiso INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nombre_permiso VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE ROL_PERMISO(
	id_rol INT NOT NULL,
    id_permiso INT NOT NULL,
    PRIMARY KEY(id_rol, id_permiso),
    FOREIGN KEY (id_rol) REFERENCES ROL(id_rol) ON DELETE CASCADE,
    FOREIGN KEY (id_permiso) REFERENCES PERMISO(id_permiso) ON DELETE CASCADE
);

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

-- INFORMACION BASE - PERMISOS DEL ROL
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

-- INFORMACION BASE - ROLES
INSERT INTO `rutapp_bd`.`rol` (`nombre_rol`) VALUES ('Super Administrador');
INSERT INTO `rutapp_bd`.`rol` (`nombre_rol`) VALUES ('Administrador');
INSERT INTO `rutapp_bd`.`rol` (`nombre_rol`) VALUES ('Conductor');
INSERT INTO `rutapp_bd`.`rol` (`nombre_rol`) VALUES ('Padre de Familia');

-- INFORMACION BASE - ROL_PERMISO
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
INSERT INTO `rutapp_bd`.`usuario` (`id_usuario`, `nombre_usuario`, `hash_password`, `nombres_y_apellidos`, `correo`, `telefono`, `id_rol`) VALUES ('1', 'SUPERADMINISTRADOR', md5('12345'), 'Cristina Salazar', 'isabelsalazazar1589@gmialicom', '3164539219', '1');

