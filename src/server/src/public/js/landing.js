
// GET ALL AGENCIES
$(document).ready(function(){

  /*   $("#txtsearch").keypress(function(event) {
        if (event.which == 13) {
            event.preventDefault();
            $("#btnsearch").click();
        }
    }); */
    $("#btnArticles").click(function(){
        //sessionStorage.removeItem("searchValue");
        window.location.href = "articles.html";
    });

   /*  $("#btnsearch").click(function(){
        if (typeof(Storage) !== "undefined") {
            sessionStorage.setItem("searchValue", $("#txtsearch").val());
        }
        window.location.href = "articles.html";
    });    */
});