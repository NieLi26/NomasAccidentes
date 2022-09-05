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
      { "data": "precio" },
      { "data": "id" }
    ],
    columnDefs: [
      {
        targets: [-2],
        class: "text-center",
        orderable: false,
        render: function (data, type, row) {
          return `<b>$</b>${data}`;
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


