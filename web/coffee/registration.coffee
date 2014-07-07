fields = ['email', 'username', 'password', 'team-name-new', 'team-password-new', 'team-school-new', 'team-adv-name-new', 'team-adv-email-new', 'team-name-existing', 'team-password-existing', 'create-new-team']

clear = ->
  $('#reg-'+field).val('') for field in fields

getRegData = ->
  post = {}
  post[field] = $('#reg-'+field).val() for field in fields
  post['create-new-team'] = $('#reg-create-new-team').is(':checked')
  return post

window.submit_registration = ->
  console.log("submit_registration function")
  post = getRegData()
  console.log(post)
  $.ajax(type: 'POST', url: '/api/user/create', dataType: 'json', data: post)
  .done (data) ->
    if data['status'] == 0
      console.log(data.message)
      $('#message-box').html(data.message)
    else if data['status'] == 1
      clear()
      console.log(data.message)
      $('#message-box').html(data.message)
    else
      console.log(data.message)
      $('#message-box').html(data.message)

$(document).ready ->
  $('#reg-email').focus()
