function toggleDrawer() {
    document.getElementById("drawer").classList.toggle("active");
}

function openModal(tipo) {
    toggleDrawer(); // Esconde a aba
    document.getElementById("modalOverlay").style.display = "flex"; // Mostra o modal
    document.getElementById("tipoOperacao").value = tipo;

    // Alterar o visual consoante a escolha (Depositar vs Levantar)
    if (tipo === "investir") {
        document.getElementById("modalTitle").innerText =
            "Adicionar Fundo";
        document.getElementById("btnExecutar").style.background = "#27ae60"; // Verde
        document.getElementById("btnExecutar").innerText =
            "Confirmar Depósito";
    } else {
        document.getElementById("modalTitle").innerText = "Resgatar Fundo";
        document.getElementById("btnExecutar").style.background = "#e74c3c"; // Vermelho
        document.getElementById("btnExecutar").innerText =
            "Solicitar Levantamento";
    }
}

function closeModal() {
    document.getElementById("modalOverlay").style.display = "none";
}

// Fechar ao clicar fora da caixa
window.onclick = function (event) {
    let overlay = document.getElementById("modalOverlay");
    if (event.target == overlay) {
        closeModal();
    }
};