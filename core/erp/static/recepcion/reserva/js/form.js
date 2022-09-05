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
            var html = ''  ;
            var htmlDisponible = ''  ;
            var htmlOcupado = ''  ;
            var htmlReservado = ''  ;
            for (i of data['estacionamiento']) {     
                if (i.estado_estacionamiento == "disponible" ) {
                    html+= '  <div class="col-lg-2">'              
                    html+= '<div class="small-box bg-success">'              
    
                    html+= ' <div class="inner">'
                    html+= `<h3><sup style="font-size: 15px">Estacionamiento</sup> ${i.numero_estacionamiento}</h3>` 
                    html+= `<p>Categoria: ${i.tipo_estacionamiento} </p>` 
                    html+= ' </div>'
    
                    html+= ' <div class="icon">'
                    html+= ' <i class="fas fa-car-side"></i>'
                    html+= ' </div>'
    
                    html+= `<a href="#" class="small-box-footer btnAddReservaDiaria" rel="${i.id}" >`
                    html+= i.estado_estacionamiento.toUpperCase()
                    html+= ' <i class="fas fa-caret-square-right"></i> '
                    html+= '</a>'
                
    
                    html+= ' </div>'              
                    html+= ' </div>'   

                    /*   DISPONIBLE  */   
                    htmlDisponible+= '  <div class="col-lg-2">'              
                    htmlDisponible+= '<div class="small-box bg-success">'              
        
                    htmlDisponible+= ' <div class="inner">'
                    htmlDisponible+= `<h3><sup style="font-size: 15px">Estacionamiento</sup> ${i.numero_estacionamiento}</h3>` 
                    htmlDisponible+= `<p>Categoria: ${i.tipo_estacionamiento} </p>` 
                    htmlDisponible+= ' </div>'
        
                    htmlDisponible+= ' <div class="icon">'
                    htmlDisponible+= ' <i class="fas fa-car-side"></i>'
                    htmlDisponible+= ' </div>'
        
                    htmlDisponible+= `<a href="#" class="small-box-footer btnAddReservaDiaria" rel="${i.id}" >`
                    htmlDisponible+= i.estado_estacionamiento.toUpperCase()
                    htmlDisponible+= ' <i class="fas fa-caret-square-right"></i> '
                    htmlDisponible+= '</a>'
                
        
                    htmlDisponible+= ' </div>'              
                    htmlDisponible+= ' </div>'      

                } else if (i.estado_estacionamiento == "ocupado" )   {
                    html+= '  <div class="col-lg-2">'              
                    html+= '<div class="small-box bg-danger">'              
    
                    html+= ' <div class="inner">'

                    for (p of data['reserva']){
                        if (p.estacionamiento.id === i.id){
                            html+= `<h3><sup style="font-size: 20px" class="mr-5 text-dark">${p.patente.toUpperCase()}</sup> ${i.numero_estacionamiento}</h3>` 
                        }         
                    }

                    html+= `<p>Categoria: ${i.tipo_estacionamiento} </p>` 
                    html+= ' </div>'
    
                    html+= ' <div class="icon">'
                    html+= ' <i class="fas fa-car-side"></i>'
                    html+= ' </div>'
    
                    html+= `<a href="#" class="small-box-footer" rel="${i.id}" >`
                    html+= i.estado_estacionamiento.toUpperCase()
                    html+= ' <i class="fas fa-caret-square-right"></i> '
                    html+= '</a>'
                
    
                    html+= ' </div>'              
                    html+= ' </div>'   
                    
                    /* OCUPADO */
                    htmlOcupado+= '  <div class="col-lg-2">'              
                    htmlOcupado+= '<div class="small-box bg-danger">'              
    
                    htmlOcupado+= ' <div class="inner">'

                    for (p of data['reserva']){
                        if (p.estacionamiento.id === i.id){
                            htmlOcupado+= `<h3><sup style="font-size: 20px" class="mr-5 text-dark">${p.patente.toUpperCase()}</sup> ${i.numero_estacionamiento}</h3>` 
                        }             
                    }
      
                    htmlOcupado+= `<p>Categoria: ${i.tipo_estacionamiento} </p>` 
                    htmlOcupado+= ' </div>'
    
                    htmlOcupado+= ' <div class="icon">'
                    htmlOcupado+= ' <i class="fas fa-car-side"></i>'
                    htmlOcupado+= ' </div>'
    
                    htmlOcupado+= `<a href="#" class="small-box-footer" rel="${i.id}" >`
                    htmlOcupado+= i.estado_estacionamiento.toUpperCase()
                    htmlOcupado+= ' <i class="fas fa-caret-square-right"></i> '
                    htmlOcupado+= '</a>'
                
                    htmlOcupado+= ' </div>'              
                    htmlOcupado+= ' </div>' 

                }else if (i.estado_estacionamiento == "reservado" )   {

                    html+= '  <div class="col-lg-2">'              
                    html+= '<div class="small-box bg-orange">'              
    
                    html+= ' <div class="inner">'
                    for (p of data['plan']){
                        if (p.estacionamiento.id === i.id){
                            html+= `<h3><sup style="font-size: 20px" class="mr-5 text-white">${p.patente.toUpperCase()}</sup> ${i.numero_estacionamiento}</h3>` 
                        }             
                    }
                    html+= `<p>Categoria: ${i.tipo_estacionamiento} </p>` 
                    html+= ' </div>'
    
                    html+= ' <div class="icon">'
                    html+= ' <i class="fas fa-car-side"></i>'
                    html+= ' </div>'
    
                    html+= `<a href="#" class="small-box-footer btnFreePlan" rel="${i.id}" >`
                    html+= i.estado_estacionamiento.toUpperCase()
                    html+= ' <i class="fas fa-caret-square-right"></i> '
                    html+= '</a>'
                
    
                    html+= ' </div>'              
                    html+= ' </div>'    

                    /* RESERVADO */
                    htmlReservado+= '  <div class="col-lg-2">'              
                    htmlReservado+= '<div class="small-box bg-orange">'              
    
                    htmlReservado+= ' <div class="inner">'
                    for (p of data['plan']){
                        if (p.estacionamiento.id === i.id){
                            htmlReservado+= `<h3><sup style="font-size: 20px" class="mr-5 text-white">${p.patente.toUpperCase()}</sup> ${i.numero_estacionamiento}</h3>` 
                        }             
                    }
                    htmlReservado+= `<p>Categoria: ${i.tipo_estacionamiento} </p>` 
                    htmlReservado+= ' </div>'
    
                    htmlReservado+= ' <div class="icon">'
                    htmlReservado+= ' <i class="fas fa-car-side"></i>'
                    htmlReservado+= ' </div>'
    
                    htmlReservado+= `<a href="#" class="small-box-footer btnFreePlan" rel="${i.id}" >`
                    htmlReservado+= i.estado_estacionamiento.toUpperCase()
                    htmlReservado+= ' <i class="fas fa-caret-square-right"></i> '
                    htmlReservado+= '</a>'
                
    
                    htmlReservado+= ' </div>'              
                    htmlReservado+= ' </div>'   
                }
            }
            $('#estacionamientos_all').html(html)
            $('#estacionamientos_disponible').html(htmlDisponible)
            $('#estacionamientos_ocupado').html(htmlOcupado)
            $('#estacionamientos_reservado').html(htmlReservado)

        inicio()
        return false;
      }
      message_error(data.error);
    });
}

