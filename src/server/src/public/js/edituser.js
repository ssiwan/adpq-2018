var userid = getParameterByName("userId"); // gets userid from the URL querystring
var role = sessionStorage.getItem("role");
var token = sessionStorage.getItem("token");
var usersid = sessionStorage.getItem("id");
$(document).ready(function(){
 if(!isEmpty(role) && !isEmpty(token))
 {

    if (role === "admin") {
        $("#adminprofile").attr("href","edit-profile-admin.html?userId="+ usersid);
    }
    else{
        $("#adminprofile").attr("href","edit-profile-staff.html?userId="+ usersid); 
    }
          
   LoadAgencies(); 
    function LoadAgencies() {
        var options = $("#idagency");
    $.ajax({
        url: APIURL + "agencies",
        type: 'GET',
        dataType: 'json',
        cache:false
      })
      .done(function(response) {
        if (response.data != null) {
            for (let index = 0; index < response.data.length; index++) {
                options.append($("<option />").val(response.data[index].id).text(response.data[index].name));
             }
        }
        else
        {
            alert(response.error);
        }

      })
      .fail(function( jqXHR, textStatus, errorThrown) {
        alert(jqXHR.responseJSON.error);
    });

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
                document.getElementById('idagency').value = response.data.agencyId;
                if (response.data.allowUploads === 1) {
                    $("#uploadchk").prop('checked', true);
                } 
                else
                {
                    $("#uploadchk").prop('checked', false);
                }             
            })
            .fail(function( jqXHR, textStatus, errorThrown) {
                alert(jqXHR.responseJSON.error);
            });
        }

           

        var user = {
            firstName: "",
            lastName: "",
            email: "",
            phone: "",
            agencyId: "",
            allowUploads: 0,
            userId:"",
            password:""
          }


        $("#btnSave").click(function(){

            user.firstName = $("#idfirst").val();
            user.lastName = $("#idlast").val();
            user.email = $("#idemail").val();
            user.agencyId =  document.getElementById('idagency').value;
            var flag = $('#uploadchk').prop('checked');
            if (flag === true) {
                user.allowUploads = 1;
            } else {
                user.allowUploads = 0;
            }
            user.userId = userid;
            user.password = $("#idpassword").val();
        

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
                url: APIURL + "user",
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
                        alert("User updated successfully.")
                        window.location.href = "dashboard-admin.html";
                    }
                }
                else{
                    alert("There seems to be a problem with updating.Please try again.");
                }
            })
            .fail(function( jqXHR, textStatus, errorThrown) {
                alert(jqXHR.responseJSON.error);
            });
        });

        $("#btnCancel").click(function() {
            window.location.href = "dashboard-admin.html";
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