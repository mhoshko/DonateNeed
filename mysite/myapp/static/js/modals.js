function confirmDeleteModal(id) {
  $('#deleteModal').modal();
  $('#deleteButton').html('<a href="?delete='+id+'" class="btn btn-danger" onclick="return closeDeleteModal('+id+')">Confirm</a>');
}

function closeDeleteModal(id) {
  $('#deleteModal').modal('hide');
  return true
}


function confirmUnfollowModal(id) {
  $('#unfollowModal').modal();
  $('#deleteButton').html('<a href="?delete='+id+'" class="btn btn-danger" onclick="return closeUnfollowModal('+id+')">Confirm</a>');
}

function closeUnfollowModal(id) {
  $('#unfollowModal').modal('hide');
  return true
}
