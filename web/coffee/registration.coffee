submit_registration = (e) ->
  e.preventDefault()
  $.post "/api/user/create", $("#user-registration-form").serialize()
  .done (data) ->
    $("#message-box").html(data.message)

$ ->
  $("#user-registration-form").on "submit", submit_registration

  $("#new-team-registration").hide()
  $("#create-new-team").on "change", (e) ->
    $(".team-registration-form").toggle()
