var checkboxReceta = document.getElementById('receta')
var checkboxExamen = document.getElementById('examen')
var textoReceta = document.getElementById('id_Receta_Cita')
var textoExamen = document.getElementById('id_Examenes_Cita')
window.onload = function() {
    disabled_receta ()
    disabled_examen ()
};
function disabled_receta (){
    console.log("Dentro de la funcion")
    console.log(`valor de checkboxReceta ${checkboxReceta}`)
    console.log(`valor de textoReceta ${textoReceta}`)
    if(checkboxReceta.checked){
        console.log("Dentro del if de receta")
        textoReceta.value=''
        textoReceta.disabled=false
    }else{
        console.log("Dentro del else del receta")
        textoReceta.value=''
        textoReceta.disabled=true
    }
}

function disabled_examen (){
    console.log("Dentro de la funcion disabled_examen")
    console.log(`valor de checkboxReceta ${checkboxReceta}`)
    console.log(`valor de textoReceta ${textoExamen}`)
    if(checkboxExamen.checked){
        console.log("Dentro del if de receta")
        textoExamen.value=''
        textoExamen.disabled=false
    }else{
        console.log("Dentro del else del receta")
        textoExamen.value=''
        textoExamen.disabled=true
    }
}

