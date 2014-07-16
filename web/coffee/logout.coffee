window.logout = ->
  apiCall "GET", "/api/user/logout"
  .done (data) ->
    switch data['status'] 
      when 1
        document.location.href = "/"
      when 0
        document.location.href = "/login"
