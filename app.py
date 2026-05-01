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
    cue: str
    nombre_establecimiento: str
    email: str
    password: str

class SolicitudUpdate(BaseModel):
    estado: Optional[str] = None
    motivo_rechazo: Optional[str] = None

class InstitucionCreate(BaseModel):
    cue: str
    nombre: str
    direccion: Optional[str] = None
    telefono: Optional[str] = None
    email: Optional[str] = None
    sitio_web: Optional[str] = None
    tipo_id: Optional[int] = None
    distrito: Optional[str] = None

class InstitucionUpdate(BaseModel):
    nombre: Optional[str] = None
    direccion: Optional[str] = None
    telefono: Optional[str] = None
    email: Optional[str] = None
    sitio_web: Optional[str] = None
    tipo_id: Optional[int] = None
    distrito: Optional[str] = None
    activo: Optional[bool] = None

class CompetenciaCreate(BaseModel):
    nombre: str
    descripcion: Optional[str] = None

class CompetenciaUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    activo: Optional[bool] = None

class OfertaCreate(BaseModel):
    nombre: str
    nivel_id: int
    descripcion: Optional[str] = None
    tipo_oferta_id: Optional[int] = None
    area_id: Optional[int] = None
    duracion_meses: Optional[int] = None

class OfertaUpdate(BaseModel):
    nombre: Optional[str] = None
    nivel_id: Optional[int] = None
    descripcion: Optional[str] = None
    tipo_oferta_id: Optional[int] = None
    area_id: Optional[int] = None
    duracion_meses: Optional[int] = None
    activo: Optional[bool] = None

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
    
    if 'password' not in user:
        raise HTTPException(status_code=500, detail="Error al verificar contraseña")
    
    if not bcrypt.checkpw(request.password.encode('utf-8'), user['password'].encode('utf-8')):
        raise HTTPException(status_code=401, detail="Contraseña incorrecta")
    
    database.update('usuarios', {'ultimo_login': datetime.now().isoformat()}, {'id': user['id']})
    
    rol_nombre = 'admin' if user.get('rol_id') == 1 else 'institucion'
    
    return {
        "success": True,
        "user": {
            "id": user['id'],
            "usuario": user['usuario'],
            "email": user.get('email'),
            "rol": rol_nombre,
            "rol_id": user.get('rol_id'),
            "institucion_cue": user.get('institucion_cue')
        }
    }

