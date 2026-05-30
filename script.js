document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector(".cadastro-form");
    const inputHora = document.getElementById("hora");
    const checkboxHora = document.getElementById("nao-sei-hora");
    const appScreen = document.querySelector(".app-screen");

    // Se marcar "Não sei minha hora", preenche e bloqueia
    checkboxHora.addEventListener("change", (e) => {
        if (e.target.checked) {
            inputHora.value = "12:00";
            inputHora.disabled = true;
        } else {
            inputHora.value = "";
            inputHora.disabled = false;
        }
    });

    // --- AÇÃO DO BOTÃO: ENTRAR NO PORTAL ---
    form.addEventListener("submit", (e) => {
        e.preventDefault();

        const nome = document.getElementById("nome").value;
        const data = document.getElementById("data").value;
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
