const carga = () => {
    $.ajax({
      url: window.location.pathname,
      type: "POST",
      data: {
          'action': "actualizar",
      },
      headers: {
          'X-CSRFToken': csrftoken
      },
      dataType: "json",
    }).done(function (data) {
        if (!data.hasOwnProperty("error")) {
            // console.log(data)
              var html = ''  ;
              for (i of data) {            
                  if (i.estacionamiento.estado_estacionamiento === "ocupado" && i.estado_reserva === "entrada" ) {
                      html+= '  <div class="col-lg-2">'              
                      html+= '<div class="small-box bg-secondary">'              
      
                      html+= ' <div class="inner">'
                      html+= `<h3><sup style="font-size: 20px" class="mr-5 text-dark">${i.patente.toUpperCase()}</sup> ${i.estacionamiento.numero_estacionamiento}</h3>` 
                      html+= `<p>Categoria: ${i.estacionamiento.tipo_estacionamiento} </p>` 
                      html+= ' </div>'
      
                      html+= ' <div class="icon">'
                      html+= ' <i class="fas fa-car-side"></i>'
                      html+= ' </div>'
      
                      html+= `<a href="#" class="small-box-footer btnAddPago" rel="${i.id}" >`
                      html+= 'PAGAR'
                      // html+= i.estacionamiento.estado_estacionamiento.toUpperCase()
                      html+= ' <i class="fas fa-caret-square-right"></i> '
                      html+= '</a>'
                  
      
                      html+= ' </div>'              
                      html+= ' </div>'   
                    }   
              }
                    // // $('#estacionamientos_test').html('')
              $('#salida_test').html(html)
              inicio()
              return false;
        }
        message_error(data.error);
      });
  }
  
  window.onload = carga
  
  
  const inicio = ()=> {


        /* ############### BUSCAr RESERVA ################*/
        const searchBooking = (test)=> {
          $.ajax({
           url: window.location.pathname,
           type: "POST",
           data: {
               'action': "actualizar",
           },
           headers: {
               'X-CSRFToken': csrftoken
           },
           dataType: "json",
          }).done((data)=>{
            test(data)
          //   console.log(data)
            return false
          })
        };
      


      /* ############### EVENT CLICK SELECT PAGO ################*/
      const btnAddPago = Array.from(document.querySelectorAll('.btnAddPago'));
      if (btnAddPago) {
          btnAddPago.forEach(res => { 
              res.addEventListener('click', e => { 
                  let value = e.currentTarget.getAttribute('rel') 
                  $("select[name='reserva']").val(value);
                  searchBooking((response)=>{
                    console.log(response)
                    //   if (response.find(p => p.id === Number(value)) === undefined){
                    //     console.log('se ah pagado')
                    // }else{
                    //     console.log('aun no se paga')
                    // }
                    if(response.find(p => p.id === Number(value)) !== undefined){
                      $.ajax({
                        url: window.location.pathname,
                        type: "POST",
                        data: {
                          action: "create_pago",
                          id: value
                        },
                        dataType: "json",
                        headers: {
                          "X-CSRFToken": csrftoken,
                        },
                      }).done(function (data) {
                        if (!data.hasOwnProperty("error")) {
                          // console.log(data)
                          $("input[name='fecha_entrada']").val(data.fecha_entrada);
                          $("input[name='fecha_salida']").val(data.fecha_salida);
                          $("input[name='hora_entrada']").val(moment(data.hora_entrada, 'HH:mm a').format('HH:mm'));
                          $("input[name='hora_salida']").val(moment(data.hora_salida, 'HH:mm a').format('HH:mm'));
                          tero = `${data.fecha_entrada} ${moment(data.hora_entrada, 'HH:mm a').format('HH:mm')}`
                          tero2 = `${data.fecha_salida} ${moment(data.hora_salida, 'HH:mm a').format('HH:mm')}`
                          let entrada = moment(tero)
                          let salida = moment(tero2)
                          // console.log(moment.duration(entrada - salida).asMinutes())
                          let diferencia = moment.duration(salida.diff(entrada)).asMinutes()

                          if( diferencia <= 30){
                            $("input[name='total']").val(500);
                          }else{
                            $("input[name='total']").val((data.tarifa.precio * (diferencia-30)) + 500);
                          }
                          document.getElementById('tarifa_valor').innerHTML = `$${data.tarifa.precio} pesos`


                          if(diferencia >= 60){
                            let tiempoHoras = Math.floor(diferencia/60)
                            let tiempoMinutos = Math.floor(diferencia%60)
                            if (tiempoHoras >1){
                              if(tiempoMinutos >1){
                                document.getElementById('tiempo_valor').innerHTML = `${tiempoHoras} Horas y ${tiempoMinutos} Minutos` 
                              }else{
                                document.getElementById('tiempo_valor').innerHTML = `${tiempoHoras} Horas y ${tiempoMinutos} Minuto` 
                              }
                            }else{
                              if(tiempoMinutos >1){
                                document.getElementById('tiempo_valor').innerHTML = `${tiempoHoras} Hora y ${tiempoMinutos} Minutos` 
                              }else{
                                document.getElementById('tiempo_valor').innerHTML = `${tiempoHoras} Hora y ${tiempoMinutos} Minuto` 
                              }
                            }
                          }else if(diferencia == 1){
                            document.getElementById('tiempo_valor').innerHTML = `${diferencia} minuto` 
                          }else{
                            document.getElementById('tiempo_valor').innerHTML = `${diferencia} minutos` 
                          }

                          document.getElementById('patente_valor').innerHTML = data.patente
                          $("#myModalSalida").modal("show"); // usamos la funcion modal y el evento "show" para mostrar
                          formulario()
                          return false;
                        }
                        message_error(data.error);
                      });
                    }else{
                      Swal.fire({
                        icon: 'error',
                        title: 'Oops...',
                        text: 'Este reserva ha terminado!',
                        timer: 2000,
                        onClose: () => {
                            location.reload()
                        }
                      })
                    }
                  })

              })
          });
  
      }
  
    
      /* ############### EVENT TRIGGER MODAL HIDE RESERVA ################*/
      $("#myModalSalida").off("hidden.bs.modal")
      $("#myModalSalida").on("hidden.bs.modal", function (event) {
          $('#frmSalida').trigger('reset') // ejecutamos llamamos al metodo trigger y ejecutamos el evento reset, para limpiar el formulario
      });
    
  
  }
  
  

  const formulario = ()=>{
      /* ############### SUBMIT PAGO ################*/
      $("#frmSalida").off("submit")
      $("#frmSalida").on("submit", function (e) {
          e.preventDefault();
          var parameters = new FormData(this); // con el "this" llenamos el FormData a partir del fomulario al que apunto, lo cual crea una array de elementos
          parameters.append("action", "guardar_pago"); // creamos una acción para que llegue a mi vista
          // console.log(parameters)
          submit_with_ajax(
              window.location.pathname,
              "Notificación",
              "¿Estas seguro de hacer  el pago?",
              parameters,
              function (response) {
                  // console.log(response)
                  $("#myModalSalida").modal("hide"); // para que el modal se oculte
                  window.open('/erp/reserva/invoice_salida/pdf/' + response.id + '/', '_blank');
                  Swal.fire({
                    title: "Alerta!",
                    text: "Pago registrado correctamente",
                    icon: "success",
                    timer: 2000,
                    onClose: () => {
                        carga();
                    }
                })
                  // $("#calendar").fullCalendar('refetchEvents')
              }
          );
      });
    
 /* ############### ANULAR SALIDA ################*/
      const frmSalida = document.querySelector('#frmSalida')
      $(".btnAnularSalida").off("click")
      $(".btnAnularSalida").on("click", function (e){
        let parameters2 = new FormData(frmSalida)
        parameters2.append('action','anular_salida')
        parameters2.set('numero_boleta', 0)
        console.log(parameters2.get('obs'))
        if (parameters2.get('obs') !== '' ) {
          alert_action('Notificación', "¿Estas seguro de anular el pago?", ()=> {
            $.ajax({
              url: window.location.pathname,
              type: "POST",
              data: parameters2,
              dataType: "json",
              processData: false,
              contentType: false,
              headers: {
                "X-CSRFToken": csrftoken,
              },
            }).done(()=>{
              $("#myModalSalida").modal("hide"); // para que el modal se oculte
              Swal.fire({
                title: "Alerta!",
                text: "Pago anulado correctamente",
                icon: "success",
                timer: 2000,
                onClose: () => {
                    carga();
                }
            })
            })
          
          });

        }else{
          Swal.fire({
            icon: 'error',
            title: 'Oops...',
            text: 'Observación debe ser incluida!',
            timer: 2000,
          })
        }

      })
      
      // const btnAnularSalida = document.querySelector('.btnAnularSalida');
      // const frmSalida = document.querySelector('#frmSalida')
      // btnAnularSalida.addEventListener('click', function (e){
      //   let parameters2 = new FormData(frmSalida)
      //   parameters2.append('action','anular_salida')
      //   parameters2.set('numero_boleta', 0)
      //   alert_action('Notificación', "¿Estas seguro de anular el pago?", ()=> {
      //     $.ajax({
      //       url: window.location.pathname,
      //       type: "POST",
      //       data: parameters2,
      //       dataType: "json",
      //       processData: false,
      //       contentType: false,
      //       headers: {
      //         "X-CSRFToken": csrftoken,
      //       },
      //     })
      //     $("#myModalSalida").modal("hide"); // para que el modal se oculte
      //   })
      // })
  
  }
  
  
  
  