document.addEventListener("DOMContentLoaded", function () {
  // Get all elements with class 'alert' and hide them initially
  var alerts = document.querySelectorAll('.alert');
  alerts.forEach(function (alert) {
    alert.style.display = 'none';
  });

  // Show alerts with class 'alert' if they are not empty
  alerts.forEach(function (alert) {
    if (alert.textContent.trim() !== '') {
      alert.style.display = 'block';
    }
  });

  // Hide alerts after 5 seconds
  setTimeout(function () {
    alerts.forEach(function (alert) {
      alert.style.display = 'none';
    });
  }, 3000);
});
