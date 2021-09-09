/* When the user clicks on the button,
toggle between hiding and showing the dropdown content */

function myFunction() {
  var input, filter, cards, cardContainer, h5, title, i;
  input = document.getElementById("myFilter");
  filter = input.value.toUpperCase();
  cardContainer = document.getElementById("myItems");
  cards = cardContainer.getElementsByClassName("card");
  for (i = 0; i < cards.length; i++) {
      title = cards[i].querySelector(".card-body h5.card-title");
      if (title.innerText.toUpperCase().indexOf(filter) > -1) {
          cards[i].style.display = "";
      } else {
          cards[i].style.display = "none";
      }
  }
}

function myFunctionA() {
    document.getElementById("myDropdownA").classList.toggle("show");
  }
  
  function filterFunctionA() {
    var input, filter, ul, li, a, i;
    input = document.getElementById("myInputA");
    filter = input.value.toUpperCase();
    div = document.getElementById("myDropdownA");
    a = div.getElementsByTagName("a");
    for (i = 0; i < a.length; i++) {
      txtValue = a[i].textContent || a[i].innerText;
      if (txtValue.toUpperCase().indexOf(filter) > -1) {
        a[i].style.display = "";
      } else {
        a[i].style.display = "none";
      }
    }
  }

  function myFunctionB() {
    document.getElementById("myDropdownB").classList.toggle("show");
  }
  
  function filterFunctionB() {
    var input, filter, ul, li, a, i;
    input = document.getElementById("myInputB");
    filter = input.value.toUpperCase();
    div = document.getElementById("myDropdownB");
    a = div.getElementsByTagName("a");
    for (i = 0; i < a.length; i++) {
      txtValue = a[i].textContent || a[i].innerText;
      if (txtValue.toUpperCase().indexOf(filter) > -1) {
        a[i].style.display = "";
      } else {
        a[i].style.display = "none";
      }
    }
  }

  function myFunctionC() {
    document.getElementById("myDropdownC").classList.toggle("show");
  }
  
  function filterFunctionC() {
    var input, filter, ul, li, a, i;
    input = document.getElementById("myInputC");
    filter = input.value.toUpperCase();
    div = document.getElementById("myDropdownC");
    a = div.getElementsByTagName("a");
    for (i = 0; i < a.length; i++) {
      txtValue = a[i].textContent || a[i].innerText;
      if (txtValue.toUpperCase().indexOf(filter) > -1) {
        a[i].style.display = "";
      } else {
        a[i].style.display = "none";
      }
    }
  }