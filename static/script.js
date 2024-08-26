// script.js (Client-side JavaScript)
document.getElementById('predictForm').onsubmit = function(event) {
  event.preventDefault();

  // Get the feature values from the form
  var features = [
    document.getElementById('feature1').value,
    document.getElementById('feature2').value,
    document.getElementById('feature3').value,
    document.getElementById('feature4').value
  ];

  // Send the features to the server for prediction
  fetch('/predict', {
    method: 'GET','POST',
    headers: {
      'Content-Type': 'application/json',
      'Accept-Type': 'application/json'
    },
    body: JSON.stringify({ features: features })
  })
  .then(response => response.json())
  .then(data => {
    // Display the result
    document.getElementById('predictionResult').textContent = 'The predicted species is: ' + data.species;
  })
  .catch(error => console.error('Error:', error));
};
