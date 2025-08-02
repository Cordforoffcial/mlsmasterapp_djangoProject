// Navigation functions
function goHome() {
    alert('Home button clicked!');
    // Add your home navigation logic here
}

function selectTab(tabElement) {
    // Remove active class from all tabs
    document.querySelectorAll('.nav-tab').forEach(tab => {
        tab.classList.remove('active');
    });
    
    // Add active class to clicked tab
    tabElement.classList.add('active');
    
    // Add your tab switching logic here
    console.log('Selected tab:', tabElement.textContent);
}

function performSearch() {
    const searchTerm = document.getElementById('searchInput').value;
    if (searchTerm.trim()) {
        alert('Searching for: ' + searchTerm);
        // Add your search logic here
    }
}

// Allow search on Enter key
document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('searchInput').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            performSearch();
        }
    });
});

// Form submission handling
function submitForm() {
    const form = document.getElementById('inspectionForm');
    
    // Get form values
    const date = document.getElementById('inspectionDate').value;
    const batchNumber = document.getElementById('batchNumber').value;
    const section = document.getElementById('section').value;
    
    // Basic validation
    if (!date || !batchNumber || !section) {
        alert('Please fill in all required fields.');
        return;
    }
    
    // Prepare the data
    const data = {
        date: date,
        batchNumber: batchNumber,
        section: section
    };
    
    // Send AJAX request
    fetch('/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            alert('Form submitted successfully!');
            form.reset();
            // Set today's date as default after form reset
            document.getElementById('inspectionDate').value = new Date().toISOString().split('T')[0];
        } else {
            alert('Error: ' + data.message);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while submitting the form. Please try again.');
    });
}

// Clear form function
function clearForm() {
    if (confirm('Are you sure you want to clear all form data?')) {
        document.getElementById('inspectionForm').reset();
    }
}

// Enhanced form validation
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('inspectionForm');
    const inputs = form.querySelectorAll('input[required]');
    
    inputs.forEach(input => {
        input.addEventListener('blur', function() {
            validateField(this);
        });
        
        input.addEventListener('input', function() {
            if (this.classList.contains('error')) {
                validateField(this);
            }
        });
    });
});

function validateField(field) {
    const isValid = field.value.trim() !== '';
    
    if (!isValid) {
        field.style.borderColor = '#d93025';
        field.classList.add('error');
    } else {
        field.style.borderColor = '#ddd';
        field.classList.remove('error');
    }
}

// Set today's date as default
document.addEventListener('DOMContentLoaded', function() {
    const today = new Date().toISOString().split('T')[0];
    document.getElementById('inspectionDate').value = today;
});
