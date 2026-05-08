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

app.mount("/static/estilo", StaticFiles(directory=os.path.join(os.path.dirname(__file__), '..', 'vista', 'estilo')), name="estilo")
app.mount("/static/controlador", StaticFiles(directory=os.path.join(os.path.dirname(__file__), '..', 'vista', 'controlador')), name="controlador")
app.mount("/static/multimedia", StaticFiles(directory=os.path.join(os.path.dirname(__file__), '..', 'vista', 'multimedia')), name="multimedia")

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
    email: str
    password: str
    nombre_contacto: Optional[str] = None
    nombre_establecimiento: Optional[str] = None
    direccion: Optional[str] = None
    barrio: Optional[str] = None

class SolicitudUpdate(BaseModel):
    estado: Optional[str] = None
    motivo_rechazo: Optional[str] = None

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

class InstitucionProfileUpdate(BaseModel):
    telefono: Optional[str] = None
    sitio_web: Optional[str] = None
    email: Optional[str] = None
    direccion: Optional[str] = None

class InstitucionCarreraCreate(BaseModel):
    nombre: str
    nivel_id: int
    duracion_meses: Optional[int] = None
    turno_id: Optional[int] = None
    descripcion: Optional[str] = None

@app.get("/")
def root():
    return FileResponse(os.path.join(os.path.dirname(__file__), '..', 'index.html'))

@app.get("/horizontes")
def horizontes():
    return FileResponse(os.path.join(os.path.dirname(__file__), '..', 'vista', 'horizontes.html'))

@app.get("/admin")
def admin():
    return FileResponse(os.path.join(os.path.dirname(__file__), '..', 'vista', 'admin.html'))

@app.get("/registro")
def registro():
    return FileResponse(os.path.join(os.path.dirname(__file__), '..', 'vista', 'registro.html'))

@app.get("/institucion")
def institucion():
    return FileResponse(os.path.join(os.path.dirname(__file__), '..', 'vista', 'institucion.html'))

