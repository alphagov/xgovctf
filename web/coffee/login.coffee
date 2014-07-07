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

login = (e) ->
  e.preventDefault()
  $.post("/api/login", $("#login-form").serialize())
  .done (data) ->
    switch data['status']
      when 0
        if (typeof(Storage) != "undefined")
          sessionStorage.signInStatus = "notLoggedIn"
        $("#error-alert").hide().text(data["message"]).show().delay(2000).fadeOut()
      when 1
        if (typeof(Storage) != "undefined")
          sessionStorage.signInStatus = "loggedIn"
        document.location.href = "problems.html"
      when 2
        if (typeof(Storage) != "undefined")
          sessionStorage.signInStatus = "notLoggedIn"
        console.log(data.message)

$ ->
  $("#error-alert").hide()
  $("#login-form").on "submit", login
