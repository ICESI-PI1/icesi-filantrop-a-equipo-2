const search_input = document.getElementById('search-box');
const results_list = document.getElementById('offices-list');

const offices_list = [];

const elements = document.querySelectorAll('#offices-list li');

elements.forEach(li => {
  offices_list.push(li.textContent.trim());
});

console.log('Resultados: ', offices_list);

function update_results() {
  const search_term = search_input.value.toLowerCase();

  const filtered_results = offices_list.filter
  (result => 
    result.toLowerCase().includes(search_term)
  );

  results_list.innerHTML = '';

  filtered_results.forEach(result => {
    const li = document.createElement('li');
    li.classList.add('list-group-item');
    li.textContent = result;
    results_list.appendChild(li);
  });
}

search_input.addEventListener('input', update_results);