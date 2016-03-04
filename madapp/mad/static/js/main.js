$(document).ready(function() {
  $.get("./templates/menu.html", function(data) { 
    $("#navigation-menu").append(data); 
    var page = window.location.href.slice(window.location.href.lastIndexOf("/")+1);
    $("a[href*='" + page + "']").parent().addClass("active");
  });
});
$(document).ready(function() {
  $.get("leftmenu.html", function(data) { 
    $("#leftmenu-menu").append(data);
    var page = window.location.href.slice(window.location.href.lastIndexOf("/")+1); 
    $("a[href*='" + page + "']").parent().addClass("active");
  });
});
