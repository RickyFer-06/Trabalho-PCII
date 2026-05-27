function toggleCorpDrawer() {
    document.getElementById("corpDrawer").classList.toggle("active");
}

function openCorpModal(type) {
    const drawer = document.getElementById("corpDrawer");
    if (drawer.classList.contains("active")) {
        drawer.classList.remove("active");
    }

    const addModal = document.getElementById("corpAddModal");
    const removeModal = document.getElementById("corpRemoveModal");
    addModal.style.display = "none";
    removeModal.style.display = "none";

    if (type === "add") {
        addModal.style.display = "flex";
    } else if (type === "remove") {
        removeModal.style.display = "flex";
    }
}
function openCorpCloseModal() {
    toggleCorpDrawer(); // Fecha o menu lateral
    document.getElementById("corpCloseModal").style.display = "flex";
}

function closeCorpCloseModal() {
    document.getElementById("corpCloseModal").style.display = "none";
}

function closeCorpModal() {
    document.getElementById("corpAddModal").style.display = "none";
    document.getElementById("corpRemoveModal").style.display = "none";
}

window.onclick = function (event) {
    const addModal = document.getElementById("corpAddModal");
    const removeModal = document.getElementById("corpRemoveModal");
    const closeCorpModalOverlay = document.getElementById("corpCloseModal");

    if (event.target === addModal || event.target === removeModal) {
        closeCorpModal();
    } else if (event.target === closeCorpModalOverlay) {
        closeCorpCloseModal();
    }
};
