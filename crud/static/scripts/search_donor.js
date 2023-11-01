/**
 * Fetches all the donors created and adds to the HTML view all those that contain what is typed in the search box.
 */

const donors_list = [];

fetch('/api/getDonors/')
        .then(response => response.json())
        .then(data => {
            console.log(data);

            data.forEach((donor, index) => {
                donor_aux = donor.nit + " - " + donor.name + " " + donor.lastname;

                donors_list[index] = {
                    "display_text" : donor_aux,
                    "id" : donor.id
                };
            });
        })
        .catch(error => console.error('Error al obtener datos:', error));

        
const donor_search_input = document.getElementById('donor-search-box');
const donor_results_list = document.getElementById('donors-list');

const donor_prompt_message = document.getElementById('donors-prompt-message');

/**
 * Updates the list items with those that contain the search term written by the user.
 */
function update_results() {
    const search_term = donor_search_input.value.toLowerCase();

    const filtered_results = donors_list.filter
    (result =>
        result.display_text.toLowerCase().includes(search_term)
    );
        
    donor_results_list.innerHTML = '';

    if (!search_term) {
        filtered_results.splice(0, filtered_results.length);

        donor_results_list.appendChild(donor_prompt_message);
    }

    filtered_results.forEach(result => {
        const li = document.createElement('li');
        li.classList.add('list-group-item', 'student-item');
        li.textContent = result.display_text;

        // Set the email as a data attribute.
        li.setAttribute('data-id', result.id);

        donor_results_list.appendChild(li);
    
        // Adds the click event to each new element.
        li.addEventListener('click', function () {
            var donor_info = this.textContent.trim().split(' - ');
            var donor_name = donor_info[1];
            var donor_nit = donor_info[0];

            donor_search_input.value = donor_nit + " - " + donor_name;
            update_results();

            // Get the id.
            var donor_id = this.getAttribute('data-id');

            document.getElementById('donor-id-input').value = donor_id;
        });
    });

}

donor_search_input.addEventListener('input', update_results);