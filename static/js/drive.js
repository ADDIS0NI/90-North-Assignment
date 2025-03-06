class DriveManager {
    constructor() {
        this.initializeDownloadButtons();
    }

    initializeDownloadButtons() {
        const downloadButtons = document.querySelectorAll('.download-btn');
        
        downloadButtons.forEach(button => {
            button.addEventListener('click', async (e) => {
                await this.handleDownload(e.target);
            });
        });
    }

    async handleDownload(button) {
        const fileId = button.dataset.fileId;
        const fileName = button.dataset.filename;
        const progressContainer = button.nextElementSibling;
        const progressBar = progressContainer.querySelector('.progress');
        const progressText = progressContainer.querySelector('.progress-text');

        try {
            // Hide button, show progress
            button.style.display = 'none';
            progressContainer.style.display = 'block';

            // Start download
            const response = await fetch(`/files/download/${fileId}/`);
            
            if (!response.ok) throw new Error('Download failed');

            // Create blob and download
            const blob = await response.blob();
            this.downloadBlob(blob, fileName);

            // Show success
            this.updateProgress(progressBar, progressText, 100);

            // Reset UI after a moment
            setTimeout(() => {
                progressContainer.style.display = 'none';
                button.style.display = 'inline-block';
                this.updateProgress(progressBar, progressText, 0);
            }, 1000);

        } catch (error) {
            console.error('Download error:', error);
            alert('Download failed. Please try again.');
            progressContainer.style.display = 'none';
            button.style.display = 'inline-block';
        }
    }

    downloadBlob(blob, fileName) {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = fileName;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
    }

    updateProgress(progressBar, progressText, percentage) {
        progressBar.style.width = `${percentage}%`;
        progressText.textContent = `${percentage}%`;
    }
}

// Initialize drive features when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    if (document.querySelector('.file-list-container')) {
        new DriveManager();
    }
});