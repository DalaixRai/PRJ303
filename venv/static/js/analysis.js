document.addEventListener('DOMContentLoaded', (event) => {
  const ctx = document.getElementById('water_temperatureChart').getContext('2d');
  const water_temperatureChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: [],
      datasets: [{
        label: 'Water Temperature (°C)',
        data: [],
        borderColor: '#00B8DC',
        borderWidth: 1,
        fill: false
      }]
    },
    options: {
      scales: {
        x: {
          type: 'time',
          time: {
            unit: 'day'
          },
          title: {
            display: true,
            text: 'Date',
            color: '#fff'
          },
          ticks: {
            color: '#fff'
          }
        },
        y: {
          title: {
            display: true,
            text: 'Water Temperature (°C)',
            color: '#fff'
          },
          ticks: {
            color: '#fff'
          }
        }
      },
      plugins: {
        legend: {
          labels: {
            color: '#fff'
          }
        }
      }
    }
  });

  function updateChart() {
    fetch('/update_plot')
      .then(response => response.json())
      .then(data => {
        if (data.error) {
          alert(data.error);
        } else {
          water_temperatureChart.data.labels = data.labels;
          water_temperatureChart.data.datasets[0].data = data.water_temperature_data;
          water_temperatureChart.update();
        }
      })
      .catch(error => console.error('Error fetching the data:', error));
  }

  // Initial chart update
  updateChart();

  // Periodic updates every 5 minutes
  setInterval(updateChart, 300000); // 300000 ms = 5 minutes
});
