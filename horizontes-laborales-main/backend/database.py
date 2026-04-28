from supabase import create_client, Client
import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def execute_query(query, params=None, fetch=True):
    """Ejecuta una consulta SQL a través de Supabase"""
    try:
        from supabase import lib
        response = supabase.rpc('exec_sql', {'query': query, 'params': params or []}).execute()
        if response.data:
            return response.data if fetch else len(response.data)
        return [] if fetch else None
    except Exception as e:
        print(f"Error en execute_query: {e}")
        try:
            result = supabase.cli.postgrest.execute(query, params or [])
            return result if fetch else None
        except Exception as e2:
            print(f"Error alternativo: {e2}")
            return None if fetch else None

def execute_query_one(query, params=None):
    """Ejecuta una consulta y retorna un solo resultado"""
    result = execute_query(query, params, fetch=True)
    if result and len(result) > 0:
        return result[0]
    return None

def get_all(table, filters=None):
    """Obtiene todos los registros de una tabla"""
    try:
        query = supabase.table(table).select('*')
        if filters:
            for key, value in filters.items():
                query = query.eq(key, value)
        result = query.execute()
        return result.data if result.data else []
    except Exception as e:
        print(f"Error en get_all: {e}")
        return []

def get_one(table, filters):
    """Obtiene un registro"""
    try:
        query = supabase.table(table).select('*')
        for key, value in filters.items():
            query = query.eq(key, value)
        result = query.execute()
        if result.data and len(result.data) > 0:
            return result.data[0]
        return None
    except Exception as e:
        print(f"Error en get_one: {e}")
        return None

def insert(table, data):
    """Inserta un registro y retorna el ID"""
    try:
        result = supabase.table(table).insert(data).execute()
        if result.data and len(result.data) > 0:
            return result.data[0].get('id')
        return None
    except Exception as e:
        print(f"Error en insert: {e}")
        return None

def update(table, data, filters):
    """Actualiza registros"""
    try:
        query = supabase.table(table).update(data)
        for key, value in filters.items():
            query = query.eq(key, value)
        result = query.execute()
        return result.data
    except Exception as e:
        print(f"Error en update: {e}")
        return None

def delete(table, filters):
    """Elimina registros"""
    try:
        query = supabase.table(table).delete()
        for key, value in filters.items():
            query = query.eq(key, value)
        result = query.execute()
        return result.data
    except Exception as e:
        print(f"Error en delete: {e}")
        return None

def count(table, filters=None):
    """Cuenta registros"""
    try:
        query = supabase.table(table).select('*', count='exact')
        if filters:
            for key, value in filters.items():
                query = query.eq(key, value)
        result = query.execute()
        return result.count if result.count else 0
    except Exception as e:
        print(f"Error en count: {e}")
        return 0