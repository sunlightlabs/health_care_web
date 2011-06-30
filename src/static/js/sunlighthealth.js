$().ready(function() {
    $("div#switcher a").click(function(){
        $("div#iphone img").attr("src", this.href);
        $(this).addClass("active").siblings("a").removeClass("active");
        return false;
    });
});