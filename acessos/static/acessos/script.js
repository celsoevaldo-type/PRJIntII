// busca na tabela enquanto a pessoa digita, sem recarregar a página
const busca = document.getElementById("busca");

if (busca) {
  const tabela = document.getElementById(busca.dataset.tabela);
  const linhas = tabela.querySelectorAll("tbody tr");
  const aviso = document.getElementById("sem-resultado");

  busca.addEventListener("input", function () {
    const termo = busca.value.toLowerCase();
    let visiveis = 0;

    linhas.forEach(function (linha) {
      const bate = linha.textContent.toLowerCase().includes(termo);
      linha.style.display = bate ? "" : "none";
      if (bate) visiveis++;
    });

    // se nada bater, mostra o aviso (que também é lido pelo leitor de tela)
    aviso.classList.toggle("d-none", visiveis > 0);
  });
}

// pede confirmação antes de desligar alguém ou retirar um acesso,
// porque são ações que não dá para desfazer com um clique
document.querySelectorAll("form[data-confirmar]").forEach(function (form) {
  form.addEventListener("submit", function (evento) {
    if (!confirm(form.dataset.confirmar)) {
      evento.preventDefault();
    }
  });
});

// o Django gera os campos sem a classe do Bootstrap, então colocamos aqui
document.querySelectorAll("form input:not([type=hidden]), form select").forEach(function (campo) {
  if (campo.classList.contains("form-control") || campo.classList.contains("form-select")) return;
  campo.classList.add(campo.tagName === "SELECT" ? "form-select" : "form-control");
});
