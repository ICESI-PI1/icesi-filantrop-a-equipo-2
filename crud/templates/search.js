document
// Get a search box
.getElementById("search-box")
// Add keyup event
.addEventListener("keyup", function () {

  // Search functionality

  // Decalare a variables
  let input, filter, ul, li, a, i, txtValue;

  // Assign values
  input = document.getElementById("search-box");
  filter = input.value.toUpperCase();
  ul = document.getElementById("car-list");
  li = ul.getElementsByTagName("li");

  // Loop through all list items, and hide those who don't match the search query
  for (i = 0; i < li.length; i++) {
    a = li[i].getElementsByTagName("a")[0];
    txtValue = a.textContent || a.innerText;
    if (txtValue.toUpperCase().indexOf(filter) > -1) {
      li[i].style.display = "";
    } else {
      li[i].style.display = "none";
    }
  }

});