// Additional JavaScript for enhanced functionality

// Chart.js integration for reports
function initializeCharts() {
    // Task Status Chart
    const taskStatusCtx = document.getElementById('taskStatusChart');
    if (taskStatusCtx) {
        new Chart(taskStatusCtx, {
            type: 'doughnut',
            data: {
                labels: ['مكتملة', 'قيد التنفيذ', 'جديدة', 'معلقة'],
                datasets: [{
                    data: [45, 32, 15, 8],
                    backgroundColor: ['#28a745', '#ffc107', '#17a2b8', '#dc3545'],
                    borderWidth: 2,
                    borderColor: '#fff'
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            font: {
                                family: 'Segoe UI'
                            }
                        }
                    }
                }
            }
        });
    }

    // Department Tasks Chart
    const deptTasksCtx = document.getElementById('deptTasksChart');
    if (deptTasksCtx) {
        new Chart(deptTasksCtx, {
            type: 'bar',
            data: {
                labels: ['القسم الفني', 'قسم المساحة', 'تطوير الأعمال', 'الموارد البشرية'],
                datasets: [{
                    label: 'عدد المهام',
                    data: [15, 12, 9, 6],
                    backgroundColor: '#b78b1e',
                    borderColor: '#9a7419',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true
                    }
                },
                plugins: {
                    legend: {
                        labels: {
                            font: {
                                family: 'Segoe UI'
                            }
                        }
                    }
                }
            }
        });
    }
}

// File upload handling
function handleFileUpload(inputElement, previewElement) {
    inputElement.addEventListener('change', function(e) {
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function(e) {
                if (previewElement) {
                    if (file.type.startsWith('image/')) {
                        previewElement.innerHTML = `<img src="${e.target.result}" class="img-thumbnail" style="max-width: 200px;">`;
                    } else {
                        previewElement.innerHTML = `<div class="alert alert-info">تم اختيار الملف: ${file.name}</div>`;
                    }
                }
            };
            reader.readAsDataURL(file);
        }
    });
}

// Real-time notifications
function initializeNotifications() {
    // Check for new notifications every 30 seconds
    setInterval(function() {
        fetch('/api/notifications')
            .then(response => response.json())
            .then(data => {
                if (data.notifications && data.notifications.length > 0) {
                    showNotificationBadge(data.notifications.length);
                }
            })
            .catch(error => console.log('Notification check failed:', error));
    }, 30000);
}

function showNotificationBadge(count) {
    const badge = document.getElementById('notificationBadge');
    if (badge) {
        badge.textContent = count;
        badge.style.display = count > 0 ? 'inline' : 'none';
    }
}

// Advanced search functionality
function initializeAdvancedSearch() {
    const searchInputs = document.querySelectorAll('.advanced-search');
    searchInputs.forEach(input => {
        input.addEventListener('input', function() {
            const searchTerm = this.value.toLowerCase();
            const targetTable = this.getAttribute('data-target');
            const table = document.getElementById(targetTable);
            
            if (table) {
                const rows = table.querySelectorAll('tbody tr');
                rows.forEach(row => {
                    const text = row.textContent.toLowerCase();
                    row.style.display = text.includes(searchTerm) ? '' : 'none';
                });
            }
        });
    });
}

// Dark mode toggle
function initializeDarkMode() {
    const darkModeToggle = document.getElementById('darkModeToggle');
    if (darkModeToggle) {
        darkModeToggle.addEventListener('click', function() {
            document.body.classList.toggle('dark-mode');
            localStorage.setItem('darkMode', document.body.classList.contains('dark-mode'));
        });
        
        // Load saved preference
        if (localStorage.getItem('darkMode') === 'true') {
            document.body.classList.add('dark-mode');
        }
    }
}

// Initialize all enhanced features
document.addEventListener('DOMContentLoaded', function() {
    initializeCharts();
    initializeNotifications();
    initializeAdvancedSearch();
    initializeDarkMode();
    
    // Initialize file upload handlers
    const fileInputs = document.querySelectorAll('input[type="file"]');
    fileInputs.forEach(input => {
        const previewId = input.getAttribute('data-preview');
        const previewElement = previewId ? document.getElementById(previewId) : null;
        handleFileUpload(input, previewElement);
    });
});

// Export functions for reports
function exportTableToExcel(tableId, filename) {
    const table = document.getElementById(tableId);
    const wb = XLSX.utils.table_to_book(table);
    XLSX.writeFile(wb, filename + '.xlsx');
}

function exportTableToPDF(tableId, filename) {
    const { jsPDF } = window.jspdf;
    const doc = new jsPDF();
    
    // Add Arabic font support
    doc.setFont('Arial', 'normal');
    doc.text('تقرير النظام', 20, 20);
    
    const table = document.getElementById(tableId);
    doc.autoTable({
        html: table,
        startY: 30,
        styles: {
            font: 'Arial',
            fontSize: 10
        }
    });
    
    doc.save(filename + '.pdf');
}

// Print functionality
function printReport(elementId) {
    const element = document.getElementById(elementId);
    const printWindow = window.open('', '_blank');
    
    printWindow.document.write(`
        <html>
        <head>
            <title>طباعة التقرير</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
            <style>
                body { font-family: Arial, sans-serif; direction: rtl; }
                @media print { .no-print { display: none; } }
            </style>
        </head>
        <body>
            <div class="container">
                <h2 class="text-center mb-4">شركة رِواق للاستشارات الهندسية</h2>
                ${element.innerHTML}
            </div>
        </body>
        </html>
    `);
    
    printWindow.document.close();
    printWindow.print();
}

