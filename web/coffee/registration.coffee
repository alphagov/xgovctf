submit_registration = (e) ->
  e.preventDefault()
  $.post "/api/user/create", $("#user-registration-form").serialize()
  .done (data) ->
    switch data['status']
      when 0
        $("#register-button").apiNotify(data, {position: "right"})
      when 1
        document.location.href = "/"

$ ->
  $("#user-registration-form").on "submit", submit_registration

  $("#new-team-registration").hide()
  $("#create-new-team").on "change", (e) ->
    $(".team-registration-form").toggle()
