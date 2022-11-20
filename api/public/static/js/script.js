
$(document).ready(function(){        
    $("select.residencial_state_select").change(function(){
        var seleccion= $(this).children("option:selected").val();
        var array = seleccion.split('-');    
        $("#residencial_phone_area_code").val(array[1]);    
        $("#residencial_state").val(array[0]);            
    });

    $("#flag_visa_chk").change(function(){
        $("#flag_visa").val(0);    
        if(this.checked){
            $("#flag_visa").val(1);    
        }
    });

    $("#flag_mastercard_chk").change(function(){
        $("#flag_mastercard").val(0);    
        if(this.checked){
            $("#flag_mastercard").val(1);    
        }
    });


    $("#flag_diners_chk").change(function(){
        $("#flag_diners").val(0);    
        if(this.checked){
            $("#flag_diners").val(1);    
        }
    });

    $("#flag_american_express_chk").change(function(){
        $("#flag_american_express").val(0);    
        if(this.checked){
            $("#flag_american_express").val(1);    
        }
    });
    
    $("#flag_other_cards_chk").change(function(){
        $("#flag_other_cards").val(0);    
        if(this.checked){
            $("#flag_other_cards").val(1);    
        }
    });

    $("#flag_has_job_chk").change(function(){
        $("#flag_has_job").val(0);    
        $("#professional_data").hide();
        if(this.checked){
            $("#flag_has_job").val(1); 
            $("#professional_data").show();   
        }
    });
    
});            