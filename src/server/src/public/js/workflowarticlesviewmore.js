$(document).ready(function(){

    var role = sessionStorage.getItem("role");
    var token = sessionStorage.getItem("token");

    //console.log(role);
    //console.log(token);

    if(!isEmpty(role) && !isEmpty(token))
    {
            if (role === "admin") {
                $("#adminsettingsbtn").show();
            }
            var table;
    var url = APIURL + "dashboardWorkflow";

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
                        return_data[index] = {
                            /*'articleinfo':"<div class='article-title'>"    + json.data[index].title + "</div>"
                                          +"<div class='article-agency'>Agency:" + json.data[index].agency + "</div>"
                                          + json.data[index].summary + "<br/>"
                                          + "<div class='article-author'>Author: </div>" + json.data[index].createdBy.name.first + "  " + json.data[index].createdBy.name.last +
                                          + "<div class='article-publishdate'>PublishedDate:</div> " + convertToLocalDate(json.data[index].createdAt),*/
                            'articleinfo': "<strong>" + json.data[index].title + "</strong><br/>"
                                             + "<strong>Agency:" + json.data[index].agency + "</strong><br/>" 
                                             + json.data[index].summary + "<br/>" 
                                             + "<strong>Author: </strong>" + json.data[index].createdBy.name.first + "  " + json.data[index].createdBy.name.last + "<br/>"
                                             + "<strong>PublishedDate:</strong> " + convertToLocalDate(json.data[index].createdAt),
                            'lastupdated': convertToLocalDate(json.data[index].createdAt),
                            'views': json.data[index].views,
                            'shares': json.data[index].shares,
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
                "targets": [ 5 ],
                "visible": false,
                "searchable": false
            }
        ],
            "columns": [
                    { "data": "articleinfo", "autoWidth": true },
                    { "data": "lastupdated", "autoWidth": true },
                    { "data": "views", "autoWidth": true },
                    { "data": "shares", "autoWidth": true },   
                    { "data": "status", "autoWidth": true },
                    { "data": "id", "autoWidth": true }    
            ]
        }); 
    }
    

    $('#articles').delegate('tbody tr', 'click', function () {
        //console.log("articleid  " + table.row(this).data().id);
        window.location.href = "articles-details-admin-history.html?articleId=" + table.row(this).data().id;
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