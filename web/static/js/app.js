const btnClasificar     = document.getElementById("btn-clasificar");
const btnLimpiar        = document.getElementById("btn-limpiar");
const ticketIdEl        = document.getElementById("ticket-id");
const subjectEl         = document.getElementById("subject");
const descripcionEl     = document.getElementById("descripcion");
const charCount         = document.getElementById("char-count");
const seccionResult     = document.getElementById("resultado");
const resultTicketIdEl  = document.getElementById("resultado-ticket-id");
const categoriaEl       = document.getElementById("categoria");
const seccionError      = document.getElementById("error");
const errorMsgEl        = document.getElementById("error-msg");

// ── Generación de Ticket ID ─────────────────────────────
function generarTicketId() {
    const num = Math.floor(10000 + Math.random() * 90000);
    return `TKT-${num}`;
}

function nuevoTicketId() {
    ticketIdEl.value = generarTicketId();
}

nuevoTicketId();

// ── Contador de caracteres ──────────────────────────────
descripcionEl.addEventListener("input", () => {
    const len = descripcionEl.value.length;
    const max = descripcionEl.maxLength;
    charCount.textContent = `${len} / ${max}`;
    charCount.classList.toggle("near-limit", len > max * 0.85);
});

// ── UI helpers ──────────────────────────────────────────
function mostrarResultado(categoria) {
    resultTicketIdEl.textContent = ticketIdEl.value;
    categoriaEl.textContent = categoria;
    seccionResult.classList.remove("hidden");
    seccionError.classList.add("hidden");
}

function mostrarError(mensaje) {
    errorMsgEl.textContent = mensaje;
    seccionError.classList.remove("hidden");
    seccionResult.classList.add("hidden");
}

function limpiarPantalla() {
    seccionResult.classList.add("hidden");
    seccionError.classList.add("hidden");
}

function setLoading(activo) {
    btnClasificar.disabled = activo;
    if (activo) {
        btnClasificar.innerHTML =
            '<span class="spinner"></span><span class="btn-text">Clasificando...</span>';
    } else {
        btnClasificar.innerHTML =
            '<span class="btn-text">Clasificar Ticket</span><span class="btn-arrow">→</span>';
    }
}

// ── Clasificar ──────────────────────────────────────────
async function clasificar() {
    const subject     = subjectEl.value.trim();
    const descripcion = descripcionEl.value.trim();

    if (!subject && !descripcion) {
        mostrarError("Por favor completa al menos el asunto o la descripción del ticket.");
        return;
    }

    // Concatenar asunto y descripción para la clasificación
    const texto = [subject, descripcion].filter(Boolean).join(" ");

    limpiarPantalla();
    setLoading(true);

    try {
        const respuesta = await fetch("/predict", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ texto }),
        });

        const datos = await respuesta.json();

        if (!respuesta.ok || datos.error) {
            mostrarError(datos.error || "Error desconocido en el servidor.");
            return;
        }

        mostrarResultado(datos.categoria);

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
    charCount.textContent = "0 / 2000";
    charCount.classList.remove("near-limit");
    limpiarPantalla();
    nuevoTicketId();
    subjectEl.focus();
}

// ── Eventos ─────────────────────────────────────────────
btnClasificar.addEventListener("click", clasificar);
btnLimpiar.addEventListener("click", nuevoTicket);

descripcionEl.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && e.ctrlKey) clasificar();
});
