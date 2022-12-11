
/**
 * Objective:
 * - Handles all controls related to the score page.
 * - fetch the data from the json dictionary and load it
 * - retrieves the values from the database and graphs them
 */
$(document).ready(function(){        
    $("select.residencial_state_select").change(function(){        
        var seleccion= $(this).children("option:selected").val();
        var array = seleccion.split('-');    
        $("#residencial_phone_area_code").val(array[1]);    
        $("#residencial_zip_3").val(array[1]);            
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
        $("#professional_data2").hide();
        if(this.checked){            
            $("#flag_has_job").val(1); 
            $("#professional_data").show();   
            $("#professional_data2").show();   
        }
    });

    $("select.professional_state_select").change(function(){              
        var seleccion= $(this).children("option:selected").val();        
        var array = seleccion.split('-');    
        $("#professional_phone_area_code").val(array[1]);    
        $("#professional_state").val(array[0]);            
    });   
    
    $( "#btn_submit" ).click(function() {

        if($("#product").val() == ''){            
            $("#errmsg15").html("Required Value").show().fadeOut(10000);                        
            $('#product').focus()
            $('#product').select()    
            return false;
        }	  

        if($("#credit_amount").val() == ''){            
            $("#errmsg10").html("Required Value").show().fadeOut(10000);                        
            $('#credit_amount').focus()
            return false;
        }
        
        if($("#months_term").val() == ''){            
            $("#errmsg11").html("Required Value").show().fadeOut(10000);                        
            $('#months_term').focus()
            return false;
        }
         
        if($("#first_name").val() == ''){            
            $("#errmsg16").html("Required Value").show().fadeOut(10000);                        
            $('#first_name').focus()
            return false;
        }        
        
        if($("#last_name").val() == ''){            
            $("#errmsg17").html("Required Value").show().fadeOut(10000);                        
            $('#last_name').focus()
            return false;
        }        

        if($("#age").val() == '' || $("#age").val() == '0'){
            $("#errmsg9").html("Required Value").show().fadeOut(10000);                        
            $('#age').focus()            
            return false;
        }

        if($("#sex").val() == ''){
            //alert("You must enter the value Gender")
            $("#errmsg14").html("Required Value").show().fadeOut(10000);                        
            $('#sex').focus()
            $('#sex').select()    
            return false;
        }

        if($("#nacionality").val() == ''){            
            $("#errmsg18").html("Required Value").show().fadeOut(10000);
            $('#nacionality').focus()
            $('#nacionality').select()    
            return false;
        }    
        
        if($("#marital_status").val() == ''){
            $("#errmsg19").html("Required Value").show().fadeOut(10000);
            $('#marital_status').focus()
            $('#marital_status').select()    
            return false;
        }     
        
        if($("#postal_address_type").val() == ''){
            $("#errmsg20").html("Required Value").show().fadeOut(10000);
            $('#postal_address_type').focus()
            $('#postal_address_type').select()    
            return false;
        } 
        
        if($("#quant_dependants").val() == ''){
            $("#errmsg1").html("Required Value").show().fadeOut(10000);
            $('#quant_dependants').focus()            
            return false;
        }      

        if($("#residencial_state_select").val() == '-'){
            $("#errmsg21").html("Required Value").show().fadeOut(10000);
            $('#residencial_state_select').focus()
            $('#residencial_state_select').select()    
            return false;
        }	

        if($("#residencial_phone_area_code").val() == ''){
            $("#errmsg2").html("Required Value").show().fadeOut(10000);
            $('#residencial_phone_area_code').focus()            
            return false;
        }	

        if($("#residence_type").val() == ''){
            $("#errmsg22").html("Required Value").show().fadeOut(10000);
            $('#residence_type').focus()
            $('#residence_type').select()    
            return false;
        }
        
        if($("#months_in_residence").val() == '' ||
           $("#months_in_residence").val() == '0'){
            $("#errmsg3").html("Required Value").show().fadeOut(10000);
            $('#months_in_residence').focus()            
            return false;
        }        

        if($("#state_of_birth").val() == ''){
            $("#errmsg23").html("Required Value").show().fadeOut(10000);
            $('#state_of_birth').focus()
            $('#state_of_birth').select()    
            return false;
        }

        if($('#flag_residencial_phone_yes').is(':checked') == false && 
        $('#flag_residencial_phone_no').is(':checked') == false){
            $("#errmsg24").html("Required Value").show().fadeOut(10000);
            $('#flag_residencial_phone').focus()            
            return false;
        }	

        if($('#flag_email_yes').is(':checked') == false && 
        $('#flag_email_no').is(':checked') == false){
            $("#errmsg25").html("Required Value").show().fadeOut(10000);
            $('#flag_email_yes').focus()            
            $('#flag_email_no').focus()            
            return false;
        }	        

        if($("#personal_monthly_income").val() == '' ||
           $("#personal_monthly_income").val() == '0'){
            $("#errmsg4").html("Required Value").show().fadeOut(10000);
            $('#personal_monthly_income').focus()            
            return false;
        }           
                
        if($('#other_incomes').val() == ''){
            $("#other_incomes").val('0');             
        }                

        if($('#quant_banking_accounts').val() == ''){
            $("#quant_banking_accounts").val('0');             
        }                

        if($('#personal_assets_value').val() == ''){
            $("#personal_assets_value").val('0');             
        } 

        if($('#quant_cars').val() == ''){
            $("#quant_cars").val('0');             
        }                 

        if($('#flag_visa_chk').is(':checked')){
            $("#flag_visa").val('1');             
        }                
        
        if($('#flag_mastercard_chk').is(':checked')){
            $("#flag_mastercard").val('1');             
        }                

        if($('#flag_diners_chk').is(':checked')){
            $("#flag_diners").val('1');             
        }                
        
        if($('#flag_american_express_chk').is(':checked')){
            $("#flag_american_express").val('1');             
        }                
        
        if($('#flag_other_cards_chk').is(':checked')){
            $("#flag_other_cards").val('1');             
        }                         
            
        if($('#flag_has_job_yes').is(':checked') == false && 
        $('#flag_has_job_no').is(':checked') == false){
            $("#errmsg32").html("Required Value").show().fadeOut(10000);
            $('#flag_residencial_phone').focus()            
            return false;
        }

        if($('#flag_has_job_yes').is(':checked') == true){            
            /*
            $("#flag_has_job_chk").val('1');    
            $("#company").val($("#company option:first").val());   
            $("#payment_day").val($("#payment_day option:first").val());   
            $("#professional_state").val($("#professional_state option:first").val());            
            $('input[name="flag_professional_phone"]').attr('checked', false);
            $("#professional_phone_area_code").val('');                    
            $("#profession_code").val($("#profession_code option:first").val());      
            $("#occupation_type").val($("#occupation_type option:first").val());
            */

            if($("#company").val() == ''){
                $("#errmsg26").html("Required Value").show().fadeOut(10000);
                $('#company').focus()
                $('#company').select()    
                return false;
            }
    
            if($("#payment_day").val() == ''){
                $("#errmsg27").html("Required Value").show().fadeOut(10000);
                $('#payment_day').focus()
                $('#payment_day').select()    
                return false;
            } 
                   
            if($("#months_in_the_job").val() == '' ||
            $("#months_in_the_job").val() == '0'){
                $("#errmsg13").html("Required Value").show().fadeOut(10000);
                $('#months_in_the_job').focus()            
                return false;
            } 

            if($("#professional_state_select").val() == '-'){
                $("#errmsg28").html("Required Value").show().fadeOut(10000);
                $('#professional_state_select').focus()
                $('#professional_state_select').select()    
                return false;
            }         
            
            if($("#professional_phone_area_code").val() == ''){
                $("#errmsg12").html("Required Value").show().fadeOut(10000);
                $('#professional_phone_area_code').focus()            
                return false;
            }             
                        
            if($('#flag_professional_phone_yes').is(':checked') == false && 
            $('#flag_professional_phone_no').is(':checked') == false){
                $("#errmsg29").html("Required Value").show().fadeOut(10000);
                $('#flag_professional_phone_yes').focus()            
                return false;
            }	            
            
            if($("#profession_code").val() == ''){
                $("#errmsg30").html("Required Value").show().fadeOut(10000);
                $('#profession_code').focus()
                $('#profession_code').select()    
                return false;
            }               
            
            if($("#occupation_type").val() == ''){
                $("#errmsg31").html("Required Value").show().fadeOut(10000);
                $('#occupation_type').focus()
                $('#occupation_type').select()    
                return false;
            }                                      
        }else{
            $("#professional_state").val("NONE").change();
            $("#flag_professional_phone_no").attr('checked', 'checked');
            $("#professional_phone_area_code").val('NONE');        
            $("#profession_code").val("NONE").change();
            $("#occupation_type").val("NONE").change();  
            $("#company").val("N").change();              
            $("#payment_day").val("NONE").change();        
            $("#months_in_the_job").val('0');              
            $("#flag_has_job_chk").val('0'); 
        }                      
    });

    $("#quant_dependants").keypress(function (e) {
        //if the letter is not digit then display error and don't type anything
        if (e.which != 8 && e.which != 0 && (e.which < 48 || e.which > 57)) {
           //display error message
           $("#errmsg1").html("Digits Only").show().fadeOut("slow");
                  return false;
       }
    });

    $("#residencial_phone_area_code").keypress(function (e) {
        //if the letter is not digit then display error and don't type anything
        if (e.which != 8 && e.which != 0 && (e.which < 48 || e.which > 57)) {
           //display error message
           $("#errmsg2").html("Digits Only").show().fadeOut("slow");
                  return false;
       }
    });

    $("#months_in_residence").keypress(function (e) {
        //if the letter is not digit then display error and don't type anything
        if (e.which != 8 && e.which != 0 && (e.which < 48 || e.which > 57)) {
           //display error message
           $("#errmsg3").html("Digits Only").show().fadeOut("slow");
                  return false;
       }
    });    

    $("#personal_monthly_income").keypress(function (e) {
        //if the letter is not digit then display error and don't type anything
        if (e.which != 8 && e.which != 0 && (e.which < 48 || e.which > 57)) {
           //display error message
           $("#errmsg4").html("Digits Only").show().fadeOut("slow");
                  return false;
       }
    });        

    $("#other_incomes").keypress(function (e) {
        //if the letter is not digit then display error and don't type anything
        if (e.which != 8 && e.which != 0 && (e.which < 48 || e.which > 57)) {
           //display error message
           $("#errmsg5").html("Digits Only").show().fadeOut("slow");
                  return false;
       }
    });            
    
    $("#quant_banking_accounts").keypress(function (e) {
        //if the letter is not digit then display error and don't type anything
        if (e.which != 8 && e.which != 0 && (e.which < 48 || e.which > 57)) {
           //display error message
           $("#errmsg6").html("Digits Only").show().fadeOut("slow");
                  return false;
       }
    });
    
    $("#personal_assets_value").keypress(function (e) {
        //if the letter is not digit then display error and don't type anything
        if (e.which != 8 && e.which != 0 && (e.which < 48 || e.which > 57)) {
           //display error message
           $("#errmsg7").html("Digits Only").show().fadeOut("slow");
                  return false;
       }
    });    
    
    $("#quant_cars").keypress(function (e) {
        //if the letter is not digit then display error and don't type anything
        if (e.which != 8 && e.which != 0 && (e.which < 48 || e.which > 57)) {
           //display error message
           $("#errmsg8").html("Digits Only").show().fadeOut("slow");
                  return false;
       }
    }); 

    $("#age").keypress(function (e) {
        //if the letter is not digit then display error and don't type anything
        if (e.which != 8 && e.which != 0 && (e.which < 48 || e.which > 57)) {
           //display error message
           $("#errmsg9").html("Digits Only").show().fadeOut("slow");
                  return false;
       }
    }); 

    $("#credit_amount").keypress(function (e) {
        //if the letter is not digit then display error and don't type anything
        if (e.which != 8 && e.which != 0 && (e.which < 48 || e.which > 57)) {
           //display error message
           $("#errmsg10").html("Digits Only").show().fadeOut("slow");
                  return false;
       }
    }); 
    
    $("#months_term").keypress(function (e) {
        //if the letter is not digit then display error and don't type anything
        if (e.which != 8 && e.which != 0 && (e.which < 48 || e.which > 57)) {
           //display error message
           $("#errmsg11").html("Digits Only").show().fadeOut("slow");
                  return false;
       }
    });     

    $("#professional_phone_area_code").keypress(function (e) {
        //if the letter is not digit then display error and don't type anything
        if (e.which != 8 && e.which != 0 && (e.which < 48 || e.which > 57)) {
           //display error message
           $("#errmsg12").html("Digits Only").show().fadeOut("slow");
                  return false;
       }
    }); 
    
    $("#months_in_the_job").keypress(function (e) {
        //if the letter is not digit then display error and don't type anything
        if (e.which != 8 && e.which != 0 && (e.which < 48 || e.which > 57)) {
           //display error message
           $("#errmsg13").html("Digits Only").show().fadeOut("slow");
                  return false;
       }
    }); 

    $('#job_data_information').hide();
    $('input[type=radio][name=flag_has_job]').change(function() {
        if (this.value == '1') {
            $('#job_data_information').show();
        }
        else if (this.value == '0') {
            $('#job_data_information').hide();
        }
    });    
    
    
});            