

// Espera o conteúdo da página carregar antes de executar o script
document.addEventListener('DOMContentLoaded', (event) => {

    // --- Lógica do Relógio e Data ---
    const date = new Date();
    let dia = date.getDate(); // Corrigido de getDay() para getDate()
    let mes = date.getMonth() + 1; // JS conta meses de 0 a 11
    let ano = date.getFullYear()
    
    // Formata para dois dígitos
    if (dia < 10) dia = '0' + dia;
    if (mes < 10) mes = '0' + mes;

    document.getElementById('date').innerHTML = `${dia} / ${mes} / ${ano}`;   

    function relogio(){
        const hora = new Date();
        let H = hora.getHours();
        let M = hora.getMinutes();

        // Formata para dois dígitos
        if (H < 10) H = '0' + H;
        if (M < 10) M = '0' + M;

        document.getElementById('relogio').innerHTML = `${H}:${M}`;
    }

    setInterval(relogio, 1000);
    relogio(); // Chama a função imediatamente

    
    // --- Lógica do Sistema de Integridade ---
    let n1 = 1; // Variável de controle para integridade
    
    function sistema() {
        let integri;
        if (n1 == 1){
            integri = 100;
        } else {
            integri = Math.floor(Math.random() * 100) + 1;
        }
        
        // Atualiza o valor no botão
        document.getElementById('integr_ysys').value = `Integridade do sistema:${integri}%`;
        
        // Atualiza também o valor no popup
        const popupValor = document.getElementById('integr_ysys01');
        if (popupValor) {
            popupValor.innerHTML = `${integri}%`;
        }
    }

    setInterval(sistema, 10000); // Verifica a cada 10 segundos
    sistema(); // Chama a função imediatamente

    
    // --- Lógica do Botão "Porta" ---
    const button = document.getElementById('naveButton');
    let aberto = false;
    const contagemElement = document.getElementById('contagem');

    button.addEventListener('click', () => {
      // Impede novo clique se já estiver abrindo
      if (aberto) return; 

      aberto = true;
      button.classList.toggle('open', aberto);
      
      let tempo = 3; // Contagem regressiva de 3
      contagemElement.innerHTML= `Iniciando em: ${tempo}`;
      
      const contagem = setInterval(() => {
        tempo--;
        if (tempo > 0) {
            contagemElement.innerHTML= `Iniciando em: ${tempo}`;
        } else if (tempo === 0) {
            contagemElement.innerHTML= `Conectando...`;
        } else {
            clearInterval(contagem);
            // Redireciona para a página de chat (usando o link do Flask)
            window.location.href = '/chat'; 
        }
      }, 1000);
    });

});

// --- Função para mostrar/esconder o popup ---
// (Fora do DOMContentLoaded para ser acessível pelo 'onclick' no HTML)
function show_sys() {
    const meuElemento = document.getElementById('sistema-popup');
    meuElemento.classList.toggle('sistema');
}