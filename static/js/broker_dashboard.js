function toggleDrawer() {
    document.getElementById("drawer").classList.toggle("active");
}

function openModal(tipo) {
    toggleDrawer();
    document.getElementById("modalOverlay").style.display = "flex";
    document.getElementById("actionType").value = tipo;

    let wAdd = document.getElementById("wrapperAdicionar");
    let sAdd = document.getElementById("selectAdicionar");
    let wRem = document.getElementById("wrapperRemover");
    let sRem = document.getElementById("selectRemover");

    if (tipo === "adicionar") {
        document.getElementById("modalTitle").innerText = "👥 Associar Novo Cliente";
        document.getElementById("btnExecutar").style.background = "#27ae60";
        document.getElementById("btnExecutar").innerText = "Adicionar à Carteira";

        wAdd.style.display = "block";
        sAdd.name = "client_id";
        sAdd.required = true;

        wRem.style.display = "none";
        sRem.removeAttribute("name");
        sRem.required = false;
    } else {
        document.getElementById("modalTitle").innerText = "❌ Remover Cliente";
        document.getElementById("btnExecutar").style.background = "#e74c3c";
        document.getElementById("btnExecutar").innerText = "Remover da Carteira";

        wRem.style.display = "block";
        sRem.name = "client_id";
        sRem.required = true;

        wAdd.style.display = "none";
        sAdd.removeAttribute("name");
        sAdd.required = false;
    }
}

function closeModal() {
    document.getElementById("modalOverlay").style.display = "none";
}

window.onclick = function (event) {
    let overlay = document.getElementById("modalOverlay");
    if (event.target == overlay) closeModal();
};
