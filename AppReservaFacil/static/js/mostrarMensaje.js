function mostrarMensaje(id) {
  fechaID = id;
  console.log(fechaID)
  document.getElementById("mensaje").style.display = "block";
}
function ocultarMensaje() {
  document.getElementById("mensaje").style.display = "none";
}
function eliminarCita() {
  console.log(fechaID)
  // Actualizar el valor del botón con fechaID
  document.getElementById("conf_delet_cit_button").value = fechaID;
  // Enviar el formulario
  document.querySelector('form').submi
  ocultarMensaje();
}
