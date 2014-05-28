clear = ->
  $('#reg-'+field).val('') for field in fields

getRegData = ->
  post = {}
  post[field] = $('#reg-'+field).val() for field in fields
  return post

window.submit_registration = ->
  console.log("submit_registration function")
  post = getRegData()
  console.log(post)
  $.ajax(type: 'POST', url: '/api/register', dataType: 'json', data: post)
  .done (data) ->
    if data['status'] == 0      
      console.log(data.message)
    else if data['status'] == 1
      clear()
      console.log(data.message)

$(document).ready ->
  $('#reg-email').focus()