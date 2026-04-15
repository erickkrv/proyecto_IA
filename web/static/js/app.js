const btnClasificar   = document.getElementById("btn-clasificar");
const btnLimpiar      = document.getElementById("btn-limpiar");
const ticketIdEl      = document.getElementById("ticket-id");
const subjectEl       = document.getElementById("subject");
const descripcionEl   = document.getElementById("descripcion");
const charCountEl     = document.getElementById("char-count");
const emptyState      = document.getElementById("empty-state");
const resultContent   = document.getElementById("resultado");
const resultTicketRef = document.getElementById("resultado-ticket-id");
const categoriaEl     = document.getElementById("categoria");
const resultConf      = document.getElementById("result-confidence");
const probChartEl     = document.getElementById("prob-chart");
const errorBlock      = document.getElementById("error");
const errorMsgEl      = document.getElementById("error-msg");

// ── Ticket ID ───────────────────────────────────────────
function generarTicketId() {
    return "TKT-" + Math.floor(10000 + Math.random() * 90000);
}

ticketIdEl.textContent = generarTicketId();

// ── Contador de caracteres ──────────────────────────────
descripcionEl.addEventListener("input", () => {
    const len = descripcionEl.value.length;
    charCountEl.textContent = `${len} / 2000`;
    charCountEl.classList.toggle("near-limit", len > 1700);
});

// ── Loading state ───────────────────────────────────────
function setLoading(on) {
    btnClasificar.disabled = on;
    document.getElementById("btn-label").textContent = on ? "Clasificando..." : "Clasificar Ticket";
    const spinner = btnClasificar.querySelector(".spinner");
    if (on && !spinner) {
        const s = document.createElement("span");
        s.className = "spinner";
        btnClasificar.prepend(s);
    } else if (!on && spinner) {
        spinner.remove();
    }
}

// ── Probability chart ───────────────────────────────────
function buildChart(probabilidades, ganadora) {
    const sorted = Object.entries(probabilidades).sort((a, b) => b[1] - a[1]);

    probChartEl.innerHTML = sorted.map(([clase, pct], i) => {
        const isWinner = clase === ganadora;
        return `
        <div class="prob-row ${isWinner ? "prob-row--winner" : ""}"
             style="--delay:${i * 45}ms; --pct:${pct}%">
            <span class="prob-name">${clase}</span>
            <div class="prob-track"><div class="prob-fill"></div></div>
            <span class="prob-pct">${pct.toFixed(1)}%</span>
        </div>`;
    }).join("");
}

// ── Mostrar resultado ───────────────────────────────────
function mostrarResultado(categoria, probabilidades) {
    const topPct = probabilidades[categoria];

    categoriaEl.textContent = categoria;
    resultTicketRef.textContent = ticketIdEl.textContent;
    resultConf.innerHTML = `
        <span class="confidence-value">${topPct.toFixed(1)}%</span>
        <span class="confidence-label">Confianza</span>
    `;
    buildChart(probabilidades, categoria);

    emptyState.classList.add("hidden");
    errorBlock.classList.add("hidden");
    resultContent.classList.remove("hidden");
}

function mostrarError(msg) {
    errorMsgEl.textContent = msg;
    emptyState.classList.add("hidden");
    resultContent.classList.add("hidden");
    errorBlock.classList.remove("hidden");
}

function limpiarResultados() {
    resultContent.classList.add("hidden");
    errorBlock.classList.add("hidden");
    emptyState.classList.remove("hidden");
}

// ── Clasificar — solo usa la descripción ───────────────
async function clasificar() {
    const descripcion = descripcionEl.value.trim();

    if (!descripcion) {
        mostrarError("Por favor escribe una descripción antes de clasificar.");
        return;
    }

    limpiarResultados();
    setLoading(true);

    try {
        const res  = await fetch("/predict", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ texto: descripcion }),
        });
        const data = await res.json();

        if (!res.ok || data.error) {
            mostrarError(data.error || "Error desconocido en el servidor.");
            return;
        }

        mostrarResultado(data.categoria, data.probabilidades);

    } catch {
        mostrarError("No se pudo conectar con el servidor. Verifica que esté corriendo.");
    } finally {
        setLoading(false);
    }
}

// ── Nuevo ticket ────────────────────────────────────────
function nuevoTicket() {
    subjectEl.value = "";
    descripcionEl.value = "";
    charCountEl.textContent = "0 / 2000";
    charCountEl.classList.remove("near-limit");
    ticketIdEl.textContent = generarTicketId();
    limpiarResultados();
    subjectEl.focus();
}

// ── Eventos ─────────────────────────────────────────────
btnClasificar.addEventListener("click", clasificar);
btnLimpiar.addEventListener("click", nuevoTicket);
descripcionEl.addEventListener("keydown", e => {
    if (e.key === "Enter" && e.ctrlKey) clasificar();
});
