
document.getElementById('date-picker').addEventListener('change', function () {
  const selectedDate = this.value;
  console.log("Selected Date:", selectedDate);  // Debug log
  fetch(`/fetch_data?date=${selectedDate}`)
    .then(response => response.json())
    .then(data => {
      console.log("Fetched Data:", data);  // Debug log
      // Update the table with the new data
      const tableBody = document.querySelector('#weekly tbody');
      tableBody.innerHTML = '';
      data.forEach(row => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
  <td>${row.datetime}</td>
  <td>${row.water_temperature}</td>
  <td>${row.humidity}</td>
  <td>${row.water_level}</td>
  `;
        tableBody.appendChild(tr);
      });
    })
    .catch(error => console.error('Error fetching data:', error));
});

