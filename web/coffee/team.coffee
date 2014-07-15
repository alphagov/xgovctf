renderTeamInformation = _.template($("#team-info-template").remove().text())
renderGroupInformation = _.template($("#group-info-template").remove().text())

load_team_info = ->
  $.get "/api/team"
  .done (data) ->
    switch data["status"]
      when 0
        #TODO: Better error management
        console.log data.message
      when 1
        $("#team-info").html renderTeamInformation({data: data.data})

load_group_info = ->
  $.get "/api/group"
  .done (data) ->
    switch data["status"]
      when 0
        #TODO: Better error management
        console.log data.message
      when 1
        $("#group-info").html renderGroupInformation({data: data.data})

        $("#group-request-form").on "submit", group_request
        $(".leave-team-span").on "click", (e) ->
          leave_group $(e).data("group-name")
          load_group_info()

create_group = (group_name) ->
  $.post "/api/group/create", {"group-name": group_name}
  .done (data) ->
    console.log data.message

join_group = (group_name) ->
  $.post "/api/group/join", {"group-name": group_name}
  .done (data) ->
    console.log data.message

leave_group = (group_name) ->
  $.post "/api/group/leave", {"group-name": group_name}
  .done (data) ->
    console.log data.message

group_request = (e) ->
  e.preventDefault()

  group_name = $("#group-name-input").val()
  action = $("#group-request-action").val()

  switch action
    when "join"
      join_group group_name
    when "create"
      create_group group_name

  load_group_info()

$ ->
  load_team_info()
  load_group_info()
  return
