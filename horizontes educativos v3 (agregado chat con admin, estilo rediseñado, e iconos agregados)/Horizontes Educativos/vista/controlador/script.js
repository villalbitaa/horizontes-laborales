let institucionesData = [];
let competenciasData = [];
let carrerasData = [];
let tiposInstitucionData = [];

let competenciasSeleccionadas = [];

document.addEventListener('DOMContentLoaded', () => {
    inicializarApp();
});

async function inicializarApp() {
    document.getElementById('menu-inicio')?.addEventListener('click', () => {
        window.location.href = '/';
    });

    document.getElementById('menu-institucion')?.addEventListener('click', () => {
        window.location.href = '/institucion';
    });

    document.getElementById('menu-horizontes')?.addEventListener('click', (e) => {
        window.location.href = '/horizontes';
    });

    try {
        const [instRes, compRes, carrerasRes, tiposRes] = await Promise.all([
            fetch('/api/instituciones'),
            fetch('/api/competencias'),
            fetch('/api/carreras'),
            fetch('/api/tipos-institucion')
        ]);

        institucionesData = await instRes.json();
        competenciasData = await compRes.json();
        carrerasData = await carrerasRes.json();
        tiposInstitucionData = await tiposRes.json();
    } catch (e) {
        console.error('Error cargando datos:', e);
    }

    inicializarTabs();
    inicializarVistaInstitucion();
    inicializarVistaCompetencia();
    inicializarVistaCarrera();
}

function inicializarTabs() {
    const tabs = document.querySelectorAll('.tab-button');
    const contenidos = document.querySelectorAll('.tab-content');

    const carreraTab = document.querySelector('.tab-button[data-tab="carrera"]');
    if (carreraTab && carreraTab.classList.contains('active')) {
        cargarCarrerasAgrupadas();
    }

    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            const tabId = tab.dataset.tab;

            tabs.forEach(t => t.classList.remove('active'));
            tab.classList.add('active');

            contenidos.forEach(contenido => {
                contenido.classList.remove('active');
                if (contenido.id === `vista-${tabId}`) {
                    contenido.classList.add('active');
                }
            });

            if (tabId === 'carrera') {
                cargarCarrerasAgrupadas();
            }

            if (tabId === 'competencia') {
                setTimeout(() => {
                    inicializarVistaCompetencia();
                }, 50);
            }
        });
    });
}

function inicializarVistaInstitucion() {
    const select = document.getElementById('filtro-tipo-inst');
    tiposInstitucionData.forEach(tipo => {
        const option = document.createElement('option');
        option.value = tipo.nombre || tipo;
        option.textContent = tipo.nombre || tipo;
        select.appendChild(option);
    });

    const input = document.getElementById('buscar-institucion');
    input.addEventListener('input', () => filtrarInstituciones());
    select.addEventListener('change', () => filtrarInstituciones());

    renderizarInstituciones(institucionesData);
}

