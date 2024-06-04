function fetchPrediction() {
  fetch('/predict')
    .then(response => response.json())
    .then(data => {
      if (data.motor_status) {
        document.getElementById('prediction').textContent = data.motor_status;
      } else if (data.error) {
        document.getElementById('prediction').textContent = 'Error: ' + data.error;
      }
    })
    .catch(error => {
      document.getElementById('prediction').textContent = 'Error: ' + error;
    });
}

document.addEventListener('DOMContentLoaded', function () {
  fetchPrediction();
});