-- Base de datos para Horizontes San Miguel
-- MySQL

CREATE DATABASE IF NOT EXISTS horizontes_db;
USE horizontes_db;

-- Tabla: niveles educativos
CREATE TABLE IF NOT EXISTS niveles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Tabla: tipos de institución
CREATE TABLE IF NOT EXISTS tipos_institucion (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Tabla: instituciones
CREATE TABLE IF NOT EXISTS instituciones (
    cue VARCHAR(20) PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    direccion VARCHAR(255),
    numero VARCHAR(20),
    barrio VARCHAR(100),
    distrito VARCHAR(100),
    telefono VARCHAR(50),
    email VARCHAR(255),
    tipo_id INT NOT NULL,
    turno VARCHAR(50),
    sitio_web VARCHAR(255),
    activo TINYINT(1) DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (tipo_id) REFERENCES tipos_institucion(id) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Tabla: carreras
CREATE TABLE IF NOT EXISTS carreras (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    nivel_id INT NOT NULL,
    descripcion TEXT,
    perfil_egresado TEXT,
    duracion VARCHAR(50),
    activo TINYINT(1) DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (nivel_id) REFERENCES niveles(id) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Tabla: relación institución-carrera (oferta académica)
CREATE TABLE IF NOT EXISTS institucion_carrera (
    id INT AUTO_INCREMENT PRIMARY KEY,
    institucion_cue VARCHAR(20) NOT NULL,
    carrera_id INT NOT NULL,
    turno VARCHAR(50),
    modalidad VARCHAR(50) DEFAULT 'Presencial',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (institucion_cue) REFERENCES instituciones(cue) ON DELETE CASCADE,
    FOREIGN KEY (carrera_id) REFERENCES carreras(id) ON DELETE CASCADE,
    UNIQUE KEY unique_inst_carrera (institucion_cue, carrera_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Tabla: competencias
CREATE TABLE IF NOT EXISTS competencias (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Tabla: relación carrera-competencia
CREATE TABLE IF NOT EXISTS carrera_competencia (
    id INT AUTO_INCREMENT PRIMARY KEY,
    carrera_id INT NOT NULL,
    competencia_id INT NOT NULL,
    FOREIGN KEY (carrera_id) REFERENCES carreras(id) ON DELETE CASCADE,
    FOREIGN KEY (competencia_id) REFERENCES competencias(id) ON DELETE CASCADE,
    UNIQUE KEY unique_carrera_competencia (carrera_id, competencia_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Tabla: usuarios (admin e instituciones)
CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario VARCHAR(50) NOT NULL UNIQUE,
    contraseña VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    nombre VARCHAR(100),
    rol ENUM('admin', 'institucion') DEFAULT 'admin',
    institucion_cue VARCHAR(20),
    ultimo_login TIMESTAMP NULL,
    activo TINYINT(1) DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (institucion_cue) REFERENCES instituciones(cue) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Tabla: solicitudes de registro de instituciones
CREATE TABLE IF NOT EXISTS solicitudes_registro (
    id INT AUTO_INCREMENT PRIMARY KEY,
    institucion_cue VARCHAR(20) NOT NULL,
    email VARCHAR(255) NOT NULL,
    contraseña VARCHAR(255) NOT NULL,
    nombre_contacto VARCHAR(100),
    estado ENUM('pendiente', 'aprobado', 'rechazado') DEFAULT 'pendiente',
    motivo_rechazo TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (institucion_cue) REFERENCES instituciones(cue) ON DELETE CASCADE,
    UNIQUE KEY unique_solicitud_cue (institucion_cue),
    UNIQUE KEY unique_solicitud_email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Tabla: solicitudes de carreras (oferta académica)
CREATE TABLE IF NOT EXISTS solicitudes_carreras (
    id INT AUTO_INCREMENT PRIMARY KEY,
    institucion_cue VARCHAR(20) NOT NULL,
    carrera_id INT NOT NULL,
    turno VARCHAR(50),
    modalidad VARCHAR(50) DEFAULT 'Presencial',
    estado ENUM('pendiente', 'aprobado', 'rechazado') DEFAULT 'pendiente',
    motivo_rechazo TEXT,
    revisado_por INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (institucion_cue) REFERENCES instituciones(cue) ON DELETE CASCADE,
    FOREIGN KEY (carrera_id) REFERENCES carreras(id) ON DELETE CASCADE,
    FOREIGN KEY (revisado_por) REFERENCES usuarios(id) ON DELETE SET NULL,
    UNIQUE KEY unique_solicitud_carrera (institucion_cue, carrera_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Tabla: mensajes entre institución y admin
CREATE TABLE IF NOT EXISTS mensajes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    institucion_cue VARCHAR(20) NOT NULL,
    remitente VARCHAR(20) NOT NULL DEFAULT 'institucion',
    contenido TEXT NOT NULL,
    leido TINYINT(1) DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (institucion_cue) REFERENCES instituciones(cue) ON DELETE CASCADE,
    INDEX idx_mensajes_cue (institucion_cue),
    INDEX idx_mensajes_created (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Tabla: solicitudes de cambio de información institucional
CREATE TABLE IF NOT EXISTS solicitudes_cambio (
    id INT AUTO_INCREMENT PRIMARY KEY,
    institucion_cue VARCHAR(20) NOT NULL,
    campo VARCHAR(50) NOT NULL,
    valor_actual TEXT,
    valor_nuevo TEXT NOT NULL,
    estado ENUM('pendiente', 'aprobado', 'rechazado') DEFAULT 'pendiente',
    motivo_rechazo TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (institucion_cue) REFERENCES instituciones(cue) ON DELETE CASCADE,
    INDEX idx_solicitudes_cue (institucion_cue),
    INDEX idx_solicitudes_estado (estado)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Tabla: historial de acciones
CREATE TABLE IF NOT EXISTS historial_acciones (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT,
    accion VARCHAR(50) NOT NULL,
    entidad VARCHAR(50) NOT NULL,
    entidad_id INT,
    detalle JSON,
    ip_address VARCHAR(45),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE SET NULL,
    INDEX idx_created_at (created_at),
    INDEX idx_usuario (usuario_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Datos iniciales: niveles educativos
INSERT INTO niveles (nombre) VALUES 
('Secundario'),
('Superior'),
('Formación Profesional');

-- Datos iniciales: tipos de institución
INSERT INTO tipos_institucion (nombre) VALUES 
('Escuela Secundaria'),
('Instituto Superior'),
('Centro de Formación Profesional'),
('Escuela de Arte'),
('Escuela Técnica');

-- Usuario admin inicial (contraseña: admin123)
INSERT INTO usuarios (usuario, contraseña, email, nombre, rol) VALUES 
('admin', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4.FRnFJ4pBDeYLTu', 'admin@horizontes.edu.ar', 'Administrador', 'admin');