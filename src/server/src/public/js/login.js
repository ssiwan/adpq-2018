$(document).ready(function(){
    var LoginData = {
        email: "",
        password: ""
};
var LoginResponse = { token:""};

/*
{
    "error": "Please provide an authentication token"
}

*/

       

    $("#signin").click(function(){
        var password = $('#password').val();
        var username = $('#email').val();
        //console.log(username);
        if(!isEmpty(username) &&  !isEmpty(password))
        {
                LoginData.email = username;
                LoginData.password = password;
                console.log("Request JSON" + JSON.stringify(LoginData));
                $.ajax({
                type: "POST",
                url: APIURL + "user/signIn",
                dataType: "json",
                contentType: "application/json",
                data: JSON.stringify(LoginData),
                })
                .done(function (result) {
                console.log(result);
                    if(!isEmpty(result.token))
                    {
                        if (typeof(Storage) !== "undefined") {
                                sessionStorage.setItem("token", result.token);
                                sessionStorage.setItem("role", result.role);
                                sessionStorage.setItem("id", result.id);
                                sessionStorage.setItem("agencyid", result.agencyId);
                                sessionStorage.setItem("agency", result.agencyName);
                                
                            }
                        $('#password').val("");
                        $('#username').val("");
                        var role = result.role;
                        if (!isEmpty(role)) {
                            if (role === "admin") {
                                window.location.href = "dashboard-admin.html";
                            } else {
                                window.location.href = "dashboard-staff.html";
                            }    
                        }
                    }
                else
                {
                    alert("Invalid login");
                    $('#password').val("");
                    $('#username').val("");
                }
            })
            .fail(function (data, textStatus, xhr) {
             alert("signin endpoint error");
            });
        }
        else
        {
            alert("Please enter email and password");
            return;
        }
    });



});