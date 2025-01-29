// Document Ready Function
document.addEventListener('DOMContentLoaded', function () {
    // Initialize tooltips (if using Bootstrap)
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    });

    // Handle CV upload feedback
    document.getElementById('cv-upload-form').addEventListener('submit', function (event) {
        event.preventDefault();
        const formData = new FormData(this);
        fetch('/upload_cv', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('CV uploaded successfully!');
                document.getElementById('cv-upload-form').reset();
            } else {
                alert('Failed to upload CV.');
            }
        })
        .catch(error => console.error('Error:', error));
    });

    // Handle JD upload feedback
    document.getElementById('jd-upload-form').addEventListener('submit', function (event) {
        event.preventDefault();
        const formData = new FormData(this);
        fetch('/upload_jd', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('JD uploaded successfully!');
                document.getElementById('jd-upload-form').reset();
            } else {
                alert('Failed to upload JD.');
            }
        })
        .catch(error => console.error('Error:', error));
    });

    // Form validation
    function validateForm(formId, fields) {
        let isValid = true;
        fields.forEach(field => {
            const input = document.querySelector(`${formId} [name="${field}"]`);
            if (!input.value.trim()) {
                isValid = false;
                input.classList.add('is-invalid');
            } else {
                input.classList.remove('is-invalid');
            }
        });
        return isValid;
    }

    // Handle match form submission with loading indicator
    document.getElementById('match-form').addEventListener('submit', function (event) {
        event.preventDefault();
        
        // Show loading indicator
        const submitButton = document.querySelector('#match-form button[type="submit"]');
        submitButton.disabled = true;
        submitButton.innerHTML = 'Matching...';

        const formData = new FormData(this);
        fetch('/match', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': '{{ csrf_token() }}'  // Ensure CSRF token is included if necessary
            }
        })
        .then(response => response.text())
        .then(html => {
            document.body.innerHTML = html;  // Replace current page content with new HTML
        })
        .catch(error => console.error('Error:', error))
        .finally(() => {
            submitButton.disabled = false;
            submitButton.innerHTML = 'Match';
        });
    });

    // Load dynamic content for admin/user dashboard
    function loadDashboardContent(url, targetElement) {
        fetch(url)
        .then(response => response.text())
        .then(html => {
            document.querySelector(targetElement).innerHTML = html;
        })
        .catch(error => console.error('Error:', error));
    }

    // Example call to load dashboard content
    // Uncomment and modify as needed
    // loadDashboardContent('/admin_dashboard', '#admin-dashboard-content');

    // Render charts for statistical details
    function renderChart(chartId, labels, data, title) {
        const ctx = document.getElementById(chartId).getContext('2d');
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: title,
                    data: data,
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    }

    // Example usage of rendering chart
    // Uncomment and modify as needed
    /*
    const labels = ['Skill 1', 'Skill 2', 'Skill 3'];
    const data = [50, 80, 60];
    renderChart('myChart', labels, data, 'Skill Match Percentage');
    */
});