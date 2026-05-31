document.addEventListener("DOMContentLoaded", () => {

    const form = document.querySelector(".cadastro-form");
    const inputData = document.getElementById("data");
    const idadeTexto = document.getElementById("idade");
    const inputHora = document.getElementById("hora");
    const checkboxHora = document.getElementById("nao-sei-hora");
    const appScreen = document.querySelector(".app-screen");

    // Exibir idade automaticamente

    inputData.addEventListener("change", () => {

        if (!inputData.value) {
            idadeTexto.textContent = "";
            return;
        }

        const nascimento = new Date(inputData.value);
        const hoje = new Date();

        let idade = hoje.getFullYear() - nascimento.getFullYear();

        const diferencaMes = hoje.getMonth() - nascimento.getMonth();

        if (
            diferencaMes < 0 ||
            (
                diferencaMes === 0 &&
                hoje.getDate() < nascimento.getDate()
            )
        ) {
            idade--;
        }

        idadeTexto.textContent = `${idade} anos`;
    });

    // Não sei a hora de nascimento

    checkboxHora.addEventListener("change", (e) => {

        if (e.target.checked) {

            inputHora.value = "12:00";
            inputHora.disabled = true;

        } else {

            inputHora.value = "";
            inputHora.disabled = false;

        }

    });

    // Envio do formulário

    form.addEventListener("submit", async (e) => {

        e.preventDefault();

        const nome = document.getElementById("nome").value.trim();
        const data = document.getElementById("data").value;
        const hora = inputHora.value;
        const cidade = document.getElementById("cidade").value.trim();

        if (!nome || !data || !hora || !cidade) {

            alert(
                "Por favor, preencha todos os dados para alinhar os astros!"
            );

            return;
        }

        appScreen.innerHTML = `
            <div class="carregamento-container">
                <h1 class="titulo-medieval" style="font-size:24px;">
                    Conjurando o Céu...
                </h1>

                <div class="orbe-mistica"></div>

                <p class="texto-carregamento">
                    Consultando as efemérides de Merlin e Morgana para
                    <strong>${nome}</strong>...
                </p>

                <p class="subtexto-carregamento">
                    Calculando casas pelo sistema Regiomontanus...
                </p>
            </div>
        `;

        try {

            const resposta = await fetch(
                "http://127.0.0.1:8000/calcular-mapa",
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({
                        nome,
                        data,
                        hora,
                        cidade
                    })
                }
            );

            if (!resposta.ok) {
                throw new Error(
                    `Erro HTTP: ${resposta.status}`
                );
            }

            const resultadoAstrologico =
                await resposta.json();

            console.log(
                "Resposta do Motor de cálculo:",
                resultadoAstrologico
            );

            // Próxima etapa:
            // Renderizar o dashboard do mapa astral

        } catch (erro) {

            console.error(
                "Erro ao conectar ao motor Python:",
                erro
            );

            appScreen.innerHTML = `
                <div class="carregamento-container">
                    <h2>⚠️ Conexão interrompida</h2>

                    <p>
                        Não foi possível acessar o motor
                        astrológico.
                    </p>

                    <p>
                        Verifique se o servidor Python
                        está em execução.
                    </p>
                </div>
            `;
        }

    });

});
