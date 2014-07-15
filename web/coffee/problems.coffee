renderProblemList = _.template($("#problem-list-template").remove().text())
renderProblem = _.template($("#problem-template").remove().text())

submitProblem = (e) ->
  e.preventDefault()
  input = $(e.target).find("input")
  $.post("/api/problems/submit", {pid: input.data("pid"), key: input.val()})
  .done (data) ->
    console.log data
    switch data["status"]
      when 0
        console.log data.message
        alert data.message
      when 1
        console.log data.message
        alert data.message
    loadProblems()


loadProblems = ->
  $.get "/api/problems"
  .done (data) ->
    switch data["status"]
      when 0
        #TODO: Better error management
        alert data.message
      when 1
        $("#problem-list-holder").html renderProblemList({problems: data.data, renderProblem: renderProblem})
        $(".problem-submit").on "submit", submitProblem

$ ->
  loadProblems()
