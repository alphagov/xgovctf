window.logout = ->
  apiCall "GET", "/api/user/logout"
  .done (data) ->
    document.location.href = "/"
