const DATOS = {
    instituciones: [
        {
            cue: '0001234',
            nombre: 'EEST N°1 "General San Martín"',
            tipo: 'Secundaria Técnica',
            direccion: 'Av. Libertador 1234',
            barrio: 'San Miguel Centro',
            telefono: '011-4455-1234',
            competencias: ['Computación', 'Electrónica', 'Mecánica']
        },
        {
            cue: '0002345',
            nombre: 'ISFT N°182 "Dr. Antonio F. Celesia"',
            tipo: 'Superior',
            direccion: 'Calle Buenos Aires 567',
            barrio: 'Muñiz',
            telefono: '011-4667-2345',
            competencias: ['Programación', 'Redes', 'Análisis de Sistemas']
        },
        {
            cue: '0003456',
            nombre: 'Escuela Secundaria N°45',
            tipo: 'Secundaria',
            direccion: 'Calle Maipú 890',
            barrio: 'Campo de Mayo',
            telefono: '011-4778-3456',
            competencias: ['Pedagogía', 'Didáctica', 'Matemática']
        },
        {
            cue: '0004567',
            nombre: 'Centro Educativo de Formación Profesional N°401',
            tipo: 'Formación Profesional',
            direccion: 'Calle San Juan 123',
            barrio: 'Los Polvorines',
            telefono: '011-4889-4567',
            competencias: ['Soldadura', 'Mecánica', 'Industria']
        },
        {
            cue: '0005678',
            nombre: 'Instituto Superior de Formación Técnica N°207',
            tipo: 'Superior',
            direccion: 'Av. Perón 2456',
            barrio: 'San Miguel',
            telefono: '011-4990-5678',
            competencias: ['Electrónica', 'Automatización', 'Industria']
        },
        {
            cue: '0006789',
            nombre: 'Escuela de Educación Secundaria N°78',
            tipo: 'Secundaria',
            direccion: 'Calle Rivadavia 789',
            barrio: 'Bella Vista',
            telefono: '011-5001-6789',
            competencias: ['Pedagogía', 'Didáctica']
        }
    ],
    competencias: [
        { id: 1, nombre: 'Programación', icono: 'fa-code', descripcion: 'Desarrollo de software' },
        { id: 2, nombre: 'Redes', icono: 'fa-network-wired', descripcion: 'Infraestructura de redes' },
        { id: 3, nombre: 'Electrónica', icono: 'fa-microchip', descripcion: 'Circuitos y sistemas' },
        { id: 4, nombre: 'Automatización', icono: 'fa-robot', descripcion: 'Control automático' },
        { id: 5, nombre: 'Pedagogía', icono: 'fa-chalkboard-teacher', descripcion: 'Educación y enseñanza' },
        { id: 6, nombre: 'Didáctica', icono: 'fa-book-open', descripcion: 'Métodos de enseñanza' },
        { id: 7, nombre: 'Matemática', icono: 'fa-calculator', descripcion: 'Cálculo y lógica' },
        { id: 8, nombre: 'Mecánica', icono: 'fa-cogs', descripcion: 'Máquinas y motores' },
        { id: 9, nombre: 'Industria', icono: 'fa-industry', descripcion: 'Producción industrial' },
        { id: 10, nombre: 'Soldadura', icono: 'fa-fire', descripcion: 'Unión de metales' },
        { id: 11, nombre: 'Computación', icono: 'fa-laptop', descripcion: 'Tecnología digital' },
        { id: 12, nombre: 'Análisis de Sistemas', icono: 'fa-project-diagram', descripcion: 'Diseño de sistemas' }
    ],
    carreras: [
        { id: 1, nombre: 'Técnico en Programación', nivel: 'Superior', competencias: ['Programación', 'Computación'], duracion: '3 años' },
        { id: 2, nombre: 'Analista de Sistemas', nivel: 'Superior', competencias: ['Análisis de Sistemas', 'Redes'], duracion: '3 años' },
        { id: 3, nombre: 'Técnico en Electrónica', nivel: 'Secundaria Técnica', competencias: ['Electrónica', 'Automatización'], duracion: '6 años' },
        { id: 4, nombre: 'Técnico Mecánico', nivel: 'Secundaria Técnica', competencias: ['Mecánica', 'Industria'], duracion: '6 años' },
        { id: 5, nombre: 'Bachiller en Ciencias Naturales', nivel: 'Secundaria', competencias: ['Matemática', 'Didáctica'], duracion: '5 años' },
        { id: 6, nombre: 'Bachiller en Ciencias Sociales', nivel: 'Secundaria', competencias: ['Pedagogía'], duracion: '5 años' },
        { id: 7, nombre: 'Bachiller en Economía y Administración', nivel: 'Secundaria', competencias: ['Didáctica'], duracion: '5 años' },
        { id: 8, nombre: 'Profesorado de Matemática', nivel: 'Superior', competencias: ['Matemática', 'Pedagogía'], duracion: '4 años' },
        { id: 9, nombre: 'Técnico en Automotores', nivel: 'Secundaria Técnica', competencias: ['Mecánica'], duracion: '6 años' },
        { id: 10, nombre: 'Técnico en Construcciones', nivel: 'Secundaria Técnica', competencias: ['Industria'], duracion: '6 años' },
        { id: 11, nombre: 'Operador de PC', nivel: 'Formación Profesional', competencias: ['Computación'], duracion: '6 meses' },
        { id: 12, nombre: 'Soldador', nivel: 'Formación Profesional', competencias: ['Soldadura', 'Industria'], duracion: '8 meses' },
        { id: 13, nombre: 'Administración de Redes', nivel: 'Superior', competencias: ['Redes'], duracion: '2 años' },
        { id: 14, nombre: 'Técnico en Automatización Industrial', nivel: 'Superior', competencias: ['Automatización', 'Electrónica'], duracion: '3 años' },
        { id: 15, nombre: 'Auxiliar en Electrónica', nivel: 'Formación Profesional', competencias: ['Electrónica'], duracion: '1 año' }
    ],
    carrerasSugeridas: [
        'Bachiller en Ciencias Naturales',
        'Bachiller en Ciencias Sociales',
        'Bachiller en Economía y Administración',
        'Profesorado de Matemática',
        'Técnico en Automotores',
        'Técnico en Construcciones',
        'Técnico en Electrónica',
        'Técnico en Informática Profesional y Personal',
        'Técnico Superior en Análisis de Sistemas',
        'Analista de Sistemas',
        'Técnico en Programación',
        'Administración de Redes',
        'Operador de PC',
        'Soldador'
    ],
    tiposInstitucion: ['Secundaria', 'Secundaria Técnica', 'Superior', 'Formación Profesional']
};

