$(function () {
  $('.select2').select2({
    theme: "bootstrap4",
    language: 'es'
  });
    /* ############### EVENTO CALENDARIO ################*/
    $("#fecha_inicio, #fecha_termino").datetimepicker({
      format: "YYYY-MM-DD",
      // date: moment().format("YYYY-MM-DD"),
      locale: "es",
      minDate: moment().format("YYYY-MM-DD"),
    });
  
    const input_fecha_inicio = $("#fecha_inicio")
    input_fecha_inicio.datetimepicker("date", input_fecha_inicio.val());
  
    const input_fecha_termino = $("#fecha_termino")
    input_fecha_termino.datetimepicker("date", input_fecha_termino.val());
  
    $("#fecha_inicio").on("change.datetimepicker", (e) => {
      element = e.target // target es para indicar especificamente la etiqueta donde hago alución
      $("#fecha_termino").datetimepicker('minDate', element.value); // matener fecha minima respecto a la de inicio
      calcularTotal();
    })
  
    $("#fecha_termino").on("change.datetimepicker", (e) => {
      calcularTotal();
    })
  
    $("select[name='tarifa_plan']").on('change', function(){
      $("#fecha_inicio, #fecha_termino").val(moment().format('YYYY-MM-DD'))
      $("input[name='total']").val(0)
    })
    
    const calcularTotal = ()=>{
      let tarifa = $("select[name='tarifa_plan']").val()
      $.ajax({
        url: window.location.pathname,
        type: "POST",
        data: {
          action: "calcular_total",
          id: tarifa
        },
        dataType: "json",
        headers: {
          'X-CSRFToken': csrftoken
        }
      }).done(function (data) {
        if (!data.hasOwnProperty("error")) {
          console.log(data)
          const {precio, nombre} = data     // console.log(total)
          let entrada = moment($('#fecha_inicio').val())
          let salida = moment($('#fecha_termino').val())
          let diferencia = salida.diff(entrada, 'days')

          // 5 meses
          if (nombre === 'Mensual'){
            if (diferencia <= 30) {
              $("input[name='total']").val(precio)
            } else if(diferencia <= 60) {
              $("input[name='total']").val(precio * 2)
            }else if(diferencia <= 90) {
              $("input[name='total']").val(precio * 3)
            }else if(diferencia <= 120) {
              $("input[name='total']").val(precio * 4)
            }else if(diferencia <= 150) {
              $("input[name='total']").val(precio * 5)
            }else{
              $("input[name='total']").val(0)
            }
          }
          
          // 3 semanas
          if (nombre === 'Semanal'){
            if (diferencia <= 7) {
              $("input[name='total']").val(precio)
            } else if(diferencia <= 14) {
              $("input[name='total']").val(precio * 2)
            }else if(diferencia <= 21) {
              $("input[name='total']").val(precio * 3)
            }else{
              $("input[name='total']").val(0)
            }
          }
        
          return false;
        }
        message_error(data.error);
      });


    }
 
    /* ############### SEARCH CLIENTE ################*/
  
    $('select[name="cliente"]').select2({
      theme: "bootstrap4",
      language: "es",
      allowClear: true,
      ajax: {
        delay: 250,
        type: "POST",
        url: window.location.pathname,
        headers: {
          'X-CSRFToken': csrftoken
        },
        data: function (params) {
          var queryParameters = {
            term: params.term,
            action: "search_cliente",
          };
          return queryParameters;
        },
        processResults: function (data) {
          return {
            results: data,
          };
        },
      },
      placeholder: "Ingrese una descripción",
      minimumInputLength: 1,
    });
  
    /* ############### EVENT CLICK ADD GUEST ################*/
  
    $(".btnAddCliente").on("click", function () {
      $("#myModalCliente").modal("show"); // usamos la funcion modal y el evento "show" para mostrar
    });
  
    /* ############### EVENT TRIGGER MODAL HIDE ################*/
  
    $("#myModalCliente").on("hidden.bs.modal", function (event) {
      $('#frmCliente').trigger('reset') // ejecutamos llamamos al metodo trigger y ejecutamos el evento reset, para limpiar el formulario
    });
  

        /* ############### CHECK RUT ################*/
        // const rut = document.querySelector('#id_rut')
        // const mensajeRut = document.querySelector('#mensaje_rut')
        //   if(rut) {
        //     rut.addEventListener('keyup', e =>{
        //           let valor = e.currentTarget.value
        //           rut.value =  e.currentTarget.value.toLowerCase()
        //           console.log(valor)
        //           // Aqui esta el patron(expresion regular) a buscar en el input
        //           let patronRutChile =  /^[0-9]{8}-[A-Za-z0-9]$/;
        //           let patronDNIArgentina =  /^[0-9]{8}$/;
  
        //           patronRutChile.test(valor) ||  patronDNIArgentina.test(valor) || valor === '' ?  mensajeRut.innerHTML = ''  : mensajeRut.innerHTML = "<p class='text-danger' > Rut incorrecto, el formato debe ser(sin puntos): </p><b class='text-dark' > 99.999.999-9</b> , <b class='text-dark' >99.999.999</b>"  
                  
        //       })
        //   }

    /* ############### SUBMIT CLIENTE ################*/
  
    $("#frmCliente").on("submit", function (e) {
      e.preventDefault();
      var parameters = new FormData(this); // con el "this" llenamos el FormData a partir del fomulario al que apunto, lo cual crea una array de elementos
      parameters.append("action", "create_cliente"); // creamos una acción para que llegue a mi vista
      // let valor_rut = parameters.get('rut')
      // let patronRutChile =  /^[0-9]{8}-[A-Za-z0-9]$/;
      // let patronDNIArgentina =  /^[0-9]{8}$/;
      // if (patronRutChile.test(valor_rut) | patronDNIArgentina.test(valor_rut)){
      submit_with_ajax(
        window.location.pathname,
        "Notificación",
        "¿Estas seguro de crear al siguiente cliente?",
        parameters,
        function (response) {
          console.log(response)
          // para cargar en el select al huesped recien creado, llega la data de response(callback) y puedo llamar a la key full_name del metodo toJSON(model to dict)
          var newOption = new Option(response.get_full_name, response.id, false, true);
          $("select[name='cliente']").append(newOption).trigger("change");
          Swal.fire({
            title: "Alerta!",
            text: "Cliente creado correctamente",
            icon: "success",
            timer: 2000,
            onClose: () => {
              $("#myModalCliente").modal("hide"); // para que el modal se oculte
            }
        })
        
        }
      );
      // }else{
      //   Swal.fire({
      //       icon: 'error',
      //       title: 'Oops...',
      //       text: 'Formato de Rut Erroneo!',
      //       timer: 2000,
      //     })
      // }

    });
  


        // /* ############### CHECK PATENTE ################*/
        const patente = document.querySelector('#id_patente')
        // const mensajePatente = document.querySelector('#mensaje_patente')
          if(patente) {
              patente.addEventListener('keyup', e =>{
                  // let valor = e.currentTarget.value
                  patente.value =  e.currentTarget.value.toUpperCase()
                  // console.log(valor)
                  // Aqui esta el patron(expresion regular) a buscar en el input
                  // let patronPlacaChile =  /[A-Za-z]{2}-[A-Za-z]{2}-[0-9]{2}$/;
                  // let patronPlacaArgentina =  /[A-Za-z]{2}-[0-9]{3}-[A-Za-z]{2}$/;
  
                  // patronPlacaChile.test(valor) ||  patronPlacaArgentina.test(valor) || valor === '' ?  mensajePatente.innerHTML = ''  : mensajePatente.innerHTML = "<p class='text-danger' > Patente incorrecta, el formato debe ser: </p><b class='text-dark' > XX-XX-00</b> , <b class='text-dark' >XX-000-XX</b>"  
                  
              })
          }

         /* ############### SUBMIT PLAN ################*/
      // $("#frmReserva").off("submit")
      $("#frmReserva").on("submit", function (e) {
          e.preventDefault();
          var parameters = new FormData(this); // con el "this" llenamos el FormData a partir del fomulario al que apunto, lo cual crea una array de elementos
          // console.log(parameters.get('patente'))
          // let valor_patente = parameters.get('patente')
          // let patronPlacaChile =  /[A-Za-z]{2}-[A-Za-z]{2}-[0-9]{2}$/;
          // let patronPlacaArgentina =  /[A-Za-z]{2}-[0-9]{3}-[A-Za-z]{2}$/;
          // if (patronPlacaChile.test(valor_patente) | patronPlacaArgentina.test(valor_patente)){
              submit_with_ajax(
                  window.location.pathname,
                  "Notificación",
                  "¿Estas seguro de crear la siguiente reserva?",
                  parameters,
                  function (response) {
                    console.log(response)
                    window.open('/erp/plan/invoice_iniciado/pdf/' + response.id + '/', '_blank');
                      Swal.fire({
                          title: "Alerta!",
                          text: "Reserva creada correctamente",
                          icon: "success",
                          timer: 2000,
                          onClose: () => {
                            console.log(response)
                              location.href = '/erp/plan/reserva/list/'
                          }
                      })
                  }
                  
              );
          // }else{
          //     Swal.fire({
          //         icon: 'error',
          //         title: 'Oops...',
          //         text: 'Formato de Patente Erroneo!',
          //         timer: 2000,
          //       })
          // }
        
      });



  });