window.onload = carga


const inicio = ()=> {
        /* ############### BUSCAr PLAN RESERVA ################*/
        const searchReservaPlan = (value, test)=> {
            $.ajax({
             url: window.location.pathname,
             type: "POST",
             data: {
                 'action': "search_reserva_plan",
                 'id': value
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
     
     /* ############### EVENT CLICK LIBERAR ESTACIONAMIENTO RESERVADO ################*/
     const btnFreePlan = Array.from(document.querySelectorAll('.btnFreePlan'));
     // console.log(btnFree)
     if (btnFreePlan) {
        btnFreePlan.forEach(res => { 
             res.addEventListener('click', e => { 
                 let value = e.currentTarget.getAttribute('rel') ;
                //  console.log(value)
                 searchReservaPlan(value, (response)=>{
                     var resReserva = response.fecha_termino
                    //  console.log(resReserva)
                     if ( resReserva === moment().format('YYYY-MM-DD')) {
                         alert_action('Notificación', '¿Estas seguro dejar disponible este estacionamiento?', function () {
       
                             //metodo 1
                             $.ajax({
                                 url: window.location.pathname,
                                 type: "POST",
                                 data: {
                                     'action': "estacionamiento_libre",
                                     'id': value
                                 },
                                 headers: {
                                     'X-CSRFToken': csrftoken
                                 },
                                 dataType: "json",
                                 // processData: false, //no las usa pq no envia archivos
                                 // contentType: false,
                             }).done(()=>{
                                 Swal.fire({
                                     title: "Alerta!",
                                     text: "Estacionamiento liberado correctamente",
                                     icon: "success",
                                     timer: 2000,
                                     onClose: () => {
                                         carga();
                                     }
                                 })
                             })
                           //   location.reload();
                             // location.href = '/erp/recepcion/'
           
                         }, function () { })
     
                     }else{
                         Swal.fire({
                             icon: 'error',
                             title: 'Oops...',
                             text: 'Aun no se cumple la fecha de termino del plan!',
                             timer: 2000,
                           })
                     }
     
                 });
 
   
             })
         });
   
     }




    /* ############### BUSCAr RESERVAA ################*/
    const searchReserva = (value, test)=> {
           $.ajax({
            url: window.location.pathname,
            type: "POST",
            data: {
                'action': "search_reserva",
                'id': value
            },
            headers: {
                'X-CSRFToken': csrftoken
            },
            dataType: "json",
        }).done((data)=>{
         test(data)
         return false
        })
    };
    
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

    /* ############### EVENT CLICK CARGAR ESTACIONAMIENTO ################*/
    const btnAddReservaDiaria = Array.from(document.querySelectorAll('.btnAddReservaDiaria'));
    if (btnAddReservaDiaria) {
        btnAddReservaDiaria.forEach(res => { 
            res.addEventListener('click', e => { 
                let value = e.currentTarget.getAttribute('rel') 
                searchBooking((response)=>{
                    // response.find(user => user.id === 2)
                    // console.log(response['reserva'].find(p => p.estacionamiento.id === Number(value)))
                    // if (response['reserva'].find(p => p.estacionamiento.id === Number(value)) === undefined){
                    //     console.log('no esta ocupado')
                    // }else{
                    //     console.log('SI ESTA OCUPADO')
                    // }
                    if (response['reserva'].find(p => p.estacionamiento.id === Number(value)) === undefined){
                        $("#valueEsta").html(`<a href="/erp/plan/reserva/add/${value}/" class="btn btn-warning"> Reserva Mensual</a>`)
                        $("select[name='estacionamiento']").val(value);
                        $("input[name='fecha_entrada']").val(moment().format('YYYY-MM-DD'));
                        // $("input[name='hora_entrada']").val(moment().format('HH:mm'));
                        $("#myModalReservaDiaria").modal("show");
                        formulario()
                        comprobarPatente()
                    }else{
                        Swal.fire({
                            icon: 'error',
                            title: 'Oops...',
                            text: 'Este estacionamiento esta en uso!',
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
    $("#myModalReservaDiaria").off("hidden.bs.modal")
    $("#myModalReservaDiaria").on("hidden.bs.modal", function (event) {
        // console.log(event)
        $('#frmReservaDiaria').trigger('reset') // ejecutamos llamamos al metodo trigger y ejecutamos el evento reset, para limpiar el formulario}
    });

    /* ############### CHECK PATENTE ################*/
    const comprobarPatente = () => {
        const patente = document.querySelector('#id_patente')
        // const mensajePatente = document.querySelector('#mensaje_patente')
          if(patente) {
              patente.addEventListener('keyup', e =>{
                //   let valor = e.target.value
                  patente.value =  e.target.value.toUpperCase()
                //   console.log(valor)
                  // Aqui esta el patron(expresion regular) a buscar en el input
                //   let patronPlacaChile =  /[A-Za-z]{2}-[A-Za-z]{2}-[0-9]{2}$/;
                //   let patronPlacaArgentina =  /[A-Za-z]{2}-[0-9]{3}-[A-Za-z]{2}$/;
  
                //   patronPlacaChile.test(valor) ||  patronPlacaArgentina.test(valor) || valor === '' ?  mensajePatente.innerHTML = ''  : mensajePatente.innerHTML = "<p class='text-danger' > Patente incorrecta, el formato debe ser: </p><b class='text-dark' > XX-XX-00</b> , <b class='text-dark' >XX-000-XX</b>"  
                  
              })
          }
      }
 
 }
 

 const formulario = ()=>{
        /* ############### SUBMIT BOOKING ################*/
        $("#frmReservaDiaria").off("submit")
        $("#frmReservaDiaria").on("submit", function (e) {
            e.preventDefault();
            var parameters = new FormData(this); // con el "this" llenamos el FormData a partir del fomulario al que apunto, lo cual crea una array de elementos
            parameters.append("action", "create_reserva"); // creamos una acción para que llegue a mi vista
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
                        // console.log(response)
                        $("#myModalReservaDiaria").modal("hide"); // para que el modal se oculte
                        window.open('/erp/reserva/invoice_ingreso/pdf/' + response.id + '/', '_blank');
                        // console.log(response)
                        Swal.fire({
                            title: "Alerta!",
                            text: "Reserva creada correctamente",
                            icon: "success",
                            timer: 2000,
                            onClose: () => {
                                carga();
                            }
                        })
                        // carga();
                        //   location.reload();
                        // location.href = '/erp/recepcion/'
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
    
 }

