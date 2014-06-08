window.handle_submit = (prob_id) ->
  $.ajax(
    type: "POST"
    cache: false
    url: "/api/submit"
    dataType: "json"
    data:
      pid: prob_id
      key: $("#" + prob_id).val()
      viewer: "basic"
  ).done (data) ->
    prob_msg = $("#msg_" + prob_id)
    alert_class = ""
    if data["status"] is 0
      alert_class = "alert-error"      
    else if data["status"] is 1
      alert_class = "alert-success"      
    prob_msg.hide().html("<div class=\"alert " + alert_class + "\">" + data["message"] + "</div>").slideDown("normal")
    setTimeout (->
      prob_msg.slideUp "normal", ->
        prob_msg.html("").show()
        window.location.reload() if data["status"] is 1              
    ), 2500

window.redirect_if_not_logged_in = ->
  $.ajax(
    type: "GET"
    url: "/api/isloggedin"
    cache: false
  ).done((data) ->
    window.location.href = "/login" if data["success"] is 0 
  ).fail ->
    window.location.href = "/"    