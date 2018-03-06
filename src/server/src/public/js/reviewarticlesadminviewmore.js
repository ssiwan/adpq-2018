$(document).ready(function(){

    var role = sessionStorage.getItem("role");
    var token = sessionStorage.getItem("token");

    //console.log(role);
    //console.log(token);

    if(!isEmpty(role) && !isEmpty(token))
    {

    var table;
    var url = APIURL + "adminDashboardPending";
 
   
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
                            'articleinfo': "<strong>" + json.data[index].title + "</strong><br/>"
                                             + "<strong>Agency:" + json.data[index].agency + "</strong><br/>" 
                                             + json.data[index].summary + "<br/>" 
                                             + "<strong>Author: </strong>" + json.data[index].createdBy.name.first + "  " + json.data[index].createdBy.name.last + "<br/>"
                                             + "<strong>PublishedDate:</strong> " + convertToLocalDate(json.data[index].createdAt),
                            'lastupdated': convertToLocalDate(json.data[index].createdAt),
                            'views': json.data[index].views,
                            'shares': json.data[index].shares,
                            'id': json.data[index].id
                        }
                   }
                   //console.log(return_data);
                   return return_data;
               }
        },
        "columnDefs": [
            {
                "targets": [ 4 ],
                "visible": false,
                "searchable": false
            }
        ],
            "columns": [
                    { "data": "articleinfo", "autoWidth": true },
                    { "data": "lastupdated", "autoWidth": true },
                    { "data": "views", "autoWidth": true },
                    { "data": "shares", "autoWidth": true },
                    { "data": "id", "autoWidth": true }     
            ]
        }); 
    }
    

    $('#articles').delegate('tbody tr', 'click', function () {
        //console.log("articleid  " + table.row(this).data().id);
        window.location.href = "articles-details-admin-history.html?articleId=" + table.row(this).data().id;
    });

    
    }
    else {
        window.location.href = "index.html";
    }


});