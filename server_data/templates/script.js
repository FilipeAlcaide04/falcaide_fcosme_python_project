
let chart;
const cores = {
  "PS": "#FF0000",
  "PSD": "#FF9900",
  "BE": "#9900FF",
  "CDU": "#CC0000",
  "CDS-PP": "#0000FF",
  "PAN": "#00FF00",
  "IL": "#00FFFF",
  "CHEGA": "#000000",
  "Livre": "#FFCC00"
};

window.onload = async function() {
  const res = await fetch('/api/distritos');
  const distritos = await res.json();
  
  const select = document.getElementById("distrito");
  distritos.forEach(d => {
    const opt = document.createElement("option");
    opt.value = d;
    opt.textContent = d;
    select.appendChild(opt);
  });
};

async function carregarFreguesias() {
  const distrito = document.getElementById("distrito").value;
  const res = await fetch(`/api/freguesias?distrito=${distrito}`);
  const freguesias = await res.json();

  const select = document.getElementById("freguesia");
  select.innerHTML = "<option value=''>Escolha uma freguesia</option>";

  freguesias.forEach(f => {
    const opt = document.createElement("option");
    opt.value = f;
    opt.textContent = f;
    select.appendChild(opt);
  });
}

function atualizarResultados() {
  if (document.getElementById("freguesia").value) {
    mostrarResultados();
  }
}

async function mostrarResultadosNacionais() {
  const ano = document.getElementById("ano").value;
  const res = await fetch(`/api/resultados?ano=${ano}`);
  const data = await res.json();
  
  // Mostrar container nacional e esconder local
  document.getElementById("nacionalContainer").style.display = "block";
  document.getElementById("localContainer").style.display = "none";
  
  // Atualizar informações nacionais
  document.getElementById("anoNacional").textContent = ano;
  
  // Vencedor nacional
  const vencedorNacional = document.getElementById("vencedorNacional");
  vencedorNacional.innerHTML = `
    <h4>Vencedor Nacional: <span style="color: ${cores[data.vencedor] || '#000'}">${data.vencedor}</span></h4>
    <div>Com ${data.percentagens[data.vencedor].toFixed(2)}% dos votos válidos</div>
  `;
  
  // Estatísticas
  document.getElementById("totalEleitores").textContent = data.estatisticas.total_eleitores.toLocaleString();
  document.getElementById("totalVotantes").textContent = data.estatisticas.total_votantes.toLocaleString();
  document.getElementById("totalAbstencao").textContent = `${data.estatisticas.abstencao.toLocaleString()} (${(data.estatisticas.abstencao/data.estatisticas.total_eleitores*100).toFixed(2)}%)`;
  document.getElementById("totalBrancos").textContent = `${data.estatisticas.brancos.toLocaleString()} (${(data.estatisticas.brancos/data.estatisticas.total_votantes*100).toFixed(2)}%)`;
  document.getElementById("totalValidos").textContent = `${data.estatisticas.votos_validos.toLocaleString()} (${(data.estatisticas.votos_validos/data.estatisticas.total_votantes*100).toFixed(2)}%)`;
  
  // Barras de progresso
  const progressBars = document.getElementById("progressBarsNacional");
  progressBars.innerHTML = "";
  
  // Ordenar por percentagem
  const partidosOrdenados = Object.entries(data.percentagens)
    .sort((a, b) => b[1] - a[1]);
  
  partidosOrdenados.forEach(([partido, percentagem]) => {
    const bar = document.createElement("div");
    bar.className = "progress";
    bar.innerHTML = `
      <div class="progress-bar" 
           role="progressbar" 
           style="width: ${percentagem}%; background-color: ${cores[partido] || '#999999'}"
           aria-valuenow="${percentagem}" 
           aria-valuemin="0" 
           aria-valuemax="100">
        <strong>${partido}</strong>: ${percentagem.toFixed(2)}%
      </div>
    `;
    progressBars.appendChild(bar);
  });
}

