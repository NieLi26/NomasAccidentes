var tblReserva;

function format(d) {
  console.log(d)
  var html = "<table class='table text-center'>";
  html += "<thead class='thead-dark'>";
  html += "<tr>"
  html += "<th scope='col'>Patente</th>";
  html += "<th scope='col'>Numero de Estacionamiento</th>";
  html += "<th scope='col'>Tipo de Estacionamiento</th>";
  html += "<th scope='col'>Tarifa</th>";
  html += "</tr>";
  html += "</thead>";
  html += "<tbody>";
  html += "<tr>";
  html += "<td>" + d.patente.toUpperCase() + "</td>";
  html += "<td>" + d.estacionamiento.numero_estacionamiento + "</td>";
  html += "<td>" + d.estacionamiento.tipo_estacionamiento + "</td>";
  html += "<td>$" + d.tarifa.precio + "</td>";
  html += "</tr>";
  html += "</tbody>";
  html += "</table>";
  return html;
}

$(function () {


  tblReserva = $("#data").DataTable({
    responsive: true,
    // scrollX: true,
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
      { "data": "fecha_entrada" },
      { "data": "hora_entrada" },
      { "data": "fecha_salida" },
      { "data": "hora_salida" },
      { "data": "estado_reserva" },
      {
        "className": 'details-control text-center',
        "orderable": false,
        "data": null,
        "defaultContent": ''
      },
      { "data": "id" }
    ],
    columnDefs: [
      {
        targets: [-3],
        class: "text-center",
        orderable: false,
        render: function (data, type, row) {
          if (data == "reserva terminada") {
            return '<span class="badge badge-success">' + data.toUpperCase() + '</span> ';
          } else if (data == "no ingreso") {
            return '<span class="badge badge-danger">' + data.toUpperCase() + '</span> ';
          } else if (data == "entrada") {
            return '<span class="badge badge-secondary">' + data.toUpperCase() + '</span> ';
          } else if (data == "pago pendiente") {
            return '<span class="badge badge-warning">' + data.toUpperCase() + '</span> ';
          } else {
            return '<span class="badge badge-primary">' + data.toUpperCase() + '</span> ';
          }

        },
      },
      {
        targets: [-1],
        class: "text-center",
        orderable: false,
        render: function (data, type, row) {
          let buttons = '<a href="/erp/reserva/invoice_ingreso/pdf/' +row.id+'/" target="_blank" class="btn btn-dark btn-xs btn-flat"><i class="fas fa-print"></i></a> ';
          return buttons
        },
      },

    ],
    initComplete: function (settings, json) { },
    // se ejecuta al haber cargado la tabla



  });
  //MODAL
  $("#data tbody")
    .on("click", "td.details-control", function () {
      var tr = $(this).closest("tr");
      var row = tblReserva.row(tr);
      if (row.child.isShown()) {
        row.child.hide();
        tr.removeClass("shown");
      } else {
        row.child(format(row.data())).show();
        tr.addClass("shown");
      }
    })

  
});
