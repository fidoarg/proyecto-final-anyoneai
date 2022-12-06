/*
Objective: manages all the controls related to the sign in page.
*/
$(document).ready(function(){        

    $("#username").focus()
    
    $("#btn_singup").click(function(){        
        window.location.href = "/auth/signup";
    }); 

    $( "#btn_singin" ).click(function() {
         
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