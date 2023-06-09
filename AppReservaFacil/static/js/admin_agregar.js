const formulario = document.getElementById('formulario');  /*acceso al id=formulario*/
const inputs = document.querySelectorAll('#formulario input'); /*optiene todos los arreglos de los input*/

const expresiones = {

	nombre: /^[a-zA-ZÀ-ÿ\s]{1,40}$/, /* Letras y espacios, pueden llevar acentos.*/
    cargo: /^[a-zA-ZÀ-ÿ\s]{1,40}$/, /* Letras y espacios, pueden llevar acentos.*/
    rut: /^\d{7,14}$/, /* 7 a 14 numeros.*/
	sexo: /^[a-zA-ZÀ-ÿ\s]{1,40}$/, /* Letras y espacios, pueden llevar acentos.*/
	correo: /^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$/,
	telefonoCelular: /^\d{7,14}$/, /* 7 a 14 numeros.*/
    telefono: /^\d{7,14}$/, /* 7 a 14 numeros.*/
    telefonoContacto: /^\d{7,14}$/, /* 7 a 14 numeros.*/

}


const campos = {

	nombre: false,
	cargo: false,
	rut: false,
	sexo: false,
	correo: false,
	telefonoCelular: false,
    telefono: false,
	telefonoContacto: false,
    
}


const validarFormulario = (e) => {
	switch (e.target.name) {
		case "nombre":
			validarCampo(expresiones.nombre, e.target, 'nombre');
		break;
        case "cargo":
			validarCampo(expresiones.cargo, e.target, 'cargo');
		break;
        case "rut":
			validarCampo(expresiones.rut, e.target, 'rut');
		break;
		case "sexo":
			validarCampo(expresiones.sexo, e.target, 'sexo');
		break;
        case "correo":
			validarCampo(expresiones.correo, e.target, 'correo');
		break;
        case "telefonoCelular":
			validarCampo(expresiones.telefonoCelular, e.target, 'telefonoCelular');
		break;
        case "telefono":
			validarCampo(expresiones.telefono, e.target, 'telefono');
		break;
        case "telefonoContacto":
			validarCampo(expresiones.telefonoContacto, e.target, 'telefonoContacto');
		break;
        
        
	}
}

const validarCampo = (expresion, input, campo) => {
	if(expresion.test(input.value)){
		document.getElementById(`grupo__${campo}`).classList.remove('formulario__grupo-incorrecto');
		document.getElementById(`grupo__${campo}`).classList.add('formulario__grupo-correcto');
		document.querySelector(`#grupo__${campo} i`).classList.add('fa-check-circle');
		document.querySelector(`#grupo__${campo} i`).classList.remove('fa-times-circle');
		document.querySelector(`#grupo__${campo} .formulario__input-error`).classList.remove('formulario__input-error-activo');
		campos[campo] = true;
	} else {
		document.getElementById(`grupo__${campo}`).classList.add('formulario__grupo-incorrecto');
		document.getElementById(`grupo__${campo}`).classList.remove('formulario__grupo-correcto');
		document.querySelector(`#grupo__${campo} i`).classList.add('fa-times-circle');
		document.querySelector(`#grupo__${campo} i`).classList.remove('fa-check-circle');
		document.querySelector(`#grupo__${campo} .formulario__input-error`).classList.add('formulario__input-error-activo');
		campos[campo] = false;
	}
}



inputs.forEach((input) => {
	input.addEventListener('keyup', validarFormulario);
	input.addEventListener('blur', validarFormulario);
});

formulario.addEventListener('submit', (e) => {
	e.preventDefault();

	

	if(campos.nombre && campos.cargo && campos.rut && campos.sexo && campos.correo && campos.telefonoCelular && campos.telefono && campos.telefonoContacto /*&& campos.fecha && campos.hora*/){
		formulario.reset();

		document.getElementById('formulario__mensaje-exito').classList.add('formulario__mensaje-exito-activo');
		setTimeout(() => {
			document.getElementById('formulario__mensaje-exito').classList.remove('formulario__mensaje-exito-activo');
		}, 5000);

		document.querySelectorAll('.formulario__grupo-correcto').forEach((icono) => {
			icono.classList.remove('formulario__grupo-correcto');
		});
	} else {
		document.getElementById('formulario__mensaje').classList.add('formulario__mensaje-activo');
	}
});
