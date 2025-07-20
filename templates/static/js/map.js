// Dados das consultas disponíveis
const queries = [
    {
        id: "total-desastres",
        title: "Total de Desastres",
        description: "Número total de desastres naturais",
        endpoint: "/queries/total-desastres-por-pais",
        icon: "📊"
    },
    {
        id: "pessoas-afetadas",
        title: "Pessoas Afetadas",
        description: "Total de pessoas afetadas pelos desastres",
        endpoint: "/queries/total-pessoas-afetadas",
        icon: "👥"
    },
    {
        id: "danos-economicos",
        title: "Danos Econômicos",
        description: "Valor total dos danos econômicos",
        endpoint: "/queries/total-danos-economicos",
        icon: "💰"
    },
    {
        id: "desastres-por-tipo",
        title: "Desastres por Tipo",
        description: "Distribuição por tipo de desastre",
        endpoint: "/queries/desastres-por-tipo",
        icon: "🌪️"
    },
    {
        id: "desastres-por-grupo",
        title: "Desastres por Grupo",
        description: "Distribuição por grupo de desastre",
        endpoint: "/queries/desastres-por-grupo",
        icon: "📈"
    },
    {
        id: "tendencia-historica",
        title: "Tendência Histórica",
        description: "Evolução dos desastres ao longo do tempo",
        endpoint: "/queries/tendencia-historica",
        icon: "📅"
    },
    {
        id: "top-mortais",
        title: "Top 5 Mais Mortais",
        description: "Os 5 desastres com mais vítimas fatais",
        endpoint: "/queries/top-5-desastres-mais-mortais",
        icon: "💀"
    }
];

// Função para abrir o popup
async function openPopup(countryName) {
    const popup = document.getElementById('countryPopup');
    const popupTitle = document.getElementById('popupTitle');
    const queryList = document.getElementById('queryList');
    
    // Atualizar título do popup
    popupTitle.textContent = `${countryName}`;
    
    // Limpar lista anterior
    queryList.innerHTML = '';
    
    // Mostrar loading
    queryList.innerHTML = '<div class="loading">Carregando dados do país...</div>';
    
    // Mostrar popup
    popup.style.display = 'block';
    
    try {
        // Buscar dados principais do país
        const totalDesastresResponse = await fetch(`/queries/total-desastres-por-pais?pais=${encodeURIComponent(countryName)}`);
        const totalDesastres = await totalDesastresResponse.json();
        
        const pessoasAfetadasResponse = await fetch(`/queries/total-pessoas-afetadas?pais=${encodeURIComponent(countryName)}`);
        const pessoasAfetadas = await pessoasAfetadasResponse.json();
        
        const danosEconomicosResponse = await fetch(`/queries/total-danos-economicos?pais=${encodeURIComponent(countryName)}`);
        const danosEconomicos = await danosEconomicosResponse.json();
        
        // Limpar loading e mostrar dados principais
        queryList.innerHTML = `
            <div class="country-stats">
                <div class="stat-card">
                    <div class="stat-icon">📊</div>
                    <div class="stat-value">${totalDesastres.total || 0}</div>
                    <div class="stat-label">Total de Desastres</div>
                </div>
                <div class="stat-card">
                    <div class="stat-icon">👥</div>
                    <div class="stat-value">${formatNumber(pessoasAfetadas.total_afetados || 0)}</div>
                    <div class="stat-label">Pessoas Afetadas</div>
                </div>
                <div class="stat-card">
                    <div class="stat-icon">💰</div>
                    <div class="stat-value">${formatCurrency(danosEconomicos.total_danos || 0)}</div>
                    <div class="stat-label">Danos Econômicos</div>
                </div>
            </div>
            <div class="queries-section">
                <h3>📋 Consultas Disponíveis</h3>
                <div class="queries-grid">
                    ${queries.map(query => `
                        <div class="query-card" onclick="executeQuery('${query.id}', '${countryName}')">
                            <div class="query-icon">${query.icon}</div>
                            <div class="query-title">${query.title}</div>
                            <div class="query-description">${query.description}</div>
                        </div>
                    `).join('')}
                </div>
            </div>
        `;
        
    } catch (error) {
        queryList.innerHTML = '<div class="error">Erro ao carregar dados do país. Tente novamente.</div>';
        console.error('Erro ao carregar dados:', error);
    }
}

// Função para formatar números grandes
function formatNumber(num) {
    if (num >= 1000000) {
        return (num / 1000000).toFixed(1) + 'M';
    } else if (num >= 1000) {
        return (num / 1000).toFixed(1) + 'K';
    }
    return num.toString();
}

