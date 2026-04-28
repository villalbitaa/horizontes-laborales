from fastapi import FastAPI, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional, List
import database
import os
from datetime import datetime
import bcrypt

app = FastAPI(title="Horizontes API", description="API para Horizontes San Miguel")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory=os.path.join(os.path.dirname(__file__), '..', 'vista')), name="static")

def log_accion(usuario_id: int, accion: str, entidad: str, entidad_id: int = None, detalle: dict = None, ip: str = None):
    data = {
        'usuario_id': usuario_id,
        'accion': accion,
        'entidad': entidad,
        'entidad_id': entidad_id,
        'detalle': detalle,
        'ip_address': ip
    }
    database.insert('historial_acciones', data)

class LoginRequest(BaseModel):
    usuario: str
    password: str

class SolicitudCreate(BaseModel):
    institucion_cue: str
    email: str
    password: str
    nombre_contacto: Optional[str] = None

class SolicitudUpdate(BaseModel):
    estado: Optional[str] = None
    motivo_rechazo: Optional[str] = None

class InstitucionCreate(BaseModel):
    cue: str
    nombre: str
    direccion: Optional[str] = None
    numero: Optional[str] = None
    barrio: Optional[str] = None
    distrito_id: Optional[int] = None
    telefono: Optional[str] = None
    email: Optional[str] = None
    tipo_id: int
    turno: Optional[str] = None
    sitio_web: Optional[str] = None

class InstitucionUpdate(BaseModel):
    nombre: Optional[str] = None
    direccion: Optional[str] = None
    numero: Optional[str] = None
    barrio: Optional[str] = None
    telefono: Optional[str] = None
    email: Optional[str] = None
    tipo_id: Optional[int] = None
    turno: Optional[str] = None
    sitio_web: Optional[str] = None
    activo: Optional[bool] = None

class CarreraCreate(BaseModel):
    nombre: str
    nivel_id: int
    descripcion: Optional[str] = None
    perfil_egresado: Optional[str] = None
    duracion: Optional[str] = None
    competencias: Optional[List[int]] = None

class CarreraUpdate(BaseModel):
    nombre: Optional[str] = None
    nivel_id: Optional[int] = None
    descripcion: Optional[str] = None
    perfil_egresado: Optional[str] = None
    duracion: Optional[str] = None
    activo: Optional[bool] = None
    competencias: Optional[List[int]] = None

class InstitucionCarreraCreate(BaseModel):
    institucion_cue: str
    carrera_id: int
    turno: Optional[str] = None
    modalidad: Optional[str] = "Presencial"

class SolicitudCarreraCreate(BaseModel):
    carrera_id: int
    turno: Optional[str] = None
    modalidad: Optional[str] = "Presencial"

class SolicitudCarreraUpdate(BaseModel):
    estado: Optional[str] = None
    motivo_rechazo: Optional[str] = None

@app.get("/")
def root():
    return FileResponse("../index.html")

@app.get("/horizontes")
def horizontes():
    return FileResponse("../vista/horizontes.html")

@app.get("/admin")
def admin():
    return FileResponse("../vista/admin.html")

@app.get("/registro")
def registro():
    return FileResponse("../vista/registro.html")

@app.get("/institucion")
def institucion():
    return FileResponse("../vista/institucion.html")

@app.post("/api/auth/login")
def login(request: LoginRequest):
    users = database.get_all('usuarios', {'usuario': request.usuario, 'activo': True})
    
    if not users:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")
    
    user = users[0]
    
    if not bcrypt.checkpw(request.password.encode('utf-8'), user['password'].encode('utf-8')):
        raise HTTPException(status_code=401, detail="Contraseña incorrecta")
    
    database.update('usuarios', {'ultimo_login': datetime.now().isoformat()}, {'id': user['id']})
    
    return {
        "success": True,
        "user": {
            "id": user['id'],
            "usuario": user['usuario'],
            "nombre": user.get('nombre'),
            "rol": user.get('rol', 'institucion'),
            "institucion_cue": user.get('institucion_cue')
        }
    }

