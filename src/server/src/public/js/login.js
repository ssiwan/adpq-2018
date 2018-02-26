$(document).ready(function(){
    var LoginData = {
        email: ""//,
       // password: ""
};
var LoginResponse = { token:""};

/*
{
    "error": "Please provide an authentication token"
}

*/

    $("#signin").click(function(){
        //var password = $('#password').val();
        var username = $('#email').val();
        //console.log(username);
        if(!isEmpty(username))
        {
            
            LoginData.email = username;
            //LoginData.password = password;
            //console.log("Request JSON" + JSON.stringify(LoginData));
            $.ajax({
            type: "POST",
            url: APIURL + "user/signIn",
            dataType: "json",
            contentType: "application/json",
            data: JSON.stringify(LoginData),
            })
            .done(function (result) {
            //console.log(result);
            if(!isEmpty(result.token))
            {
                 if (typeof(Storage) !== "undefined") {
                        sessionStorage.setItem("token", result.token);
                    }
                $('#password').val("");
                $('#username').val("");
                window.location.href = "articles.html"; // should go to dashboard page change later
            }
            else
            {
                alert("Invalid login");
                $('#password').val("");
                $('#username').val("");
                
            }
            })
            .fail(function (data, textStatus, xhr) {
             //console.log(data.responseJSON.Error);
             alert(data.responseJSON.Error);
             /*console.log("error", data.status);
             console.log("STATUS: "+xhr); */
            });
        }
        else
        {
            alert("Please enter email and password.");
            return;
        }
    });










});