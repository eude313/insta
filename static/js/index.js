// Get the sidebar
function toggleNav() {
  var sidepanel = document.getElementById("mySidepanel");
  if (sidepanel.style.display === "block") {
    sidepanel.style.display = "none";
  } else {
    sidepanel.style.display = "block";
  }
}


// Get the modal
var modal = document.getElementById("myModal");
var btn = document.getElementById("myBtn");
var span = document.getElementsByClassName("close")[0];

btn.onclick = function () {
  modal.style.display = "block";
};

span.onclick = function () {
  modal.style.display = "none";
};

window.onclick = function (event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
};
// modal form
$(document).ready(function() {
  $('#uploadForm').submit(function(event) {
      event.preventDefault();

      // Disable the submit button to prevent multiple submissions
      $('#submitBtn').prop('disabled', true);
      $('#myModal').prrop('display', none)
      var formData = new FormData();
      formData.append('images', $('#imagesInput')[0].files[0]);
      formData.append('location', $('#locationInput').val());
      formData.append('captions', $('#captionsInput').val());

      // Include the CSRF token in the AJAX request headers
      var csrftoken = getCookie('csrftoken');
      $.ajax({
          url: '{% url "upload" %}',
          type: 'POST',
          data: formData,
          processData: false,
          contentType: false,
          beforeSend: function(xhr, settings) {
              xhr.setRequestHeader("X-CSRFToken", csrftoken);
          },
          success: function(response) {
              alert(response.message); 
              $('#uploadForm')[0].reset();
              $('#submitBtn').prop('disabled', false);
          },
          error: function(xhr, status, error) {
              var errorMessage = xhr.responseJSON ? xhr.responseJSON.error : 'An error occurred.';
              alert(errorMessage); // Show error message
              // Enable the submit button
              $('#submitBtn').prop('disabled', true);
          }
      });
  });
});

// Function to get CSRF cookie value
function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie !== '') {
      var cookies = document.cookie.split(';');
      for (var i = 0; i < cookies.length; i++) {
          var cookie = cookies[i].trim();
          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
}



// JavaScript code to handle the search functionality
document.addEventListener("DOMContentLoaded", function() {
  const searchForm = document.getElementById('searchForm');
  const searchInput = document.getElementById('searchInput');
  const searchResults = document.getElementById('searchResults');

  searchForm.addEventListener('submit', async function(event) {
      event.preventDefault();
      const query = searchInput.value.trim();
      if (query.length > 0) {
          try {
              const response = await fetch(`/search/profiles?q=${query}`);
              const profiles = await response.json();
              displaySearchResults(profiles);
          } catch (error) {
              console.error('Error fetching search results:', error);
          }
      } else {
          searchResults.innerHTML = ''; // Clear search results if search input is empty
      }
  });

  function displaySearchResults(profiles) {
      searchResults.innerHTML = '';
      profiles.forEach(profile => {
          const profileElement = document.createElement('div');
          profileElement.textContent = profile.user.username;
          searchResults.appendChild(profileElement);
      });
  }
});

