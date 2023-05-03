$(document).ready(function() {
    var tableRows = $(".table tbody tr");
    var tableBody = $(".table tbody");
    var rowsPerPage = 4;
    var currentPage = 0;
    var totalPages = Math.ceil(tableRows.length / rowsPerPage);
  
    // Agregar los botones de paginación
    for (var i = 0; i < totalPages; i++) {
      var li = $("<li><a href='#'>" + (i + 1) + "</a></li>");
      $(".pagination").append(li);
    }
  
    // Mostrar la primera página
    showPage(0);
  
    // Manejar los clicks en los botones de paginación
    $(".pagination li").on("click", function() {
      currentPage = $(this).index();
      showPage(currentPage);
    });
  
    // Función para mostrar una página específica
    function showPage(page) {
      tableBody.empty();
  
      // Obtener las filas de la página actual
      var rows = tableRows.slice(page * rowsPerPage, (page + 1) * rowsPerPage);
  
      // Agregar las filas a la tabla
      $.each(rows, function(index, row) {
        tableBody.append(row);
      });
  
      // Remover la clase 'active' de todos los botones de paginación
      $(".pagination li").removeClass("active");
  
      // Agregar la clase 'active' al botón de la página actual
      $(".pagination li").eq(page).addClass("active");
    }
  });