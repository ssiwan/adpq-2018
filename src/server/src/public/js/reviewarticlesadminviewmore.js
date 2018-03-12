$(document).ready(function(){

    var role = sessionStorage.getItem("role");
    var token = sessionStorage.getItem("token");
    var userid = sessionStorage.getItem("id");
    //console.log(role);
    //console.log(token);

    if(!isEmpty(role) && !isEmpty(token))
    {

    var table;
    var url = APIURL + "adminDashboardPending";
    if (role === "admin") {
        $("#adminprofile").attr("href","edit-profile-admin.html?userId="+ userid);
    }
    else{
        $("#adminprofile").attr("href","edit-profile-staff.html?userId="+ userid); 
    }
   
    Load();
    function Load() {
        table = $('#articles').DataTable({
            "bDestroy": true,
            "pagingType": "full_numbers",
            "ajax": {
                type: "GET",
                url: url,
                cache:false,
                headers:{
                    'Authorization':token,
                    'Content-Type':'application/json'
                },
               "dataSrc": function (json) {
                   //console.log(json);
                   var return_data = new Array();
                   for (let index = 0; index < json.data.length; index++) {
                        var id = json.data[index].id;
                        var title = json.data[index].title;
                        var agency = json.data[index].agency;
                        var summary = json.data[index].summary;
                        var name = json.data[index].createdBy.name.first + "  " + json.data[index].createdBy.name.last;
                        var createdAt = convertToLocalDate(json.data[index].createdAt);
                        return_data[index] = {
                            'articleinfo':"<div class='trending-admin-review'><div class='trending-left-column'><div class='left-row-one'><div class='left-title'><a href=articles-details-admin-history.html?articleId="+id+">"+title+"</a></div><div class='left-column-tools'></div></div><div class='left-row-two'><div class='left-agency'>"+agency+"</div></div><div class='left-row-three'><div class='left-shortdesc'>"+summary+"</div></div><div class='left-row-four'><div class='left-publish-date'><div class='author'>"+name+"</div></div><div class='left-column-tools'><div class='left-most-pubdate'>"+createdAt+"</div></div></div></div></div>",
                            'status': json.data[index].status,
                            'id': json.data[index].id
                        }
                        if (return_data[index].status===0) {
                            return_data[index].status = "pending";  
                        }
        
                        if (return_data[index].status===1) {
                            return_data[index].status = "published";  
                        }
                        if (return_data[index].status===2) {
                            return_data[index].status = "declined";  
                        }
                   }
                   //console.log(return_data);
                   return return_data;
               }
        },
        "columnDefs": [
            {
                "targets": [ 2],
                "visible": false,
                "searchable": false
            }
        ],
            "columns": [
                    { "data": "articleinfo", "autoWidth": true },
                    { "data": "status", "autoWidth": true },
                    { "data": "id", "autoWidth": true }     
            ]
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