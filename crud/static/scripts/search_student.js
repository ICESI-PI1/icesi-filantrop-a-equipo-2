/**
 * Fetches all the students created and adds to the HTML view all those that contain what is typed in the search box.
 */

const students_list = [];

fetch('/api/getStudents/')
        .then(response => response.json())
        .then(data => {
            console.log(data);

            data.forEach((student, index) => {
                student_aux = student.student_code + " - " + student.name;

                students_list[index] = student_aux;
            });
        })
        .catch(error => console.error('Error al obtener datos:', error));


const search_input = document.getElementById('student-search-box');
const results_list = document.getElementById('students-list');

const student_prompt_message = document.getElementById('student-prompt-message');


/**
 * Updates the list items with those that contain the search term written by the user.
 */
function update_results() {
    const search_term = search_input.value.toLowerCase();

    const filtered_results = students_list.filter
    (result =>
        result.toLowerCase().includes(search_term)
    );
        
    results_list.innerHTML = '';

    if (!search_term) {
        filtered_results.splice(0, filtered_results.length);

        results_list.appendChild(student_prompt_message);
    }

    filtered_results.forEach(result => {
        const li = document.createElement('li');
        li.classList.add('list-group-item', 'student-item');
        li.textContent = result;
        results_list.appendChild(li);
    
        // Adds the click event to each new element.
        li.addEventListener('click', function () {
            var student_info = this.textContent.trim().split(' - ');
            var student_name = student_info[0];
            var student_code = student_info[1];

            document.getElementById('message-area').value += '\n-' + student_name + ' - ' + student_code;
        });
    });

}

search_input.addEventListener('input', update_results);