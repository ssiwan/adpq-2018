var userid = getParameterByName("userid"); // gets userid from the URL querystring
var role = sessionStorage.getItem("role");
var token = sessionStorage.getItem("token");
$(document).ready(function(){
 if(!isEmpty(role) && !isEmpty(token))
 {
          
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
      .fail(function(xhr) {
        console.log('error', xhr);
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
                $("#idfirst").val(response.firstName);
                $("#idlast").val(response.lastName);
                $("#idemail").val(response.email);
                document.getElementById('idagency').value = response.agencyId;
                if (response.allowUploads === 1) {
                    $("#uploadchk").prop('checked', true);
                } 
                else
                {
                    $("#uploadchk").prop('checked', false);
                }             
            })
            .fail(function(data, textStatus, xhr) {
                alert("Loading user details failed");
            });
        }

           

        var user = {
            firstName: "",
            lastName: "",
            email: "",
            phone: "",
            agencyId: "",
            allowUploads: "no"
          }


        $("#btnSave").click(function(){

            user.firstName = $("#idfirst").val();
            user.lastName = $("#idlast").val();
            user.email = $("#idemail").val();
            user.agencyId = $("#idagency").val();
            var flag = $('#uploadchk').prop('checked');
            if (flag === true) {
                user.allowUploads = 1;
            } else {
                user.allowUploads = 0;
            }
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
                type: 'POST',
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
                        alert("User created successfully.")
                        setTimeout(function(){ window.location.href = "dashboard-admin.html"; }, 1000);
                    }
                }
                else{
                    alert("There seems to be a problem with saving.Please try again.");
                }
            })
            .fail(function(data, textStatus, xhr) {
                alert("Create user failed");
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