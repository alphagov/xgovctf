
apiOffline =
  News: "/news"

userLoggedIn =
  Problems: "/problems"
  Team: "/team"
  Scoreboard: "/scoreboard"
  Logout: "/api/user/logout"

userNotLoggedIn =
  Registration: "/registration"
  Login: "/login"
  Scoreboard: "/scoreboard"

load_navbar = (renderNavbarLinks) ->
  apiCall "GET", "/api/user/isloggedin", {}

  .done (data) ->
    navLinks = userNotLoggedIn
    if data["status"] == 1
      navLinks = userLoggedIn

    $("#navbar-links").html renderNavbarLinks({links: navLinks})

  .fail ->
    $("#navbar-links").html renderNavbarLinks({links: apiOffline})

$ ->
  renderNavbarLinks = _.template($("#navbar-links-template").remove().text())
  load_navbar(renderNavbarLinks)
