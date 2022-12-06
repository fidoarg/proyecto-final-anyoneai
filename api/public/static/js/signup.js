$(document).ready(function(){        
  
    
    $( "#btn_singup" ).click(function() {
         
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

        if($("#birth_date").val() == ''){
            $("#errmsg9").html("Required Value").show().fadeOut(10000);                        
            $('#birth_date').focus()            
            return false;
        }

        if($("#sex").val() == ''){
            //alert("You must enter the value Gender")
            $("#errmsg14").html("Required Value").show().fadeOut(10000);                        
            $('#sex').focus()
            $('#sex').select()    
            return false;
        }

        if($("#nationality").val() == ''){            
            $("#errmsg18").html("Required Value").show().fadeOut(10000);
            $('#nationality').focus()
            $('#nationality').select()    
            return false;
        }    
        
        if($("#state_of_birth").val() == ''){
            $("#errmsg23").html("Required Value").show().fadeOut(10000);
            $('#state_of_birth').focus()
            $('#state_of_birth').select()    
            return false;
        }


        if($("#username").val() == ''){
            $("#errmsg1").html("Required Value").show().fadeOut(10000);
            $('#username').focus()            
            return false;
        } 

        if($("#password").val() == ''){
            $("#errmsg2").html("Required Value").show().fadeOut(10000);
            $('#password').focus()
            return false;
        }
       
    }); 

 
    
    
});            