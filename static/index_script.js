// static/js/input_script.js

document.addEventListener('DOMContentLoaded', function() {
    // Get DOM elements
    const textToggle = document.getElementById('text-toggle');
    const fileToggle = document.getElementById('file-toggle');
    const textInputContainer = document.getElementById('text-input-container');
    const fileInputContainer = document.getElementById('file-input-container');
    const textInput = document.getElementById('text-input');
    const fileInput = document.getElementById('file-input');
    const fileNameDisplay = document.getElementById('file-name');
    const submitButton = document.querySelector('.submit-btn');
    const form = document.getElementById('input-form');

    // Toggle between text and file input
    textToggle.addEventListener('click', function() {
        textToggle.classList.add('active');
        fileToggle.classList.remove('active');
        textInputContainer.classList.add('active');
        fileInputContainer.classList.remove('active');
        
        // Clear file input when switching to text mode
        fileInput.value = '';
        fileNameDisplay.textContent = 'Choose a file';
    });

    fileToggle.addEventListener('click', function() {
        fileToggle.classList.add('active');
        textToggle.classList.remove('active');
        fileInputContainer.classList.add('active');
        textInputContainer.classList.remove('active');
        
        // Clear text input when switching to file mode
        textInput.value = '';
    });

    // Update file name display when file is selected
    fileInput.addEventListener('change', function() {
        if (fileInput.files.length > 0) {
            fileNameDisplay.textContent = fileInput.files[0].name;
        } else {
            fileNameDisplay.textContent = 'Choose a file';
        }
    });

    // Form validation before submission
    form.addEventListener('submit', function(event) {
        // Check if text input is active but empty
        if (textInputContainer.classList.contains('active') && !textInput.value.trim()) {
            event.preventDefault();
            alert('Please enter text or switch to file upload.');
            return;
        }
        
        // Check if file input is active but no file is selected
        if (fileInputContainer.classList.contains('active') && fileInput.files.length === 0) {
            event.preventDefault();
            alert('Please select a file or switch to text input.');
            return;
        }
        
        // Ensure only one input method is submitted
        if (textInputContainer.classList.contains('active')) {
            fileInput.value = ''; // Clear file input
        } else {
            textInput.value = ''; // Clear text input
        }
    });

    // Optional: Animation for submit button
    submitButton.addEventListener('mousedown', function() {
        this.style.transform = 'scale(0.98)';
    });
    
    submitButton.addEventListener('mouseup', function() {
        this.style.transform = 'scale(1)';
    });
    
    submitButton.addEventListener('mouseleave', function() {
        this.style.transform = 'scale(1)';
    });
});