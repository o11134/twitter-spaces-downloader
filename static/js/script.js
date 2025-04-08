// JavaScript for Twitter Spaces Downloader Website

document.addEventListener('DOMContentLoaded', function() {
    const downloadForm = document.getElementById('downloadForm');
    const statusContainer = document.getElementById('status');
    const resultContainer = document.getElementById('result');
    const errorContainer = document.getElementById('error');
    const progressBar = document.getElementById('progressBar');
    const statusMessage = document.getElementById('statusMessage');
    const errorMessage = document.getElementById('errorMessage');
    const downloadLink = document.getElementById('downloadLink');

    // Hide all result containers initially
    function resetContainers() {
        statusContainer.style.display = 'none';
        resultContainer.style.display = 'none';
        errorContainer.style.display = 'none';
        progressBar.style.width = '0%';
    }

    // Handle form submission
    downloadForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Get the URL from the input
        const url = document.getElementById('url').value.trim();
        
        // Validate URL (basic validation)
        if (!url || (!url.includes('twitter.com') && !url.includes('x.com'))) {
            errorContainer.style.display = 'block';
            errorMessage.textContent = 'يرجى إدخال رابط Twitter/X صالح.';
            return;
        }
        
        // Reset containers and show status
        resetContainers();
        statusContainer.style.display = 'block';
        statusMessage.textContent = 'جاري تحليل الرابط...';
        
        // Generate a task ID for progress tracking
        const taskId = Date.now().toString();
        
        // Start listening for progress updates
        const eventSource = new EventSource(`/progress/${taskId}`);
        
        eventSource.onmessage = function(event) {
            const data = JSON.parse(event.data);
            
            // Update progress bar
            progressBar.style.width = data.progress + '%';
            
            // Update status message based on progress
            if (data.progress < 30) {
                statusMessage.textContent = 'جاري تحليل الرابط...';
            } else if (data.progress < 60) {
                statusMessage.textContent = 'جاري تحميل المحادثة الصوتية...';
            } else if (data.progress < 90) {
                statusMessage.textContent = 'جاري معالجة الملف الصوتي...';
            } else {
                statusMessage.textContent = 'جاري إكمال التحميل...';
            }
            
            // Close the event source when complete
            if (data.complete) {
                eventSource.close();
            }
        };
        
        // Send AJAX request to the server
        fetch('/download', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ url: url }),
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            // Close the event source if it's still open
            eventSource.close();
            
            if (data.success) {
                // Show success result
                statusContainer.style.display = 'none';
                resultContainer.style.display = 'block';
                
                // Set download link with absolute URL
                const absoluteUrl = window.location.origin + data.download_url;
                downloadLink.href = absoluteUrl;
                
                // Force download attribute
                downloadLink.setAttribute('download', data.filename);
                
                // Add click handler to trigger download directly
                downloadLink.onclick = function(e) {
                    // Create a temporary link and trigger click
                    const tempLink = document.createElement('a');
                    tempLink.href = absoluteUrl;
                    tempLink.setAttribute('download', data.filename);
                    tempLink.setAttribute('target', '_blank');
                    document.body.appendChild(tempLink);
                    tempLink.click();
                    document.body.removeChild(tempLink);
                    
                    // Prevent default to avoid navigation
                    e.preventDefault();
                    
                    // Show message that download has started
                    statusMessage.textContent = 'بدأ التحميل، يرجى الانتظار...';
                    statusContainer.style.display = 'block';
                    
                    // Hide status after 3 seconds
                    setTimeout(function() {
                        statusContainer.style.display = 'none';
                    }, 3000);
                };
                
                progressBar.style.width = '100%';
            } else {
                // Show error message
                statusContainer.style.display = 'none';
                errorContainer.style.display = 'block';
                errorMessage.textContent = data.error || 'حدث خطأ أثناء تحميل المحادثة.';
            }
        })
        .catch(error => {
            // Close the event source if it's still open
            eventSource.close();
            
            console.error('Error:', error);
            
            // Show error message
            statusContainer.style.display = 'none';
            errorContainer.style.display = 'block';
            errorMessage.textContent = 'حدث خطأ في الاتصال بالخادم. يرجى المحاولة مرة أخرى لاحقًا.';
        });
    });
});
