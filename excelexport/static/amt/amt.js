// Form validation and submission
function submitForm() {
    const formData = {};
    const inputs = document.querySelectorAll('.field-input');
    const submitBtn = document.querySelector('.submit-btn');
    const submitText = document.getElementById('submit-text');
    let hasErrors = false;

    // Reset previous error states
    inputs.forEach(input => {
        input.classList.remove('error', 'success');
    });

    // Collect data and validate
    inputs.forEach(input => {
        const fieldName = input.dataset.field;
        const value = input.value.trim();
        
        if (fieldName) {
            formData[fieldName] = value;
            
            // Validate required fields
            if (input.hasAttribute('required') && !value) {
                input.classList.add('error');
                hasErrors = true;
            } else if (value) {
                input.classList.add('success');
            }
        }
    });

    if (hasErrors) {
        submitText.textContent = 'Please fill required fields';
        setTimeout(() => {
            submitText.textContent = 'Submit Parameters';
        }, 2000);
        return;
    }

    // Simulate submission
    submitBtn.classList.add('loading');
    submitText.textContent = 'Submitting...';
    
    setTimeout(() => {
        console.log('Form Data:', formData);
        submitText.textContent = 'Submitted Successfully!';
        
        // Show success state
        document.querySelector('.form-container').style.transform = 'scale(0.98)';
        document.querySelector('.form-container').style.opacity = '0.8';
        
        setTimeout(() => {
            submitText.textContent = 'Submit Parameters';
            submitBtn.classList.remove('loading');
            document.querySelector('.form-container').style.transform = 'scale(1)';
            document.querySelector('.form-container').style.opacity = '1';
        }, 1500);
    }, 1500);
}

function closeSection(button) {
    const section = button.closest('.grid-section');
    section.style.transform = 'translateX(100%)';
    section.style.opacity = '0';
    setTimeout(() => {
        section.style.display = 'none';
    }, 300);
}

function showMenu(button) {
    const options = [
        '📝 Edit Section',
        '📋 Duplicate Section', 
        '🗑️ Delete Section',
        '➕ Add Field',
        '📊 View Data',
        '⚙️ Settings'
    ];
    
    const choice = prompt('Select an option:\n\n' + options.map((opt, i) => `${i + 1}. ${opt}`).join('\n'));
    
    if (choice) {
        const optionIndex = parseInt(choice) - 1;
        if (optionIndex >= 0 && optionIndex < options.length) {
            alert(`Selected: ${options[optionIndex]}`);
        }
    }
}

// Real-time validation
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.field-input').forEach(input => {
        input.addEventListener('input', function() {
            this.classList.remove('error');
            
            if (this.value.trim() && this.hasAttribute('required')) {
                this.classList.add('success');
            } else {
                this.classList.remove('success');
            }
        });

        input.addEventListener('blur', function() {
            if (this.hasAttribute('required') && !this.value.trim()) {
                this.classList.add('error');
            }
        });
    });
    
    // Excel export functionality
    function exportToExcel() {
        const excelBtn = document.querySelector('.excel-btn');
        const originalText = excelBtn.textContent;
        
        // Show loading state
        excelBtn.textContent = 'Exporting...';
        excelBtn.disabled = true;
        excelBtn.style.background = '#d97706';
        
        // Simulate export process
        setTimeout(() => {
            // Get form data for export
            const formData = {};
            document.querySelectorAll('.field-input').forEach(input => {
                if (input.dataset.field && input.value.trim()) {
                    formData[input.dataset.field] = input.value.trim();
                }
            });
            
            console.log('Exporting to Excel:', formData);
            alert('Excel export started!\n\nData has been prepared for download.\nCheck your downloads folder for the Excel file.');
            
            // Reset button state
            excelBtn.textContent = originalText;
            excelBtn.disabled = false;
            excelBtn.style.background = '#f59e0b';
        }, 1500);
    }

    // Drag and drop functionality
    let draggedElement = null;

    document.querySelectorAll('.drag-handle').forEach(handle => {
        handle.addEventListener('mousedown', function(e) {
            draggedElement = this.closest('.field-row');
            draggedElement.style.opacity = '0.6';
            draggedElement.style.transform = 'rotate(2deg)';
            document.body.style.cursor = 'grabbing';
        });
    });

    document.addEventListener('mouseup', function() {
        if (draggedElement) {
            draggedElement.style.opacity = '1';
            draggedElement.style.transform = 'none';
            document.body.style.cursor = 'default';
            draggedElement = null;
        }
    });
});

// Search functionality
function performSearch() {
    const countryInput = document.getElementById('country_input');
    const yearSelect = document.getElementById('year_select');
    const searchBtn = document.querySelector('.search-btn');
    
    const country = countryInput.value.trim();
    const year = yearSelect.value;
    
    if (!country) {
        alert('Please enter a country name');
        return;
    }
    
    // Simulate search process
    const originalText = searchBtn.innerHTML;
    searchBtn.innerHTML = '<span class="search-icon">⏳</span> Searching...';
    searchBtn.disabled = true;
    
    setTimeout(() => {
        searchBtn.innerHTML = originalText;
        searchBtn.disabled = false;
        alert(`Searching for data from ${country} in ${year || 'all years'}`);
    }, 1500);
}

// Export to Excel functionality
function exportToExcel() {
    const data = {
        timestamp: new Date().toISOString(),
        fields: {}
    };

    // Collect all field values
    document.querySelectorAll('.field-input').forEach(input => {
        if (input.dataset.field) {
            data.fields[input.dataset.field] = input.value.trim();
        }
    });

    console.log('Exporting data:', data);
    alert('Export to Excel feature will be implemented here');
}
