$(document).ready(function($) {
    // Select a language from navbar which want to change.
    var currentURL = window.location.href;
        const element = document.getElementById('gb')
        element.addEventListener("click", () => {
            if (currentURL.includes("/es/")) {
                location.href = currentURL.split("/es/")[0] + "/en/" + currentURL.split("/es/")[1]
            }
        });
        const element1 = document.getElementById('es')
        element1.addEventListener("click", () => {
            if (currentURL.includes("/en/")) {
                location.href = currentURL.split("/en/")[0] + "/es/" + currentURL.split("/en/")[1]
            }
    });
	$('table.tablesorter').tablesorter();
	$('#authentication-select').change(function() {
		$('.authentication-method').hide();
		let method = $(this).val();
		$(`#authenticate-${method}`).show();
	});
});

// Redirect to API-Explorer, just click on Try Ii button in API-Collection and Dynamic Endpoint after success response.
function redirect_api_explorer_url(api_explorer_url) {
     var currentURL = window.location.href.split("/");
     if (currentURL[3] == "en") {
        location.href = api_explorer_url + "&locale=en_GB";
        }
     else {
        location.href = api_explorer_url + "&locale=es_ES";
     }
  }
