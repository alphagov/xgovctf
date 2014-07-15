window.apiCall = (type, url, data) ->
  $.ajax {url: url, type: type, data: data, cache: false}
  .fail (jqXHR, text) ->
    $.notify "API is offline. :(", "error"

window.redirectIfNotLoggedIn = ->
  apiCall "GET", "/api/user/isloggedin", {}
  .done (data) ->
    switch data["status"]
      when 0
        window.location.href = "/login"

