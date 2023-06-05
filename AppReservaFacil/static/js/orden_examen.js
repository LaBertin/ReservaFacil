
var lista = []

function prueba(){
    var valor = document.getElementById('pruebacosa').value
    if (valor != 0){
        lista.push(valor)
        console.log(lista)

        // Creo la lista de la tabla
        document.getElementById('pruebacosa').value = ''
        var tbody = document.getElementById('seleccion-body')
        var tr = document.createElement('tr')
        var td1 = document.createElement('td')
        var td2 = document.createElement('td')
        
        // boton para eliminar de la lista 
        var boton = document.createElement('button');
        boton.setAttribute('type','button');
        boton.setAttribute('name','borrar_examen');
        
        var boton_id = "borrar_examen_"+valor
        boton.setAttribute('id',boton_id);
        boton.setAttribute('value',valor);
        boton.classList.add('btn-naranja-mediano')
        boton.setAttribute('onclick', 'pruebaeliminar("' + boton_id + '")');

        var text = document.createTextNode('Borrar')
      
        boton.appendChild(text)
        td1.appendChild(document.createTextNode(valor))
        td2.appendChild(boton)
        tr.setAttribute('id',valor)
        tr.appendChild(td1)
        tr.appendChild(td2)
        tbody.appendChild(tr)

        var dato = lista.join(',')
        console.log(dato)
        document.getElementById('id_examenes').value=dato
    }
}

function pruebaeliminar(id){
    var valoreliminar = document.getElementById(id).value
    console.log(valoreliminar)
    var tdeliminar = document.getElementById(valoreliminar)
    console.log(tdeliminar)
    tdeliminar.remove()

    
}   