@app.post("/api/auth/login")
def login(request: LoginRequest):
    users = database.get_all('usuarios', {'usuario': request.usuario, 'activo': True})
    if not users:
        users = database.get_all('usuarios', {'email': request.usuario, 'activo': True})
    
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
    existe_user = database.get_one('usuarios', {'institucion_cue': request.cue})
    if existe_user:
        raise HTTPException(status_code=400, detail="Esta institución ya tiene un usuario asignado")

    existe_email = database.get_one('usuarios', {'email': request.email})
    if existe_email:
        raise HTTPException(status_code=400, detail="Este email ya está registrado")

    existe_solicitud = database.get_one('solicitudes_registro', {'cue': request.cue, 'estado': 'pendiente'})
    if existe_solicitud:
        raise HTTPException(status_code=400, detail="Ya existe una solicitud pendiente para este CUE")

    solicitud_data = {
        'cue': request.cue,
        'nombre_establecimiento': request.nombre_establecimiento or 'Sin nombre',
        'email': request.email,
        'password_temp': request.password,
        'nombre_contacto': request.nombre_contacto,
        'direccion': request.direccion,
        'barrio': request.barrio,
        'estado': 'pendiente'
    }

    result = database.insert('solicitudes_registro', solicitud_data)

    if not result:
        raise HTTPException(status_code=500, detail="Error al enviar la solicitud")

    return {
        "success": True,
        "message": "Solicitud enviada. El administrador la revisará pronto."
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
    
    # Si el CUE no existe en instituciones, crearla automáticamente
    institucion = database.get_one('instituciones', {'cue': solicitud['cue']})
    if not institucion:
        tipos = database.get_all('tipos_institucion')
        inst_data = {
            'cue': solicitud['cue'],
            'nombre': solicitud.get('nombre_establecimiento') or solicitud.get('nombre_contacto') or 'Sin nombre',
            'direccion': solicitud.get('direccion') or 'Sin especificar',
            'tipo_id': tipos[0]['id'] if tipos else 1,
            'activo': True
        }
        database.insert('instituciones', inst_data)
    
    usuario = solicitud.get('nombre_establecimiento') or solicitud.get('nombre_contacto') or solicitud['email'].split('@')[0]
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
    result = database.insert('usuarios', user_data)
    if not result:
        raise HTTPException(status_code=500, detail="Error al crear el usuario. El email puede estar duplicado.")
    
    database.update('solicitudes_registro', {'estado': 'aprobado'}, {'id': id})
    
    return {"success": True, "message": f"Solicitud aprobada. Usuario creado: '{usuario}'"}

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
    total_carreras = database.count('ofertas_educativas', {'activo': True})

    solicitudes_pendientes = database.count('solicitudes_registro', {'estado': 'pendiente'})
    solicitudes_carreras_pendientes = 0

    instituciones_por_tipo = database.get_all('tipos_institucion')
    for tipo in instituciones_por_tipo:
        tipo['cantidad'] = database.count('instituciones', {'tipo_id': tipo['id'], 'activo': True})

    carreras_por_nivel = database.get_all('niveles')
    for nivel in carreras_por_nivel:
        nivel['cantidad'] = database.count('ofertas_educativas', {'nivel_id': nivel['id'], 'activo': True})

    return {
        "total_instituciones": total_instituciones,
        "total_usuarios": total_usuarios,
        "total_carreras": total_carreras,
        "solicitudes_pendientes": solicitudes_pendientes,
        "solicitudes_carreras_pendientes": solicitudes_carreras_pendientes,
        "instituciones_por_tipo": instituciones_por_tipo,
        "carreras_por_nivel": carreras_por_nivel
    }

@app.get("/api/historial")
def get_historial(limite: int = 50):
    historial = database.get_all('historial_acciones')
    return historial[:limite] if historial else []

@app.get("/api/instituciones")
def get_instituciones():
    instituciones = database.get_all('instituciones', {'activo': True})
    tipos = {t['id']: t['nombre'] for t in database.get_all('tipos_institucion')}
    for inst in instituciones:
        inst['tipo_nombre'] = tipos.get(inst.get('tipo_id'), '')
    return instituciones or []

@app.get("/api/instituciones/{cue}")
def get_institucion(cue: str):
    institucion = database.get_one('instituciones', {'cue': cue, 'activo': True})

    if not institucion:
        raise HTTPException(status_code=404, detail="Institución no encontrada")

    tipos = {t['id']: t['nombre'] for t in database.get_all('tipos_institucion')}
    institucion['tipo_nombre'] = tipos.get(institucion.get('tipo_id'), '')

    return institucion

@app.put("/api/instituciones/{cue}")
def update_institucion(cue: str, data: InstitucionProfileUpdate):
    institucion = database.get_one('instituciones', {'cue': cue, 'activo': True})
    if not institucion:
        raise HTTPException(status_code=404, detail="Institución no encontrada")
    updates = {}
    if data.telefono is not None:
        updates['telefono'] = data.telefono
    if data.sitio_web is not None:
        updates['sitio_web'] = data.sitio_web
    if data.email is not None:
        updates['email'] = data.email
    if data.direccion is not None:
        updates['direccion'] = data.direccion
    if updates:
        database.update('instituciones', updates, {'cue': cue})
    return {"success": True, "message": "Datos actualizados"}

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

    niveles = {n['id']: n['nombre'] for n in database.get_all('niveles')}
    areas = {a['id']: a['nombre'] for a in database.get_all('areas')}
    tipos_oferta = {t['id']: t['nombre'] for t in database.get_all('tipos_oferta')}

    for o in ofertas:
        o['nivel_nombre'] = niveles.get(o.get('nivel_id'), '')
        o['area_nombre'] = areas.get(o.get('area_id'), '')
        o['tipo_oferta_nombre'] = tipos_oferta.get(o.get('tipo_oferta_id'), '')

    return ofertas or []

@app.get("/api/carreras")
def get_carreras(nivel_id: Optional[int] = None):
    return get_ofertas(nivel_id)

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

# Endpoints para carreras por institución (admin)
@app.get("/api/solicitudes-carreras")
def get_solicitudes_carreras():
    relaciones = database.get_all('institucion_oferta', {})

    instituciones = {i['cue']: i['nombre'] for i in database.get_all('instituciones')}
    ofertas = {o['id']: o for o in database.get_all('ofertas_educativas')}
    niveles = {n['id']: n['nombre'] for n in database.get_all('niveles')}
    turnos = {t['id']: t['nombre'] for t in database.get_all('turnos')}
    modalidades = {m['id']: m['nombre'] for m in database.get_all('modalidades')}

    for r in relaciones:
        r['institucion_nombre'] = instituciones.get(r.get('institucion_cue'), '')
        oferta = ofertas.get(r.get('oferta_id'), {})
        r['carrera_nombre'] = oferta.get('nombre', '')
        r['nivel_nombre'] = niveles.get(oferta.get('nivel_id'), '')
        r['turno'] = turnos.get(r.get('turno_id'), '')
        r['modalidad'] = modalidades.get(r.get('modalidad_id'), '')

    return relaciones or []

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

    ofertas = {o['id']: o for o in database.get_all('ofertas_educativas')}
    niveles = {n['id']: n['nombre'] for n in database.get_all('niveles')}
    turnos = {t['id']: t['nombre'] for t in database.get_all('turnos')}
    modalidades = {m['id']: m['nombre'] for m in database.get_all('modalidades')}

    for r in relaciones:
        r['relacion_id'] = r['id']
        oferta = ofertas.get(r.get('oferta_id'), {})
        r['nombre'] = oferta.get('nombre', '')
        r['nivel_nombre'] = niveles.get(oferta.get('nivel_id'), '')
        r['nivel_id'] = oferta.get('nivel_id')
        r['duracion_meses'] = oferta.get('duracion_meses', '')
        r['descripcion'] = oferta.get('descripcion', '')
        r['turno'] = turnos.get(r.get('turno_id'), '')
        r['modalidad'] = modalidades.get(r.get('modalidad_id'), '')

    return relaciones or []

@app.get("/api/instituciones/{cue}/carreras")
def get_institucion_carreras(cue: str):
    return get_institucion_oferta(institucion_cue=cue)

class SolicitudCarreraCreate(BaseModel):
    oferta_id: int
    turno_id: Optional[int] = None
    modalidad_id: Optional[int] = None

@app.post("/api/solicitudes-carreras")
def create_solicitud_carrera(institucion_cue: str, solicitud: SolicitudCarreraCreate):
    existe = database.get_one('institucion_oferta', {'institucion_cue': institucion_cue, 'oferta_id': solicitud.oferta_id})
    if existe:
        raise HTTPException(status_code=400, detail="Esta oferta ya está asociada a la institución")

    data = {
        'institucion_cue': institucion_cue,
        'oferta_id': solicitud.oferta_id,
        'turno_id': solicitud.turno_id,
        'modalidad_id': solicitud.modalidad_id
    }
    result = database.insert('institucion_oferta', data)

    if not result:
        raise HTTPException(status_code=500, detail="Error al enviar solicitud")

    return {"success": True, "message": "Solicitud enviada. El admin la revisará pronto."}

@app.get("/api/mis-solicitudes")
def get_mis_solicitudes(institucion_cue: str):
    solicitudes = database.get_all('institucion_oferta', {'institucion_cue': institucion_cue})

    ofertas = {o['id']: o for o in database.get_all('ofertas_educativas')}
    niveles = {n['id']: n['nombre'] for n in database.get_all('niveles')}
    turnos = {t['id']: t['nombre'] for t in database.get_all('turnos')}
    modalidades = {m['id']: m['nombre'] for m in database.get_all('modalidades')}

    for s in solicitudes:
        s['carrera_id'] = s['oferta_id']
        oferta = ofertas.get(s.get('oferta_id'), {})
        s['carrera_nombre'] = oferta.get('nombre', '')
        s['nivel_nombre'] = niveles.get(oferta.get('nivel_id'), '')
        s['turno'] = turnos.get(s.get('turno_id'), '')
        s['modalidad'] = modalidades.get(s.get('modalidad_id'), '')

    return solicitudes or []

@app.post("/api/instituciones/{cue}/carreras")
def crear_carrera_institucion(cue: str, data: InstitucionCarreraCreate):
    oferta_data = {
        'nombre': data.nombre,
        'nivel_id': data.nivel_id,
        'duracion_meses': data.duracion_meses,
        'descripcion': data.descripcion,
        'activo': True
    }
    result = database.insert('ofertas_educativas', oferta_data)
    if not result:
        raise HTTPException(status_code=500, detail="Error al crear la carrera")
    oferta_id = result if isinstance(result, int) else result.get('id') if isinstance(result, dict) else None
    if not oferta_id:
        raise HTTPException(status_code=500, detail="Error al obtener ID de la carrera")
    existe = database.get_one('institucion_oferta', {'institucion_cue': cue, 'oferta_id': oferta_id})
    if not existe:
        database.insert('institucion_oferta', {
            'institucion_cue': cue,
            'oferta_id': oferta_id,
            'turno_id': data.turno_id
        })
    return {"success": True, "message": "Carrera creada correctamente", "id": oferta_id}

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

# === ENDPOINTS DE MENSAJES ===
class MensajeCreate(BaseModel):
    institucion_cue: str
    contenido: str
    remitente: Optional[str] = 'institucion'

@app.get("/api/mensajes")
def get_mensajes(institucion_cue: str):
    mensajes = database.get_all('mensajes', {'institucion_cue': institucion_cue})
    if mensajes:
        mensajes.sort(key=lambda m: m.get('created_at', ''))
    return mensajes or []

@app.post("/api/mensajes")
def create_mensaje(msg: MensajeCreate):
    data = {
        'institucion_cue': msg.institucion_cue,
        'contenido': msg.contenido,
        'remitente': msg.remitente or 'institucion',
        'leido': 0
    }
    result = database.insert('mensajes', data)
    if not result:
        raise HTTPException(status_code=500, detail="Error al enviar mensaje")
    return {"success": True, "message": "Mensaje enviado", "id": result}

# === ENDPOINTS DE SOLICITUDES DE CAMBIO ===
class SolicitudCambioCreate(BaseModel):
    institucion_cue: str
    campo: str
    valor_actual: Optional[str] = None
    valor_nuevo: str

@app.get("/api/solicitudes-cambio")
def get_solicitudes_cambio(institucion_cue: str, estado: Optional[str] = None):
    filters = {'institucion_cue': institucion_cue}
    if estado:
        filters['estado'] = estado
    solicitudes = database.get_all('solicitudes_cambio', filters)
    return solicitudes or []

@app.post("/api/solicitudes-cambio")
def create_solicitud_cambio(sol: SolicitudCambioCreate):
    data = {
        'institucion_cue': sol.institucion_cue,
        'campo': sol.campo,
        'valor_actual': sol.valor_actual,
        'valor_nuevo': sol.valor_nuevo,
        'estado': 'pendiente'
    }
    result = database.insert('solicitudes_cambio', data)
    if not result:
        raise HTTPException(status_code=500, detail="Error al crear solicitud de cambio")
    return {"success": True, "message": "Solicitud de cambio enviada", "id": result}

# === ADMIN: TODAS LAS CONVERSACIONES ===
@app.get("/api/admin/conversaciones")
def get_conversaciones():
    mensajes = database.get_all('mensajes') or []
    instituciones = {i['cue']: i for i in (database.get_all('instituciones') or [])}
    grupos = {}
    for m in mensajes:
        cue = m['institucion_cue']
        if cue not in grupos:
            grupos[cue] = []
        grupos[cue].append(m)
    result = []
    for cue, msgs in grupos.items():
        msgs.sort(key=lambda x: x.get('created_at', ''))
        ultimo = msgs[-1]
        inst = instituciones.get(cue, {})
        no_leidos = sum(1 for m in msgs if m.get('remitente') == 'institucion' and not m.get('leido'))
        result.append({
            'institucion_cue': cue,
            'institucion_nombre': inst.get('nombre', 'Sin nombre'),
            'email': inst.get('email', ''),
            'ultimo_mensaje': ultimo.get('contenido', ''),
            'fecha_ultimo': ultimo.get('created_at', ''),
            'total': len(msgs),
            'no_leidos': no_leidos,
            'ultimo_remitente': ultimo.get('remitente', '')
        })
    result.sort(key=lambda x: x.get('fecha_ultimo', ''), reverse=True)
    return result

# === ADMIN: MENSAJES POR INSTITUCION ===
@app.get("/api/admin/mensajes/{cue}")
def get_admin_mensajes(cue: str):
    mensajes = database.get_all('mensajes', {'institucion_cue': cue}) or []
    mensajes.sort(key=lambda m: m.get('created_at', ''))
    # Mark as read when admin views
    for m in mensajes:
        if m.get('remitente') == 'institucion' and not m.get('leido'):
            database.update('mensajes', {'leido': 1}, {'id': m['id']})
            m['leido'] = 1
    return mensajes

# === ADMIN: SOLICITUDES DE CAMBIO ===
class SolicitudRechazo(BaseModel):
    motivo_rechazo: Optional[str] = None

@app.get("/api/admin/solicitudes-cambio")
def get_admin_solicitudes_cambio(estado: Optional[str] = None):
    filters = {}
    if estado:
        filters['estado'] = estado
    solicitudes = database.get_all('solicitudes_cambio', filters) or []
    instituciones = {i['cue']: i['nombre'] for i in (database.get_all('instituciones') or [])}
    for s in solicitudes:
        s['institucion_nombre'] = instituciones.get(s.get('institucion_cue'), '')
    solicitudes.sort(key=lambda x: x.get('created_at', ''), reverse=True)
    return solicitudes

@app.put("/api/admin/solicitudes-cambio/{id}/aprobar")
def aprobar_solicitud_cambio(id: int):
    solicitud = database.get_one('solicitudes_cambio', {'id': id, 'estado': 'pendiente'})
    if not solicitud:
        raise HTTPException(status_code=404, detail="Solicitud no encontrada o ya procesada")
    cue = solicitud['institucion_cue']
    campo = solicitud['campo']
    valor_nuevo = solicitud['valor_nuevo']
    database.update('instituciones', {campo: valor_nuevo}, {'cue': cue})
    database.update('solicitudes_cambio', {'estado': 'aprobado'}, {'id': id})
    return {"success": True, "message": f"Cambio de '{campo}' aprobado y aplicado"}

@app.put("/api/admin/solicitudes-cambio/{id}/rechazar")
def rechazar_solicitud_cambio(id: int, data: SolicitudRechazo):
    updates = {'estado': 'rechazado', 'motivo_rechazo': data.motivo_rechazo or ''}
    result = database.update('solicitudes_cambio', updates, {'id': id, 'estado': 'pendiente'})
    if not result:
        raise HTTPException(status_code=404, detail="Solicitud no encontrada o ya procesada")
    return {"success": True, "message": "Solicitud rechazada"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)