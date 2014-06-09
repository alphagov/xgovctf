window.load_team_info = ->
  $.ajax(type: "GET", cache: false, url: "/api/team", dataType: "json")
   .done (response) -> 
        console.log(response.data)
        html = ""
        html += "Your team is " + response.data.team_name # JB: XSS check needed
        $("#team_info_holder").html html