document.addEventListener('DOMContentLoaded', function () {
  // Initialize Firebase (if needed)
  // Example:
  firebase.initializeApp({
    apiKey: "AIzaSyC4TNQl40Lccy-nr0uPnVYXVYVqZ89dE6Y",
    authDomain: "dht11-firebase-3094c.firebaseapp.com",
    databaseURL: "https://dht11-firebase-3094c-default-rtdb.asia-southeast1.firebasedatabase.app",
    projectId: "dht11-firebase-3094c",
    storageBucket: "dht11-firebase-3094c.appspot.com",
    messagingSenderId: "421392299639",
    appId: "1:421392299639:web:cb664a71ab1aed5dc4b872",
    measurementId: "G-YQBKBDKJ42"
  });

  // Function to update notification timestamp
  function updateNotificationTimestamp(timestamp) {
    const currentTimestamp = Date.now();
    const timeDifference = currentTimestamp - timestamp;

    const seconds = Math.floor(timeDifference / 1000);
    const minutes = Math.floor(seconds / 60);
    const hours = Math.floor(minutes / 60);
    const days = Math.floor(hours / 24);

    let timeAgo;
    if (days > 0) {
      timeAgo = `${days} days ago`;
    } else if (hours > 0) {
      timeAgo = `${hours} hours ago`;
    } else if (minutes > 0) {
      timeAgo = `${minutes} minutes ago`;
    } else {
      timeAgo = `Just now`;
    }

    // Update timestamp element in the notification
    const timestampElement = document.querySelector('.timestamp');
    if (timestampElement) {
      timestampElement.textContent = timeAgo;
    }
  }

  // Fetch realtime data from Firebase (assuming you have Firebase initialized)
  const db = firebase.database();
  db.ref('realtime_data').once('value', function (snapshot) {
    const realtimeData = snapshot.val();
    if (realtimeData) {
      // Update notification timestamp with the fetched timestamp
      updateNotificationTimestamp(realtimeData.timestamp);
    }
  });
});