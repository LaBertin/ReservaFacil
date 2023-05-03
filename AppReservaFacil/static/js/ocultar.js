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


function grupoMultiSelect(){
    var multi_p = document.getElementsByName("dia_p")
    var multi_s = document.getElementsByName("dia_s")
    var multi_t = document.getElementsByName("dia_t")
    var multi_c = document.getElementsByName("dia_c")

    
    const actualizarCampos = () =>{
        const valoresSeleccionados_p = Array.from(multi_p)
            .filter(checkbox => checkbox.checked)
            .map(checkbox => checkbox.value);
        
            const valoresSeleccionados_s = Array.from(multi_s)
            .filter(checkbox => checkbox.checked)
            .map(checkbox => checkbox.value);

            const valoresSeleccionados_t = Array.from(multi_t)
            .filter(checkbox => checkbox.checked)
            .map(checkbox => checkbox.value);

            const valoresSeleccionados_c = Array.from(multi_c)
            .filter(checkbox => checkbox.checked)
            .map(checkbox => checkbox.value);


        const min_lun = document.getElementById("div_min_lun_p");
        const min_mar = document.getElementById("div_min_mar_p");
        const min_mie = document.getElementById("div_min_mie_p");
        const min_jue = document.getElementById("div_min_jue_p");
        const min_vie = document.getElementById("div_min_vie_p");
        const min_sab = document.getElementById("div_min_sab_p");
        const min_dom = document.getElementById("div_min_dom_p");

        Array.from(multi_p).forEach(checkbox => {
            checkbox.addEventListener('change', function(event){
                if (event.target.checked && event.target.value == 'lun'){
                    min_lun.style.display="block"
                }else if (event.target.checked && event.target.value == 'mar'){
                    min_mar.style.display="block"
                }else if (event.target.checked && event.target.value == 'mie'){
                    min_mie.style.display="block"
                }else if (event.target.checked && event.target.value == 'jue'){
                    min_jue.style.display="block"
                }else if (event.target.checked && event.target.value == 'vie'){
                    min_vie.style.display="block"
                }else if (event.target.checked && event.target.value == 'sab'){
                    min_sab.style.display="block"
                }else if (event.target.checked && event.target.value == 'dom'){
                    min_dom.style.display="block"
                }else if (!event.target.checked && event.target.value == 'lun'){
                    min_lun.style.display="none"
                }else if (!event.target.checked && event.target.value == 'mar'){
                    min_mar.style.display="none"
                }else if (!event.target.checked && event.target.value == 'mie'){
                    min_mie.style.display="none"
                }else if (!event.target.checked && event.target.value == 'jue'){
                    min_jue.style.display="none"
                }else if (!event.target.checked && event.target.value == 'vie'){
                    min_vie.style.display="none"
                }else if (!event.target.checked && event.target.value == 'sab'){
                    min_sab.style.display="none"
                }else{
                    min_dom.style.display="none"
                }
            })
            
            if(valoresSeleccionados_c.includes(checkbox.value)||valoresSeleccionados_t.includes(checkbox.value)||valoresSeleccionados_s.includes(checkbox.value)){
                checkbox.disabled = true
                
            }else{
                checkbox.disabled = false
            }
        })

        const min_lun_s = document.getElementById("div_min_lun_s");
        const min_mar_s = document.getElementById("div_min_mar_s");
        const min_mie_s = document.getElementById("div_min_mie_s");
        const min_jue_s = document.getElementById("div_min_jue_s");
        const min_vie_s = document.getElementById("div_min_vie_s");
        const min_sab_s = document.getElementById("div_min_sab_s");
        const min_dom_s = document.getElementById("div_min_dom_s");

        Array.from(multi_s).forEach(checkbox => {
            checkbox.addEventListener('change', function(event){
                if (event.target.checked && event.target.value == 'lun'){
                    min_lun_s.style.display="block"
                }else if (event.target.checked && event.target.value == 'mar'){
                    min_mar_s.style.display="block"
                }else if (event.target.checked && event.target.value == 'mie'){
                    min_mie_s.style.display="block"
                }else if (event.target.checked && event.target.value == 'jue'){
                    min_jue_s.style.display="block"
                }else if (event.target.checked && event.target.value == 'vie'){
                    min_vie_s.style.display="block"
                }else if (event.target.checked && event.target.value == 'sab'){
                    min_sab_s.style.display="block"
                }else if (event.target.checked && event.target.value == 'dom'){
                    min_dom_s.style.display="block"
                }else if (!event.target.checked && event.target.value == 'lun'){
                    min_lun_s.style.display="none"
                }else if (!event.target.checked && event.target.value == 'mar'){
                    min_mar_s.style.display="none"
                }else if (!event.target.checked && event.target.value == 'mie'){
                    min_mie_s.style.display="none"
                }else if (!event.target.checked && event.target.value == 'jue'){
                    min_jue_s.style.display="none"
                }else if (!event.target.checked && event.target.value == 'vie'){
                    min_vie_s.style.display="none"
                }else if (!event.target.checked && event.target.value == 'sab'){
                    min_sab_s.style.display="none"
                }else{
                    min_dom_s.style.display="none"
                }
            })
            if(valoresSeleccionados_p.includes(checkbox.value)||valoresSeleccionados_c.includes(checkbox.value)||valoresSeleccionados_t.includes(checkbox.value)){
                checkbox.disabled = true
            }else{
                checkbox.disabled = false
            }
        })

        Array.from(multi_t).forEach(checkbox => {
            if(valoresSeleccionados_p.includes(checkbox.value)||valoresSeleccionados_s.includes(checkbox.value)||valoresSeleccionados_c.includes(checkbox.value)){
                checkbox.disabled = true
            }else{
                checkbox.disabled = false
            }
        })

        Array.from(multi_c).forEach(checkbox => {
            if(valoresSeleccionados_p.includes(checkbox.value)||valoresSeleccionados_s.includes(checkbox.value)||valoresSeleccionados_t.includes(checkbox.value)){
                checkbox.disabled = true
            }else{
                checkbox.disabled = false
            }
        })
    }

    Array.from(multi_p).forEach(checkbox => {
        checkbox.addEventListener('click', actualizarCampos);
      });

    Array.from(multi_s).forEach(checkbox => {
        checkbox.addEventListener('click', actualizarCampos);
      });
    Array.from(multi_t).forEach(checkbox => {
        checkbox.addEventListener('click', actualizarCampos);
      });
    Array.from(multi_c).forEach(checkbox => {
        checkbox.addEventListener('click', actualizarCampos);
    });
}