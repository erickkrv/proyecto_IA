const btnClasificar  = document.getElementById("btn-clasificar");
const btnLimpiar     = document.getElementById("btn-limpiar");
const textoInput     = document.getElementById("texto");
const charCount      = document.getElementById("char-count");
const seccionResult  = document.getElementById("resultado");
const categoriaEl    = document.getElementById("categoria");
const seccionError   = document.getElementById("error");
const errorMsgEl     = document.getElementById("error-msg");

// ── Contador de caracteres ──────────────────────────────
textoInput.addEventListener("input", () => {
    const len = textoInput.value.length;
    const max = textoInput.maxLength;
    charCount.textContent = `${len} / ${max}`;
    charCount.classList.toggle("near-limit", len > max * 0.85);
});

// ── UI helpers ──────────────────────────────────────────
function mostrarResultado(categoria) {
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
            '<span class="btn-text">Clasificar</span><span class="btn-arrow">→</span>';
    }
}

// ── Clasificar ──────────────────────────────────────────
async function clasificar() {
    const texto = textoInput.value.trim();

    if (!texto) {
        mostrarError("Por favor ingresa una solicitud antes de clasificar.");
        return;
    }

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

function limpiarTodo() {
    textoInput.value = "";
    charCount.textContent = "0 / 2000";
    charCount.classList.remove("near-limit");
    limpiarPantalla();
    textoInput.focus();
}

// ── Eventos ─────────────────────────────────────────────
btnClasificar.addEventListener("click", clasificar);
btnLimpiar.addEventListener("click", limpiarTodo);

textoInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && e.ctrlKey) clasificar();
});
