window.check_logged_in = ->
  $.get("/api/user/isloggedin")
    .done (data) ->
      if data['status'] == 1
        document.location.href = "/problems"

login = (e) ->
  e.preventDefault()
  $.post("/api/login", $("#login-form").serialize())
  .done (data) ->
    switch data['status']
      when 0
        $("#login-button").notify(data['message'], {position: "right"})
      when 1
        document.location.href = "/problems"

$ ->
  $("#error-alert").hide()
  $("#login-form").on "submit", login