// Função para formatar moeda
function formatCurrency(amount) {
    if (amount >= 1000000000) {
        return '$' + (amount / 1000000000).toFixed(1) + 'B';
    } else if (amount >= 1000000) {
        return '$' + (amount / 1000000).toFixed(1) + 'M';
    } else if (amount >= 1000) {
        return '$' + (amount / 1000).toFixed(1) + 'K';
    }
    return '$' + amount.toString();
}

// Função para executar consultas
async function executeQuery(queryId, countryName) {
    const query = queries.find(q => q.id === queryId);
    if (!query) return;
    
    try {
        const response = await fetch(`${query.endpoint}?pais=${encodeURIComponent(countryName)}`);
        const data = await response.json();
        
        // Mostrar resultado em um modal
        showQueryResult(query.title, data);
        
    } catch (error) {
        console.error('Erro ao executar consulta:', error);
        alert('Erro ao executar consulta. Tente novamente.');
    }
}

// Função para mostrar resultado da consulta
function showQueryResult(title, data) {
    const modal = document.createElement('div');
    modal.className = 'result-modal';
    
    let content = '';
    
    // Formatar dados baseado no tipo de consulta
    if (title === 'Total de Desastres') {
        content = `<div class="result-value">${data.total}</div>`;
    } else if (title === 'Pessoas Afetadas') {
        content = `<div class="result-value">${formatNumber(data.total_afetados)}</div>`;
    } else if (title === 'Danos Econômicos') {
        content = `<div class="result-value">${formatCurrency(data.total_danos)}</div>`;
    } else if (title === 'Desastres por Tipo' || title === 'Desastres por Grupo') {
        content = '<div class="result-chart">';
        for (const [key, value] of Object.entries(data)) {
            content += `<div class="chart-item"><span class="chart-label">${key}</span><span class="chart-value">${value}</span></div>`;
        }
        content += '</div>';
    } else if (title === 'Tendência Histórica') {
        content = '<div class="result-chart">';
        for (const [year, count] of Object.entries(data)) {
            content += `<div class="chart-item"><span class="chart-label">${year}</span><span class="chart-value">${count}</span></div>`;
        }
        content += '</div>';
    } else if (title === 'Top 5 Mais Mortais') {
        content = '<div class="result-list">';
        data.top_5.forEach((item, index) => {
            content += `<div class="list-item"><span class="list-rank">${index + 1}</span><span class="list-value">${item[1]} mortes</span></div>`;
        });
        content += '</div>';
    }
    
    modal.innerHTML = `
        <div class="result-content">
            <div class="result-header">
                <h2>${title}</h2>
                <span class="close" onclick="this.parentElement.parentElement.parentElement.remove()">&times;</span>
            </div>
            <div class="result-body">
                ${content}
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
}

// Função para fechar o popup
function closePopup() {
    const popup = document.getElementById('countryPopup');
    popup.style.display = 'none';
}

// Fechar popup ao clicar fora dele
window.onclick = function(event) {
    const popup = document.getElementById('countryPopup');
    if (event.target === popup) {
        closePopup();
    }
}

// Variável para controlar se o mapa está sendo arrastado/zoomado
// Esta solução previne que o popup abra durante interações de navegação do mapa
let mapIsBeingDragged = false;

// Aguardar o carregamento do Plotly e adicionar eventos
document.addEventListener('DOMContentLoaded', function() {
    // Aguardar um pouco para o Plotly carregar completamente
    setTimeout(function() {
        const plotDiv = document.querySelector('#plotly-div');
        if (plotDiv && plotDiv._fullData) {
            
            // Detectar quando o mapa é arrastado ou zoomado (relayout)
            plotDiv.on('plotly_relayout', function(eventData) {
                // Verificar se foi um arraste (pan) ou zoom
                if (eventData && (
                    'geo.center.lon' in eventData || 
                    'geo.center.lat' in eventData ||
                    'geo.projection.scale' in eventData ||
                    'geo.projection.rotation.lon' in eventData ||
                    'geo.projection.rotation.lat' in eventData
                )) {
                    mapIsBeingDragged = true;
                    // Reset após um tempo para permitir cliques normais
                    setTimeout(() => {
                        mapIsBeingDragged = false;
                    }, 250);
                }
            });
            
            // Adicionar evento de clique ao mapa
            plotDiv.on('plotly_click', function(data) {
                // Só abrir popup se o mapa não estiver sendo arrastado
                if (!mapIsBeingDragged && data.points && data.points.length > 0) {
                    const point = data.points[0];
                    const countryName = point.location;
                    if (countryName) {
                        openPopup(countryName);
                    }
                }
            });
        }
    }, 1000);
}); 