let competenciasSeleccionadas = [];
let chipActivo = null;

document.addEventListener('DOMContentLoaded', () => {
    inicializarApp();
});

function inicializarApp() {
    document.getElementById('menu-inicio')?.addEventListener('click', () => {
        window.location.href = '../index.html';
    });
    
    inicializarTabs();
    inicializarVistaInstitucion();
    inicializarVistaCompetencia();
    inicializarVistaCarrera();
}

function inicializarTabs() {
    const tabs = document.querySelectorAll('.tab-button');
    const contenidos = document.querySelectorAll('.tab-content');
    
    // Verificar si la pestaña de carreras ya está activa
    const carreraTab = document.querySelector('.tab-button[data-tab="carrera"]');
    if (carreraTab && carreraTab.classList.contains('active')) {
        console.log('Pestaña carrera ya está activa, cargando...');
        cargarCarrerasAgrupadas();
    }
    
    // Renderizar competencias si el tab ya está activo
    const compTab = document.querySelector('.tab-button[data-tab="competencia"]');
    if (compTab && compTab.classList.contains('active')) {
        inicializarVistaCompetencia();
    }
    
    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            const tabId = tab.dataset.tab;
            console.log('Tab clickeado:', tabId);
            
            tabs.forEach(t => t.classList.remove('active'));
            tab.classList.add('active');
            
            contenidos.forEach(contenido => {
                contenido.classList.remove('active');
                if (contenido.id === `vista-${tabId}`) {
                    contenido.classList.add('active');
                }
            });
            
            // Cargar carreras cuando se seleccione la pestaña
            if (tabId === 'carrera') {
                console.log('Cargando carreras...');
                cargarCarrerasAgrupadas();
            }
            
            // Renderizar competencias cuando se seleccione la pestaña
            if (tabId === 'competencia') {
                console.log('Tab competencia clickeado');
                // Pequeño delay para asegurar que el tab sea visible
                setTimeout(() => {
                    inicializarVistaCompetencia();
                }, 50);
            }
        });
    });
}

