
function toggleDrawer() {
    document.getElementById("drawer").classList.toggle("active");
}

function openModal(tipo) {
    const drawer = document.getElementById("drawer");
    if (drawer.classList.contains("active")) {
        drawer.classList.remove("active");
    }
    
    document.getElementById("modalOverlay").style.display = "flex"; // Mostra o modal
    document.getElementById("tipoOperacao").value = tipo;

    const brokerSelect = document.querySelector('select[name="broker_id"]');
    brokerSelect.innerHTML = '<option value="" disabled selected>-- Escolha um Broker --</option>';

    if (tipo === "investir") {
        document.getElementById("modalTitle").innerText = "Adicionar Fundos";
        document.getElementById("btnExecutar").style.background = "#27ae60"; // Verde
        document.getElementById("btnExecutar").innerText = "Confirmar Depósito";
        
        brokersAdicionar.forEach(b => {
            const opt = document.createElement('option');
            opt.value = b.id;
            opt.textContent = b.name;
            brokerSelect.appendChild(opt);
        });

    } else {
        document.getElementById("modalTitle").innerText = "Resgatar Fundos";
        document.getElementById("btnExecutar").style.background = "#e74c3c"; // Vermelho
        document.getElementById("btnExecutar").innerText = "Solicitar Levantamento";
        
        brokersLevantar.forEach(b => {
            const opt = document.createElement('option');
            opt.value = b.id;
            const saldoFormatado = b.saldo.toLocaleString('pt-PT', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
            opt.textContent = `${b.name} (Disponível: ${saldoFormatado} €)`;
            brokerSelect.appendChild(opt);
        });
    }
}

function closeModal() {
    document.getElementById("modalOverlay").style.display = "none";
    document.getElementById("insufficientFundsModal").style.display = "none";
    
    document.querySelector('#modalOverlay form').reset();
}

window.onclick = function (event) {
    let overlay = document.getElementById("modalOverlay");
    let fundsOverlay = document.getElementById("insufficientFundsModal");
    
    if (event.target === overlay) {
        closeModal();
    } else if (event.target === fundsOverlay) {
        fundsOverlay.style.display = "none";
    }
};

document.querySelector('#modalOverlay form').addEventListener('submit', function(e) {
    const tipo = document.getElementById('tipoOperacao').value;
    
    if (tipo === 'levantar') {
        const brokerSelect = document.querySelector('select[name="broker_id"]');
        const brokerId = parseInt(brokerSelect.value);
        const amountInput = document.querySelector('input[name="amount"]');
        const amountRequested = parseFloat(amountInput.value);
        
        const targetBroker = brokersLevantar.find(b => b.id === brokerId);
        
        if (targetBroker && amountRequested > targetBroker.saldo) {
            e.preventDefault(); 
            
            const reqStr = amountRequested.toLocaleString('pt-PT', { minimumFractionDigits: 2 });
            const dispStr = targetBroker.saldo.toLocaleString('pt-PT', { minimumFractionDigits: 2 });
            
            document.getElementById('insufficientFundsMsg').innerHTML = 
                `Impossível levantar <strong>${reqStr} €</strong>.<br>` +
                `Apenas possui <strong>${dispStr} €</strong> disponível para levantar neste corretor.`;
            
            document.getElementById('btnProceedMax').onclick = function() {
                
                amountInput.value = targetBroker.saldo.toFixed(2);
                document.getElementById('insufficientFundsModal').style.display = 'none';
                
                e.target.submit(); 
            };
            
            document.getElementById('btnCancelPopup').onclick = function() {
                document.getElementById('insufficientFundsModal').style.display = 'none';
            };
            
            document.getElementById('insufficientFundsModal').style.display = 'flex';
        }
    }
});

// Funções para o Modal de Encerrar Conta
function openCloseAccountModal() {
    const drawer = document.getElementById("drawer");
    if (drawer.classList.contains("active")) {
        drawer.classList.remove("active");
    }
    document.getElementById("closeAccountModal").style.display = "flex";
}

function closeCloseAccountModal() {
    document.getElementById("closeAccountModal").style.display = "none";
    document.getElementById("closeAccountForm").reset();
    document.getElementById("ibanError").style.display = "none";
}

// Atualiza a função window.onclick existente para suportar o fecho deste novo modal ao clicar fora dele
window.onclick = function (event) {
    let overlay = document.getElementById("modalOverlay");
    let fundsOverlay = document.getElementById("insufficientFundsModal");
    let closeAccOverlay = document.getElementById("closeAccountModal");
    
    if (event.target === overlay) {
        closeModal();
    } else if (event.target === fundsOverlay) {
        fundsOverlay.style.display = "none";
    } else if (event.target === closeAccOverlay) {
        closeCloseAccountModal();
    }
};

// Validação Interativa do IBAN ao Submeter
document.getElementById("closeAccountForm").addEventListener("submit", function(e) {
    const ibanInput = document.getElementById("ibanInput").value;
    
    // Removemos espaços vazios para permitir que o utilizador escreva formatado ou tudo junto
    const cleanIban = ibanInput.replace(/\s+/g, '').toUpperCase();
    
    // Expressão Regular: Exige "PT50" seguido de exatamente 21 dígitos numéricos
    const ibanRegex = /^PT50\d{21}$/;
    
    if (!ibanRegex.test(cleanIban)) {
        e.preventDefault(); // Impede o formulário de seguir para o Python
        document.getElementById("ibanError").style.display = "block"; // Mostra o erro
    } else {
        document.getElementById("ibanError").style.display = "none";
        // Último alerta nativo do browser de segurança
        if (!confirm("Tem a certeza absoluta que deseja liquidar os fundos e apagar a sua conta?")) {
            e.preventDefault(); // Cancela se clicar em "Não" no popup nativo
        }
    }
});