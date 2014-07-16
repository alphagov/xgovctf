renderScoreboardTabs = _.template($("#scoreboard-tabs-template").remove().text())
renderScoreboard = _.template($("#scoreboard-template").remove().text())

load_scoreboard = ->
  apiCall "GET", "/api/scoreboard", {}
  .done (data) ->
    $("#scoreboard-tabs").html renderScoreboardTabs({
      data: data.data
      renderScoreboard: renderScoreboard
    })

$ ->
  load_scoreboard()
