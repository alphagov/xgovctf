submit_registration = (e) ->
  e.preventDefault()
  
  registrationData = $("#user-registration-form").serializeObject()
  
  registrationData["create-new-team"] = registrationData["create-new-team"] == "on"
  console.log registrationData
  $.post "/api/user/create", registrationData
  .done (data) ->
    switch data['status']
      when 0
        $("#register-button").apiNotify(data, {position: "right"})
      when 1
        document.location.href = "/login"

$ ->
  $("#user-registration-form").on "submit", submit_registration

  $("#new-team-registration").hide()
  $("#create-new-team").on "change", (e) ->
    $(".team-registration-form").toggle()
