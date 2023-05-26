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
  document.getElementById("conf_delet_cit_button").value = fechaID;
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
  document.getElementById("conf_delet_cit_button").value = fechaID;
  document.querySelector('form').submit
  ocultarMensajeDeleteEsp();
}

//Eliminar Operador
function mostrarMensajeDeleteOpe(id) {
  fechaID = id;
  console.log(fechaID)
  document.getElementById("mensajeDeleteOpe").style.display = "block";
}
function ocultarMensajeDeleteOpe() {
  document.getElementById("mensajeDeleteOpe").style.display = "none";
}
function eliminarDeleteOpe() {
  console.log(fechaID)
  console.log("JOORRGEE")
  document.getElementById("conf_delet_cit_button").value = fechaID;
  document.querySelector('form').submit
  ocultarMensajeDeleteOpe();
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

//Especialidad Bubble
function mostrarMensajeEspecialidad() {
  document.getElementById("mensajeEspecialidad").style.display = "block";
}
function ocultarMensajeEspecialidad() {
  document.getElementById("mensajeEspecialidad").style.display = "none";
}

//Cita medica Bubble
function mostrarMensajeCitaRecetaDos() {
  document.getElementById("mensajeCita").style.display = "block";
}

function ocultarMensajeCitaRecetaDos() {
  document.getElementById("mensajeCita").style.display = "none";
  document.getElementById("mensajeCitaExamen").style.display = "block"
}

function finalizarCitaMedica(redireccionar){
  var form = document.getElementById('form_cita');
  var redireccionar = document.getElementById('redireccionar_field')
  if (redireccionar){
    redireccionar.value = "1"
  }
  form.submit()
}

function finalizarCitaMedicaOrden(redireccionar_o){
  var form = document.getElementById('form_cita');
  var redireccionar_o = document.getElementById('redireccionar_o_field')
  if (redireccionar_o){
    redireccionar_o.value = "1"
  }
  form.submit()
}


function finalizarCita(){
  var form = document.getElementById('form_confirmar_cita');
  form.submit()
}

function ConfirmarAgenda() {
  var form = document.getElementById('form_confirmar_cita');
  form.submit();
}


function ConfirmarPago(redireccion_confirmar){
  var form = document.getElementById('form_confirmar_cita');
  console.log(form)
  if (redireccion_confirmar) {
    var redirectInput = document.getElementById('redireccion_confirmar');
    console.log(redirectInput)
    redirectInput.value = "1";
    console.log(redirectInput)
  }
  form.submit();
}



