let date_range = null;
let date_now = moment().format('YYYY-MM-DD')

const generate_report = () =>{
    let parameters = {
        'action': 'search_report',
        'start_date': date_now,
        'end_date': date_now
    }

    if(date_range !== null){
        parameters['start_date'] = date_range.startDate.format('YYYY-MM-DD')
        parameters['end_date'] = date_range.endDate.format('YYYY-MM-DD')
    }

    $("#data").DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        ajax: {
          url: window.location.pathname,
          type: "POST",
          data: parameters, 
          dataSrc: "",
          headers: {
            'X-CSRFToken': csrftoken
            }
        },
        // Deshabilitar ascpectos visuales
        order:false, 
        paging:false,
        ordering:false,
        searching:false,
        info:false,
        // buttons
        dom: 'Bfrtip',
        buttons: [
          {
              extend: 'excelHtml5',
              text: 'Descargar Excel <i class="fas fa-file-excel"></i>',
              titleAttr: 'Excel',
              className: 'btn btn-success btn-flat btn-xs',
              customize: function( xlsx, row ) {
                var sheet = xlsx.xl.worksheets['sheet1.xml'];
                 $('row c[r^="D"]', sheet).attr( 's', 63);
                 $('row:eq(1) c', sheet).attr( 's', 2 );
            }
          },
          {
              extend: 'pdfHtml5',
              text: 'Descargar Pdf <i class="fas fa-file-pdf"></i>',
              titleAttr: 'PDF',
              className: 'btn btn-danger btn-flat btn-xs',
              download: 'open',
              orientation: 'landscape',
              pageSize: 'LEGAL',
              customize: function (doc) {
                  doc.styles = {
                      header: {
                          fontSize: 18,
                          bold: true,
                          alignment: 'center'
                      },
                      subheader: {
                          fontSize: 13,
                          bold: true
                      },
                      quote: {
                          italics: true
                      },
                      small: {
                          fontSize: 8
                      },
                      tableHeader: {
                          bold: true,
                          fontSize: 11,
                          color: 'white',
                          fillColor: '#2d4154',
                          alignment: 'center'
                      }
                  };
                  doc.content[1].table.widths = ['10%','10%','10%','10%','10%','10%','10%'];
                  doc.content[1].margin = [0, 35, 0, 0];
                  doc.content[1].layout = {};
                  doc['footer'] = (function (page, pages) {
                      return {
                          columns: [
                              {
                                  alignment: 'left',
                                  text: ['Fecha de creación: ', {text: date_now}]
                              },
                              {
                                  alignment: 'right',
                                  text: ['página ', {text: page.toString()}, ' de ', {text: pages.toString()}]
                              }
                          ],
                          margin: 20
                      }
                  });

              }
          }
      ],
        columnDefs: [
            {
                targets: [-1],
                orderable: false,
                render: function (data, type, row) {
                    // let valor = new Intl.NumberFormat('es-CL', { style: 'currency', currency: 'CLP' }).format(data)
                    return "$" + data; 
                },
              },
        ],
        initComplete: function (settings, json) { },
        // se ejecuta al haber cargado la tabla
      });
}

$(function(){
    $('input[name="date_range"]').daterangepicker({
        locale: {
        format: 'YYYY-MM-DD',
        applyLabel: '<i class="fas fa-chart-pie"></i> Aplicar',
        cancelLabel: '<i class="fas fa-times"></i> Cancelar',
        }
    }).on('apply.daterangepicker', function(ev, picker) {
        date_range = picker;
        generate_report()
    }).on('cancel.daterangepicker', function(ev, picker) {
        $(this).data('daterangepicker').setStartDate(date_now);
        $(this).data('daterangepicker').setEndDate(date_now);
        date_range = picker;
        generate_report()
    });

    generate_report();
});