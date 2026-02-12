const formulario = document.getElementById("formCadastroLivro");

formulario.addEventListener("submit", async function(evento) {

    evento.preventDefault(); // impede recarregar página

    // Pegando dados do formulário
    const dadosFormulario = new FormData(formulario);

    const livro = {
        titulo: dadosFormulario.get("titulo"),
        autor: dadosFormulario.get("autor")
    };

    try {

        const resposta = await fetch("http://localhost:5000/livros", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(livro)
        });

        if (resposta.ok) {
            alert("Livro cadastrado com sucesso!");
            formulario.reset();
        } else {
            alert("Erro ao cadastrar livro.");
        }

    } catch (erro) {
        console.error("Erro:", erro);
        alert("Erro ao conectar com a API.");
    }

});
