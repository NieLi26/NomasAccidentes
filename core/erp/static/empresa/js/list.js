var modal_title;
var tblClient;

function getData() {
    tblClient= $('#data').DataTable({
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
            {"data": "name"},
            {"data": "rubro"},
            {"data": "rut"},
            {"data": "address"},
            {"data": "cell"},
            {"data": "id"},
        ],
        columnDefs: [
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var buttons = '<a href="/erp/empresa/update/' + row.id + '/" class="btn btn-warning btn-xs btn-flat"><i class="fas fa-edit"></i></a> ';
                    // buttons += '<a href="/erp/empresa/invoice/pdf/' +row.id+'/" target="_blank" class="btn btn-info btn-xs btn-flat"><i class="fas fa-file-pdf"></i></a> ';
                    buttons += '<a href="/erp/empresa/delete/' + row.id + '/" type="button" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash-alt"></i></a> ';
                    buttons += '<a href="/erp/empresa/dashboard/' +row.id+'/" target="_blank" class="btn btn-info btn-xs btn-flat"><i class="fas fa-chart-pie"></i></a> ';
                    buttons += '<a href="/erp/empresa/factura/' +row.id+'/" target="_blank" class="btn btn-dark btn-xs btn-flat"><i class="fas fa-file-invoice"></i></a> ';
                    // buttons += '<a href="/erp/empresa/grafico/invoice/pdf/' +row.id+'/" target="_blank" class="btn btn-info btn-xs btn-flat"><i class="fas fa-file-pdf"></i></a> ';
                    buttons += '<a href="#" rel="edit" type="button" class="btn btn-success btn-xs btn-flat"><i class="fas fa-search"></i></a>';
                    return buttons;
                }
            },
        ],
        initComplete: function (settings, json) {

        }
    });
};

$(function () {

    modal_title = $('.modal-title');

    getData();


    $('#data tbody').on('click', 'a[rel="edit"]', function () {
        modal_title.find("span").html("Detalles de Pago");
        modal_title.find("i").removeClass().addClass("fas fa-search");
        var tr = tblClient.cell($(this).closest('td, li')).index();
        var data = tblClient.row(tr.row).data();
            
        $('#tblDet').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        ajax: {
            url: window.location.pathname,
            type: 'POST',
            data: {
                'action': 'searchdata_details',
                'id': data.id
            },
            dataSrc: ""
        },
        columns: [
            {"data": "id"},
            {"data": "fecha_expiracion"},
            {"data": "asunto"},
            {"data": "valor"},
            {"data": "cumplido"},
        ],
        columnDefs: [
             {
                "targets": [-1],
                "render": function ( data, type, row, meta ) {
                if (data == true) {
                    return '<span class="badge badge-success"> Realizado </span> ';
                    }
                else if (data == false) {
                  return '<span class="badge badge-danger"> Pendiente </span> ';
                }
                    return data;
                },
            },
        ],
        initComplete: function (settings, json) {

        }
        });

        $('#myModalPago').modal('show');
    });



    $('#myModalPago').on('shown.bs.modal', function () {
        // $('form')[0].reset();
    });

});