function inicializarVistaInstitucion() {
    const select = document.getElementById('filtro-tipo-inst');
    DATOS.tiposInstitucion.forEach(tipo => {
        const option = document.createElement('option');
        option.value = tipo;
        option.textContent = tipo;
        select.appendChild(option);
    });
    
    const input = document.getElementById('buscar-institucion');
    input.addEventListener('input', () => filtrarInstituciones());
    select.addEventListener('change', () => filtrarInstituciones());
    
    renderizarInstituciones(DATOS.instituciones);
}

function filtrarInstituciones() {
    const texto = document.getElementById('buscar-institucion').value.toLowerCase();
    const tipo = document.getElementById('filtro-tipo-inst').value;
    
    const filtradas = DATOS.instituciones.filter(inst => {
        const matchTexto = inst.nombre.toLowerCase().includes(texto) || 
                          inst.direccion.toLowerCase().includes(texto) ||
                          inst.barrio.toLowerCase().includes(texto);
        const matchTipo = !tipo || inst.tipo === tipo;
        return matchTexto && matchTipo;
    });
    
    renderizarInstituciones(filtradas);
}

function renderizarInstituciones(instituciones) {
    const container = document.getElementById('resultados-instituciones');
    
    if (instituciones.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <i class="fas fa-search"></i>
                <h3>No se encontraron resultados</h3>
                <p>Probá modificar los filtros o buscar otro término</p>
            </div>
        `;
        return;
    }
    
    container.innerHTML = instituciones.map(inst => `
        <div class="card" data-cue="${inst.cue}">
            <div class="card-header">
                <div>
                    <h3 class="card-title">${inst.nombre}</h3>
                    <span class="card-badge">${inst.tipo}</span>
                </div>
                <div class="card-arrow">
                    <i class="fas fa-arrow-right"></i>
                </div>
            </div>
            <div class="card-info">
                <div class="card-info-item">
                    <i class="fas fa-map-marker-alt"></i>
                    <span>${inst.direccion}${inst.barrio ? ', ' + inst.barrio : ''}</span>
                </div>
                <div class="card-info-item">
                    <i class="fas fa-phone"></i>
                    <span>${inst.telefono}</span>
                </div>
                <div class="card-info-item">
                    <i class="fas fa-tools"></i>
                    <span>${inst.competencias.join(', ')}</span>
                </div>
            </div>
        </div>
    `).join('');
    
    container.querySelectorAll('.card').forEach(card => {
        card.addEventListener('click', () => {
            const cue = card.dataset.cue;
            const inst = DATOS.instituciones.find(i => i.cue === cue);
            if (inst) {
                alert(`Institución: ${inst.nombre}\n\nCompetencias: ${inst.competencias.join(', ')}`);
            }
        });
    });
}

function inicializarVistaCompetencia() {
    const container = document.getElementById('competencias-tarjetas-container');
    
    if (!container) {
        console.log('ERROR: Contenedor no encontrado');
        document.querySelector('.section-header').insertAdjacentHTML('afterend', '<div id="competencias-tarjetas-container"></div>');
        const nuevoContainer = document.getElementById('competencias-tarjetas-container');
        console.log('Contenedor creado:', nuevoContainer);
    }
    
    if (container.innerHTML.trim() !== '') {
        console.log('Competencias ya renderizadas');
        return;
    }
    
    console.log('Renderizando competencias..., container:', container);
    
    // Generar el HTML directamente
    let html = '';
    for (const comp of DATOS.competencias) {
        html += '<div class="competencia-card">';
        html += '<input type="checkbox" id="comp-' + comp.id + '" value="' + comp.id + '">';
        html += '<label for="comp-' + comp.id + '">';
        html += '<i class="fas ' + comp.icono + ' card-icono"></i>';
        html += '<span class="card-titulo">' + comp.nombre + '</span>';
        html += '<span class="card-descripcion">' + comp.descripcion + '</span>';
        html += '</label>';
        html += '</div>';
    }
    
    console.log('HTML generado:', html);
    container.innerHTML = html;
    
    // Agregar event listeners
    container.querySelectorAll('input[type="checkbox"]').forEach(cb => {
        cb.addEventListener('change', actualizarCompetenciasSeleccionadas);
    });
    
    // Event listener para botón limpiar
    document.getElementById('btn-limpiar-seleccion').addEventListener('click', limpiarSeleccion);
    
    console.log('Competencias renderizadas correctamente');
    renderizarCarrerasPorCompetencia();
}

function actualizarCompetenciasSeleccionadas() {
    competenciasSeleccionadas = [];
    document.querySelectorAll('#competencias-tarjetas-container input[type="checkbox"]:checked').forEach(cb => {
        const id = parseInt(cb.value);
        const comp = DATOS.competencias.find(c => c.id === id);
        if (comp) competenciasSeleccionadas.push(comp.nombre);
    });
    
    // Mostrar/ocultar botón de limpiar
    const btnLimpiar = document.getElementById('btn-limpiar-seleccion');
    if (competenciasSeleccionadas.length > 0) {
        btnLimpiar.style.display = 'flex';
    } else {
        btnLimpiar.style.display = 'none';
    }
    
    renderizarCarrerasPorCompetencia();
}

function limpiarSeleccion() {
    document.querySelectorAll('#competencias-tarjetas-container input[type="checkbox"]').forEach(cb => {
        cb.checked = false;
    });
    competenciasSeleccionadas = [];
    document.getElementById('btn-limpiar-seleccion').style.display = 'none';
    renderizarCarrerasPorCompetencia();
}

function renderizarCarrerasPorCompetencia() {
    const container = document.getElementById('resultados-competencias');
    
    if (competenciasSeleccionadas.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <i class="fas fa-search"></i>
                <h3>No hay carreras seleccionadas</h3>
                <p>Elegí alguna competencia para ver las ofertas educativas</p>
            </div>
        `;
        return;
    }
    
    const carrerasFiltradas = DATOS.carreras.filter(carrera => {
        return carrera.competencias.some(comp => competenciasSeleccionadas.includes(comp));
    });
    
    if (carrerasFiltradas.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <i class="fas fa-folder-open"></i>
                <h3>Sin resultados</h3>
                <p>No hay carreras que coincidan con las competencias seleccionadas</p>
            </div>
        `;
        return;
    }
    
    container.innerHTML = `
        <div style="grid-column: 1/-1; margin-bottom: 10px; color: var(--text-gray); font-size: 0.95rem;">
            <i class="fas fa-info-circle"></i> ${carrerasFiltradas.length} carrera${carrerasFiltradas.length !== 1 ? 's' : ''} encontrada${carrerasFiltradas.length !== 1 ? 's' : ''}
        </div>
        ${carrerasFiltradas.map(carrera => crearCardCarrera(carrera)).join('')}
    `;
}

function inicializarVistaCarrera() {
    // Cargar carreras desde Supabase
    cargarCarrerasAgrupadas();
}

function renderizarChipsCarreras() {
    const container = document.getElementById('chips-carreras');
    
    container.innerHTML = DATOS.carrerasSugeridas.map((carrera, idx) => `
        <div class="chip" data-index="${idx}">
            <i class="fas fa-graduation-cap"></i>
            ${carrera}
        </div>
    `).join('');
    
    container.querySelectorAll('.chip').forEach(chip => {
        chip.addEventListener('click', () => {
            const nombre = chip.textContent.trim();
            document.getElementById('buscar-carrera').value = nombre;
            chipActivo = parseInt(chip.dataset.index);
            container.querySelectorAll('.chip').forEach(c => c.classList.remove('active'));
            chip.classList.add('active');
            buscarCarreras();
        });
    });
}

function buscarCarreras() {
    const texto = document.getElementById('buscar-carrera').value.toLowerCase().trim();
    const container = document.getElementById('resultados-carreras');
    
    if (!texto) {
        renderizarTodasCarreras();
        return;
    }
    
    const carrerasFiltradas = DATOS.carreras.filter(carrera => 
        carrera.nombre.toLowerCase().includes(texto) ||
        carrera.competencias.some(comp => comp.toLowerCase().includes(texto))
    );
    
    if (carrerasFiltradas.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <i class="fas fa-search"></i>
                <h3>Sin resultados</h3>
                <p>No se encontraron carreras que coincidan con "${texto}"</p>
            </div>
        `;
        return;
    }
    
    container.innerHTML = `
        <div style="grid-column: 1/-1; margin-bottom: 10px; color: var(--text-gray); font-size: 0.95rem;">
            <i class="fas fa-check-circle"></i> ${carrerasFiltradas.length} carrera${carrerasFiltradas.length !== 1 ? 's' : ''} encontrada${carrerasFiltradas.length !== 1 ? 's' : ''}
        </div>
        ${carrerasFiltradas.map(carrera => crearCardCarrera(carrera)).join('')}
    `;
}

