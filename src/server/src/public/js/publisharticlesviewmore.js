$(document).ready(function(){

    var role = sessionStorage.getItem("role");
    var token = sessionStorage.getItem("token");
    var userid = sessionStorage.getItem("id");
    //console.log(role);
    //console.log(token);

    if(!isEmpty(role) && !isEmpty(token))
    {
            if (role === "admin") {
                $("#adminsettingsbtn").show();
            }
            if (role === "admin") {
                $("#adminprofile").attr("href","edit-profile-admin.html?userId="+ userid);
            }
            else{
                $("#adminprofile").attr("href","edit-profile-staff.html?userId="+ userid); 
            }
            var table;

    var url = APIURL + "dashboardMyPublished";

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
                            'articleinfo':"<div class='trending-landing-articles'><div class='trending-left-column'><div class='left-row-one'><div class='left-title'><a href=articles-details-admin-history.html?articleId="+id+">"+title+"</a></div><div class='left-column-tools'></div></div><div class='left-row-two'><div class='left-agency'>"+agency+"</div></div><div class='left-row-three'><div class='left-shortdesc'>"+summary+"</div></div><div class='left-row-four'><div class='left-publish-date'><div class='author'>"+name+"</div></div><div class='left-column-tools'><div class='left-most-pubdate'>"+createdAt+"</div></div></div></div></div>",
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
    
/* 
    $('#articles').delegate('tbody tr', 'click', function () {
        //console.log("articleid  " + table.row(this).data().id);
        window.location.href = "articles-details-admin-history.html?articleId=" + table.row(this).data().id;
    });
 */
    $("#logout").click(function() {
        sessionStorage.clear();
        window.location.href = "index.html";
    })
    }
    else {
        window.location.href = "index.html";
    }


});