submit_registration = (e) ->
  e.preventDefault()
  $.post "/api/user/create", $("#user-registration-form").serialize()
  .done (data) ->
    $("#message-box").html(data.message)

$(document).ready ->
  $('#user-registration-form').on "submit", submit_registration
