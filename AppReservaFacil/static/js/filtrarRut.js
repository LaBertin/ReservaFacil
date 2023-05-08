// Obtener elementos del DOM
const searchBtn = document.getElementById('buscar-btn');
const searchInput = document.getElementById('buscar-input');
const rows = document.querySelectorAll('tbody tr');

// Función para filtrar por RUT
const filterByRut = () => {
  const searchTerm = searchInput.value.trim().toLowerCase();
  rows.forEach((row) => {
    const rut = row.querySelector('.rut').textContent.toLowerCase();
    if (rut.includes(searchTerm)) {
      row.style.display = '';
    } else {
      row.style.display = 'none';
    }
  });
};

// Asignar evento al botón de búsqueda
searchBtn.addEventListener('click', filterByRut);