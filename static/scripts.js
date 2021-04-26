document.addEventListener('DOMContentLoaded', () => {
    // handle uploaded file
    document.getElementById("upload-file").addEventListener('change', function(e) {
        var files = [...this.files].sort();
    
        if (files.length > 0) {
            // send audio to server
        }
    }, false);
});