function filtrarInstituciones() {
    const texto = document.getElementById('buscar-institucion').value.toLowerCase();
    const tipo = document.getElementById('filtro-tipo-inst').value;

    const filtradas = institucionesData.filter(inst => {
        const matchTexto = inst.nombre.toLowerCase().includes(texto) ||
                          (inst.direccion && inst.direccion.toLowerCase().includes(texto));
        const matchTipo = !tipo || (inst.tipo_nombre && inst.tipo_nombre === tipo);
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
                    <span class="card-badge">${inst.tipo_nombre || ''}</span>
                </div>
                <div class="card-arrow">
                    <i class="fas fa-arrow-right"></i>
                </div>
            </div>
            <div class="card-info">
                <div class="card-info-item">
                    <i class="fas fa-map-marker-alt"></i>
                    <span>${inst.direccion || ''}</span>
                </div>
                <div class="card-info-item">
                    <i class="fas fa-phone"></i>
                    <span>${inst.telefono || ''}</span>
                </div>
            </div>
        </div>
    `).join('');

    container.querySelectorAll('.card').forEach(card => {
        card.addEventListener('click', () => {
            const cue = card.dataset.cue;
            const inst = institucionesData.find(i => i.cue === cue);
            if (inst) {
                verInstitucionDetalle(cue, inst.nombre);
            }
        });
    });
}

async function verInstitucionDetalle(cue, nombre) {
    const modal = document.getElementById('modal-detalle-carrera');
    const loading = document.getElementById('modal-detalle-loading');
    const body = document.getElementById('modal-detalle-body');

    modal.style.display = 'flex';
    loading.style.display = 'block';
    body.style.display = 'none';

    try {
        const [instRes, carrerasRes] = await Promise.all([
            fetch(`/api/instituciones/${cue}`),
            fetch(`/api/instituciones/${cue}/carreras`)
        ]);
        const inst = await instRes.json();
        const carreras = await carrerasRes.json();

        const nivelMap = {};
        try {
            const res = await fetch('/api/niveles');
            if (res.ok) {
                const niveles = await res.json();
                niveles.forEach(n => { nivelMap[n.id] = n.nombre; });
            }
        } catch (e) {}

        body.innerHTML = `
            <div class="detalle-carrera-header">
                <h2><i class="fas fa-school"></i> ${inst.nombre}</h2>
                ${inst.direccion ? `<p style="color: #666; margin-top: 5px;"><i class="fas fa-map-marker-alt"></i> ${inst.direccion}</p>` : ''}
                ${inst.telefono ? `<p style="color: #666;"><i class="fas fa-phone"></i> ${inst.telefono}</p>` : ''}
            </div>
            <div class="detalle-carrera-body">
                <div class="detalle-seccion">
                    <h3><i class="fas fa-graduation-cap"></i> Carreras (${carreras.length})</h3>
                    ${carreras.length === 0
                        ? '<p style="color: #666;">Esta institución no tiene carreras registradas.</p>'
                        : carreras.map(c => `
                            <div class="carrera-item" style="background: #f8f9fa; border-radius: 8px; padding: 15px; margin-bottom: 10px; border-left: 4px solid #3498db;">
                                <h4 style="color: #2c3e50; margin-bottom: 5px;">${c.nombre}</h4>
                                <span style="font-size: 0.9rem; color: #666;">
                                    ${nivelMap[c.nivel_id] || c.nivel_nombre || ''} | ${c.duracion_meses ? formatDuracion(c.duracion_meses) : ''} | ${c.turno || ''}
                                </span>
                                ${c.descripcion ? `<p style="color: #666; font-size: 0.85rem; margin-top: 8px;"><i class="fas fa-user-graduate"></i> ${c.descripcion}</p>` : ''}
                            </div>
                        `).join('')
                    }
                </div>
            </div>
        `;

        loading.style.display = 'none';
        body.style.display = 'block';
    } catch (error) {
        console.error('Error:', error);
        body.innerHTML = `
            <div style="padding: 40px; text-align: center;">
                <i class="fas fa-exclamation-circle" style="font-size: 3rem; color: #e74c3c;"></i>
                <p style="margin-top: 16px; color: #666;">Error al cargar los datos de la institución.</p>
            </div>
        `;
        loading.style.display = 'none';
        body.style.display = 'block';
    }
}

function inicializarVistaCompetencia() {
    const container = document.getElementById('competencias-tarjetas-container');

    if (!container) {
        document.querySelector('.section-header').insertAdjacentHTML('afterend', '<div id="competencias-tarjetas-container"></div>');
    }

    if (container.innerHTML.trim() !== '') {
        return;
    }

    let html = '';
    for (const comp of competenciasData) {
        html += '<div class="competencia-card">';
        html += '<input type="checkbox" id="comp-' + comp.id + '" value="' + comp.id + '">';
        html += '<label for="comp-' + comp.id + '">';
        html += '<i class="fas fa-check-circle card-icono"></i>';
        html += '<span class="card-titulo">' + comp.nombre + '</span>';
        html += '<span class="card-descripcion">' + (comp.descripcion || '') + '</span>';
        html += '</label>';
        html += '</div>';
    }

    container.innerHTML = html;

    container.querySelectorAll('input[type="checkbox"]').forEach(cb => {
        cb.addEventListener('change', actualizarCompetenciasSeleccionadas);
    });

    document.getElementById('btn-limpiar-seleccion').addEventListener('click', limpiarSeleccion);

    renderizarCarrerasPorCompetencia();
}

function actualizarCompetenciasSeleccionadas() {
    competenciasSeleccionadas = [];
    document.querySelectorAll('#competencias-tarjetas-container input[type="checkbox"]:checked').forEach(cb => {
        const id = parseInt(cb.value);
        const comp = competenciasData.find(c => c.id === id);
        if (comp) competenciasSeleccionadas.push(comp.nombre);
    });

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

    const carrerasFiltradas = carrerasData.filter(carrera => {
        return carrera.nombre.toLowerCase().includes(competenciasSeleccionadas[0].toLowerCase());
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
    cargarCarrerasAgrupadas();
}

function buscarCarreras() {
    const texto = document.getElementById('buscar-carrera').value.toLowerCase().trim();
    const container = document.getElementById('resultados-carreras');

    if (!texto) {
        renderizarTodasCarreras();
        return;
    }

    const carrerasFiltradas = carrerasData.filter(carrera =>
        carrera.nombre.toLowerCase().includes(texto)
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

    if (carrerasData.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <i class="fas fa-search"></i>
                <h3>Ingresá un término de búsqueda</h3>
                <p>Escribí en el campo de arriba para buscar carreras</p>
            </div>
        `;
        return;
    }

    container.innerHTML = `
        <div style="grid-column: 1/-1; margin-bottom: 10px; color: var(--text-gray); font-size: 0.95rem;">
            <i class="fas fa-book-open"></i> Todas las carreras (${carrerasData.length})
        </div>
        ${carrerasData.map(carrera => crearCardCarrera(carrera)).join('')}
    `;
}

function formatDuracion(meses) {
    if (!meses) return '';
    const años = Math.floor(meses / 12);
    const resto = meses % 12;
    let r = '';
    if (años > 0) r += años + (años === 1 ? ' año' : ' años');
    if (resto > 0) r += (r ? ' ' : '') + resto + (resto === 1 ? ' mes' : ' meses');
    return r;
}

function crearCardCarrera(carrera) {
    const nivel = carrera.nivel_nombre || '';
    const duracion = carrera.duracion_meses ? formatDuracion(carrera.duracion_meses) : '';
    return `
        <div class="card">
            <div class="card-header">
                <div>
                    <h3 class="card-title">${carrera.nombre}</h3>
                    <span class="card-badge">${nivel}</span>
                </div>
                <div class="card-arrow">
                    <i class="fas fa-chevron-right"></i>
                </div>
            </div>
            <div class="card-info">
                <div class="card-info-item">
                    <i class="fas fa-clock"></i>
                    <span>Duración: ${duracion || 'Según plan'}</span>
                </div>
            </div>
        </div>
    `;
}

const CATEGORIAS = {
    tecnologia: {
        nombre: 'Tecnología',
        icono: 'fa-microchip',
        color: '#3b82f6'
    },
    administracion: {
        nombre: 'Administración y Gestión',
        icono: 'fa-chart-line',
        color: '#10b981'
    },
    salud: {
        nombre: 'Salud',
        icono: 'fa-heartbeat',
        color: '#ef4444'
    },
    educacion: {
        nombre: 'Educación y Cultura',
        icono: 'fa-graduation-cap',
        color: '#8b5cf6'
    },
    industria: {
        nombre: 'Industria y Producción',
        icono: 'fa-industry',
        color: '#f59e0b'
    },
    servicios: {
        nombre: 'Servicios',
        icono: 'fa-concierge-bell',
        color: '#06b6d4'
    }
};

async function cargarCarrerasAgrupadas() {
    try {
        const container = document.getElementById('resultados-carreras');
        if (!container) return;

        container.innerHTML = '<div class="carreras-empty"><i class="fas fa-spinner fa-spin"></i><h3>Cargando carreras...</h3></div>';

        let carreras = [];
        try {
            const response = await fetch('/api/carreras');
            if (response.ok) {
                carreras = await response.json();
            }
        } catch (e) {
            console.error('Error fetch carreras:', e);
        }

        if (!carreras || carreras.length === 0) {
            container.innerHTML = `
                <div class="carreras-empty">
                    <i class="fas fa-folder-open"></i>
                    <h3>No hay carreras disponibles</h3>
                    <p>No se encontraron carreras en la base de datos.</p>
                </div>
            `;
            return;
        }

        const nivelMap = {};
        try {
            const res = await fetch('/api/niveles');
            if (res.ok) {
                const niveles = await res.json();
                niveles.forEach(n => { nivelMap[n.id] = n.nombre; });
            }
        } catch (e) {}

        const carrerasPorCategoria = {};

        function getCategoria(nombre) {
            const n = nombre.toLowerCase();
            if (n.includes('técnico') || n.includes('computación') || n.includes('electrónica') ||
                n.includes('sistemas') || n.includes('analista') || n.includes('redes') || n.includes('programación')) {
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
            return 'tecnologia';
        }

        carreras.forEach(carrera => {
            const nivelNombre = nivelMap[carrera.nivel_id] || 'Otros';
            let categoriaAsignada = getCategoria(carrera.nombre);

            if (!carrerasPorCategoria[categoriaAsignada]) {
                carrerasPorCategoria[categoriaAsignada] = [];
            }

            carrerasPorCategoria[categoriaAsignada].push({
                ...carrera,
                nivel: nivelNombre
            });
        });

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

    let html = '';
    let totalCarreras = 0;

    const ordenCategorias = ['tecnologia', 'administracion', 'industria', 'salud', 'educacion', 'servicios'];

    for (const catKey of ordenCategorias) {
        const carreras = carrerasPorCategoria[catKey];
        if (!carreras || carreras.length === 0) continue;

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
    const duracion = carrera.duracion_meses ? formatDuracion(carrera.duracion_meses) : 'Según plan de estudios';
    const nivelKey = carrera.nivel ? carrera.nivel.toLowerCase().replace(/\s+/g, '') : 'formacion';

    return `
        <div class="tarjeta-carrera">
            <div class="carrera-card" onclick="verDetalleCarrera(${carrera.id})">
                <div class="carrera-card-header">
                    <span class="carrera-card-nivel ${nivelKey}">${carrera.nivel || 'General'}</span>
                    <h3 class="carrera-card-titulo">${carrera.nombre}</h3>
                    <p class="carrera-card-desc">${descripcion}</p>
                </div>
                <div class="carrera-card-info">
                    <div class="carrera-card-info-item">
                        <i class="fas fa-clock"></i>
                        <span>${duracion}</span>
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

    fetch(`/api/ofertas/${id}`)
        .then(res => res.json())
        .then(data => {
            const nivelNombre = data.nivel_nombre || 'General';
            const nivelKey = nivelNombre.toLowerCase().replace(/\s+/g, '');

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
                                <span>${data.duracion_meses ? formatDuracion(data.duracion_meses) : 'Según plan de estudios'}</span>
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

document.addEventListener('DOMContentLoaded', () => {
    const inputBusqueda = document.getElementById('buscar-carrera');

    if (inputBusqueda) {
        inputBusqueda.addEventListener('input', () => {
            if (window.carrerasData) {
                const container = document.getElementById('resultados-carreras');
                const carrerasPorCategoria = window.carrerasData;
                renderizarCarrerasPorCategoria(container, carrerasPorCategoria);
            }
        });
    }
});

window.carrerasData = null;

const originalRenderizar = renderizarCarrerasPorCategoria;
renderizarCarrerasPorCategoria = function(container, carrerasPorCategoria) {
    window.carrerasData = carrerasPorCategoria;
    originalRenderizar(container, carrerasPorCategoria);
};
