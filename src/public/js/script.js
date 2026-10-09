// Get the dropdown toggle button
const dropdownToggle = document.querySelector('.dropdown_toggle');

// Get the dropdown menu
const dropdownMenu = document.querySelector('.dropdown-menu');

// Add click event listener to the toggle button
dropdownToggle.addEventListener('click', function() {
  // Toggle the 'show' class on the dropdown menu
  dropdownMenu.classList.toggle('show');
});