@app.post("/api/auth/registro")
def registro(request: SolicitudCreate):
    institucion = database.get_one('instituciones', {'cue': request.institucion_cue})
    
    if not institucion:
        raise HTTPException(status_code=400, detail="El CUE no corresponde a una institución válida")
    
    existe_user = database.get_one('usuarios', {'institucion_cue': request.institucion_cue})
    if existe_user:
        raise HTTPException(status_code=400, detail="Esta institución ya tiene un usuario asignado")
    
    existe_email = database.get_one('usuarios', {'email': request.email})
    if existe_email:
        raise HTTPException(status_code=400, detail="Este email ya está registrado")
    
    password_hash = bcrypt.hashpw(request.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    usuario = request.email.split('@')[0]
    existe_usuario = database.get_one('usuarios', {'usuario': usuario})
    if existe_usuario:
        import random
        usuario = f"{usuario}{random.randint(1, 99)}"
    
    user_data = {
        'usuario': usuario,
        'password': password_hash,
        'email': request.email,
        'nombre': request.nombre_contacto,
        'rol': 'institucion',
        'institucion_cue': request.institucion_cue,
        'activo': True
    }
    
    result = database.insert('usuarios', user_data)
    
    if not result:
        raise HTTPException(status_code=500, detail="Error al crear usuario")
    
    log_accion(
        usuario_id=1,
        accion='crear',
        entidad='usuario',
        detalle={
            'usuario': usuario,
            'institucion': request.institucion_cue,
            'email': request.email
        }
    )
    
    return {
        "success": True, 
        "message": "Registro exitoso. Ya podés iniciar sesión.",
        "usuario": usuario
    }

@app.get("/api/solicitudes")
def get_solicitudes():
    solicitudes = database.get_all('solicitudes_registro')
    return solicitudes or []

@app.put("/api/solicitudes/{id}/aprobar")
def aprobar_solicitud(id: int):
    solicitud = database.get_one('solicitudes_registro', {'id': id, 'estado': 'pendiente'})
    
    if not solicitud:
        raise HTTPException(status_code=404, detail="Solicitud no encontrada o ya procesada")
    
    usuario = solicitud['email'].split('@')[0]
    existe = database.get_one('usuarios', {'usuario': usuario})
    if existe:
        import random
        usuario = f"{usuario}{random.randint(1, 99)}"
    
    password_hash = pwd_context.hash(solicitud['password'])
    
    user_data = {
        'usuario': usuario,
        'password': password_hash,
        'email': solicitud['email'],
        'nombre': solicitud.get('nombre_contacto'),
        'rol': 'institucion',
        'institucion_cue': solicitud['institucion_cue'],
        'activo': True
    }
    database.insert('usuarios', user_data)
    
    database.update('solicitudes_registro', {'estado': 'aprobado'}, {'id': id})
    
    return {"success": True, "message": "Solicitud aprobada. Usuario creado correctamente."}

@app.put("/api/solicitudes/{id}/rechazar")
def rechazar_solicitud(id: int, update: SolicitudUpdate):
    result = database.update('solicitudes_registro', {
        'estado': 'rechazado', 
        'motivo_rechazo': update.motivo_rechazo or ''
    }, {'id': id, 'estado': 'pendiente'})
    
    if not result:
        raise HTTPException(status_code=404, detail="Solicitud no encontrada o ya procesada")
    
    return {"success": True, "message": "Solicitud rechazada"}

@app.delete("/api/solicitudes/{id}")
def eliminar_solicitud(id: int):
    result = database.delete('solicitudes_registro', {'id': id})
    
    if not result:
        raise HTTPException(status_code=500, detail="Error al eliminar solicitud")
    
    return {"success": True, "message": "Solicitud eliminada"}

@app.post("/api/solicitudes-carreras")
def crear_solicitud_carrera(solicitud: SolicitudCarreraCreate, institucion_cue: str):
    existe = database.get_one('solicitudes_carreras', {
        'institucion_cue': institucion_cue, 
        'carrera_id': solicitud.carrera_id, 
        'estado': 'pendiente'
    })
    if existe:
        raise HTTPException(status_code=400, detail="Ya existe una solicitud pendiente para esta carrera")
    
    aprobada = database.get_one('institucion_carrera', {
        'institucion_cue': institucion_cue, 
        'carrera_id': solicitud.carrera_id
    })
    if aprobada:
        raise HTTPException(status_code=400, detail="Esta carrera ya está en la oferta de tu institución")
    
    data = {
        'institucion_cue': institucion_cue,
        'carrera_id': solicitud.carrera_id,
        'turno': solicitud.turno,
        'modalidad': solicitud.modalidad,
        'estado': 'pendiente'
    }
    result = database.insert('solicitudes_carreras', data)
    
    if not result:
        raise HTTPException(status_code=500, detail="Error al crear solicitud")
    
    return {"success": True, "message": "Solicitud enviada. El admin la revisará pronto."}

@app.get("/api/solicitudes-carreras")
def get_solicitudes_carreras(estado: Optional[str] = None):
    filters = {}
    if estado:
        filters['estado'] = estado
    solicitudes = database.get_all('solicitudes_carreras', filters if filters else None)
    return solicitudes or []

@app.get("/api/mis-solicitudes")
def get_mis_solicitudes(institucion_cue: str):
    solicitudes = database.get_all('solicitudes_carreras', {'institucion_cue': institucion_cue})
    return solicitudes or []

@app.put("/api/solicitudes-carreras/{id}/aprobar")
def aprobar_solicitud_carrera(id: int):
    solicitud = database.get_one('solicitudes_carreras', {'id': id, 'estado': 'pendiente'})
    
    if not solicitud:
        raise HTTPException(status_code=404, detail="Solicitud no encontrada o ya procesada")
    
    data = {
        'institucion_cue': solicitud['institucion_cue'],
        'carrera_id': solicitud['carrera_id'],
        'turno': solicitud.get('turno'),
        'modalidad': solicitud.get('modalidad')
    }
    database.insert('institucion_carrera', data)
    
    database.update('solicitudes_carreras', {'estado': 'aprobado', 'revisado_por': 1}, {'id': id})
    
    return {"success": True, "message": "Solicitud aprobada. La carrera se agregó a la oferta."}

@app.put("/api/solicitudes-carreras/{id}/rechazar")
def rechazar_solicitud_carrera(id: int, update: SolicitudCarreraUpdate):
    solicitud = database.get_one('solicitudes_carreras', {'id': id, 'estado': 'pendiente'})
    
    if not solicitud:
        raise HTTPException(status_code=404, detail="Solicitud no encontrada o ya procesada")
    
    database.update('solicitudes_carreras', {
        'estado': 'rechazado', 
        'motivo_rechazo': update.motivo_rechazo or '',
        'revisado_por': 1
    }, {'id': id})
    
    return {"success": True, "message": "Solicitud rechazada"}

@app.get("/api/dashboard")
def get_dashboard():
    total_instituciones = database.count('instituciones', {'activo': True})
    total_carreras = database.count('carreras', {'activo': True})
    total_usuarios = database.count('usuarios', {'activo': True})
    
    solicitudes_pendientes = database.count('solicitudes_registro', {'estado': 'pendiente'})
    solicitudes_carreras_pendientes = database.count('solicitudes_carreras', {'estado': 'pendiente'})
    
    return {
        "total_instituciones": total_instituciones,
        "total_carreras": total_carreras,
        "total_usuarios": total_usuarios,
        "solicitudes_pendientes": solicitudes_pendientes,
        "solicitudes_carreras_pendientes": solicitudes_carreras_pendientes,
        "instituciones_por_tipo": [],
        "carreras_por_nivel": []
    }

@app.get("/api/historial")
def get_historial(limite: int = 50):
    historial = database.get_all('historial_acciones')
    return historial[:limite] if historial else []

@app.get("/api/instituciones")
def get_instituciones():
    instituciones = database.get_all('instituciones', {'activo': True})
    return instituciones or []

@app.get("/api/instituciones/{cue}")
def get_institucion(cue: str):
    institucion = database.get_one('instituciones', {'cue': cue, 'activo': True})
    
    if not institucion:
        raise HTTPException(status_code=404, detail="Institución no encontrada")
    
    carreras = database.get_all('institucion_carrera', {'institucion_cue': cue})
    institucion['carreras'] = carreras or []
    
    return institucion

@app.post("/api/instituciones")
def create_institucion(institucion: InstitucionCreate):
    data = {
        'cue': institucion.cue,
        'nombre': institucion.nombre,
        'direccion': institucion.direccion,
        'numero': institucion.numero,
        'barrio': institucion.barrio,
        'telefono': institucion.telefono,
        'email': institucion.email,
        'tipo_id': institucion.tipo_id,
        'turno': institucion.turno,
        'sitio_web': institucion.sitio_web,
        'activo': True
    }
    
    result = database.insert('instituciones', data)
    
    if not result:
        raise HTTPException(status_code=500, detail="Error al crear institución")
    
    return {"success": True, "message": "Institución creada correctamente"}

@app.put("/api/instituciones/{cue}")
def update_institucion(cue: str, institucion: InstitucionUpdate):
    updates = {}
    
    if institucion.nombre is not None:
        updates['nombre'] = institucion.nombre
    if institucion.direccion is not None:
        updates['direccion'] = institucion.direccion
    if institucion.numero is not None:
        updates['numero'] = institucion.numero
    if institucion.barrio is not None:
        updates['barrio'] = institucion.barrio
    if institucion.telefono is not None:
        updates['telefono'] = institucion.telefono
    if institucion.email is not None:
        updates['email'] = institucion.email
    if institucion.tipo_id is not None:
        updates['tipo_id'] = institucion.tipo_id
    if institucion.turno is not None:
        updates['turno'] = institucion.turno
    if institucion.sitio_web is not None:
        updates['sitio_web'] = institucion.sitio_web
    if institucion.activo is not None:
        updates['activo'] = institucion.activo
    
    if not updates:
        raise HTTPException(status_code=400, detail="No hay datos para actualizar")
    
    result = database.update('instituciones', updates, {'cue': cue})
    
    if not result:
        raise HTTPException(status_code=500, detail="Error al actualizar institución")
    
    return {"success": True, "message": "Institución actualizada correctamente"}

@app.delete("/api/instituciones/{cue}")
def delete_institucion(cue: str):
    result = database.update('instituciones', {'activo': False}, {'cue': cue})
    
    if not result:
        raise HTTPException(status_code=500, detail="Error al eliminar institución")
    
    return {"success": True, "message": "Institución eliminada correctamente"}

@app.get("/api/instituciones/{cue}/carreras")
def get_carreras_institucion(cue: str):
    relaciones = database.get_all('institucion_carrera', {'institucion_cue': cue})
    return relaciones or []

@app.get("/api/instituciones/{cue}/competencias")
def get_competencias_institucion(cue: str):
    return []

@app.get("/api/carreras")
def get_carreras(nivel_id: Optional[int] = None):
    filters = {'activo': True}
    if nivel_id:
        filters['nivel_id'] = nivel_id
    carreras = database.get_all('carreras', filters)
    return carreras or []

@app.get("/api/carreras/{id}")
def get_carrera(id: int):
    carrera = database.get_one('carreras', {'id': id, 'activo': True})
    
    if not carrera:
        raise HTTPException(status_code=404, detail="Carrera no encontrada")
    
    competencias = database.get_all('carrera_competencia', {'carrera_id': id})
    carrera['competencias'] = competencias or []
    
    return carrera

@app.get("/api/carreras/{id}/detalle")
def get_carrera_detalle(id: int):
    carrera = database.get_one('carreras', {'id': id, 'activo': True})
    
    if not carrera:
        raise HTTPException(status_code=404, detail="Carrera no encontrada")
    
    relaciones = database.get_all('institucion_carrera', {'carrera_id': id})
    
    instituciones_detalle = []
    if relaciones:
        for rel in relaciones:
            inst = database.get_one('instituciones', {'cue': rel['institucion_cue'], 'activo': True})
            if inst:
                instituciones_detalle.append({
                    'institucion': {
                        'cue': inst['cue'],
                        'nombre': inst['nombre'],
                        'direccion': inst['direccion'],
                        'barrio': inst['barrio'],
                        'telefono': inst['telefono'],
                        'email': inst['email'],
                        'sitio_web': inst['sitio_web']
                    },
                    'turno': rel['turno'],
                    'modalidad': rel['modalidad']
                })
    
    competencias = database.get_all('carrera_competencia', {'carrera_id': id})
    competencias_detalle = []
    if competencias:
        for comp in competencias:
            c = database.get_one('competencias', {'id': comp['competencia_id'], 'activo': True})
            if c:
                competencias_detalle.append(c)
    
    return {
        'id': carrera['id'],
        'nombre': carrera['nombre'],
        'nivel_id': carrera['nivel_id'],
        'descripcion': carrera['descripcion'],
        'perfil_egresado': carrera['perfil_egresado'],
        'duracion': carrera['duracion'],
        'instituciones': instituciones_detalle,
        'competencias': competencias_detalle
    }

@app.post("/api/carreras")
def create_carrera(carrera: CarreraCreate):
    data = {
        'nombre': carrera.nombre,
        'nivel_id': carrera.nivel_id,
        'descripcion': carrera.descripcion,
        'perfil_egresado': carrera.perfil_egresado,
        'duracion': carrera.duracion,
        'activo': True
    }
    
    result = database.insert('carreras', data)
    
    if not result:
        raise HTTPException(status_code=500, detail="Error al crear carrera")
    
    if carrera.competencias:
        for comp_id in carrera.competencias:
            database.insert('carrera_competencia', {
                'carrera_id': result,
                'competencia_id': comp_id
            })
    
    return {"success": True, "message": "Carrera creada correctamente"}

@app.put("/api/carreras/{id}")
def update_carrera(id: int, carrera: CarreraUpdate):
    updates = {}
    
    if carrera.nombre is not None:
        updates['nombre'] = carrera.nombre
    if carrera.nivel_id is not None:
        updates['nivel_id'] = carrera.nivel_id
    if carrera.descripcion is not None:
        updates['descripcion'] = carrera.descripcion
    if carrera.perfil_egresado is not None:
        updates['perfil_egresado'] = carrera.perfil_egresado
    if carrera.duracion is not None:
        updates['duracion'] = carrera.duracion
    if carrera.activo is not None:
        updates['activo'] = carrera.activo
    
    if not updates:
        raise HTTPException(status_code=400, detail="No hay datos para actualizar")
    
    result = database.update('carreras', updates, {'id': id})
    
    if carrera.competencias is not None:
        database.delete('carrera_competencia', {'carrera_id': id})
        for comp_id in carrera.competencias:
            database.insert('carrera_competencia', {
                'carrera_id': id,
                'competencia_id': comp_id
            })
    
    return {"success": True, "message": "Carrera actualizada correctamente"}

@app.delete("/api/carreras/{id}")
def delete_carrera(id: int):
    result = database.update('carreras', {'activo': False}, {'id': id})
    
    if not result:
        raise HTTPException(status_code=500, detail="Error al eliminar carrera")
    
    return {"success": True, "message": "Carrera eliminada correctamente"}

@app.post("/api/institucion-carrera")
def add_carrera_institucion(data: InstitucionCarreraCreate):
    result = database.insert('institucion_carrera', {
        'institucion_cue': data.institucion_cue,
        'carrera_id': data.carrera_id,
        'turno': data.turno,
        'modalidad': data.modalidad
    })
    
    if not result:
        raise HTTPException(status_code=500, detail="Error al agregar carrera a institución")
    
    return {"success": True, "message": "Carrera agregada a la institución"}

@app.delete("/api/institucion-carrera/{id}")
def remove_carrera_institucion(id: int):
    result = database.delete('institucion_carrera', {'id': id})
    
    if not result:
        raise HTTPException(status_code=500, detail="Error al eliminar carrera de institución")
    
    return {"success": True, "message": "Carrera eliminada de la institución"}

@app.get("/api/niveles")
def get_niveles():
    niveles = database.get_all('niveles')
    return niveles or []

@app.get("/api/tipos-institucion")
def get_tipos_institucion():
    tipos = database.get_all('tipos_institucion')
    return tipos or []

@app.get("/api/competencias")
def get_competencias():
    competencias = database.get_all('competencias')
    return competencias or []

@app.get("/api/usuarios")
def get_usuarios():
    usuarios = database.get_all('usuarios')
    return usuarios or []

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)