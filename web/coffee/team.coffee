renderTeamInformation = _.template($("#team-info-template").remove().text())

load_team_info = ->
  $.get "/api/team"
  .done (data) ->
    switch data["status"]
      when 0
        #TODO: Better error management
        console.log data.message
      when 1
        $("#team-info").html renderTeamInformation({data: data.data})
  
$ ->
  load_team_info()
