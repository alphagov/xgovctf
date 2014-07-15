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

window.apiNotify = (data) ->
  style = "info"
  if data.status == 0
    style = "error"

  $.notify data.message, style

$.fn.apiNotify = (data, configuration) ->
  style = "info"
  if data.status == 0
    style = "error"
  configuration["className"] = style

  return $(this).notify(message, configuration)