function renderizarTodasCarreras() {
    const container = document.getElementById('resultados-carreras');
    
    if (DATOS.carreras.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <i class="fas fa-search"></i>
                <h3>Ingresá un término de búsqueda</h3>
                <p>Escribí en el campo de arriba o hacé clic en una carrera sugerida</p>
            </div>
        `;
        return;
    }
    
    container.innerHTML = `
        <div style="grid-column: 1/-1; margin-bottom: 10px; color: var(--text-gray); font-size: 0.95rem;">
            <i class="fas fa-book-open"></i> Todas las carreras (${DATOS.carreras.length})
        </div>
        ${DATOS.carreras.map(carrera => crearCardCarrera(carrera)).join('')}
    `;
}

function crearCardCarrera(carrera) {
    return `
        <div class="card">
            <div class="card-header">
                <div>
                    <h3 class="card-title">${carrera.nombre}</h3>
                    <span class="card-badge">${carrera.nivel}</span>
                </div>
                <div class="card-arrow">
                    <i class="fas fa-chevron-right"></i>
                </div>
            </div>
            <div class="card-info">
                <div class="card-info-item">
                    <i class="fas fa-clock"></i>
                    <span>Duración: ${carrera.duracion}</span>
                </div>
                <div class="card-info-item">
                    <i class="fas fa-tools"></i>
                    <span>${carrera.competencias.join(', ')}</span>
                </div>
            </div>
        </div>
    `;
}

/* ==========================================================================
   CARRERAS AGRUPADAS - Nuevo Diseño con Supabase
   ========================================================================== */

// Configuración de categorías basadas en competencias
const CATEGORIAS = {
    tecnologia: { 
        nombre: 'Tecnología', 
        icono: 'fa-microchip', 
        color: '#3b82f6',
        competencias: ['Computación', 'Electrónica', 'Redes', 'Análisis de Sistemas', 'Programación']
    },
    administracion: { 
        nombre: 'Administración y Gestión', 
        icono: 'fa-chart-line', 
        color: '#10b981',
        competencias: ['Administración', 'Contabilidad', 'Recursos Humanos']
    },
    salud: { 
        nombre: 'Salud', 
        icono: 'fa-heartbeat', 
        color: '#ef4444',
        competencias: ['Salud', 'Enfermería', 'Medicina']
    },
    educacion: { 
        nombre: 'Educación y Cultura', 
        icono: 'fa-graduation-cap', 
        color: '#8b5cf6',
        competencias: ['Pedagogía', 'Didáctica', 'Educación']
    },
    industria: { 
        nombre: 'Industria y Producción', 
        icono: 'fa-industry', 
        color: '#f59e0b',
        competencias: ['Mecánica', 'Industria', 'Soldadura', 'Construcción']
    },
    servicios: { 
        nombre: 'Servicios', 
        icono: 'fa-concierge-bell', 
        color: '#06b6d4',
        competencias: ['Gastronomía', 'Turismo', 'Hotelería']
    }
};

async function cargarCarrerasAgrupadas() {
    try {
        const container = document.getElementById('resultados-carreras');
        if (!container) return;
        
        container.innerHTML = '<div class="carreras-empty"><i class="fas fa-spinner fa-spin"></i><h3>Cargando carreras...</h3></div>';
        
        // Obtener carreras de Supabase via API
        let carreras = [];
        try {
            const response = await fetch('/api/carreras');
            if (response.ok) {
                carreras = await response.json();
            }
        } catch (e) {
            console.error('Error fetch carreras:', e);
        }
        
        // Si no hay datos de API, usar datos locales de ejemplo
        if (!carreras || carreras.length === 0) {
            carreras = [
                {id: 2, nombre: 'Técnico en Programación', nivel_id: 5, nivel: 'Superior', nivelKey: 'superior', descripcion: 'Formación integral en desarrollo de software, aplicaciones móviles y sistemas informatizados.', duracion: '3 años'},
                {id: 3, nombre: 'Técnico en Electrónica', nivel_id: 5, nivel: 'Superior', nivelKey: 'superior', descripcion: 'Estudio de circuitos electrónicos, sistemas digitales y microprocesadores.', duracion: '3 años'},
                {id: 4, nombre: 'Técnico Mecánico', nivel_id: 5, nivel: 'Superior', nivelKey: 'superior', descripcion: 'Formación en diseño, fabricación y mantenimiento de sistemas mecánicos.', duracion: '3 años'},
                {id: 5, nombre: 'Analista de Sistemas', nivel_id: 6, nivel: 'Formación Profesional', nivelKey: 'formacion', descripcion: 'Curso de formación profesional en análisis y desarrollo de sistemas.', duracion: '1 año'},
                {id: 6, nombre: 'Operador de PC', nivel_id: 6, nivel: 'Formación Profesional', nivelKey: 'formacion', descripcion: 'Formación básica en uso de computadoras y herramientas ofimáticas.', duracion: '6 meses'},
                {id: 7, nombre: 'Soldador', nivel_id: 6, nivel: 'Formación Profesional', nivelKey: 'formacion', descripcion: 'Formación en técnicas de soldadura industrial (SMAW, TIG, MIG/MAG).', duracion: '8 meses'},
                {id: 8, nombre: 'Bachiller Secundario', nivel_id: 4, nivel: 'Secundaria', nivelKey: 'secundaria', descripcion: 'Educación secundaria completa con orientación en ciencias sociales.', duracion: '5 años'},
                {id: 9, nombre: 'Técnico en Gastronomía', nivel_id: 5, nivel: 'Superior', nivelKey: 'superior', descripcion: 'Formación integral en técnicas culinarias, pastelería y gestión gastronómica.', duracion: '2 años'}
            ];
        }
        
        // Mapeo de nivel_id a nivel
        const nivelMap = {
            4: {nombre: 'Secundaria', key: 'secundaria'},
            5: {nombre: 'Superior', key: 'superior'},
            6: {nombre: 'Formación Profesional', key: 'formacion'}
        };
        
        // Agrupar carreras por categoría
        const carrerasPorCategoria = {};
        
        // Función para determinar categoría basada en nombre
        function getCategoria(nombre) {
            const n = nombre.toLowerCase();
            if (n.includes('técnico') || n.includes('computación') || n.includes('electrónica') || 
                n.includes('sistemas') || n.includes('analista') || n.includes('redes')) {
                return 'tecnologia';
            }
            if (n.includes('administración') || n.includes('gestión') || n.includes('contable')) {
                return 'administracion';
            }
            if (n.includes('salud') || n.includes('enfermería') || n.includes('medicina')) {
                return 'salud';
            }
            if (n.includes('profesorado') || n.includes('docencia') || n.includes('educación')) {
                return 'educacion';
            }
            if (n.includes('mecánica') || n.includes('soldadura') || n.includes('construcción')) {
                return 'industria';
            }
            if (n.includes('gastronomía') || n.includes('turismo') || n.includes('hotelería') ||
                n.includes('operador') || n.includes('bachiller')) {
                return 'servicios';
            }
            return 'tecnologia'; // default
        }
        
        carreras.forEach(carrera => {
            const infoNivel = nivelMap[carrera.nivel_id] || {nombre: 'Otros', key: 'formacion'};
            const nivelKey = infoNivel.key;
            
            // Determinar categoría basada en nombre
            let categoriaAsignada = getCategoria(carrera.nombre);
            
            if (!carrerasPorCategoria[categoriaAsignada]) {
                carrerasPorCategoria[categoriaAsignada] = [];
            }
            
            carrerasPorCategoria[categoriaAsignada].push({
                ...carrera,
                nivel: infoNivel.nombre,
                nivelKey: nivelKey
            });
        });
        
        // Renderizar por categorías
        renderizarCarrerasPorCategoria(container, carrerasPorCategoria);
        
    } catch (error) {
        console.error('Error al cargar carreras:', error);
        const container = document.getElementById('resultados-carreras');
        if (container) {
            container.innerHTML = `
                <div class="carreras-empty">
                    <i class="fas fa-exclamation-triangle"></i>
                    <h3>Error al cargar</h3>
                    <p>No se pudieron cargar las carreras. Intenta más tarde.</p>
                </div>
            `;
        }
    }
}

function renderizarCarrerasPorCategoria(container, carrerasPorCategoria) {
    const busqueda = document.getElementById('buscar-carrera')?.value.toLowerCase() || '';
    const modalidad = document.getElementById('filtro-modalidad')?.value || '';
    
    let html = '';
    let totalCarreras = 0;
    
    // Orden de categorías
    const ordenCategorias = ['tecnologia', 'administracion', 'industria', 'salud', 'educacion', 'servicios'];
    
    for (const catKey of ordenCategorias) {
        const carreras = carrerasPorCategoria[catKey];
        if (!carreras || carreras.length === 0) continue;
        
        // Filtrar por búsqueda
        let carrerasFiltradas = carreras;
        if (busqueda) {
            carrerasFiltradas = carreras.filter(c => 
                c.nombre.toLowerCase().includes(busqueda)
            );
        }
        
        if (carrerasFiltradas.length === 0) continue;
        
        totalCarreras += carrerasFiltradas.length;
        const categoria = CATEGORIAS[catKey];
        
        html += `
            <div class="categoria-seccion">
                <div class="categoria-header">
                    <div class="categoria-icono" style="background: ${categoria.color}">
                        <i class="fas ${categoria.icono}"></i>
                    </div>
                    <div>
                        <h3 class="categoria-titulo">${categoria.nombre}</h3>
                    </div>
                    <span class="categoria-cantidad">${carrerasFiltradas.length} carrera${carrerasFiltradas.length !== 1 ? 's' : ''}</span>
                </div>
                <div class="carreras-grid">
                    ${carrerasFiltradas.map(carrera => crearCardCarreraModerna(carrera, categoria)).join('')}
                </div>
            </div>
        `;
    }
    
    if (totalCarreras === 0) {
        html = `
            <div class="carreras-empty">
                <i class="fas fa-search"></i>
                <h3>Sin resultados</h3>
                <p>No se encontraron carreras que coincidan con tu búsqueda.</p>
            </div>
        `;
    }
    
    container.innerHTML = html;
}

function crearCardCarreraModerna(carrera, categoria) {
    const descripcion = carrera.descripcion || 'Formación profesional integral con salida laboral.';
    const duracion = carrera.duracion || 'Según plan de estudios';
    
    return `
        <div class="tarjeta-carrera">
            <div class="carrera-card" onclick="verDetalleCarrera(${carrera.id})">
                <div class="carrera-card-header">
                    <span class="carrera-card-nivel ${carrera.nivelKey}">${carrera.nivel}</span>
                    <h3 class="carrera-card-titulo">${carrera.nombre}</h3>
                    <p class="carrera-card-desc">${descripcion}</p>
                </div>
                <div class="carrera-card-info">
                    <div class="carrera-card-info-item">
                        <i class="fas fa-clock"></i>
                        <span>${duracion}</span>
                    </div>
                    <div class="carrera-card-info-item">
                        <i class="fas fa-school"></i>
                        <span>Presencial</span>
                    </div>
                </div>
                <div class="carrera-card-footer">
                    <button class="carrera-card-btn">
                        <i class="fas fa-eye"></i> Ver más
                    </button>
                </div>
            </div>
        </div>
    `;
}

function verDetalleCarrera(id) {
    const modal = document.getElementById('modal-detalle-carrera');
    const loading = document.getElementById('modal-detalle-loading');
    const body = document.getElementById('modal-detalle-body');
    
    modal.style.display = 'flex';
    loading.style.display = 'block';
    body.style.display = 'none';
    
    fetch(`/api/carreras/${id}/detalle`)
        .then(res => res.json())
        .then(data => {
            const nivelKey = data.nivel_id === 1 ? 'secundaria' : data.nivel_id === 2 ? 'superior' : 'formacion';
            const nivelNombre = data.nivel_id === 1 ? 'Secundaria' : data.nivel_id === 2 ? 'Superior' : 'Formación Profesional';
            
            const institucionesHTML = data.instituciones && data.instituciones.length > 0 
                ? data.instituciones.map(inst => `
                    <div class="institucion-card">
                        <h4><i class="fas fa-school"></i> ${inst.institucion.nombre}</h4>
                        <p><i class="fas fa-map-marker-alt"></i> ${inst.institucion.direccion || 'Sin dirección'}, ${inst.institucion.barrio || ''}</p>
                        <p><i class="fas fa-clock"></i> Turno: ${inst.turno || 'Según dispone la institución'}</p>
                        <p><i class="fas fa-laptop-house"></i> Modalidad: ${inst.modalidad || 'Presencial'}</p>
                        ${inst.institucion.telefono ? `<div class="contacto-item"><i class="fas fa-phone"></i> <a href="tel:${inst.institucion.telefono}">${inst.institucion.telefono}</a></div>` : ''}
                        ${inst.institucion.email ? `<div class="contacto-item"><i class="fas fa-envelope"></i> <a href="mailto:${inst.institucion.email}">${inst.institucion.email}</a></div>` : ''}
                        ${inst.institucion.sitio_web ? `<div class="contacto-item"><i class="fas fa-globe"></i> <a href="${inst.institucion.sitio_web}" target="_blank">${inst.institucion.sitio_web}</a></div>` : ''}
                    </div>
                `).join('')
                : '<p>No hay instituciones registradas para esta carrera.</p>';
            
            const competenciasHTML = data.competencias && data.competencias.length > 0
                ? data.competencias.map(c => `
                    <span class="competencia-tag">
                        <i class="fas fa-check-circle"></i> ${c.nombre}
                    </span>
                `).join('')
                : '<p style="color: var(--text-gray);">No hay competencias asociadas.</p>';
            
            body.innerHTML = `
                <div class="detalle-carrera-header">
                    <h2>${data.nombre}</h2>
                    <span class="detalle-nivel ${nivelKey}">${nivelNombre}</span>
                </div>
                <div class="detalle-carrera-body">
                    <div class="detalle-seccion">
                        <h3><i class="fas fa-info-circle"></i> Información General</h3>
                        <div class="detalle-info-grid">
                            <div class="detalle-info-item">
                                <i class="fas fa-clock"></i>
                                <span>${data.duracion || 'Según plan de estudios'}</span>
                            </div>
                            <div class="detalle-info-item">
                                <i class="fas fa-graduation-cap"></i>
                                <span>${nivelNombre}</span>
                            </div>
                        </div>
                    </div>
                    
                    <div class="detalle-seccion">
                        <h3><i class="fas fa-align-left"></i> Descripción</h3>
                        <p class="detalle-descripcion">${data.descripcion || 'No hay descripción disponible.'}</p>
                    </div>
                    
                    <div class="detalle-seccion">
                        <h3><i class="fas fa-user-graduate"></i> Perfil del Egresado</h3>
                        <div class="detalle-perfil">
                            <p>${data.perfil_egresado || 'No hay información del perfil del egresado.'}</p>
                        </div>
                    </div>
                    
                    <div class="detalle-seccion">
                        <h3><i class="fas fa-building"></i> Instituciones donde se Dicta</h3>
                        <div class="detalle-instituciones">
                            ${institucionesHTML}
                        </div>
                    </div>
                    
                    <div class="detalle-seccion">
                        <h3><i class="fas fa-tools"></i> Competencias que aprenderás</h3>
                        <div class="detalle-competencias">
                            ${competenciasHTML}
                        </div>
                    </div>
                </div>
            `;
            
            loading.style.display = 'none';
            body.style.display = 'block';
        })
        .catch(error => {
            console.error('Error:', error);
            body.innerHTML = `
                <div style="padding: 40px; text-align: center;">
                    <i class="fas fa-exclamation-circle" style="font-size: 3rem; color: #e74c3c;"></i>
                    <p style="margin-top: 16px; color: #666;">Error al cargar los detalles de la carrera.</p>
                </div>
            `;
            loading.style.display = 'none';
            body.style.display = 'block';
        });
}

function cerrarModalDetalle() {
    document.getElementById('modal-detalle-carrera').style.display = 'none';
}

document.addEventListener('click', function(e) {
    const modal = document.getElementById('modal-detalle-carrera');
    if (e.target === modal) {
        modal.style.display = 'none';
    }
});

// Event listeners para búsqueda en tiempo real
document.addEventListener('DOMContentLoaded', () => {
    const inputBusqueda = document.getElementById('buscar-carrera');
    const selectModalidad = document.getElementById('filtro-modalidad');
    
    if (inputBusqueda) {
        inputBusqueda.addEventListener('input', () => {
            // Recargar con nuevos filtros
            if (window.carrerasData) {
                const container = document.getElementById('resultados-carreras');
                const carrerasPorCategoria = window.carrerasData;
                renderizarCarrerasPorCategoria(container, carrerasPorCategoria);
            }
        });
    }
    
    if (selectModalidad) {
        selectModalidad.addEventListener('change', () => {
            if (window.carrerasData) {
                const container = document.getElementById('resultados-carreras');
                const carrerasPorCategoria = window.carrerasData;
                renderizarCarrerasPorCategoria(container, carrerasPorCategoria);
            }
        });
    }
});

// Guardar datos globally para filtros
window.carrerasData = null;

// Guardar carreras por categoría globally para filtros en tiempo real
const originalRenderizar = renderizarCarrerasPorCategoria;
renderizarCarrerasPorCategoria = function(container, carrerasPorCategoria) {
    window.carrerasData = carrerasPorCategoria;
    originalRenderizar(container, carrerasPorCategoria);
};
