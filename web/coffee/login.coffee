window.check_logged_in = ->
    $.ajax(type: "GET", cache: false, url: "/api/isloggedin")
      .done (data) ->
        if data['status'] == 0
          if (typeof(Storage) != "undefined")
            sessionStorage.signInStatus = "notLoggedIn"
          console.log(data.message)
        else if data['status'] == 1
          if (typeof(Storage) != "undefined")
            sessionStorage.signInStatus = "loggedIn"
          document.location.href = "problems.html"

window.submit_login = ->
  $.ajax(type: "POST", cache: false, url: "/api/login", dataType: "json", data: {'username': $("#login-username").val(), 'password': $("#login-password").val()})
  .done (data) ->
    if data['status'] == 0
      if (typeof(Storage) != "undefined")
        sessionStorage.signInStatus = "notLoggedIn"
#$('#error-alert').text(data['message']).show().delay(3000).fadeOut()
      console.log(data.message)
    else if data['status'] == 1
      if (typeof(Storage) != "undefined")
        sessionStorage.signInStatus = "loggedIn"
      document.location.href = "problems.html"
    else if data['status'] == 2
      if (typeof(Storage) != "undefined")
        sessionStorage.signInStatus = "notLoggedIn"
      console.log(data.message)
