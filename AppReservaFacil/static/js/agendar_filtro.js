const areaMedicaField = document.getElementById('id_area_medica_a');
const especialidadField = document.getElementById('id_especialidad_a');
            
areaMedicaField.addEventListener('change', () => {
    const areaMedicaId = areaMedicaField.value;
    if (areaMedicaId) {
        fetch(`/obtener_especialidades/${areaMedicaId}/`)
            .then(response => response.json())
            .then(data => {
                // Limpiar las opciones existentes y agregar las nuevas
                especialidadField.innerHTML = '';
                data.forEach(option => {
                    const optionEl = document.createElement('option');
                    optionEl.value = option[0];
                    optionEl.innerText = option[1];
                    especialidadField.appendChild(optionEl);
                });
            });
    } else {
        // Si no se seleccionó ninguna opción, borrar las opciones existentes
        especialidadField.innerHTML = '';
    }
});