@app.post("/api/auth/registro")
def registro(request: SolicitudCreate):
    institucion = database.get_one('instituciones', {'cue': request.cue})
    
    if not institucion:
        raise HTTPException(status_code=400, detail="El CUE no corresponde a una institución válida")
    
    existe_user = database.get_one('usuarios', {'institucion_cue': request.cue})
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
        'rol_id': 2,
        'institucion_cue': request.cue,
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
            'institucion': request.cue,
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
    
    password_hash = bcrypt.hashpw(solicitud['password_temp'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    user_data = {
        'usuario': usuario,
        'password': password_hash,
        'email': solicitud['email'],
        'rol_id': 2,
        'institucion_cue': solicitud['cue'],
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

@app.get("/api/dashboard")
def get_dashboard():
    total_instituciones = database.count('instituciones', {'activo': True})
    total_usuarios = database.count('usuarios', {'activo': True})
    
    solicitudes_pendientes = database.count('solicitudes_registro', {'estado': 'pendiente'})
    
    return {
        "total_instituciones": total_instituciones,
        "total_usuarios": total_usuarios,
        "solicitudes_pendientes": solicitudes_pendientes,
        "instituciones_por_tipo": []
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
    
    return institucion

@app.post("/api/instituciones")
def create_institucion(institucion: InstitucionCreate):
    data = {
        'cue': institucion.cue,
        'nombre': institucion.nombre,
        'direccion': institucion.direccion,
        'telefono': institucion.telefono,
        'email': institucion.email,
        'sitio_web': institucion.sitio_web,
        'tipo_id': institucion.tipo_id,
        'distrito': institucion.distrito,
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
    if institucion.telefono is not None:
        updates['telefono'] = institucion.telefono
    if institucion.email is not None:
        updates['email'] = institucion.email
    if institucion.sitio_web is not None:
        updates['sitio_web'] = institucion.sitio_web
    if institucion.tipo_id is not None:
        updates['tipo_id'] = institucion.tipo_id
    if institucion.distrito is not None:
        updates['distrito'] = institucion.distrito
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

@app.get("/api/niveles")
def get_niveles():
    niveles = database.get_all('niveles')
    return niveles or []

@app.get("/api/tipos-institucion")
def get_tipos_institucion():
    tipos = database.get_all('tipos_institucion')
    return tipos or []

@app.get("/api/roles")
def get_roles():
    roles = database.get_all('roles')
    return roles or []

@app.get("/api/usuarios")
def get_usuarios():
    usuarios = database.get_all('usuarios')
    return usuarios or []

@app.get("/api/localidades")
def get_localidades():
    localidades = database.get_all('localidades')
    return localidades or []

@app.get("/api/barrios")
def get_barrios():
    barrios = database.get_all('barrios')
    return barrios or []

@app.get("/api/turnos")
def get_turnos():
    turnos = database.get_all('turnos')
    return turnos or []

@app.get("/api/modalidades")
def get_modalidades():
    modalidades = database.get_all('modalidades')
    return modalidades or []

@app.get("/api/areas")
def get_areas():
    areas = database.get_all('areas')
    return areas or []

@app.get("/api/tipos-oferta")
def get_tipos_oferta():
    tipos = database.get_all('tipos_oferta')
    return tipos or []

@app.get("/api/competencias")
def get_competencias(activo: Optional[bool] = None):
    if activo is not None:
        competencias = database.get_all('competencias', {'activo': activo})
    else:
        competencias = database.get_all('competencias')
    return competencias or []

@app.post("/api/competencias")
def create_competencia(competencia: CompetenciaCreate):
    data = {
        'nombre': competencia.nombre,
        'descripcion': competencia.descripcion,
        'activo': True
    }
    result = database.insert('competencias', data)
    if not result:
        raise HTTPException(status_code=500, detail="Error al crear competencia")
    return {"success": True, "message": "Competencia creada correctamente", "id": result}

@app.put("/api/competencias/{id}")
def update_competencia(id: int, competencia: CompetenciaUpdate):
    updates = {}
    if competencia.nombre is not None:
        updates['nombre'] = competencia.nombre
    if competencia.descripcion is not None:
        updates['descripcion'] = competencia.descripcion
    if competencia.activo is not None:
        updates['activo'] = competencia.activo
    
    if not updates:
        raise HTTPException(status_code=400, detail="No hay datos para actualizar")
    
    result = database.update('competencias', updates, {'id': id})
    if not result:
        raise HTTPException(status_code=500, detail="Error al actualizar competencia")
    return {"success": True, "message": "Competencia actualizada correctamente"}

@app.delete("/api/competencias/{id}")
def delete_competencia(id: int):
    result = database.update('competencias', {'activo': False}, {'id': id})
    if not result:
        raise HTTPException(status_code=500, detail="Error al eliminar competencia")
    return {"success": True, "message": "Competencia eliminada correctamente"}

@app.get("/api/ofertas")
def get_ofertas(nivel_id: Optional[int] = None):
    filters = {'activo': True}
    if nivel_id:
        filters['nivel_id'] = nivel_id
    ofertas = database.get_all('ofertas_educativas', filters)
    return ofertas or []

@app.get("/api/ofertas/{id}")
def get_oferta(id: int):
    oferta = database.get_one('ofertas_educativas', {'id': id, 'activo': True})
    if not oferta:
        raise HTTPException(status_code=404, detail="Oferta no encontrada")
    return oferta

@app.post("/api/ofertas")
def create_oferta(oferta: OfertaCreate):
    data = {
        'nombre': oferta.nombre,
        'nivel_id': oferta.nivel_id,
        'descripcion': oferta.descripcion,
        'tipo_oferta_id': oferta.tipo_oferta_id,
        'area_id': oferta.area_id,
        'duracion_meses': oferta.duracion_meses,
        'activo': True
    }
    result = database.insert('ofertas_educativas', data)
    if not result:
        raise HTTPException(status_code=500, detail="Error al crear oferta")
    return {"success": True, "message": "Oferta creada correctamente", "id": result}

@app.put("/api/ofertas/{id}")
def update_oferta(id: int, oferta: OfertaUpdate):
    updates = {}
    if oferta.nombre is not None:
        updates['nombre'] = oferta.nombre
    if oferta.nivel_id is not None:
        updates['nivel_id'] = oferta.nivel_id
    if oferta.descripcion is not None:
        updates['descripcion'] = oferta.descripcion
    if oferta.tipo_oferta_id is not None:
        updates['tipo_oferta_id'] = oferta.tipo_oferta_id
    if oferta.area_id is not None:
        updates['area_id'] = oferta.area_id
    if oferta.duracion_meses is not None:
        updates['duracion_meses'] = oferta.duracion_meses
    if oferta.activo is not None:
        updates['activo'] = oferta.activo
    
    if not updates:
        raise HTTPException(status_code=400, detail="No hay datos para actualizar")
    
    result = database.update('ofertas_educativas', updates, {'id': id})
    if not result:
        raise HTTPException(status_code=500, detail="Error al actualizar oferta")
    return {"success": True, "message": "Oferta actualizada correctamente"}

@app.delete("/api/ofertas/{id}")
def delete_oferta(id: int):
    result = database.update('ofertas_educativas', {'activo': False}, {'id': id})
    if not result:
        raise HTTPException(status_code=500, detail="Error al eliminar oferta")
    return {"success": True, "message": "Oferta eliminada correctamente"}

@app.get("/api/ofertas/{id}/competencias")
def get_oferta_competencias(id: int):
    relaciones = database.get_all('oferta_competencias', {'oferta_id': id})
    competencias = []
    for rel in relaciones:
        comp = database.get_one('competencias', {'id': rel['competencia_id'], 'activo': True})
        if comp:
            competencias.append(comp)
    return competencias

@app.post("/api/ofertas/{id}/competencias")
def add_competencia_oferta(id: int, competencia_id: int):
    existe = database.get_one('oferta_competencias', {'oferta_id': id, 'competencia_id': competencia_id})
    if existe:
        raise HTTPException(status_code=400, detail="Esta competencia ya está asociada a la oferta")
    
    data = {
        'oferta_id': id,
        'competencia_id': competencia_id
    }
    result = database.insert('oferta_competencias', data)
    if not result:
        raise HTTPException(status_code=500, detail="Error al agregar competencia a oferta")
    return {"success": True, "message": "Competencia agregada a la oferta"}

@app.delete("/api/ofertas/{id}/competencias/{competencia_id}")
def remove_competencia_oferta(id: int, competencia_id: int):
    result = database.delete('oferta_competencias', {'oferta_id': id, 'competencia_id': competencia_id})
    if not result:
        raise HTTPException(status_code=500, detail="Error al eliminar competencia de oferta")
    return {"success": True, "message": "Competencia eliminada de la oferta"}

@app.get("/api/institucion-oferta")
def get_institucion_oferta(institucion_cue: str):
    relaciones = database.get_all('institucion_oferta', {'institucion_cue': institucion_cue})
    return relaciones or []

@app.post("/api/institucion-oferta")
def add_oferta_institucion(institucion_cue: str, oferta_id: int, turno_id: Optional[int] = None, modalidad_id: Optional[int] = None):
    existe = database.get_one('institucion_oferta', {'institucion_cue': institucion_cue, 'oferta_id': oferta_id})
    if existe:
        raise HTTPException(status_code=400, detail="Esta oferta ya está asociada a la institución")
    
    data = {
        'institucion_cue': institucion_cue,
        'oferta_id': oferta_id,
        'turno_id': turno_id,
        'modalidad_id': modalidad_id
    }
    result = database.insert('institucion_oferta', data)
    
    if not result:
        raise HTTPException(status_code=500, detail="Error al agregar oferta a institución")
    
    return {"success": True, "message": "Oferta agregada a la institución"}

@app.delete("/api/institucion-oferta/{id}")
def remove_oferta_institucion(id: int):
    result = database.delete('institucion_oferta', {'id': id})
    
    if not result:
        raise HTTPException(status_code=500, detail="Error al eliminar oferta de institución")
    
    return {"success": True, "message": "Oferta eliminada de la institución"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)