$(document).ready(function(){
    var role = sessionStorage.getItem("role");
    var token = sessionStorage.getItem("token");
    //console.log(role);
    //console.log(token);
    if(!isEmpty(role) && !isEmpty(token))
    {
        if (role === "admin") {
            $("#adminsettingsbtn").show();
            $("#adminusersbtn").show();
        }

   LoadAnalytics();
   LoadTrendingArticles();
   LoadPublishedArticles();
   LoadWorkflowArticles();

        function LoadAnalytics() {
            $.ajax({
                url: APIURL + "dashboardAnalytics",
                type: 'GET',
                dataType: 'json',
                headers:{
                    'Authorization':token,
                    'Content-Type':'application/json'
                }
            })
            .done(function(response) {
                console.log(response);
                if (!isEmpty(response.data)) {
                    $("#publishCount").append(response.data.publishCount);
                    $("#reviewCount").append(response.data.reviewCount);
                    $("#declineCount").append(response.data.declineCount);
                    $("#viewCount").append(response.data.viewCount);
                    $("#shareCount").append(response.data.shareCount);
                    $("#userCount").append(response.data.userCount);
                }

            })
            .fail(function(data, textStatus, xhr) {
                alert(data.responseJSON.Error);
            });
        }


        function LoadTrendingArticles() {
            $.ajax({
                url: APIURL + "dashboardTrending?limit=3",
                type: 'GET',
                dataType: 'json',
                headers:{
                    'Authorization':token,
                    'Content-Type':'application/json'
                }
            })
            .done(function(response) {
                //console.log(response);
                if (!isEmpty(response.data)) {
                    var j = 1;
                    for (let index = 0; index < response.data.length; index++) {
                        var title = "<a href='articles-details-admin-history.html?articleId="+response.data[index].id+"' target='_blank'>"+ response.data[index].title +"</a>";
                        $("#trendingarticle"+j+"title").append(response.data[index].title);
                        $("#trendingarticle"+j+"views").append(response.data[index].views);
                        $("#trendingarticle"+j+"shares").append(response.data[index].shares);
                        $("#trendingarticle"+j+"agency").append("Agency - " + response.data[index].agency);
                        $("#trendingarticle"+j+"shortdesc").append(response.data[index].summary);
                        $("#trendingarticle"+j+"author").append("Author: " + response.data[index].createdBy.name.first + " " +response.data[index].createdBy.name.last);
                        $("#trendingarticle"+j+"publishdate").append("Publish Date: " + convertToLocalDate(response.data[index].createdAt));
                        j++;
                    }
                   if (response.data.length === 1) {
                       $("#trending2").hide();
                       $("#trending3").hide();
                   }
                   if (response.data.length === 2) {
                       $("#trending3").hide();
                   }

                   if (response.data.length === 0) {
                        $("#trending1").hide();
                        $("#trending2").hide();
                        $("#trending3").hide();
                   }                 
                }
            })
            .fail(function(data, textStatus, xhr) {
                alert("trending articles endpoint error");
            });
        }
     
        function LoadPublishedArticles() {
            $.ajax({
                url: APIURL + "dashboardMyPublished?limit=3",
                type: 'GET',
                dataType: 'json',
                headers:{
                    'Authorization':token,
                    'Content-Type':'application/json'
                }
            })
            .done(function(response) {
                console.log(response);
            var str = "";
            if (!isEmpty(response.data)) {
            
            for (let index = 0; index < response.data.length; index++) {
                    var title= " ";
                    var agency= " ";
                    var author= " ";
                    var publishdate= " ";
                    var updateddate = " ";
                    var views= " ";
                    var shares= " ";
                    var shortdesc = " ";
                if (!isEmpty(response.data[index].title)) {
                    title = "<a href='articles-details-admin-history.html?articleId="+response.data[index].id+"' target='_blank'>"+ response.data[index].title +"</a>";
                } 
                if (!isEmpty(response.data[index].agency)) {
                    agency = "Agency - " + response.data[index].agency;
                } 
                if (!isEmpty(response.data[index].summary)) {
                    shortdesc = response.data[index].summary;
                } 

                if (!isEmpty(response.data[index].createdBy.name.first)) {
                    author = "Author: " + response.data[index].createdBy.name.first;
                }
                if (!isEmpty(response.data[index].createdBy.name.last)) {
                    author += " " + response.data[index].createdBy.name.last;
                }
                if (!isEmpty(response.data[index].createdAt)) {
                    publishdate = convertToLocalDate(response.data[index].createdAt);
                }
                
                if (!isEmpty(response.data[index].lastUpdated)) {
                    updateddate = convertToLocalDate(response.data[index].lastUpdated);
                }
                
                    views = response.data[index].views;
                    shares = response.data[index].shares;
                

                str += "<div class='trending-row-one'><div class='trending-left-column'><div class='left-row-one'><div class='left-title'>"+ title + "</div><div class='left-column-tools'></div></div><div class='left-row-two'><div class='left-agency'>"+ agency + "</div></div><div class='left-row-three'><div class='left-shortdesc'>"+shortdesc+"</div></div><div class='left-row-four'><div class='left-publish-date'><div class='author'>"+author+"</div></div><div class='left-column-tools'><div class='left-most-pubdate'>"+ publishdate +"</div></div></div></div><div class='trending-right-column'><div class='tools-total-update'>"+updateddate + "</div><div class='tools-total-views'>" + views + "</div><div class='tools-total-shares'>" + shares + "</div></div></div>";
                //console.log(str);
                }
            $("#publishedarticles").append(str);
            }

            })
            .fail(function(data, textStatus, xhr) {
                alert("publish arrticles endpoint error");
            });
        } 

        function LoadWorkflowArticles() {
            $.ajax({
                url: APIURL + "dashboardWorkflow?limit=3",
                type: 'GET',
                dataType: 'json',
                headers:{
                    'Authorization':token,
                    'Content-Type':'application/json'
                }
            })
            .done(function(response) {
                //console.log(response);
            var strwf = " ";
            
            if (!isEmpty(response.data)) {
            for (let index = 0; index < response.data.length; index++) {
                    var title= " ";
                    var agency= " ";
                    var author= " ";
                    var publishdate= " ";
                    var articlestatus= "";
                    var shortdesc = " ";
                if (!isEmpty(response.data[index].title)) {
                    title = "<a href='articles-details-admin-history.html?articleId="+response.data[index].id+"' target='_blank'>"+ response.data[index].title +"</a>";
                } 
                if (!isEmpty(response.data[index].agency)) {
                    agency = "Agency - " + response.data[index].agency;
                } 
                if (!isEmpty(response.data[index].summary)) {
                    shortdesc = response.data[index].summary;
                } 
                if (!isEmpty(response.data[index].createdBy.name.first)) {
                    author = "Author: " + response.data[index].createdBy.name.first;
                }
                if (!isEmpty(response.data[index].createdBy.name.last)) {
                    author += " " + response.data[index].createdBy.name.last;
                }
                if (!isEmpty(response.data[index].createdAt)) {
                    publishdate = convertToLocalDate(response.data[index].createdAt);
                }
                if (response.data[index].status===0) {
                    articlestatus = "pending";  
                }

                if (response.data[index].status===1) {
                    articlestatus = "published";  
                }
                if (response.data[index].status===2) {
                    articlestatus = "declined";  
                }
                
                strwf += "<div class='trending-row-one'><div class='trending-left-column'><div class='left-row-one'><div class='left-title'>"+title+"</div><div class='left-column-tools'></div></div><div class='left-row-two'><div class='left-agency'>"+agency+"</div></div><div class='left-row-three'><div class='left-shortdesc'>"+shortdesc+"</div></div><div class='left-row-four'><div class='left-publish-date'><div class='author'>"+author+"</div></div><div class='left-column-tools'><div class='left-most-pubdate'>"+publishdate+"</div></div></div></div><div class='trending-right-column'><div class='article-status'>"+articlestatus+"</div></div></div>";
                }
            $("#workflowarticles").append(strwf);
            }
            

            })
            .fail(function(data, textStatus, xhr) {
               //console.log(xhr);
                alert("Workflow endpoint error");
            });
        } 


    }
    else {
        window.location.href = "index.html";
    }
     



});