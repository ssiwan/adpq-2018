var userid = getParameterByName("userId"); // gets userid from the URL querystring
var role = sessionStorage.getItem("role");
var token = sessionStorage.getItem("token");
var userid = sessionStorage.getItem("id");
$(document).ready(function(){
 if(!isEmpty(role) && !isEmpty(token))
 {
    
    if (role === "admin") {
        $("#adminprofile").attr("href","edit-profile-admin.html?userId="+ userid);
    }
    else{
        $("#adminprofile").attr("href","edit-profile-staff.html?userId="+ userid); 
    }


   LoadData();
        function LoadData() {
            $.ajax({
                url: APIURL + "user/" + userid,
                type: 'GET',
                dataType: 'json',
                headers:{
                    'Authorization':token,
                    'Content-Type':'application/json'
                }
              })
            .done(function(response) {
                console.log(response);
                var name = response.data.name.split(" ");
                $("#idfirst").val(name[0]);
                $("#idlast").val(name[1]);
                $("#idemail").val(response.data.email);            
            })
            .fail(function( jqXHR, textStatus, errorThrown) {
                alert(jqXHR.responseJSON.error);
            });
        }

           

        var user = {
            firstName: "",
            lastName: "",
            email: "",
            password: ""
          }


        $("#btnSave").click(function(){

            user.firstName = $("#idfirst").val();
            user.lastName = $("#idlast").val();
            user.email = $("#idemail").val();
            user.password = $("#idnewpassword").val();
            // Validation
            var errors = "";
            if (isEmpty(user.firstName)) {
                errors+= "First Name is required. \r\n";
            }
            if (isEmpty(user.lastName)) {
                errors+= "Last Name is required. \r\n";
            }
            if (isEmpty(user.email)) {
                errors+= "Email is required. \r\n";
            }

            if (!isEmpty(errors)) {
                alert(errors);
                return;
            }
           console.log("Request JSON" + JSON.stringify(user));
          
            $.ajax({
                url: APIURL + "user/editProfile",
                type: 'PATCH',
                dataType: 'json',
                headers:{
                    'Authorization':token,
                    'Content-Type':'application/json'
                },
                data: JSON.stringify(user)
            })
            .done(function(response) {
                console.log(response);
                if (!isEmpty(response.status)) {
                    if (response.status === "saved!") {
                        alert("User edited successfully.")
                        if (role === "admin") {
                            window.location.href = "dashboard-admin.html";
                        } else {
                            window.location.href = "dashboard-staff.html";
                        }
                    }
                }
                else{
                    alert("There seems to be a problem with saving.Please try again.");
                }
            })
            .fail(function( jqXHR, textStatus, errorThrown) {
                alert(jqXHR.responseJSON.error);
            });
        });

        $("#btnCancel").click(function() {
            if (role === "admin") {
                window.location.href = "dashboard-admin.html";
            } else {
                window.location.href = "dashboard-staff.html";
            }
        });

        $("#logout").click(function() {
            sessionStorage.clear();
            window.location.href = "index.html";
        })

 }
else {
    window.location.href = "index.html";
}

});