async function mostrarResultados() {
  const distrito = document.getElementById("distrito").value;
  const freguesia = document.getElementById("freguesia").value;
  const ano = document.getElementById("ano").value;

  const res = await fetch(`/api/resultados?distrito=${distrito}&freguesia=${freguesia}&ano=${ano}`);
  const data = await res.json();
  
  if (!data.votos) {
    alert("Dados não encontrados para esta freguesia");
    return;
  }

  // Mostrar container local e esconder nacional
  document.getElementById("localContainer").style.display = "block";
  document.getElementById("nacionalContainer").style.display = "none";
  
  // Vencedor local
  const vencedorLocal = document.getElementById("vencedorLocal");
  vencedorLocal.innerHTML = `
    <h4>Vencedor em ${data.info.freguesia}: <span style="color: ${cores[data.vencedor] || '#000'}">${data.vencedor}</span></h4>
    <div>Com ${data.percentagens[data.vencedor].toFixed(2)}% dos votos válidos</div>
  `;
  
  // Vencedor nacional
  const vencedorNacionalLocal = document.getElementById("vencedorNacionalLocal");
  vencedorNacionalLocal.innerHTML = `
    <span style="color: ${cores[data.resultados_nacionais.vencedor] || '#000'}">${data.resultados_nacionais.vencedor}</span>
    (${data.resultados_nacionais.percentagens[data.resultados_nacionais.vencedor].toFixed(2)}%)
  `;

  // Atualizar informações
  document.getElementById("freguesiaNome").textContent = data.info.freguesia;
  document.getElementById("infoDistrito").textContent = data.info.distrito;
  document.getElementById("infoMunicipio").textContent = data.info.municipio;
  document.getElementById("infoInscritos").textContent = data.info.inscritos.toLocaleString();
  document.getElementById("infoVotantes").textContent = `${data.info.votantes.toLocaleString()} (${(data.info.votantes/data.info.inscritos*100).toFixed(2)}%)`;
  document.getElementById("infoAbstencao").textContent = `${data.info.abstencao.toLocaleString()} (${(data.info.abstencao/data.info.inscritos*100).toFixed(2)}%)`;
  document.getElementById("infoBrancos").textContent = `${data.info.brancos.toLocaleString()} (${(data.info.brancos/data.info.votantes*100).toFixed(2)}%)`;

  // Criar gráfico
  const ctx = document.getElementById('resultadosChart').getContext('2d');
  if (chart) chart.destroy();

  // Ordenar partidos por número de votos (decrescente)
  const partidos = Object.keys(data.votos);
  const votos = Object.values(data.votos);
  
  const combined = partidos.map((partido, i) => ({partido, votos: votos[i]}));
  combined.sort((a, b) => b.votos - a.votos);
  
  const sortedPartidos = combined.map(item => item.partido);
  const sortedVotos = combined.map(item => item.votos);

  chart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: sortedPartidos,
      datasets: [{
        label: 'Nº de Votos',
        data: sortedVotos,
        backgroundColor: sortedPartidos.map(p => cores[p] || '#999999')
      }]
    },
    options: {
      responsive: true,
      plugins: {
        legend: { display: false },
        title: {
          display: true,
          text: `Resultados Eleitorais ${ano} - ${data.info.freguesia}`
        },
        tooltip: {
          callbacks: {
            label: function(context) {
              const total = data.info.votantes - data.info.brancos;
              const percent = (context.raw / total * 100).toFixed(2);
              return `${context.raw} votos (${percent}%)`;
            }
          }
        }
      },
      scales: {
        y: {
          beginAtZero: true,
          title: {
            display: true,
            text: 'Número de Votos'
          }
        }
      }
    }
  });

  // Barras de progresso locais
  const progressBarsLocal = document.getElementById("progressBarsLocal");
  progressBarsLocal.innerHTML = "";
  
  combined.forEach(({partido, votos}) => {
    const percent = data.percentagens[partido];
    const bar = document.createElement("div");
    bar.className = "progress";
    bar.innerHTML = `
      <div class="progress-bar" 
           role="progressbar" 
           style="width: ${percent}%; background-color: ${cores[partido] || '#999999'}"
           aria-valuenow="${percent}" 
           aria-valuemin="0" 
           aria-valuemax="100">
        <strong>${partido}</strong>: ${percent.toFixed(2)}%
      </div>
    `;
    progressBarsLocal.appendChild(bar);
  });

  // Barras de comparação com nacional
  const progressBarsComparacao = document.getElementById("progressBarsComparacao");
  progressBarsComparacao.innerHTML = "";
  
  combined.forEach(({partido}) => {
    const percentLocal = data.percentagens[partido];
    const percentNacional = data.resultados_nacionais.percentagens[partido] || 0;
    
    const bar = document.createElement("div");
    bar.className = "mb-3";
    bar.innerHTML = `
      <div><strong>${partido}</strong></div>
      <div class="d-flex">
        <div class="text-center" style="width: 50%; padding-right: 5px;">
          <small>Local (${percentLocal.toFixed(2)}%)</small>
          <div class="progress" style="height: 10px;">
            <div class="progress-bar" role="progressbar" 
                 style="width: ${percentLocal}%; background-color: ${cores[partido] || '#999999'}">
            </div>
          </div>
        </div>
        <div class="text-center" style="width: 50%; padding-left: 5px;">
          <small>Nacional (${percentNacional.toFixed(2)}%)</small>
          <div class="progress" style="height: 10px;">
            <div class="progress-bar" role="progressbar" 
                 style="width: ${percentNacional}%; background-color: ${cores[partido] || '#999999'}">
            </div>
          </div>
        </div>
      </div>
    `;
    progressBarsComparacao.appendChild(bar);
  });
}
