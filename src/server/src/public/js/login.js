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
                            sessionStorage.setItem("role", result.role);
                            sessionStorage.setItem("id", result.id);
                            sessionStorage.setItem("agencyid", result.agency._id);
                            sessionStorage.setItem("agency", result.agency.value);
                        }
                    $('#password').val("");
                    $('#username').val("");
                    /*
                      Valid emails:
                      staff login - jlennon@hotbsoftware.com
                      admin login - rstar@hotbsoftware.com
                    */
                    // based upon the role show the required pages.
                    // role = staff or admin
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
             //console.log(data.responseJSON.Error);
             alert(data.responseJSON.Error);
             /*console.log("error", data.status);
             console.log("STATUS: "+xhr); */
            });
        }
        else
        {
            alert("Please enter email.");
            return;
        }
    });










});