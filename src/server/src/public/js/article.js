$(document).ready(function(){
    var table;
    var agencychk = $('#chkAgency');
    var tagschk = $('#chkTags');
    var datechk = $('#chkDate');
    var url = "";
    //var APIKey = "";

    // Create calendar
		


    SetUrl();
    DatePicker();
    Load();


    // Set the URL based on the searchvalue parameter
    function SetUrl() {
        var searchval = sessionStorage.getItem("searchValue");
        if (!isEmpty(searchval)){
           url =   APIURL + "searchArticles?keyword=" + searchval;
        }
        else {
           url =  APIURL + "articles?sort=createdAt&order=1";
        }
    }  
   

   function LoadAgencies() {
        var options = $("#ddlAgency");
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

   // uncomment this section once the tag endpoint is updated with both tagid and tagname
   function LoadTags() {
            var options = $("#ddlTags");
            $.ajax({
                url: APIURL + "tags",
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


    function DatePicker() {
      
        var dateFormat = "yy-mm-dd",
        from = $("#from")
          .datepicker({
            /* changeMonth: true,
            numberOfMonths: 1,
            onSelect: function(selected) {
                $("#to").datepicker("option","minDate", selected)
            } */
          })
          .on("change", function() {
            to.datepicker("option", "minDate", getDate(this));
          }),
        to = $("#to").datepicker({
/*           changeMonth: true,
          numberOfMonths: 1,
          onSelect: function(selected) {
            $("#from").datepicker("option","maxDate", selected)
         } */
        })
        .on("change", function() {
          from.datepicker("option", "maxDate", getDate(this));
        });
   

    }



    function getDate(element) {
        var date;
        try {
          date = $.datepicker.parseDate(dateFormat, element.value);
        } catch( error ) {
          date = null;
        }
        return date;
      }

    function Load() {
        table = $('#articles').DataTable({
            "bDestroy": true,
            responsive: true,
            "pagingType": "full_numbers",
            "ordering": true,
            "ajax": {
                type: "GET",
                url: url,
                cache:false,
               contentType: "application/json;",
               "dataSrc": function (json) {
                   //console.log(json);
                   var return_data = new Array();
                   for (let index = 0; index < json.data.length; index++) {
                       var id = json.data[index].id;
                       var title = json.data[index].title;
                       var agency = json.data[index].agency;
                       var summary = json.data[index].summary;
                       var name = "";
                        if (!isEmpty(json.data[index].createdBy)) {
                           name = json.data[index].createdBy.name.first+ "  " +json.data[index].createdBy.name.last;
                        }
                       var createdAt = convertToLocalDate(json.data[index].createdAt);
                        return_data[index] = {
                            'articleinfo':"<div class='trending-landing-articles'><div class='trending-left-column'><div class='left-row-one'><div class='left-title-articles'><a href=articles-details-admin-history.html?articleId="+id+">"+title+"</a></div><div class='left-column-tools'></div></div><div class='left-row-two'><div class='left-agency'>"+agency+"</div></div><div class='left-row-three'><div class='articles-shortdesc'>"+summary+"</div></div><div class='left-row-four'><div class='left-publish-date'><div class='author'>"+name+"</div></div><div class='left-column-tools'><div class='left-most-pubdate'>"+createdAt+"</div></div></div></div></div>",
                            'lastupdated': convertToLocalDate(json.data[index].createdAt),
                            'views': json.data[index].views,
                            'shares': json.data[index].shares,
                            'id':json.data[index].id
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
        "language": {
            "search":"keyword search",
            "searchPlaceholder": "keyword search"
          },
            "columns": [
                    { "data": "articleinfo", "autoWidth": true },
                    { "data": "lastupdated", "autoWidth": true },
                    { "data": "views", "autoWidth": true },
                    { "data": "shares", "autoWidth": true },
                    { "data": "id", "autoWidth": true }, 
            ]
        }); 
    }
    

   /*  $('#articles').delegate('tbody tr', 'click', function () {
        console.log(table.row(this).data().id);
        window.location.href = "articles-details-admin-history.html?articleId=" + table.row(this).data().id;
        
    }); */

    /*$("#btnReload").click(function(){
        Load();
    });  */

    $("#btnFilters").click(function(){
        $("#btnHideFilters").show();     
        $("#btnFilters").hide();
        $("#filters").show();
    }); 
    
    $("#btnHideFilters").click(function(){
        $("#btnHideFilters").hide();
        $("#btnFilters").show();
        $("#filters").hide();
    });


    $("#chkAgency").click(function(){
        if (agencychk.prop('checked')) {
            $("#Agency").show();
            LoadAgencies();
        } else {
            $("#ddlAgency").empty();
            $("#Agency").hide();
        }
    }); 

    $("#chkTags").click(function(){
        if (tagschk.prop('checked')) {
            $("#Tags").show();
            LoadTags();
        } else {
            $("#ddlTags").empty();
            $("#Tags").hide();
        }
     }); 

     $("#chkDate").click(function(){
        if (datechk.prop('checked')) {
            $("#daterange").show();
        } else {
            //console.log($("#from").val());
            //console.log($("#to").val());
            $("#from").val('');
            $("#to").val('');
            $("#daterange").hide();
        }
     }); 

     $("#btnSearch").click(function() {
        var agencyid = $("#ddlAgency").val();
        var tagid = $("#ddlTags").val();
        var datefrom = ReplaceDateSlash($("#from").val());
        var dateto = ReplaceDateSlash($("#to").val()); 
        var searchfilter = "";
        if (!isEmpty(agencyid)) {
            searchfilter += "agencyId=" + agencyid + "&"; 
        }
        if (!isEmpty(tagid)) {
            searchfilter += "tagId=" + tagid + "&";
        }
        if (!isEmpty(datefrom)) {
            searchfilter += "dateStart=" + datefrom + "&";
        }
        if (!isEmpty(dateto)) {
            searchfilter += "dateEnd=" + dateto + "&";
        }

        // Add Validation for dates

        /*if (isEmpty(datefrom)) {
            $("#error").show();
            return;
        }*/

        var finalsearchfilter = searchfilter.substr(0, searchfilter.length-1); // Trim the last &
        console.log(finalsearchfilter); 
        ReloadTable(finalsearchfilter);
     });

/* order = 1 Descending order
 order = -1 Ascending order */


    function ReloadTable(finalsearchfilter) {
      
        $('#articles').DataTable({
            "bDestroy": true,
            "pagingType": "full_numbers",
            responsive: true,
            "ordering": true,
            "ajax": {
                type: "GET",
                cache:false,
                url: APIURL + "articles?sort=createdAt&order=1&" + finalsearchfilter,
                contentType: "application/json",
                "dataSrc": function (json) {
                    //console.log(json);
                    var return_data = new Array();
                    for (let index = 0; index < json.data.length; index++) {
                        var id = json.data[index].id;
                        var title = json.data[index].title;
                        var agency = json.data[index].agency;
                        var summary = json.data[index].summary;
                        var name = "";
                        if (!isEmpty(json.data[index].createdBy)) {
                           name = json.data[index].createdBy.name.first+ "  " +json.data[index].createdBy.name.last;
                        }
                        var createdAt = convertToLocalDate(json.data[index].createdAt);
                         return_data[index] = {
                             'articleinfo':"<div class='trending-landing-articles'><div class='trending-left-column'><div class='left-row-one'><div class='left-title-articles'><a href=articles-details-admin-history.html?articleId="+id+">"+title+"</a></div><div class='left-column-tools'></div></div><div class='left-row-two'><div class='left-agency'>"+agency+"</div></div><div class='left-row-three'><div class='left-shortdesc'>"+summary+"</div></div><div class='left-row-four'><div class='left-publish-date'><div class='author'>"+name+"</div></div><div class='left-column-tools'><div class='left-most-pubdate'>"+createdAt+"</div></div></div></div></div>",
                             'lastupdated': convertToLocalDate(json.data[index].createdAt),
                             'views': json.data[index].views,
                             'shares': json.data[index].shares,
                             'id':json.data[index].id
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
                    { "data": "id", "autoWidth": true }, 
            ]
        }); 
    }

    
   

});



