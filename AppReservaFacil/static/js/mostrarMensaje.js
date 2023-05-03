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
  document.querySelector('form').submit
  ocultarMensaje();
}
//Eliminar Especialista
function mostrarMensajeDeleteEsp(id) {
  fechaID = id;
  console.log(fechaID)
  document.getElementById("mensajeDeleteEsp").style.display = "block";
}
function ocultarMensajeDeleteEsp() {
  document.getElementById("mensajeDeleteEsp").style.display = "none";
}
function eliminarDeleteEsp() {
  console.log(fechaID)
  console.log("JOORRGEE")
  // Actualizar el valor del botón con fechaID
  document.getElementById("conf_delet_cit_button").value = fechaID;
  // Enviar el formulario
  document.querySelector('form').submit
  ocultarMensajeDeleteEsp();
}

//Especialista Bubble
function mostrarMensajeEspecialista() {
  document.getElementById("mensajeEspecialista").style.display = "block";
}
function ocultarMensajeEspecialista() {
  document.getElementById("mensajeEspecialista").style.display = "none";
}


//Operador Bubble
function mostrarMensajeOperador() {
  document.getElementById("mensajeOperador").style.display = "block";
}
function ocultarMensajeOperador() {
  document.getElementById("mensajeOperador").style.display = "none";
}