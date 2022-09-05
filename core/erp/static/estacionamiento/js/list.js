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
      { "data": "numero_estacionamiento" },
      { "data": "tipo_estacionamiento" },
      { "data": "estado_estacionamiento" },
      { "data": "id" }
    ],
    columnDefs: [
      {
        targets: [0],
        class: "text-center",
        orderable: false,
        render: function (data, type, row) {
          return data;
        },
      },
      {
        targets: [-2],
        class: "text-center",
        orderable: false,
        render: function (data, type, row) {
          if (data == "disponible") {
            return '<span class="badge badge-success">' + data.toUpperCase() + '</span> ';
          } else if (data == "ocupado") {
            return '<span class="badge badge-danger">' + data.toUpperCase() + '</span> ';
          } else {
            return '<span class="badge badge-warning">' + data.toUpperCase() + '</span> ';
          }

        },
      },
      {
        targets: [-1],
        class: "text-center",
        orderable: false,
        render: function (data, type, row) {
          let buttons = '<a href="/erp/estacionamiento/update/' + row.id + '/" class="btn btn-warning btn-xs btn-flat"><i class="fas fa-edit"></i></a> ';
          buttons += '<a href="/erp/estacionamiento/delete/' + row.id + '/" type="button" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash-alt"></i></a>';
          return buttons;
        },
      },
    ],
    initComplete: function (settings, json) { },
    // se ejecuta al haber cargado la tabla
  });
});


