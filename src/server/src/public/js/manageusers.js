var role = sessionStorage.getItem("role");
var token = sessionStorage.getItem("token");
var userid = sessionStorage.getItem("id");
$(document).ready(function(){

    //console.log(role);
    //console.log(token);
    if(!isEmpty(role) && !isEmpty(token))
    {
        
        if (role === "admin") {
            $("#adminprofile").attr("href","edit-profile-admin.html?userId="+ userid);
        }
        else{
            $("#adminprofile").attr("href","edit-profile-staff.html?userId="+ userid); 
        }
     LoadUsers();
 
    function LoadUsers() {
            $.ajax({
                url: APIURL + "user",
                type: 'GET',
                dataType: 'json',
                headers:{
                    'Authorization':token,
                    'Content-Type':'application/json'
                }
            })
            .done(function(response) {
                //console.log(response);
            var str = "";
            
            if (!isEmpty(response.data)) {
            for (let index = 0; index < response.data.length; index++) {
                    var name= " ";
                    var email= " ";
                    var id = " ";
                if (!isEmpty(response.data[index].name)) {
                    name = response.data[index].name;
                } 
                if (!isEmpty(response.data[index].email)) {
                    email = response.data[index].email;
                }
                if (!isEmpty(response.data[index].userId)) {
                    id = response.data[index].userId;
                } 
                str += "<div class='manage-user-wrap'><div class='man-user-inwrap'><div class='man-user-labels'><div class='man-username'>" + name + "</div></div><div class='man-btnwrap'><div class='man-edit'> <button id='btnEdit' name='Save User Button' class='cs-button' type='button' onclick=\"EditUser('"+id+"')\">Edit</button></div><div class='man-remove'> <button id='btnRemove' name='Remove User Button' class='cs-button' type='button' onclick=\"DeleteUser('"+id+"')\">Remove</button></div></div></div></div>";
                 //console.log(str);
                }
            $("#users").append(str);
            }

            })
            .fail(function(data, textStatus, xhr) {
                alert("get users endpoint error");
            });
        } 
     
    

       
      $("#logout").click(function() {
          sessionStorage.clear();
          window.location.href = "index.html";
      })

    }
    else {
        window.location.href = "index.html";
    }
     

});


function EditUser(userid) {
    window.location.href = "edit-user-admin.html?userid="+userid;
}

function DeleteUser(userid) {
    //console.log(userid);
    $.ajax({
        url: APIURL + "user/" + userid,
        type: 'DELETE',
        headers:{
            'Authorization':token,
            'Content-Type':'application/json'
        }
    })
    .done(function(response) {
        console.log(response);
        //console.log(isEmpty(response.status));
        if (!isEmpty(response.data)) {
            if (response.data === "user removed!") {
                if (role === "admin") {
                    window.location.href = "dashboard-admin.html";
                }
               
            }
        }
        else{
            alert("There seems to be a problem with deleting the user.Please try again.");
        }
    })
    .fail(function(data, textStatus, xhr) {
        alert("Error with delete user endpoint.");
    });
}