//OCULTAR CAMPO
function ocultarDiasS(){
    /*Obtenemos el valor asignado en HTML de la Especialidad*/
    var valorEspecialidad = document.getElementById("id_especialidad_s")
    var valor = valorEspecialidad.value;

    /*Ocultamos o desplegamos campos segun valor del campo*/
    if(valor != ""){
        /**Desplegar Dias y Minutos de Especialidad 2 / Seleccion de Especialidad 3 */
        document.getElementById("divespecialidads").className="wrapper"
        document.getElementById("divmins").className="display"
        document.getElementById("esp_display_t").className="display"
        document.getElementById("esp_display2_t").className="display"

    }else{
        /**Ocultar Dias y Minutos de Especialidad 2, Especialidad 3 y Especilidad 4*/
        document.getElementById("divespecialidads").className="wrappernone"
        document.getElementById("divespecialidadt").className="wrappernone"
        document.getElementById("divespecialidadc").className="wrappernone"
        document.getElementById("id_especialidad_t").value=""
        document.getElementById("id_especialidad_c").value=""
        document.getElementById("divmins").className="notDisplay"
        document.getElementById("divmint").className="notDisplay"
        document.getElementById("divminc").className="notDisplay"
        document.getElementById("esp_display_t").className="notDisplay"
        document.getElementById("esp_display2_t").className="notDisplay"
        document.getElementById("esp_display_c").className="notDisplay"
        document.getElementById("esp_display2_c").className="notDisplay"

    }
}

function ocultarDiasT(){
    var valorEspecialidad = document.getElementById("id_especialidad_t")
    var divid = document.getElementById("divespecialidadt")
    var valor = valorEspecialidad.value;

    /*Ocultamos o desplegamos campos segun valor del campo*/
    if(valor != ""){
        /**Desplegar Dias y Minutos de Especialidad 3 / Seleccion de Especialidad 4*/
        document.getElementById("divespecialidadt").className="wrapper"
        document.getElementById("divmint").className="display"
        document.getElementById("esp_display_c").className="display"
        document.getElementById("esp_display2_c").className="display"
    }else{
        /**Ocultar Dias y Minutos de Especialidad 3 y Especilidad 4*/
        document.getElementById("divespecialidadt").className="wrappernone"
        document.getElementById("divespecialidadc").className="wrappernone"
        document.getElementById("divmint").className="notDisplay"
        document.getElementById("divminc").className="notDisplay"
        document.getElementById("id_especialidad_c").value=""
        document.getElementById("esp_display_c").className="notDisplay"
        document.getElementById("esp_display2_c").className="notDisplay"
    }
}

function ocultarDiasC(){
    var valorEspecialidad = document.getElementById("id_especialidad_c")
    var divid = document.getElementById("divespecialidadc")
    var valor = valorEspecialidad.value;

    /*Ocultamos o desplegamos campos segun valor del campo*/
    if(valor != ""){
        /**Desplegar Dias y Minutos de Especialidad 4*/
        document.getElementById("divespecialidadc").className="wrapper"
        document.getElementById("divminc").className="display"

    }else{
        /**Ocultar Dias y Minutos de Especilidad 4*/
        document.getElementById("divespecialidadc").className="wrappernone"
        document.getElementById("divminc").className="notDisplay"
    }
}
