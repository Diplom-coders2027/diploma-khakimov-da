
const dropdownToggle = document.querySelector('.dropdown_toggle');

const dropdownMenu = document.querySelector('.dropdown-menu');


dropdownToggle.addEventListener('click', function(e) {
  e.stopPropagation();
  dropdownMenu.classList.toggle('show');
});

document.addEventListener('click', function() {
  dropdownMenu.classList.remove('show');
});

