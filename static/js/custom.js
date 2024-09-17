document.addEventListener('DOMContentLoaded', function() {
    // Add a function to reload the page with current sort parameters
    function reloadPageWithSort() {
        const sortBy = new URLSearchParams(window.location.search).get('sort_by') || 'status__name';
        const order = new URLSearchParams(window.location.search).get('order') || 'asc';
        const newUrl = `${window.location.pathname}?sort_by=${sortBy}&order=${order}`;
        window.location.href = newUrl;
    }

    document.querySelectorAll('.task-checkbox').forEach(function(checkbox) {
        checkbox.addEventListener('change', function() {
            const checkbox = this;
            const taskId = checkbox.getAttribute('data-id');
            const newStatus = checkbox.checked ? 'Completed' : 'Pending';
            
/*             // Display a confirmation dialog
            const confirmation = confirm(`Are you sure you want to mark this task as ${newStatus}?`);
            if (!confirmation) {
                // If user clicks "Cancel", revert the checkbox state
                checkbox.checked = !checkbox.checked;
                return;
            } */
            
            fetch(window.urls.updateTaskStatus, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': window.csrfToken
                },
                body: JSON.stringify({
                    id: taskId,
                    status: newStatus
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    console.log('Status updated successfully');
                    
                    // Reload the page with current sort parameters
                    reloadPageWithSort();
                    
                } else {
                    console.error('Error updating status:', data.message);
                    // Revert the checkbox state on error
                    checkbox.checked = !checkbox.checked;
                }
            })
            .catch(error => {
                console.error('AJAX error:', error);
                // Revert the checkbox state on error
                checkbox.checked = !checkbox.checked;
            });
        });
    });
});
