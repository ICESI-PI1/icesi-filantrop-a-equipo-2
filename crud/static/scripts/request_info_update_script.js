const search_input = document.getElementById('search-box');
const results_list = document.getElementById('students-list');

const students_list = [];

const elements = document.querySelectorAll('#students-list li');

elements.forEach(li => {
  students_list.push(li.textContent.trim());
});

/**
 * Updates the list items with those that contains the search term written by the user.
 */
function update_results() {
  const search_term = search_input.value.toLowerCase();

  const filtered_results = students_list.filter
  (result => 
    result.toLowerCase().includes(search_term)
  );

  results_list.innerHTML = '';

  filtered_results.forEach(result => {
    const li = document.createElement('li');
    li.classList.add('list-group-item', 'studen-item');
    li.textContent = result;
    results_list.appendChild(li);

    // Adds the event to each new element.
    li.addEventListener('click', function () {
        var student_info = this.textContent.trim().split(' - ');
        var student_name = student_info[0];
        var student_code = student_info[1];

        // document.getElementById('message-area').value = 'Buenos días/tardes.\n\nPor medio del presente, solicito la actualización de la información del estudiante ' + student_name + ', con código de estudiante ' + student_code + ', desde la Oficina de Filantropía.';

        document.getElementById('message-area').value += '\n-' + student_name + ' - ' + student_code;
    });
  });
}

search_input.addEventListener('input', update_results);

// ---

/**
 * Updates the content of the message to be sent with the data of the student who has been selected.
 */
document.addEventListener('DOMContentLoaded', function () {
    // Obtén todos los elementos de la clase student-item
    var studentItems = document.querySelectorAll('.student-item');

    // Agrega un evento de clic a cada elemento de la lista
    studentItems.forEach(function (item) {
        item.addEventListener('click', function () {
            // Obtén el contenido del elemento clicado
            var student_info = item.textContent.trim().split(' - ');
            var student_name = student_info[0];
            var student_code = student_info[1];

            // Actualiza el contenido del textarea
            // document.getElementById('message-area').value = 'Buenos días/tardes.\n\nPor medio del presente, solicito la actualización de la información del estudiante ' + student_name + ', con código de estudiante ' + student_code + ', desde la Oficina de Filantropía.';

            document.getElementById('message-area').value += '\n-' + student_name + ' - ' + student_code;
        });
    });
});

// ---

// document.querySelector('auto-resize-textarea').addEventListener('input', function() {
//   auto_resize(this);
// });

// function auto_resize(element) {
//   element.style.height = 'auto';
//   element.style.height = (element.scrollHeight) + 'px';
// }