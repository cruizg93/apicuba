$(document).ready(function(){
    //$("#currentLenguage") has the value of the actual lenguage, 
    //loaded by babel and it placed in every translate .po file
    // with the tag ID of the orginal lenguage wich is 'en'
    var lang = $("#currentLenguage").html();
    
    if(lang=='en'){
        $('#toggle_i18n').prop( "checked", true );
    }else{
        $('#toggle_i18n').prop( "checked", false);
    }

    //this set default values to input type date
    $("#dateTo").attr("value",formatFechaDefaultTo());
    $("#dateFrom").attr("value",formatFechaDefaultFrom());

    //this put a tag :after to input city from
    $("#cityFrom").after("<a href='http://www.aduana.cu/api/api_aeropuertos.php' target='_blank'>Códigos IATA</a>");
    
    //trigger for button search
    $("#btnSearch").click(function(){
		getConsult();
	});


    $("#dateTo").change(function(){
        var tomorrow = new Date();
        tomorrow.setDate(tomorrow.getDate() + 1);
        tomorrow.setHours(0,0,0,0);

        var current = new Date($("#dateTo").val()); 
        current.setDate(current.getDate()+1);
        current.setHours(0,0,0,0);
        
        var from = new Date($("#dateFrom").val());
        from.setDate(from.getDate()+1);
        from.setHours(0,0,0,0);

        if(current>tomorrow){
            $("#errorMsg").html("La fecha hasta no puede ser mayor a "+String(tomorrow.getMonth()+1)+"/"+String(tomorrow.getDate())+"/"+String(tomorrow.getFullYear()));
        }else{
            $("#errorMsg").html("");
        }
        if(current<from){
            $("#errorMsg").html("La fecha hasta no puede ser menor a "+String(from.getMonth()+1)+"/"+String(from.getDate())+"/"+String(from.getFullYear()));
        }else{
            $("#errorMsg").html("");
        }

    });

    $("#dateFrom").change(function(){
       
        var current = new Date($("#dateTo").val()); 
        current.setDate(current.getDate()+1);
        current.setHours(0,0,0,0);
        
        var from = new Date($("#dateFrom").val());
        from.setDate(from.getDate()+1);
        from.setHours(0,0,0,0);

        if(current<from){
            $("#errorMsg").html("La fecha Desde no puede ser mayor a "+String(from.getMonth()+1)+"/"+String(from.getDate())+"/"+String(from.getFullYear()));
        }else{
            $("#errorMsg").html("");
        }

    });


    //trigger getConsult() when key enter is pressed
    $('input').keypress(function (e) {
        var key = e.which;
        if(key == 13)  // the enter key code
        {
            getConsult();
            return false;  
        }
    });

    
    $("#toggle_i18n").change(function(){
        var language = '';
        if ($('#toggle_i18n').is(":checked")){
            language = 'en';
        }else{
            language = 'es';
        }
        $("#lang_code").val(language);
        $('#languageForm').submit();
    });
});



function getConsult(){
    var data = $( "#apiForm" ).serialize();
    showSpiner();
    $.ajax({
        url: '/build',
        type: 'POST',
        data: data,
        success: function(response) {
            data = JSON.parse(response);
            $("#apitable tbody").html("");
        	$("#apitable").append(data.rows);
            $("#apitable").dataTable();
            $('#cities').html(data.cities);
            hideSpiner();
        },
        error: function(error) {
            console.log(error);
        }
    });
}


function formatFechaDefaultTo(){
    
    var fecha = new Date();
    var formated = String(fecha.getFullYear());
    fecha.setDate(fecha.getDate()+1);
    
    if(String((fecha.getMonth()+1)).length == 1){
        formated += "-"+String("0"+(fecha.getMonth()+1));
    }else{
        formated += "-"+String((fecha.getMonth()+1));
    }
    

    if(String(fecha.getDate()).length==1){
        formated += "-"+String("0"+fecha.getDate());
    }else{
        formated += "-"+String(fecha.getDate());
    }
    
    return formated;
}

//Going back a week
function formatFechaDefaultFrom(){
    var fecha = new Date();
    var formated = String(fecha.getFullYear());
    
    fecha.setDate(fecha.getDate()-7);
    
    
    if(String((fecha.getMonth()+1)).length == 1){
        formated += "-"+String("0"+(fecha.getMonth()+1));
    }else{
        formated += "-"+String((fecha.getMonth()+1));
    }

    if(String(fecha.getDate()).length==1){
        formated += "-"+String("0"+fecha.getDate());
    }else{
        formated += "-"+String(fecha.getDate());
    }
    return formated;
}



/***
**** SPINNER SECTION
*****/

function showSpiner(){
    var opts = {
          lines: 11 // The number of lines to draw
        , length: 51 // The length of each line
        , width: 14 // The line thickness
        , radius: 37 // The radius of the inner circle
        , scale: 1 // Scales overall size of the spinner
        , corners: 1 // Corner roundness (0..1)
        , color: '#000' // #rgb or #rrggbb or array of colors
        , opacity: 0.2 // Opacity of the lines
        , rotate: 37 // The rotation offset
        , direction: 1 // 1: clockwise, -1: counterclockwise
        , speed: 1.5 // Rounds per second
        , trail: 60 // Afterglow percentage
        , fps: 20 // Frames per second when using setTimeout() as a fallback for CSS
        , zIndex: 2e9 // The z-index (defaults to 2000000000)
        , className: 'spinner' // The CSS class to assign to the spinner
        , top: '50%' // Top position relative to parent
        , left: '50%' // Left position relative to parent
        , shadow: true // Whether to render a shadow
        , hwaccel: false // Whether to use hardware acceleration
        , position: 'relative' // Element positioning
    }
    $("#spiner").css('display','block');
    var target = document.getElementById('spiner')
    var spinner = new Spinner(opts).spin(target);
}

function hideSpiner(){
    $("#spiner").css('display','none');
}

function renderTable(tableId){
    var table = $(tableId)
    $(tableId).dataTable();
    /*if ( $.fn.dataTable.isDataTable(tableId) ) {
        table.destroy();
        table.DataTable( {
            select: true,
            lengthChange: false
        } ).on( 'select', function ( e, dt, type, indexes ) {
            alert('on');
        } );
    }else {
        table.DataTable( {
            select: true,
            lengthChange: false
        } ).on( 'select', function ( e, dt, type, indexes ) {
            alert('on');
        } );
    }*/
    
}