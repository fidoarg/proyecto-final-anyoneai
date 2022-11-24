
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

        if($("#sex").val() == ''){
            alert("You must enter the value Gender")
            $('#sex').focus()
            $('#sex').select()    
            return false;
        }

        if($("#company").val() == ''){
            alert("You must enter the value company")
            $('#company').focus()
            $('#company').select()    
            return false;
        }

        if($("#payment_day").val() == ''){
            alert("You must enter the value Payment Day")
            $('#payment_day').focus()
            $('#payment_day').select()    
            return false;
        }

        if($("#postal_address_type").val() == ''){
            alert("You must enter the value Postal Address")
            $('#postal_address_type').focus()
            $('#postal_address_type').select()    
            return false;
        }

        if($("#marital_status").val() == ''){
            alert("You must enter the value Marital Status")
            $('#marital_status').focus()
            $('#marital_status').select()    
            return false;
        }

        if($("#quant_dependants").val() == ''){
            alert("You must enter the value Number of Dependents")
            $('#quant_dependants').focus()            
            return false;
        }

        if($("#state_of_birth").val() == ''){
            alert("You must enter the value State of Birth")
            $('#state_of_birth').focus()
            $('#state_of_birth').select()    
            return false;
        }

        if($("#nacionality").val() == ''){
            alert("You must enter the value Nacionality")
            $('#nacionality').focus()
            $('#nacionality').select()    
            return false;
        }
	
        if($("#residencial_state").val() == ''){
            alert("You must enter the Residencial State")
            $('#residencial_state').focus()
            $('#residencial_state').select()    
            return false;
        }	

        if($("#residencial_phone_area_code").val() == ''){
            alert("You must enter the Phone Area Code")
            $('#residencial_phone_area_code').focus()            
            return false;
        }	

        if($('#flag_residencial_phone_yes').is(':checked') == false && 
        $('#flag_residencial_phone_no').is(':checked') == false){
            alert("You must enter the Residencial Phone")
            $('#flag_residencial_phone').focus()            
            return false;
        }	
		
        if($("#residence_type").val() == ''){
            alert("You must enter the Residence Type")
            $('#residence_type').focus()
            $('#residence_type').select()    
            return false;
        }	

        if($("#months_in_residence").val() == '' ||
           $("#months_in_residence").val() == '0'){
            alert("You must enter the Months in Residence")
            $('#months_in_residence').focus()            
            return false;
        }
        
        if($('#flag_email_yes').is(':checked') == false && 
        $('#flag_email_no').is(':checked') == false){
            alert("You must enter the Email")
            $('#flag_email_yes').focus()            
            $('#flag_email_no').focus()            
            return false;
        }	        

        if($("#personal_monthly_income").val() == '' ||
           $("#personal_monthly_income").val() == '0'){
            alert("You must enter the Personal Monthly Income")
            $('#personal_monthly_income').focus()            
            return false;
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
        
        if($("#product").val() == ''){
            alert("You must enter the Product")
            $('#product').focus()
            $('#product').select()    
            return false;
        }	        
        
        if($("#age").val() == '' ||
           $("#age").val() == '0'){
            alert("You must enter the Age")
            $('#age').focus()            
            return false;
        }     
                
        $("#professional_state").val("NONE").change();
        $("#flag_professional_phone_no").attr('checked', 'checked');
        $("#professional_phone_area_code").val('NONE');        
        $("#profession_code").val("NONE").change();
        $("#occupation_type").val("NONE").change();        
        $("#flag_has_job_chk").val('0'); 

        if($('#flag_has_job_chk').is(':checked')){            
            $("#flag_has_job_chk").val('1');    
            $("#professional_state").val($("#professional_state option:first").val());            
            $('input[name="flag_professional_phone"]').attr('checked', false);
            $("#professional_phone_area_code").val('');                    
            $("#profession_code").val($("#profession_code option:first").val());      
            $("#occupation_type").val($("#occupation_type option:first").val());


            if($("#professional_state").val() == ''){
                alert("You must enter the Professional State")
                $('#professional_state').focus()
                $('#professional_state').select()    
                return false;
            }         
            
            if($("#professional_phone_area_code").val() == ''){
                alert("You must enter the Professional Phone Area Code")
                $('#professional_phone_area_code').focus()            
                return false;
            }             
                        
            if($('#flag_professional_phone_yes').is(':checked') == false && 
            $('#flag_professional_phone_no').is(':checked') == false){
                alert("You must enter the Professional Phone")
                $('#flag_professional_phone_yes').focus()            
                return false;
            }	            

            if($("#months_in_the_job").val() == '' ||
            $("#months_in_the_job").val() == '0'){
                alert("You must enter the Months in the Job")
                $('#months_in_the_job').focus()            
                return false;
            } 
            
            if($("#profession_code").val() == ''){
                alert("You must enter the Professional Code")
                $('#profession_code').focus()
                $('#profession_code').select()    
                return false;
            }               
            
            if($("#occupation_type").val() == ''){
                alert("You must enter the Occupation Type")
                $('#occupation_type').focus()
                $('#occupation_type').select()    
                return false;
            }                          
            
        }          
                
    });
    
});            