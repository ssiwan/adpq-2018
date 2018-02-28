$(document).ready(function(){
    var role = sessionStorage.getItem("role");
    var token = sessionStorage.getItem("token");
    console.log(role);
    console.log(token);
    if(!isEmpty(role) && !isEmpty(token)){
        if (role === "admin") {
            $("#adminsettingsbtn").show();
            $("#adminusersbtn").show();
        }

     // Analytics Area
     /*
     GET: http://adpq-staging.hotbsoftware.com/api/v1/dashboardAnalytics
       {
    "data": {
        "publishCount": 0,
        "reviewCount": 0,
        "declineCount": 0,
        "viewCount": 0,
        "shareCount": 0,
        "userCount": 4
    }
}
    */
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
            console.log(response);
            if (!isEmpty(response.data)) {
                if (!isEmpty(response.data.mostTagged)) {
                     // Most Tagged
                $("#trendingarticle1title").append(response.data.mostTagged.title);
                $("#trendingarticle1tagcount").append(response.data.mostTagged.tagCount);
                $("#trendingarticle1agency").append("Agency - " + response.data.mostTagged.agency);
                $("#trendingarticle1shortdesc").append(response.data.mostTagged.summary);
                $("#trendingarticle1author").append("Author: " + response.data.mostTagged.createdBy.name.first + " " + response.data.mostTagged.createdBy.name.last);
                $("#trendingarticle1publishdate").append("Publish Date: " + convertToLocalDate(response.data.mostTagged.createdAt));
                }
                else {
                    $("#trending1").hide();
                }
                // Most Viewed
               
                if (!isEmpty(response.data.mostViewed)) {
                    $("#trendingarticle2title").append(response.data.mostViewed.title);
                    $("#trendingarticle2viewcount").append(response.data.mostViewed.views);
                    $("#trendingarticle2agency").append("Agency - " + response.data.mostViewed.agency);
                    $("#trendingarticle2shortdesc").append(response.data.mostViewed.summary);
                    $("#trendingarticle2author").append("Author: " + response.data.mostViewed.createdBy.name.first + " " + response.data.mostViewed.createdBy.name.last);
                    $("#trendingarticle2publishdate").append("Publish Date: " + convertToLocalDate(response.data.mostViewed.createdAt));
                
                } else {
                    $("#trending2").hide();
                }
             // Most Shared
                if (!isEmpty(response.data.mostShared)) {
                        $("#trendingarticle3title").append(response.data.mostShared.title);
                        $("#trendingarticle3sharescount").append(response.data.mostShared.sharedCount);
                        $("#trendingarticle3agency").append("Agency - " + response.data.mostShared.agency);
                        $("#trendingarticle3shortdesc").append(response.data.mostShared.summary);
                        $("#trendingarticle3author").append("Author: " + response.data.mostShared.createdBy.name.first + " " + response.data.mostShared.createdBy.name.last);
                        $("#trendingarticle3publishdate").append("Publish Date: " + convertToLocalDate(response.data.mostShared.createdAt)); 
                } else {
                    $("#trending3").hide();
                }
            }

        })
        .fail(function(data, textStatus, xhr) {
            alert(data.responseJSON.Error);
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
                title = response.data[index].title;
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
                shares = response.data[index].sharedCount;
               

               str += "<div class='trending-row-one'><div class='trending-left-column'><div class='left-row-one'><div class='left-title'>"+ title + "</div><div class='left-column-tools'></div></div><div class='left-row-two'><div class='left-agency'>"+ agency + "</div></div><div class='left-row-three'><div class='left-shortdesc'>"+shortdesc+"</div></div><div class='left-row-four'><div class='left-publish-date'><div class='author'>"+author+"</div></div><div class='left-column-tools'><div class='left-most-pubdate'>"+ publishdate +"</div></div></div></div><div class='trending-right-column'><div class='tools-total-update'>"+updateddate + "</div><div class='tools-total-views'>" + views + "</div><div class='tools-total-shares'>" + shares + "</div></div></div>";
               //console.log(str);
            }
           $("#publishedarticles").append(str);
           

        })
        .fail(function(data, textStatus, xhr) {
            alert(data.responseJSON.Error);
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
            console.log(response);
           var strwf = " ";
           
           
           for (let index = 0; index < response.data.length; index++) {
                var title= " ";
                var agency= " ";
                var author= " ";
                var publishdate= " ";
                var articlestatus= "";
                var shortdesc = " ";
               if (!isEmpty(response.data[index].title)) {
                title = response.data[index].title;
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

               if (!isEmpty(response.data[index].status)) {
                if (response.data[index].status===0) {
                    articlestatus = "New/In Review";  
                }

                if (response.data[index].status===1) {
                    articlestatus = "Published";  
                }
                if (response.data[index].status===2) {
                    articlestatus = "Declined";  
                }
               }
               console.log(articlestatus);
               strwf += "<div class='trending-row-one'><div class='trending-left-column'><div class='left-row-one'><div class='left-title'>"+title+"</div><div class='left-column-tools'></div></div><div class='left-row-two'><div class='left-agency'>"+agency+"</div></div><div class='left-row-three'><div class='left-shortdesc'>"+shortdesc+"</div></div><div class='left-row-four'><div class='left-publish-date'><div class='author'>"+author+"</div></div><div class='left-column-tools'><div class='left-most-pubdate'>"+publishdate+"</div></div></div></div><div class='trending-right-column'><div class='article-status'>"+articlestatus+"</div></div></div>";
               //console.log(strwf);
            }
           $("#workflowarticles").append(strwf);
           

        })
        .fail(function(data, textStatus, xhr) {
            alert(data.responseJSON.Error);
        });
    } 


    }
    else {
        window.location.href = "index.html";
    }
     



});