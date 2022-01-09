var tblClient;
var modal_title;

function getData() {

    tblClient = $("#data").DataTable({
      responsive: true,
      autoWidth: false,
      destroy: true,
      deferRender: true,
      ajax: {
        url: window.location.pathname,
        type: "POST",
        data: {
          action: "searchdata",
        },
        dataSrc: "",
      },
      columns: [
        { "data": "id" },
        { "data": "cli.name" },
        { "data": "tipo.nombre" },
        { "data": "fecha_realizacion" },
        { "data": "completado" },
        { "data": "id" },
      ],
      columnDefs: [
         {
                "targets": -2,
                "data": "completado",
                "render": function ( data, type, row, meta ) {
                if (data == true) {
                    return '<span class="badge badge-success"> Si </span> ';
                    }
                else if (data == false) {
                  return '<span class="badge badge-warning"> No </span> ';
                }
                    return data;
                },
            },
        {
          targets: [-1],
          class: "text-center",
          orderable: false,
          render: function (data, type, row) {
            var buttons =
              '<a href="/erp/asesoria/update/' +
              row.id +
              '/" class="btn btn-warning btn-xs btn-flat"><i class="fas fa-edit"></i></a> ';
            buttons +=
              '<a href="/erp/asesoria/delete/' +
              row.id +
              '/" type="button" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash-alt"></i></a> ';
            buttons +=
              '<a href="#" rel="edit" type="button" class="btn btn-success btn-xs btn-flat"><i class="fas fa-search"></i></a>';
            return buttons;
          },
        },
      ],
      initComplete: function (settings, json) {},
    });
};

$(function () {
  modal_title = $(".modal-title");

  getData();

  // $('.btnAdd').on('click', function () {
  //     $('input[name="action"]').val('add');
  //     modal_title.find('span').html('Creación de una capacitacion');
  //     console.log(modal_title.find('i'));
  //     modal_title.find('i').removeClass().addClass('fas fa-plus');
  //     $('form')[0].reset();
  //     $('#myModalCapacitacion').modal('show');
  // });

  $("#data tbody").on("click", 'a[rel="edit"]', function () {
    // modal_title.find('span').html('Edición de una Capacitacion');
    // modal_title.find('i').removeClass().addClass('fas fa-edit');
    modal_title.find("span").html("Detalles de Asesoria");
    modal_title.find("i").removeClass().addClass("fas fa-search");
    var tr = tblClient.cell($(this).closest("td, li")).index();
    var data = tblClient.row(tr.row).data();
    // $('select[name="cli"]').val(data.cli.id);
    // $('select[name="act"]').val(data.act);
    // $('select[name="func"]').val(data.func.id);
    // $('select[name="mat"]').val(data.mat.id);
    // $('select[name="horario"]').val(data.horario.id);
    // $('input[name="asist"]').val(data.asist);
    $('textarea[name="inf"]').val(data.inf);
    // $('date[name="fecha_realizacion"]').val(data.fecha_realizacion);
    // $('input[name="completado"]').val(data.completado);
    $("#myModalAsesoria").modal("show");
  });

  $("#myModalAsesoria").on("shown.bs.modal", function () {
    // $('form')[0].reset();
  });

  // $('form').on('submit', function (e) {
  //     e.preventDefault();
  //     //var parameters = $(this).serializeArray();
  //     var parameters = new FormData(this);
  //     submit_with_ajax(window.location.pathname, 'Notificación', '¿Estas seguro de realizar la siguiente acción?', parameters, function () {
  //         $('#myModalCapacitacion').modal('hide');
  //         tblClient.ajax.reload();
  //         //getData();
  //     });
  // });
});