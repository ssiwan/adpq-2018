$(document).ready(function(){
    var role = sessionStorage.getItem("role");
    if(!isEmpty(role)){
        if (role === "admin") {
            $("#adminsettingsbtn").show();
            $("#adminusersbtn").show();
        }
           
       


    }
    else {
        window.location.href = "index.html";
    }
     



});