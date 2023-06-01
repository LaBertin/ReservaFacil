document.addEventListener('DOMContentLoaded', function() {
  var valorTipoAtencion = document.getElementById('id_Tipo_atencion_form').value;
  var efectivoOculto = document.getElementById('efectivo_oculto');
  var efectivo = document.getElementById('efectivo')

  if (valorTipoAtencion === 'Particular') {
    document.getElementById('arancel_oculto').classList.add('notDisplay');
    document.getElementById('documento_oculto').classList.add('notDisplay');
  } else {
      efectivo.classList.add('notDisplay')
      efectivoOculto.classList.add('notDisplay')
      document.getElementById('arancel_oculto').classList.remove('notDisplay');
      document.getElementById('documento_oculto').classList.remove('notDisplay');
    }
})

function ocultarEfectivo(){

    var valorMetodo = document.getElementById('id_Metodo_pago_form');
    var valorTipoAtencion = document.getElementById('id_Tipo_atencion_form')
    var efectivoOculto = document.getElementById('efectivo_oculto');
    var efectivo = document.getElementById('efectivo')


    // Obtengo el valor del metodo de pago para desplegar el campo del monto en efectivo
    const actualizar_metodo = () => {

      if (valorMetodo.value !== "Efectivo") {

        efectivoOculto.classList.add('notDisplay')
      } else {

        efectivoOculto.classList.remove('notDisplay')
      }
    }

    // Misma idea pero con el tipo de atencion
    const actualizar_atencion = () => {

      var valor = document.getElementById('id_Tipo_atencion_form').value;


      var arancel = document.getElementById('arancel_oculto');


      var numDoc = document.getElementById('documento_oculto');



      if (valor !== "Particular") {

        arancel.classList.remove('notDisplay')
        numDoc.classList.remove('notDisplay')
        efectivo.classList.add('notDisplay')
        efectivoOculto.classList.add('notDisplay')
        valorMetodo.classList.add('notDisplay')
      } else {

        arancel.classList.add('notDisplay')
        numDoc.classList.add('notDisplay')
        efectivo.classList.remove('notDisplay')
        efectivoOculto.classList.remove('notDisplay')
        valorMetodo.classList.remove('notDisplay')
      }
    }
  
    valorMetodo.addEventListener('change', actualizar_metodo);
    valorTipoAtencion.addEventListener('change',actualizar_atencion);
}