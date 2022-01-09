$(function () {
    $('#data').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        ajax: {
            url: window.location.pathname,
            type: 'POST',
            data: {
                'action': 'searchdata'
            },
            dataSrc: ""
        },
        columns: [
            {"data": "id"},
            {"data": "estado"},
            {"data": "fecha_termino"},
            {"data": "activo"},
            {"data": "id"},
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
                  return '<span class="badge badge-danger"> No </span> ';
                }
                    return data;
                },
            },
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var buttons = '<a href="/erp/infcontrato/invoice/pdf/'+row.id+'/" target="_blank" class="btn btn-info btn-xs btn-flat"><i class="fas fa-file-pdf"></i></a> ';
                    return buttons;
                }
            },
        ],
        initComplete: function (settings, json) {

        }
    });
});
