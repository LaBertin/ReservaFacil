function ocultarEfectivo(){

    var valorMetodo = document.getElementById('id_Metodo_pago_form');
    var valorTipoAtencion = document.getElementById('id_Tipo_atencion_form')
    
    // Obtengo el valor del metodo de pago para desplegar el campo del monto en efectivo
    const actualizar_metodo = () => {
      console.log("Dentro del actualizar")
      var valorMetodo = document.getElementById('id_Metodo_pago_form').value;
      console.log(`Valor metodo: ${valorMetodo}`)
      var efectivoOculto = document.getElementById('efectivo_oculto');
      console.log(`Valor efectivoOculto: ${efectivoOculto}`)
      if (valorMetodo !== "Efectivo") {
      console.log(`Dentro del if`)
        efectivoOculto.classList.add('notDisplay')
      } else {
          console.log(`Dentro del else`)
        efectivoOculto.classList.remove('notDisplay')
      }
    }

    // Misma idea pero con el tipo de atencion
    const actualizar_atencion = () => {
      console.log("Dentro del actualizar")
      var valorTipoAtencion = document.getElementById('id_Tipo_atencion_form').value;
      console.log(`Valor metodo: ${valorTipoAtencion}`)

      var arancel = document.getElementById('arancel_oculto');
      console.log(`Valor arancel: ${arancel}`)

      var numDoc = document.getElementById('documento_oculto');
      console.log(`Valor arancel: ${numDoc}`)


      if (valorTipoAtencion !== "Particular") {
      console.log(`Dentro del if Actualizar_atencion`)
        arancel.classList.remove('notDisplay')
        numDoc.classList.remove('notDisplay')
      } else {
        console.log(`Dentro del else`)
        arancel.classList.add('notDisplay')
        numDoc.classList.add('notDisplay')
      }
    }
  
    valorMetodo.addEventListener('change', actualizar_metodo);
    valorTipoAtencion.addEventListener('change',actualizar_atencion);
}