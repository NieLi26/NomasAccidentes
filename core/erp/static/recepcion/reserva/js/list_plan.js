
const getData = () =>{
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
      { "data": "patente" },
      { "data": "estacionamiento.numero_estacionamiento" },
      { "data": "tarifa_plan.nombre" },
      { "data": "fecha_inicio" },
      { "data": "fecha_termino" },
      { "data": "total" },
      { "data": "estado_plan" },
      { "data": "id" }
    ],
    columnDefs: [
      {
        targets: [1],
        class: "text-center",
        orderable: false,
        render: function (data, type, row) {
          return data.toUpperCase();
        },
      },
      {
        targets: [2],
        class: "text-center",
        orderable: false,
        render: function (data, type, row) {
          return data;
        },
      },
      {
        targets: [-3],
        class: "text-center",
        orderable: false,
        render: function (data, type, row) {
          let valor = new Intl.NumberFormat('es-CL').format(data)
          return "$" + valor;
        },
      },
      {
        targets: [-2],
        class: "text-center",
        orderable: false,
        render: function (data, type, row) {
          if (data == "iniciado") {
            return '<span class="badge badge-primary">' + data.toUpperCase() + '</span> ';
          } else if (data == "terminado") {
            return '<span class="badge badge-success">' + data.toUpperCase() + '</span> ';
          }

        },
      },
      {
        targets: [-1],
        class: "text-center",
        orderable: false,
        render: function (data, type, row) {
          if(row.estado_plan === 'iniciado'){
            let buttons = '<a rel="details" class="btn btn-warning btn-xs btn-flat"><i class="fas fa-search"></i></a> ';
            buttons += '<a href="/erp/plan/invoice_iniciado/pdf/'+row.id+'/" target="_blank" class="btn btn-dark btn-xs btn-flat"><i class="fas fa-print"></i></a> ';
            buttons += '<a href="/erp/plan/invoice_terminado/pdf/'+row.id+'/" target="_blank" class="btn btn-primary btn-xs btn-flat"><i class="fas fa-print"></i></a> ';
            return buttons;
          }else{
            let buttons = '<a rel="details" class="btn btn-success btn-xs btn-flat"><i class="fas fa-search"></i></a> ';
            buttons += '<a href="/erp/plan/invoice_iniciado/pdf/'+row.id+'/" target="_blank" class="btn btn-dark btn-xs btn-flat"><i class="fas fa-print"></i></a> ';
            buttons += '<a href="/erp/plan/invoice_terminado/pdf/'+row.id+'/" target="_blank" class="btn btn-primary btn-xs btn-flat"><i class="fas fa-print"></i></a> ';
            return buttons;
          }
        },
      },

    ],
    initComplete: function (settings, json) { },
    // se ejecuta al haber cargado la tabla



  });

}

  //MODAL
$(function () {
  modal_title = $(".modal-title");

  getData();

  $("#data tbody").on("click", 'a[rel="details"]', function () {
    modal_title.find("span").html("Información de Cliente");
    modal_title.find("i").removeClass().addClass("fas fa-search");
    var tr = tblReserva.cell($(this).closest("td, li")).index();
    var data = tblReserva.row(tr.row).data();
    console.log(data)
    if (data.estado_plan === 'terminado' ){
      $('.btnTerminarPlan').attr('style', 'display:none')
    }
    $('#id_nombre').val(data.cliente.nombre);
    $('#id_apellido').val(data.cliente.apellido);
    $('#id_rut').val(data.cliente.rut);
    $('#id_razon_social').val(data.cliente.razon_social);
    $('#id_direccion').val(data.cliente.direccion);
    $('#id_telefono').val(data.cliente.telefono);
    $('#id_mail').val(data.cliente.mail);
    // $('#id_patente').val(data.patente);
    // $('#id_patente').val(data.patente);
    $("#myModalPlan").modal("show");

    $('.btnTerminarPlan').off('click')
    $('.btnTerminarPlan').on('click', function (e){
      console.log(data.id)
      alert_action('Notificación', "¿Estas seguro de terminar el plan?", ()=> {
        $.ajax({
          url: window.location.pathname,
          type: "POST",
          data: {
            action: 'terminar_plan',
            id: data.id
          },
          dataType: "json",
          headers: {
            "X-CSRFToken": csrftoken,
          },
        }).done(()=>{
          $("#myModalPlan").modal("hide"); // para que el modal se oculte
          Swal.fire({
            title: "Alerta!",
            text: "plan terminado correctamente",
            icon: "success",
            timer: 2000,
        })
          // $('#data').dataTable().fnDestroy();
          // location.reload()
        })
      })
    })

  });

  $("#myModalPlan").on("hidden.bs.modal", function (event) {
    tblReserva.ajax.reload(null, false)
    $('.btnTerminarPlan').attr('style', '')
});


});


