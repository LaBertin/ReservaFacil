//OCULTAR CAMPO
function ocultarDiasS(){
    var valorEspecialidad = document.getElementById("id_especialidad_s")
    var divid = document.getElementById("divespecialidads")
    var valor = valorEspecialidad.value;
    console.log(divid)

    if(valor != ""){
        console.log("HOLAAA")
        document.getElementById("divespecialidads").className="wrapper"
        console.log(divid)
    }else{
        document.getElementById("divespecialidads").className="wrappernone"
    }
}

function ocultarDiasT(){
    var valorEspecialidad = document.getElementById("id_especialidad_t")
    var divid = document.getElementById("divespecialidadt")
    var valor = valorEspecialidad.value;
    console.log(divid)

    if(valor != ""){
        console.log("HOLAAA")
        document.getElementById("divespecialidadt").className="wrapper"
        console.log(divid)
    }else{
        document.getElementById("divespecialidadt").className="wrappernone"
    }
}

function ocultarDiasC(){
    var valorEspecialidad = document.getElementById("id_especialidad_c")
    var divid = document.getElementById("divespecialidadc")
    var valor = valorEspecialidad.value;
    console.log(divid)

    if(valor != ""){
        console.log("HOLAAA")
        document.getElementById("divespecialidadc").className="wrapper"
        console.log(divid)
    }else{
        document.getElementById("divespecialidadc").className="wrappernone"
    }
}


