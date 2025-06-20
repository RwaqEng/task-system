// Rivaq System JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Auto-hide alerts after 5 seconds
    setTimeout(function() {
        var alerts = document.querySelectorAll('.alert');
        alerts.forEach(function(alert) {
            var bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);

    // Add fade-in animation to cards
    var cards = document.querySelectorAll('.card');
    cards.forEach(function(card, index) {
        setTimeout(function() {
            card.classList.add('fade-in');
        }, index * 100);
    });
});

// Utility Functions
function showLoading(element) {
    element.innerHTML = '<div class="spinner-rivaq mx-auto"></div>';
    element.disabled = true;
}

function hideLoading(element, originalText) {
    element.innerHTML = originalText;
    element.disabled = false;
}

function showAlert(message, type = 'success') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    const container = document.querySelector('.container-fluid .p-4');
    container.insertBefore(alertDiv, container.firstChild);
    
    // Auto-hide after 5 seconds
    setTimeout(function() {
        const bsAlert = new bootstrap.Alert(alertDiv);
        bsAlert.close();
    }, 5000);
}

// AJAX Helper Functions
function makeRequest(url, method = 'GET', data = null) {
    const options = {
        method: method,
        headers: {
            'Content-Type': 'application/json',
        }
    };
    
    if (data) {
        options.body = JSON.stringify(data);
    }
    
    return fetch(url, options)
        .then(response => response.json())
        .catch(error => {
            console.error('Error:', error);
            showAlert('حدث خطأ في الاتصال', 'danger');
        });
}

// Task Management Functions
function createTask(taskData) {
    return makeRequest('/api/tasks', 'POST', taskData);
}

function updateTask(taskId, taskData) {
    return makeRequest(`/api/tasks/${taskId}`, 'PUT', taskData);
}

function deleteTask(taskId) {
    return makeRequest(`/api/tasks/${taskId}`, 'DELETE');
}

// User Management Functions
function createUser(userData) {
    return makeRequest('/api/users', 'POST', userData);
}

function updateUser(userId, userData) {
    return makeRequest(`/api/users/${userId}`, 'PUT', userData);
}

function deleteUser(userId) {
    return makeRequest(`/api/users/${userId}`, 'DELETE');
}

// Meeting Management Functions
function createMeeting(meetingData) {
    return makeRequest('/api/meetings', 'POST', meetingData);
}

function updateMeeting(meetingId, meetingData) {
    return makeRequest(`/api/meetings/${meetingId}`, 'PUT', meetingData);
}

// Form Validation
function validateForm(formElement) {
    const inputs = formElement.querySelectorAll('input[required], select[required], textarea[required]');
    let isValid = true;
    
    inputs.forEach(function(input) {
        if (!input.value.trim()) {
            input.classList.add('is-invalid');
            isValid = false;
        } else {
            input.classList.remove('is-invalid');
        }
    });
    
    return isValid;
}

// Date Formatting
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('ar-SA');
}

function formatDateTime(dateString) {
    const date = new Date(dateString);
    return date.toLocaleString('ar-SA');
}

// Progress Bar Animation
function animateProgressBar(element, targetValue) {
    let currentValue = 0;
    const increment = targetValue / 50;
    
    const timer = setInterval(function() {
        currentValue += increment;
        if (currentValue >= targetValue) {
            currentValue = targetValue;
            clearInterval(timer);
        }
        element.style.width = currentValue + '%';
        element.setAttribute('aria-valuenow', currentValue);
    }, 20);
}

// Search and Filter Functions
function filterTable(searchInput, tableId) {
    const filter = searchInput.value.toLowerCase();
    const table = document.getElementById(tableId);
    const rows = table.getElementsByTagName('tr');
    
    for (let i = 1; i < rows.length; i++) {
        const cells = rows[i].getElementsByTagName('td');
        let found = false;
        
        for (let j = 0; j < cells.length; j++) {
            if (cells[j].textContent.toLowerCase().indexOf(filter) > -1) {
                found = true;
                break;
            }
        }
        
        rows[i].style.display = found ? '' : 'none';
    }
}

// Export Functions
function exportToCSV(tableId, filename) {
    const table = document.getElementById(tableId);
    const rows = table.querySelectorAll('tr');
    let csv = [];
    
    rows.forEach(function(row) {
        const cells = row.querySelectorAll('th, td');
        const rowData = Array.from(cells).map(cell => cell.textContent.trim());
        csv.push(rowData.join(','));
    });
    
    const csvContent = csv.join('\n');
    const blob = new Blob([csvContent], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    
    const a = document.createElement('a');
    a.href = url;
    a.download = filename + '.csv';
    a.click();
    
    window.URL.revokeObjectURL(url);
}

// Print Function
function printPage() {
    window.print();
}

// Confirmation Dialog
function confirmAction(message, callback) {
    if (confirm(message)) {
        callback();
    }
}

