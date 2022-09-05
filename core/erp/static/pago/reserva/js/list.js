var tblPago;
var modal_title;

const getData = () =>{
  
  tblPago =   $("#data").DataTable({
    // responsive: true,
    scrollX: true,
    autoWidth: false,
    destroy: true,
    deferRender: true,
    ajax: {
      url: window.location.pathname,
      type: "POST",
      data: {
        "action": "searchdata",
      }, // parametros
      dataSrc: "",
      headers: {
        'X-CSRFToken': csrftoken
      }
    },
    columns: [
      { "data": "id" },
      { "data": "reserva.patente" },
      { "data": "numero_boleta" },
      { "data": "fecha_entrada" },
      { "data": "hora_entrada" },
      { "data": "fecha_salida" },
      { "data": "hora_salida" },
      { "data": "total" },
      { "data": "estado_pago" },
      { "data": "id" }
    ],
    columnDefs: [
      // {
      //   targets: [1,2,3,4,5,6, 7],
      //   class: "text-center",
      //   orderable: false,
      //   render: function (data, type, row) {
      //     return data;
      //   },
      // },
      {
        targets: [-3],
        class: "text-center",
        orderable: false,
        render: function (data, type, row) {
          let valor = new Intl.NumberFormat('es-CL', { style: 'currency', currency: 'CLP' }).format(data)
          return valor;
        },
      },
      {
        targets: [-2],
        class: "text-center",
        orderable: false,
        render: function (data, type, row) {
          if (data == "anulado") {
            return '<span class="badge badge-warning">' + data.toUpperCase() + '</span> ';
          } else if (data == "cancelado") {
            return '<span class="badge badge-success">' + data.toUpperCase() + '</span> ';
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
          if (row.obs !== ''){
            if(row.estado_pago === 'anulado'){
              let buttons = '<a rel="details" class="btn btn-warning btn-xs btn-flat"><i class="fas fa-search"></i></a> ';
              buttons += '<a href="/erp/reserva/invoice_salida/pdf/' +row.id+'/" target="_blank" class="btn btn-dark btn-xs btn-flat"><i class="fas fa-print"></i></a> ';
              return buttons;
            }else{
              let buttons = '<a rel="details" class="btn btn-success btn-xs btn-flat"><i class="fas fa-search"></i></a> ';
              buttons += '<a href="/erp/reserva/invoice_salida/pdf/' +row.id+'/" target="_blank" class="btn btn-dark btn-xs btn-flat"><i class="fas fa-print"></i></a> ';
              return buttons;
            }
          }else{
            let buttons = '<a class="btn btn-danger btn-xs btn-flat"><i class="fas fa-search"></i></a> ';
            buttons += '<a href="/erp/reserva/invoice_salida/pdf/' +row.id+'/" target="_blank" class="btn btn-dark btn-xs btn-flat"><i class="fas fa-print"></i></a> ';
            return buttons;
          }


        },
      },
    ],
    initComplete: function (settings, json) { },
    // se ejecuta al haber cargado la tabla
  });
}

$(function () {
  modal_title = $(".modal-title");

  getData();

  $("#data tbody").on("click", 'a[rel="details"]', function () {
    modal_title.find("span").html("Observación de Pago");
    modal_title.find("i").removeClass().addClass("fas fa-search");
    var tr = tblPago.cell($(this).closest("td, li")).index();
    var data = tblPago.row(tr.row).data();
    console.log(data.estado_pago)
    if (data.estado_pago !== 'anulado' ){
      console.log('golaaa')
      $('.btnRevisarPago').attr('style', 'display:none')
    }
    $('#obs_pago').html(data.obs);
    $("#myModalPago").modal("show");

    $('.btnRevisarPago').off('click')
    $('.btnRevisarPago').on('click', function (e){
      console.log(data.id)
      alert_action('Notificación', "¿Estas seguro de realizar esta acción?", ()=> {
        $.ajax({
          url: window.location.pathname,
          type: "POST",
          data: {
            action: 'revisar_pago',
            id: data.id
          },
          dataType: "json",
          headers: {
            "X-CSRFToken": csrftoken,
          },
        }).done(()=>{
          $("#myModalPago").modal("hide"); // para que el modal se oculte
          Swal.fire({
            title: "Alerta!",
            text: "Revisión realizada correctamente",
            icon: "success",
            timer: 2000,
        })
          // $('#data').dataTable().fnDestroy();
          // location.reload()
        })
      })
    })

  });

  $("#myModalPago").on("hidden.bs.modal", function (event) {
    tblPago.ajax.reload(null, false)
    $('.btnRevisarPago').attr('style', '')
});


});


