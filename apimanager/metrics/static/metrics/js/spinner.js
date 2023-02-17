$(document).ready(function () {
    $('.spinner').on('click', function() {
        var e=this;
        setTimeout(function() {
            e.innerHTML='<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Loading...';
            e.disabled=true;
        },0);
        return true;
    });
});
