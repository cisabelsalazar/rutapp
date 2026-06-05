/**
 * Función que abre el modal de gestión de alertas.
 * Recibe el id de la alerta, su estado actual y la observación del administrador.
 */
function abrirModal(id, estado, observacion) {

    // Muestra el modal cambiando su display a flex
    document.getElementById("modalAlerta").style.display = "flex";

    // Asigna el estado actual de la alerta al select del formulario
    document.getElementById("estado").value = estado;

    // Asigna la observación al textarea (si no existe, deja vacío)
    document.getElementById("observacion").value = observacion || "";

    // Configura dinámicamente la ruta del formulario para enviar los datos al backend
    document.getElementById("formAlerta").action = "/editar_alerta/" + id;
}

/**
 * Función que cierra el modal ocultándolo.
 */
function cerrarModal() {
    document.getElementById("modalAlerta").style.display = "none";
}

/**
 * Evento que se ejecuta cuando el documento HTML ha cargado completamente.
 * Se utiliza para asegurar que los elementos del DOM estén disponibles.
 */
document.addEventListener("DOMContentLoaded", function() {

    // Obtiene el formulario del modal por su id
    const form = document.getElementById("formAlerta");

    // Verifica que el formulario exista antes de agregar el evento
    if (form) {

        /**
         * Evento que se ejecuta cuando se envía el formulario.
         * Permite cerrar el modal después de un pequeño retraso.
         */
        form.addEventListener("submit", function() {

            // Se usa un timeout para permitir que el envío del formulario ocurra antes de cerrar
            setTimeout(() => {
                cerrarModal(); // Cierra el modal
            }, 300);

        });
    }

});

/**
 * Evento global que detecta clics en la ventana del navegador.
 * Permite cerrar el modal al hacer clic fuera del contenido del mismo.
 */
window.onclick = function(event) {

    let modal = document.getElementById("modalAlerta");

    // Verifica si el clic fue directamente sobre el fondo del modal (fuera del contenido)
    if (event.target === modal) {
        modal.style.display = "none"; // Cierra el modal
    }
}
