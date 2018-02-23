$(document).ready(function(){
    LoadAgencies();
    SuggestedTitles();
    //UploadToS3();



    function UploadToS3() {
        $("input[type=file]").onchange = function () {
            for (var file, i = 0; i < this.files.length; i++) {
                file = this.files[i];
                $.ajax({
                    url : s3presignedApiUri,
                    data: 'file='+ file.name + '&mime=' + file.type,
                    type : "GET",
                    dataType : "json",
                    cache : false,
                })
                .done(function(s3presignedUrl) {
                    $.ajax({
                        url : s3presignedUrl,
                        type : "PUT",
                        data : file,
                        dataType : "text",
                        cache : false,
                        contentType : file.type,
                        processData : false
                    })
                    .done(function(){
                        console.info('YEAH', s3presignedUrl.split('?')[0].substr(6));
                    })
                    .fail(function(){
                        console.error('damn...');
                    })
                })
            }
        };
    }


    function SuggestedTitles() {
        $("#title").autocomplete({
            source: function (request, response) {
                $.ajax({
                    url: APIURL + "agencies", // Change to suggested title endpoint
                    data: { term: request.term },
                    dataType: 'json',
                    type: 'GET',
                    cache:false,
                    contentType: "application/json; charset=utf-8",
                    success: function (result) {
                        var agencyarr = new Array();
                        for (let index = 0; index < result.data.length; index++) {
                            agencyarr.push(result.data[index].name);
                        }
                        response(agencyarr);
                    },
                    error: function (data) {
                        console.log(data);
                    }
                });
            },
            minLength: 2
        });
    }

    function LoadAgencies() {
        var options = $("#agency");
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


var article = {
    title:"",
    agencyid:"",
    audience:"",
    type:"",
    shortdesc: "",
    longdesc:"",
    tags: "",
    URLs:""
}


$("#btnSave").click(function(){

    // Add Validation
article.title = $("#title").val();
article.agencyid = $("#agency").val();
article.audience = $("#audience").val();
article.type = $("#articletype").val();
article.shortdesc = $("#shortdesc").val();
article.longdesc = JSON.stringify(quill.getContents());
article.tags = $("#tags").val();
//article.URLs = $("#articletype").val();

console.log("Request JSON" + JSON.stringify(article));
    
    /*$.ajax({
        url: APIURL + "article",
        type: 'POST',
        dataType: 'json',
        headers:{
            'Authorization':sessionStorage.getItem("token"),
            'Content-Type':'application/json'
        },
        data: JSON.stringify(article)
      })
      .done(function(response) {
        if (!isEmpty(response.data)) {
        }
        else{
            alert(response.error);
        }
      })
      .fail(function(data, textStatus, xhr) {
        alert(data.responseJSON.Error);
      });*/


});





});