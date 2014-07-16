
apiOffline =
  News: "/news"

userLoggedIn =
  Problems: "/problems"
  Team: "/team"
  Logout: "/logout"

userNotLoggedIn =
  Registration: "/registration"
  Login: "/login"

loadNavbar = (renderNavbarLinks) ->
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
  loadNavbar(renderNavbarLinks)
