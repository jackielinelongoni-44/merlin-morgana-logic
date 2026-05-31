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
    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        const nome = document.getElementById("nome").value;
        const data = document.getElementById("data").value;
        const hora = inputHora.value;
        const cidade = document.getElementById("cidade").value;

        if (!nome || !data || !hora || !cidade) {
            alert("Por favor, preencha todos os dados para alinhar os astros!");
            return;
        }

        // 1. Ativa imediatamente a Tela de Carregamento Mística da Morgana
        appScreen.innerHTML = `
            <div class="carregamento-container">
                <h1 class="titulo-medieval" style="font-size: 24px;">Conjurando o Céu...</h1>
                <div class="orbe-mistica"></div>
                <p class="texto-carregamento">Consultando as efemérides de Merlin e Morgana para <strong>${nome}</strong>...</p>
                <p class="subtexto-carregamento">Calculando casas pelo sistema Regiomontanus...</p>
            </div>
        `;

        // 2. O MENSAGEIRO: Empacota os dados e envia para o motor em Python
        try {
            // Avisamos o JavaScript para enviar os dados para o endereço do nosso motor local
            const resposta = await fetch("http://127.0.0.1:8000/calcular-mapa", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    nome: nome,
                    data: data,
                    hora: hora,
                    cidade: cidade
                })
            });

            // Recebe o Mapa Astral calculado de volta do Python
            const resultadoAstrologico = await reply.json();
            
            // Exibe o resultado no console do navegador por enquanto (para testarmos)
            console.log("Resposta do Motor de cálculo:", resultadoAstrologico);
            
            // [Próximo Passo]: Aqui vamos desenhar a Tela 3 (O Dashboard com os Signos e Casas)

        } catch (erro) {
            console.log("O motor Python ainda não está rodando no computador:", erro);
        }
    });
});
