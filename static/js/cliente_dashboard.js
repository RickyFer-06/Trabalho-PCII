
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



function fmt(val) {
    return val.toLocaleString('pt-PT', { minimumFractionDigits: 2, maximumFractionDigits: 2 }) + ' €';
}

document.querySelector('#modalOverlay form').addEventListener('submit', function(e) {
    const tipo = document.getElementById('tipoOperacao').value;
    if (tipo !== 'levantar') return;

    e.preventDefault();

    const brokerSelect = document.querySelector('select[name="broker_id"]');
    const brokerId = parseInt(brokerSelect.value);
    const amountInput = document.querySelector('input[name="amount"]');
    const amountRequested = parseFloat(amountInput.value);
    const form = e.target;

    const targetBroker = brokersLevantar.find(b => b.id === brokerId);
    if (!targetBroker) return;

    if (amountRequested > targetBroker.saldo) {
        document.getElementById('amountRequested').textContent = fmt(amountRequested);
        document.getElementById('amountAvailable').textContent = fmt(targetBroker.saldo);
        document.getElementById('maxAmountLabel').textContent = fmt(targetBroker.saldo);

        document.getElementById('btnProceedMax').onclick = function () {
            amountInput.value = targetBroker.saldo.toFixed(2);
            document.getElementById('insufficientFundsModal').style.display = 'none';
            showConfirmModal(targetBroker, targetBroker.saldo, form);
        };
        document.getElementById('btnCancelPopup').onclick = function () {
            document.getElementById('insufficientFundsModal').style.display = 'none';
        };

        document.getElementById('insufficientFundsModal').style.display = 'flex';
    } else {
        showConfirmModal(targetBroker, amountRequested, form);
    }
});

function showConfirmModal(broker, amount, form) {
    const ficaCom = broker.saldo - amount;
    document.getElementById('summaryDisponivel').textContent = fmt(broker.saldo);
    document.getElementById('summaryLevantar').textContent = fmt(amount);
    document.getElementById('summaryFinal').textContent = fmt(ficaCom);
    document.getElementById('confirmAmountLabel').textContent = fmt(amount);

    document.getElementById('btnConfirmWithdraw').onclick = function () {
        document.getElementById('confirmWithdrawModal').style.display = 'none';
        form.submit();
    };
    document.getElementById('btnCancelConfirm').onclick = function () {
        document.getElementById('confirmWithdrawModal').style.display = 'none';
    };

    document.getElementById('confirmWithdrawModal').style.display = 'flex';
}

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

window.onclick = function (event) {
    const overlays = {
        'modalOverlay': closeModal,
        'insufficientFundsModal': closeModal,
        'confirmWithdrawModal': closeModal,
        'closeAccountModal': closeCloseAccountModal
    };
    for (const [id, fn] of Object.entries(overlays)) {
        if (event.target === document.getElementById(id)) { fn(); break; }
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