// static/script.js

// Function to handle image encoding
function encodeImage() {
    // Get the selected image file
    const imageInput = document.getElementById('image-input');
    const imageFile = imageInput.files[0];

    // Get the secret message
    const secretMessage = document.getElementById('message-input').value;

    // Check if both image and message are provided
    if (imageFile && secretMessage) {
        // Create a FormData object to send the image and message
        const formData = new FormData();
        formData.append('file', imageFile);
        formData.append('message', secretMessage);

        // Make a POST request to the /encode endpoint
        fetch('/encode', {
            method: 'POST',
            body: formData,
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Display the encoded image
                const encodedSection = document.getElementById('encoded-section');
                const encodedImage = document.getElementById('encoded-image');
                encodedImage.src = data.encoded_image_path;
                encodedSection.style.display = 'block';
            } else {
                alert('Error encoding image: ' + data.error);
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    } else {
        alert('Please select an image and enter a secret message.');
    }
}

// Function to handle image decoding
function decodeImage() {
    // Get the selected image file for decoding
    const decodeImageInput = document.getElementById('decode-image-input');
    const decodeImageFile = decodeImageInput.files[0];

    // Check if an image is provided
    if (decodeImageFile) {
        // Create a FormData object to send the image
        const formData = new FormData();
        formData.append('file', decodeImageFile);

        // Make a POST request to the /decode endpoint
        fetch('/decode', {
            method: 'POST',
            body: formData,
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Display the decoded message
                const decodedMessage = document.getElementById('decoded-message');
                decodedMessage.innerText = 'Decoded Message: ' + data.decoded_message;
            } else {
                alert('Error decoding image: ' + data.error);
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    } else {
        alert('Please select an encoded image for decoding.');
    }
}
