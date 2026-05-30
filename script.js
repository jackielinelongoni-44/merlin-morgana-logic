document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector(".cadastro-form");
    const inputData = document.getElementById("data");
    const inputHora = document.getElementById("hora");
    const checkboxHora = document.getElementById("nao-sei-hora");
    const appScreen = document.querySelector(".app-screen");

    // --- MÁSCARA DA DATA (Garante as barras / automáticas) ---
    inputData.addEventListener("keyup", (e) => {
        if (e.key === "Backspace") return;

        let v = inputData.value.replace(/\D/g, ""); // Remove letras
        
        if (v.length > 2 && v.length <= 4) {
            inputData.value = v.substring(0, 2) + " / " + v.substring(2);
        } else if (v.length > 4) {
            inputData.value = v.substring(0, 2) + " / " + v.substring(2, 4) + " / " + v.substring(4, 8);
        }
    });

    // --- MÁSCARA DA HORA (Garante os dois pontos : automáticos) ---
    inputHora.addEventListener("keyup", (e) => {
        if (e.key === "Backspace") return;

        let v = inputHora.value.replace(/\D/g, ""); // Remove letras
        
        if (v.length > 2) {
            inputHora.value = v.substring(0, 2) + " : " + v.substring(2, 4);
        }
    });

    // Se marcar "Não sei minha hora", preenche com 12:00 e bloqueia o campo
    checkboxHora.addEventListener("change", (e) => {
        if (e.target.checked) {
            inputHora.value = "12 : 00";
            inputHora.disabled = true;
        } else {
            inputHora.value = "";
            inputHora.disabled = false;
        }
    });

    // --- AÇÃO DO BOTÃO: ENTRAR NO PORTAL (A parte do seu print!) ---
    form.addEventListener("submit", (e) => {
        e.preventDefault();

        const nome = document.getElementById("nome").value;
        const data = inputData.value;
        const hora = inputHora.value;
        const cidade = document.getElementById("cidade").value;

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
    });
});
