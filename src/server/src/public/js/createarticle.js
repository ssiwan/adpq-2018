$(document).ready(function(){

    var role = sessionStorage.getItem("role");
    var token = sessionStorage.getItem("token");
    var agencyid = sessionStorage.getItem("agencyid");
    var agency = sessionStorage.getItem("agency");
    var userid = sessionStorage.getItem("id");
    var articlerole = sessionStorage.getItem("articlerole");
    var articletags = sessionStorage.getItem("articletags");
    var createsimilar = sessionStorage.getItem("createsimilar");


    if(!isEmpty(role) && !isEmpty(token))
 {
           var attachments = [];
            var FileJSON = { "mime":"","name":""};
            var options = "";
           
            if (role === "admin") {
                $("#adminprofile").attr("href","edit-profile-admin.html?userId="+ userid);
            }
            else{
                $("#adminprofile").attr("href","edit-profile-staff.html?userId="+ userid); 
            }


            LoadCreateSimilarData();
            $("#agency").val(agency);
            LoadTags();
            function LoadTags() {
            
                $.ajax({
                    url: APIURL + "suggestedTags",
                    type: 'GET',
                    dataType: 'json',
                    cache:false
                })
                .done(function(response) {
                    if (!isEmpty(response.data)) {
                        for (let index = 0; index < response.data.length; index++) {
                            options += response.data[index].name + ",";
                        }
                        options = options.substring(0, options.length - 1)
                        console.log(options);
                        $('#suggestedtags').importTags(options);
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

            function UploadToS3() {
                var x = document.getElementById("fileattachments");
                console.log(x.files.length);

                for (var file, i = 0; i < x.files.length; i++) {
                    file = x.files[i];
                    //console.log(x.files[i].type);
                    //console.log(x.files[i].name);
                    FileJSON.mime = x.files[i].type;
                    FileJSON.name = x.files[i].name;
                    attachments.push(x.files[i].name);
                    $.ajax({
                        url : APIURL + "preS3",
                        data: JSON.stringify(FileJSON),
                        type : "POST",
                        dataType : "json",
                        headers:{
                            'Authorization':token,
                            'Content-Type' :'application/json'
                        }
                    })
                    .done(function(s3presignedUrl) {
                        console.log(s3presignedUrl);
                        //console.log(file.type);
                        //console.log(file);
                    $.ajax({
                            url : s3presignedUrl.url,
                            method : 'PUT',
                            data : file,
                            headers: {'Content-Type': ''},
                            processData:false
                        })
                        .done(function(){
                            console.log("Success file uploaded " + file.name);
                            
                        })
                        .fail(function(){
                            console.log("S3 file upload failed" + file.name);
                        })
                    })
                }
            }
            
           function LoadCreateSimilarData() {
               if (createsimilar === "1") {
                   console.log(articlerole);
                   //console.log(articletags);
                   document.getElementById('audience').value = articlerole;
                   $('#tags').importTags(articletags);
               }
           }

        $('#tags').tagsInput({
            width: 'auto'
        });


        var article = {
            title:"",
            agencyId:"",
            audience:"",
            shortDesc: "",
            longDesc:"",
            tags: "", 
            attachments:""
        }


        $("#btnSave").click(function(){

            article.title = $("#title").val();
            article.agencyId = agencyid;
            article.audience = $("#audience").val();
            article.shortDesc = $("#shortdesc").val();
            article.longDesc = JSON.stringify(quill.getContents());
            article.tags = $("#tags").val();
            
            
            // Validation
            var errors = "";
            if (isEmpty(article.title)) {
                errors+= "Title is required. \r\n";
            }
            if (isEmpty(article.shortDesc)) {
                errors+= "Short Description is required. \r\n";
            }
            if (isEmpty(article.longDesc)) {
                errors+= "Long Description is required. \r\n";
            }

            if (!isEmpty(errors)) {
                alert(errors);
                return;
            }

            
            UploadToS3();
            article.attachments = attachments;
         console.log("Request JSON" + JSON.stringify(article));
            
            $.ajax({
                url: APIURL + "articles",
                type: 'POST',
                dataType: 'json',
                headers:{
                    'Authorization':token,
                    'Content-Type':'application/json'
                },
                data: JSON.stringify(article)
            })
            .done(function(response) {
                console.log(response);
                console.log(isEmpty(response.status));
                if (!isEmpty(response.status)) {
                    if (response.status === "saved!") {
                        alert("Article created successfully.")
                        setTimeout(function(){ window.location.href = "dashboard-staff.html"; }, 2000);
                    }
                }
                else{
                    alert("There seems to be a problem with saving.Please try again.");
                }
            })
            .fail(function(data, textStatus, xhr) {
                alert("Create article failed");
            });


        });

        $("#btnCancel").click(function() {
            window.location.href = "dashboard-staff.html";
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