window.check_logged_in = ->
  $.get("/api/user/isloggedin")
    .done (data) ->
      if data['status'] == 0
        console.log(data.message)
      else if data['status'] == 1
        document.location.href = "/problems"

trigger_alert = (message)->
  $("#error-alert").hide().text(message).show().delay(1500).fadeOut()

login = (e) ->
  e.preventDefault()
  $.post("/api/login", $("#login-form").serialize())
  .done (data) ->
    switch data['status']
      when 0
        trigger_alert data['message']
      when 1
        document.location.href = "problems.html"

$ ->
  $("#error-alert").hide()
  $("#login-form").on "submit", login
