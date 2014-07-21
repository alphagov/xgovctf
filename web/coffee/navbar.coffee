
apiOffline =
  News: "/news"

userLoggedIn =
  Problems: "/problems"
  Team: "/team"
  Scoreboard: "/scoreboard"
  About:
    FAQ: "/faq"
    Sponsors: "/sponsors"
    News: "/news"
  Logout: "/logout"

userNotLoggedIn =
  Registration: "/registration"
  Scoreboard: "/scoreboard"
  About:
    FAQ: "/faq"
    Sponsors: "/sponsors"
    News: "/news"
  Login: "/login"


loadNavbar = (renderNavbarLinks, renderNestedNavbarLinks) ->

  navbarLayout = {
    renderNavbarLinks: renderNavbarLinks,
    renderNestedNavbarLinks: renderNestedNavbarLinks
  }

  apiCall "GET", "/api/user/isloggedin", {}
  .done (data) ->
    navbarLayout.links = userNotLoggedIn

    if data["status"] == 1
      navbarLayout.links = userLoggedIn

    $("#navbar-links").html renderNavbarLinks(navbarLayout)

  .fail ->
    navbarLayout.links = apiOffline
    console.log(navbarLayout)
    $("#navbar-links").html renderNavbarLinks(navbarLayout)

$ ->
  renderNavbarLinks = _.template($("#navbar-links-template").remove().text())
  renderNestedNavbarLinks = _.template($("#navbar-links-dropdown-template").remove().text())

  loadNavbar(renderNavbarLinks, renderNestedNavbarLinks)
