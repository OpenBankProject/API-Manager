$(document).ready(function ($) {
  // Handle datetime-local inputs for rate limiting
  function initializeDateTimeFields() {
    // Set default values for datetime fields if they're empty
    var fromDateField = $("#from_date");
    var toDateField = $("#to_date");

    // If fields are empty, set default values
    if (!fromDateField.val()) {
      fromDateField.val("2024-01-01T00:00");
    }
    if (!toDateField.val()) {
      toDateField.val("2100-01-01T00:00");
    }
  }

  // Convert ISO datetime strings to datetime-local format for form inputs
  function convertISOToLocalDateTime(isoString) {
    if (!isoString) return "";
    // Remove the 'Z' and convert to local datetime format
    return isoString.replace("Z", "").substring(0, 16);
  }

  // Initialize datetime fields with existing values if they exist
  function setExistingDateTimeValues() {
    var fromDate = $("[data-from-date]").data("from-date");
    var toDate = $("[data-to-date]").data("to-date");

    if (fromDate && fromDate !== "1099-12-31T23:00:00Z") {
      $("#from_date").val(convertISOToLocalDateTime(fromDate));
    }
    if (toDate && toDate !== "1099-12-31T23:00:00Z") {
      $("#to_date").val(convertISOToLocalDateTime(toDate));
    }
  }

  // Form validation
  function validateRateLimitingForm() {
    $("#rateLimitFormElement").on("submit", function (e) {
      var hasError = false;
      var errorMessage = "";

      // Check if any limit values are negative (except -1 which means unlimited)
      $(this)
        .find('input[type="number"]')
        .each(function () {
          var value = parseInt($(this).val());
          if (isNaN(value) || value < -1) {
            hasError = true;
            errorMessage +=
              "Rate limit values must be -1 (unlimited) or positive numbers.\n";
            return false;
          }
        });

      // Check date range
      var fromDate = new Date($("#from_date").val());
      var toDate = new Date($("#to_date").val());

      if (fromDate && toDate && fromDate > toDate) {
        hasError = true;
        errorMessage += "From Date must be before To Date.\n";
      }

      if (hasError) {
        alert(errorMessage);
        e.preventDefault();
        return false;
      }

      // Handle form submission via AJAX
      e.preventDefault();
      submitRateLimitForm();
    });
  }

  // Submit rate limit form via AJAX
  function submitRateLimitForm() {
    var form = $("#rateLimitFormElement");
    var formData = new FormData(form[0]);
    var submitBtn = $("#submitBtn");
    var originalText = submitBtn.text();

    // Disable submit button and show loading
    submitBtn.prop("disabled", true).text("Saving...");

    $.ajax({
      url: window.location.pathname,
      type: "POST",
      data: formData,
      processData: false,
      contentType: false,
      headers: {
        "X-CSRFToken": $("[name=csrfmiddlewaretoken]").val(),
      },
      success: function (response) {
        if (response.success) {
          // Hide form and reload page to show updated data
          hideRateLimitForm();
          window.location.reload();
        } else {
          alert("Error: " + (response.error || "Unknown error occurred"));
        }
      },
      error: function (xhr, status, error) {
        var errorMessage = "Error saving rate limit";
        if (xhr.responseJSON && xhr.responseJSON.error) {
          errorMessage = xhr.responseJSON.error;
        }
        alert(errorMessage);
      },
      complete: function () {
        // Re-enable submit button
        submitBtn.prop("disabled", false).text(originalText);
      },
    });
  }

  // Add visual feedback for current usage status
  function enhanceUsageDisplay() {
    $(".text-info").each(function () {
      var callsMade = parseInt($(this).text().match(/\d+/));
      var parentDiv = $(this).closest(".col-xs-6, .col-sm-3");
      var limitText = parentDiv.find("strong").text().toLowerCase();

      // You could add logic here to highlight usage that's approaching limits
      // For now, we'll just ensure consistent styling
      $(this).addClass("usage-indicator");
    });
  }

  // Initialize all functionality
  initializeDateTimeFields();
  setExistingDateTimeValues();
  validateRateLimitingForm();
  enhanceUsageDisplay();

  // Add tooltips for better UX
  $('[data-toggle="tooltip"]').tooltip();

  // Add help text for rate limiting fields
  $('input[name*="call_limit"]').each(function () {
    $(this).attr(
      "title",
      "Use -1 for unlimited, or enter a positive number for the limit",
    );
  });
});

// Global functions are now defined inline in the template
// This file now only contains form validation and initialization

// Refresh rate limits list
function refreshRateLimits() {
  window.location.reload();
}
