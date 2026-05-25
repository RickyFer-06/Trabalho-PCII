function toggleCorpDrawer() {
    document.getElementById("corpDrawer").classList.toggle("active");
}

function showCorpSection(id) {
    const sections = document.querySelectorAll(".drawer-section");
    const buttons = document.querySelectorAll(".drawer-toggle");
    sections.forEach(section => section.classList.remove("active"));
    buttons.forEach(button => button.classList.remove("active"));
    const activeSection = document.getElementById(id);
    if (activeSection) {
        activeSection.classList.add("active");
    }
    buttons.forEach(button => {
        if (button.dataset.target === id) {
            button.classList.add("active");
        }
    });
}
