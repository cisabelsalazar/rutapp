//Archivo global para confirmar acciones en el sistema//

//Confirmación para eliminar estudiante//

function confirmarEliminacion(id) {
    Swal.fire({
        text: 'Esta acción eliminará el estudiante permanentemente. ¿Deseas continuar?',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonText: 'Sí, eliminar',
        cancelButtonText: 'Cancelar'
    }).then((result) => {
        if (result.isConfirmed) {
            document.getElementById('formEliminar' + id).submit();
        }
    });
}

//Confirmación para eliminar usuario//

function confirmarEliminacionUsuario(id) {
    Swal.fire({
        text: 'Esta acción eliminará al usuario permanentemente. ¿Deseas continuar?',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonText: 'Sí, eliminar',
        cancelButtonText: 'Cancelar'
    }).then((result) => {
        if (result.isConfirmed) {
            document.getElementById('formEliminarUsuario' + id).submit();
        }
    });
}

//Confirmación guardar información editada de estudiante//

function confirmarGuardadoEstudiante() {
    Swal.fire({
        title: '¿Guardar cambios?',
        text: 'Se actualizará la información del estudiante',
        icon: 'question',
        showCancelButton: true,
        confirmButtonText: 'Sí, guardar',
        cancelButtonText: 'Cancelar',
        customClass: {
            popup: 'swal-popup',
            confirmButton: 'swal-confirm-btn',
            cancelButton: 'swal-cancel-btn'
        }
    }).then((result) => {
        if (result.isConfirmed) {
            document.getElementById('formEditarEstudiante').submit();
        }
    });
}

//Confirmación guardar información editada de usuario//
function confirmarGuardadoUsuario() {
    Swal.fire({
        title: '¿Guardar cambios?',
        text: 'Se actualizará la información del usuario',
        icon: 'question',
        showCancelButton: true,
        confirmButtonText: 'Sí, guardar',
        cancelButtonText: 'Cancelar',
        customClass: {
            popup: 'swal-popup',
            confirmButton: 'swal-confirm-btn',
            cancelButton: 'swal-cancel-btn'
        }
    }).then((result) => {
        if (result.isConfirmed) {
            document.getElementById('formEditarUsuario').submit();
        }
    });
}

//Confirmación guardar información editada de vehículo//
function confirmarGuardadoVehiculo() {
    Swal.fire({
        title: '¿Guardar cambios?',
        text: 'Se actualizará la información del vehículo',
        icon: 'question',
        showCancelButton: true,
        confirmButtonText: 'Sí, guardar',
        cancelButtonText: 'Cancelar',
        customClass: {
            popup: 'swal-popup',
            confirmButton: 'swal-confirm-btn',
            cancelButton: 'swal-cancel-btn'
        }
    }).then((result) => {
        if (result.isConfirmed) {
            document.getElementById('formEditarVehiculo').submit();
        }
    });
}

//Confirmación para la creación de un nuevo usuario en el sistema RUTAPP//

function confirmarCreacionUsuario() {
    Swal.fire({
        title: '¿Crear nuevo usuario?',
        text: 'Se guardará un nuevo usuario en el sistema. ¿Deseas continuar?',
        icon: 'question',
        showCancelButton: true,
        confirmButtonText: 'Sí, guardar',
        cancelButtonText: 'Revisar datos'
    }).then((result) => {
        if (result.isConfirmed) {
            document.getElementById('formCrearUsuarios').submit();
        }
    });
}

//Confirmación para la creación de un nuevo estudiante en el sistema RUTAPP//

function confirmarCreacionEstudiante() {
    Swal.fire({
        title: '¿Crear nuevo estudiante?',
        text: 'Se guardará un nuevo estudiante en el sistema. ¿Deseas continuar?',
        icon: 'question',
        showCancelButton: true,
        confirmButtonText: 'Sí, guardar',
        cancelButtonText: 'Revisar datos'
    }).then((result) => {
        if (result.isConfirmed) {
            document.getElementById('formCrearEstudiante').submit();
        }
    });
}

//Confirmación para la creación de un nuevo vehículo en el sistema RUTAPP//

function confirmarCreacionVehiculo() {
    Swal.fire({
        title: '¿Crear nuevo vehículo?',
        text: 'Se guardará un nuevo vehículo en el sistema. ¿Deseas continuar?',
        icon: 'question',
        showCancelButton: true,
        confirmButtonText: 'Sí, guardar',
        cancelButtonText: 'Revisar datos'
    }).then((result) => {
        if (result.isConfirmed) {
            document.getElementById('formCrearVehiculo').submit();
        }
    });
}


//Confirmación nueva contraseña creada//

function confirmarNuevaPassword() {
    Swal.fire({
        title: '¿Cambiar Contraseña?',
        text: 'La contraseña del usuario será actualizada',
        icon: 'question',
        showCancelButton: true,
        confirmButtonText: 'Sí, actualizar',
        cancelButtonText: 'Cancelar',
        customClass: {
            popup: 'swal-popup',
            confirmButton: 'swal-confirm-btn',
            cancelButton: 'swal-cancel-btn'
        }
    }).then((result) => {
        if (result.isConfirmed) {
            document.getElementById('formRecuperarPassword').submit();
        }
    });
}