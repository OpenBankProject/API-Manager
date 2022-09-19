$(document).ready(function ($) {
    $(".runner button.forSave").click(function (e) {
      e.preventDefault();
      var t = $(this);
      var runner = t.parent().parent().parent();
      var web_ui_props_name = $(runner).find(".web_ui_props_name").text();
      var web_ui_props_value = $(runner).find(".web_ui_props_value").val();
      $(".runner button.forSave").attr("disabled", "disabled");
      $(".runner button.forDelete").attr("disabled", "disabled");
      $.post(
        "save/method",
        {
          web_ui_props_name: web_ui_props_name,
          web_ui_props_value: web_ui_props_value,
        },
        function (response) {
          location.reload();
        }
      );
    });

    $(".runner button.forDelete").click(function (e) {
      e.preventDefault();
      var t = $(this);
      var runner = t.parent().parent().parent();
      var web_ui_props_name = $(runner).find(".web_ui_props_name").text();
      var textArea = runner.find(".web_ui_props_value");
      var props_id = $(runner).find(".web_ui_props_id");
      var web_ui_props_id = props_id.val();
      var webui = $("#webui");
      $(".runner button.forSave").attr("disabled", "disabled");
      $(".runner button.forDelete").attr("disabled", "disabled");
      $.post(
        "delete/method",
        {
          web_ui_props_id: web_ui_props_id,
        },
        function (response) {
          location.reload();
        }
      );
    });
    $(".runner button.forCreate").click(function (e) {
      e.preventDefault();
      var t = $(this);
      var runner = t.parent().parent().parent();
      var web_ui_props_name = $(runner).find(".web_ui_props_name").text();
      var languages = $(runner).find(".language").val();

      if (languages == "es") {
        $(runner)
          .find(".language_list")
          .text("_" + languages);
      } else {
        $(runner).find(".language_list").text("");
      }
    });
  });