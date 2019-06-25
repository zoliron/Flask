var myVar;

function myFunction() {
  myVar = setTimeout(showPage, 3000);
}

function showPage() {
  document.getElementById("loader").style.display = "none";
  document.getElementById("myDiv").style.display = "block";
}

$(function(){
    $('.loadingBtn').click(function(){
          var $this = $(this);
          $this.button('loading');
          setTimeout(function(){
            $this.button('reset'); }, 30000);
    });
});