$(function () {
  $("#data").DataTable({
    responsive: true,
    autoWidth: false,
    destroy: true,
    deferRender: true,
    ajax: {
      url: window.location.pathname,
      type: "POST",
      data: {
        action: "searchdata",
      }, // parametros
      dataSrc: "",
      headers: {
        'X-CSRFToken': csrftoken
    }
    },
    columns: [
      { "data": "id" },
      { "data": "nombre" },
      { "data": "apellido" },
      { "data": "rut" },
      { "data": "razon_social" },
      { "data": "direccion" },
      { "data": "telefono" },
      { "data": "mail" },
      { "data": "id" }
    ],
    columnDefs: [
      {
        targets: [-5],
        class: "text-center",
        orderable: false,
        render: function (data, type, row) {
          // if ( data !== null) return data
          // return "No tiene"; 
          return data;
        },
      },
      {
        targets: [-1],
        class: "text-center",
        orderable: false,
        render: function (data, type, row) {
          let buttons = '<a href="' + row.update_url + '" class="btn btn-warning btn-xs btn-flat"><i class="fas fa-edit"></i></a> ';
          buttons += '<a href="' + row.delete_url + '" type="button" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash-alt"></i></a>';
          return buttons;
        },
      },
    ],
    initComplete: function (settings, json) { },
    // se ejecuta al haber cargado la tabla
  });
});


