// Dados das consultas disponíveis
const queries = [
    {
        title: "Total de Desastres por País",
        description: "Conta quantos desastres existem para o país selecionado.",
        endpoint: "/queries/total-desastres-por-pais",
        params: "pais (string) - Nome do país"
    },
    {
        title: "Total de Desastres por País e Ano",
        description: "Conta desastres no país em determinado ano.",
        endpoint: "/queries/total-desastres-por-pais-ano",
        params: "pais (string) - Nome do país, ano (int) - Ano específico"
    },
    {
        title: "Top 5 Desastres Mais Mortais",
        description: "Retorna os 5 desastres com mais mortes no país.",
        endpoint: "/queries/top-5-desastres-mais-mortais",
        params: "pais (string) - Nome do país"
    },
    {
        title: "Total de Pessoas Afetadas",
        description: "Soma o total de pessoas afetadas no país.",
        endpoint: "/queries/total-pessoas-afetadas",
        params: "pais (string) - Nome do país"
    },
    {
        title: "Total de Danos Econômicos",
        description: "Soma o total de danos econômicos no país.",
        endpoint: "/queries/total-danos-economicos",
        params: "pais (string) - Nome do país"
    },
    {
        title: "Desastres por Tipo",
        description: "Retorna dicionário {tipo: quantidade} de desastres no país.",
        endpoint: "/queries/desastres-por-tipo",
        params: "pais (string) - Nome do país"
    },
    {
        title: "Desastres por Grupo",
        description: "Retorna dicionário {grupo: quantidade} de desastres no país.",
        endpoint: "/queries/desastres-por-grupo",
        params: "pais (string) - Nome do país"
    },
    {
        title: "Tendência Histórica",
        description: "Retorna dict {ano: total de desastres} para o país (ordem crescente ano).",
        endpoint: "/queries/tendencia-historica",
        params: "pais (string) - Nome do país"
    },
    {
        title: "Lista de Desastres Filtrada",
        description: "Retorna lista de documentos filtrados por país, grupo, tipo e ano (opcionais).",
        endpoint: "/queries/lista-desastres-filtrada",
        params: "pais (string) - Nome do país, grupo (string, opcional), tipo (string, opcional), ano (int, opcional)"
    },
    {
        title: "Exportar Dados JSON",
        description: "Retorna lista de docs para exportar em JSON (apenas do país).",
        endpoint: "/queries/exportar-dados-json",
        params: "pais (string) - Nome do país"
    }
];

// Função para abrir o popup
function openPopup(countryName) {
    const popup = document.getElementById('countryPopup');
    const popupTitle = document.getElementById('popupTitle');
    const queryList = document.getElementById('queryList');
    
    // Atualizar título do popup
    popupTitle.textContent = `Consultas Disponíveis para: ${countryName}`;
    
    // Limpar lista anterior
    queryList.innerHTML = '';
    
    // Adicionar cada consulta à lista
    queries.forEach(query => {
        const li = document.createElement('li');
        li.className = 'query-item';
        
        const endpointWithParams = query.endpoint + '?pais=' + encodeURIComponent(countryName);
        
        li.innerHTML = `
            <div class="query-title">${query.title}</div>
            <div class="query-description">${query.description}</div>
            <div class="query-endpoint">${endpointWithParams}</div>
            <div class="query-params"><strong>Parâmetros:</strong> ${query.params}</div>
        `;
        
        queryList.appendChild(li);
    });
    
    // Mostrar popup
    popup.style.display = 'block';
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