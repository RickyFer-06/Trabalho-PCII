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

    document.getElementById("avisoRemover").style.display = "none";

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

function mostrarAvisoRemover(select) {
    const aviso = document.getElementById("avisoRemover");
    const totalEl = document.getElementById("totalRemover");
    const selected = select.options[select.selectedIndex];
    if (selected && selected.dataset.total) {
        totalEl.textContent = selected.dataset.total;
        aviso.style.display = "block";
    } else {
        aviso.style.display = "none";
    }
}

window.onclick = function (event) {
    let overlay = document.getElementById("modalOverlay");
    if (event.target == overlay) closeModal();
};

function openBrokerCloseModal() {
    const drawer = document.getElementById("drawer");
    if (drawer.classList.contains("active")) {
        drawer.classList.remove("active");
    }
    document.getElementById("brokerCloseModal").style.display = "flex";
}

function closeBrokerCloseModal() {
    document.getElementById("brokerCloseModal").style.display = "none";
}

window.onclick = function (event) {
    let overlay = document.getElementById("modalOverlay");
    let brokerCloseOverlay = document.getElementById("brokerCloseModal");
    
    if (event.target === overlay) {
        closeModal();
    } else if (event.target === brokerCloseOverlay) {
        closeBrokerCloseModal();
    }
};

function openBrokerCloseModal() {
    toggleDrawer(); // Fecha o menu lateral
    document.getElementById("brokerCloseModal").style.display = "flex"; 
}

function closeBrokerCloseModal() {
    document.getElementById("brokerCloseModal").style.display = "none"; 
}
function openBrokerCloseModal() {
    toggleDrawer(); 
    document.getElementById("brokerCloseModal").style.display = "flex";
}

function closeBrokerCloseModal() {
    document.getElementById("brokerCloseModal").style.display = "none"; 
}