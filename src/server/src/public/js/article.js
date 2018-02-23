$(document).ready(function(){
    var table;
    var agencychk = $('#chkAgency');
    var tagschk = $('#chkTags');
    var datechk = $('#chkDate');
    var url = "";
    //var APIKey = "";

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
            changeMonth: true,
            numberOfMonths: 1
          })
          .on("change", function() {
            to.datepicker("option", "minDate", getDate(this));
          }),
        to = $("#to").datepicker({
          changeMonth: true,
          numberOfMonths: 1
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
            "pagingType": "full_numbers",
            "ajax": {
                type: "GET",
                url: url,
                cache:false,
               contentType: "application/json;",
               "dataSrc": function (json) {
                   //console.log(json);
                   var return_data = new Array();
                   for (let index = 0; index < json.data.length; index++) {
                        return_data[index] = {
                            'articleinfo': "<strong>" + json.data[index].title + "</strong><br/>"
                                             + "<strong>Agency:" + json.data[index].agency + "</strong><br/>" 
                                             + json.data[index].summary + "<br/>" 
                                             + "<strong>Author: </strong>" + json.data[index].createdBy + "<br/>"
                                             + "PublishedDate:</strong> " + convertToLocalDate(json.data[index].createdAt),
                            'lastupdated': convertToLocalDate(json.data[index].createdAt),
                            'views': json.data[index].views,
                            'shares': json.data[index].sharedCount,
                        }
                   }
                   //console.log(return_data);
                   return return_data;
               }
        },
        /*"columnDefs": [
            {
                "targets": [ 2 ],
                "visible": false,
                "searchable": false
            }
        ],*/
            "columns": [
                    { "data": "articleinfo", "autoWidth": true },
                    { "data": "lastupdated", "autoWidth": true },
                    { "data": "views", "autoWidth": true },
                    { "data": "shares", "autoWidth": true },      
            ]
        }); 
    }
    

    /*$('#agencies').delegate('tbody tr', 'click', function () {
        console.log("AgencyId  " + table.row(this).data().id);
        //window.location.href = "agencyarticle.html";
    });

    $("#btnReload").click(function(){
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
            console.log($("#from").val());
            console.log($("#to").val());
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
            "ajax": {
                type: "GET",
                cache:false,
                url: APIURL + "articles?sort=createdAt&order=1&" + finalsearchfilter,
                contentType: "application/json",
                "dataSrc": function (json) {
                    //console.log(json);
                    var return_data = new Array();
                    for (let index = 0; index < json.data.length; index++) {
                         return_data[index] = {
                             'articleinfo': "<strong>" + json.data[index].title + "</strong><br/>"
                                              + "<strong>Agency: " + json.data[index].agency + "</strong><br/>" 
                                              + json.data[index].summary + "<br/>" 
                                              + "<strong>Author: " + json.data[index].createdBy + "</strong><br/>"
                                              + "PublishedDate: " + convertToLocalDate(json.data[index].createdAt),
                             'lastupdated': convertToLocalDate(json.data[index].createdAt),
                             'views': json.data[index].views,
                             'shares': json.data[index].sharedCount,
                         }
                    }
                    //console.log(return_data);
                    return return_data;
                }
                
        },
        "columns": [
            { "data": "articleinfo", "autoWidth": true },
            { "data": "lastupdated", "autoWidth": true },
            { "data": "views", "autoWidth": true },
            { "data": "shares", "autoWidth": true },      
    ]
        }); 
    }
});