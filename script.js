document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector(".cadastro-form");
    const botao = document.querySelector(".botao-lavanda");
    const appScreen = document.querySelector(".app-screen");
    const inputData = document.getElementById("data");
    const inputHora = document.getElementById("hora");
    const checkboxHora = document.getElementById("nao-sei-hora");

    // --- MÁSCARA INTELIGENTE PARA A DATA (Teclado Numérico) ---
    inputData.addEventListener("input", (e) => {
        let v = e.target.value.replace(/\D/g, ""); // Remove tudo que não for número
        if (v.length >= 2) v = v.substring(0, 2) + " / " + v.substring(2);
        if (v.length >= 7) v = v.substring(0, 7) + " / " + v.substring(7, 11);
        e.target.value = v;
    });

    // --- MÁSCARA INTELIGENTE PARA A HORA ---
    inputHora.addEventListener("input", (e) => {
        let v = e.target.value.replace(/\D/g, "");
        if (v.length >= 2) v = v.substring(0, 2) + " : " + v.substring(2, 4);
        e.target.value = v;
    });

    // Se marcar "Não sei minha hora", preenche com 12:00 e desabilita o campo
    checkboxHora.addEventListener("change", (e) => {
        if (e.target.checked) {
            inputHora.value = "12 : 00";
            inputHora.disabled = true;
        } else {
            inputHora.value = "";
            inputHora.disabled = false;
        }
    });

    // --- AÇÃO DO BOTÃO: ENTRAR NO PORTAL (TELA 2) ---
    form.addEventListener("submit", (e) => {
        e.preventDefault(); // Impede a página de atualizar

        // Captura o que o usuário digitou
        const nome = document.getElementById("nome").value;
        const data = inputData.value;
        const hora = inputHora.value;
        const cidade = document.getElementById("cidade").value;

        // Validação simples: se esquecer de preencher, avisa
        if (!nome || !data || !hora || !cidade) {
            alert("Por favor, preencha todos os dados para alinhar os astros!");
            return;
        }

        // Transforma a tela na Animação de Carregamento Mística
        appScreen.innerHTML = `
            <div class="carregamento-container">
                <h1 class="titulo-medieval" style="font-size: 24px;">Conjurando o Céu...</h1>
                <div class="orbe-mistica"></div>
                <p class="texto-carregamento">Consultando as efemérides de Merlin e Morgana para <strong>${nome}</strong>...</p>
                <p class="subtexto-carregamento">Calculando casas pelo sistema Regiomontanus...</p>
            </div>
        `;

        // [Próximo Passo]: Aqui o JavaScript vai enviar esses dados para o motor.py
        console.log("Dados capturados prontos para o motor:", { nome, data, hora, city: cidade });
    });
});
