window.check_logged_in = ->
  $.get("/api/isloggedin")
    .done (data) ->
      if data['status'] == 0
        if (typeof(Storage) != "undefined")
          sessionStorage.signInStatus = "notLoggedIn"
        console.log(data.message)
      else if data['status'] == 1
        if (typeof(Storage) != "undefined")
          sessionStorage.signInStatus = "loggedIn"
        document.location.href = "problems.html"

trigger_alert = (message)->
  $("#error-alert").hide().text(message).show().delay(2000).fadeOut()


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
