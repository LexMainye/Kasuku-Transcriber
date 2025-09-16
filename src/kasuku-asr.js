// kasuku-asr.js - JavaScript for Kasuku ASR Frontend Functionality

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all functionality when the DOM is fully loaded
    initializeKasukuASR();
});

function initializeKasukuASR() {
    console.log('Initializing Kasuku ASR JavaScript functionality');
    
    // Initialize copy functionality for existing elements
    initializeCopyButtons();
    
    // Initialize delete functionality
    initializeDeleteButtons();
    
    // Initialize screen reader functionality
    initializeScreenReader();
    
    // Initialize chat bubble hover effects
    initializeChatBubbles();
    
    // Initialize material icons
    initializeMaterialIcons();
    
    // Set up mutation observer to handle dynamically added elements
    setupMutationObserver();
}

function initializeCopyButtons() {
    // Add event listeners to all copy buttons
    document.querySelectorAll('.copy-button').forEach(button => {
        button.addEventListener('click', function(e) {
            e.stopPropagation();
            const text = this.closest('.chat-bubble').querySelector('.message').textContent;
            enhancedCopyToClipboard(text, this);
        });
    });
}

function initializeDeleteButtons() {
    // Add event listeners to all delete buttons
    document.querySelectorAll('.delete-button').forEach(button => {
        button.addEventListener('click', function(e) {
            e.stopPropagation();
            const bubble = this.closest('.chat-bubble');
            const timestamp = bubble.querySelector('.timestamp').textContent;
            const message = bubble.querySelector('.message').textContent;
            
            if (confirm(`Are you sure you want to delete this transcription from ${timestamp}?`)) {
                // Find the corresponding Streamlit delete button and click it
                const buttons = document.querySelectorAll('button[title="Delete this transcription"]');
                buttons.forEach(btn => {
                    if (btn.textContent.includes('🗑️')) {
                        btn.click();
                    }
                });
            }
        });
    });
}

function initializeScreenReader() {
    // Screen reader functionality is implemented in the add_screen_reader_js() function
    // This function serves as a placeholder for any additional screen reader initialization
    console.log('Screen reader functionality available');
}

function initializeChatBubbles() {
    // Add interactive effects to chat bubbles
    const chatBubbles = document.querySelectorAll('.chat-bubble');
    
    chatBubbles.forEach(bubble => {
        // Add click event for better mobile interaction
        bubble.addEventListener('click', function(e) {
            if (!e.target.closest('.actions') && !e.target.closest('button')) {
                this.style.backgroundColor = '#f8f9fa';
                setTimeout(() => {
                    this.style.backgroundColor = '';
                }, 300);
            }
        });
    });
}

function initializeMaterialIcons() {
    // Ensure Material Icons are properly loaded and displayed
    if (!document.querySelector('link[href*="material-symbols"]')) {
        const materialIconsLink = document.createElement('link');
        materialIconsLink.rel = 'stylesheet';
        materialIconsLink.href = 'https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200';
        document.head.appendChild(materialIconsLink);
    }
}

function setupMutationObserver() {
    // Observe DOM changes to handle dynamically added elements
    const observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            if (mutation.addedNodes.length) {
                // Reinitialize functionality for new elements
                initializeCopyButtons();
                initializeDeleteButtons();
                initializeChatBubbles();
            }
        });
    });
    
    // Start observing the document body for changes
    observer.observe(document.body, {
        childList: true,
        subtree: true
    });
}

// Utility function to show a temporary notification
function showNotification(message, type = 'info', duration = 3000) {
    const notification = document.createElement('div');
    notification.className = `kasuku-notification kasuku-notification-${type}`;
    notification.innerHTML = message;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 12px 20px;
        border-radius: 5px;
        color: white;
        z-index: 10000;
        font-family: 'Satoshi', sans-serif;
        font-weight: 500;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        transition: opacity 0.3s ease;
    `;
    
    if (type === 'success') {
        notification.style.backgroundColor = '#4CAF50';
    } else if (type === 'error') {
        notification.style.backgroundColor = '#f44336';
    } else if (type === 'warning') {
        notification.style.backgroundColor = '#ff9800';
    } else {
        notification.style.backgroundColor = '#2196F3';
    }
    
    document.body.appendChild(notification);
    
    // Animate in
    setTimeout(() => {
        notification.style.opacity = '1';
    }, 10);
    
    // Remove after duration
    setTimeout(() => {
        notification.style.opacity = '0';
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 300);
    }, duration);
}

// Enhanced copy to clipboard function with fallback
function enhancedCopyToClipboard(text, buttonElement = null) {
    if (!navigator.clipboard) {
        // Fallback for older browsers
        const textArea = document.createElement('textarea');
        textArea.value = text;
        textArea.style.position = 'fixed';
        textArea.style.top = 0;
        textArea.style.left = 0;
        textArea.style.width = '2em';
        textArea.style.height = '2em';
        textArea.style.padding = 0;
        textArea.style.border = 'none';
        textArea.style.outline = 'none';
        textArea.style.boxShadow = 'none';
        textArea.style.background = 'transparent';
        
        document.body.appendChild(textArea);
        textArea.select();
        
        try {
            const successful = document.execCommand('copy');
            document.body.removeChild(textArea);
            
            if (successful && buttonElement) {
                showCopyFeedback(buttonElement);
            }
            
            return successful;
        } catch (err) {
            console.error('Fallback copy failed:', err);
            document.body.removeChild(textArea);
            return false;
        }
    }
    
    // Modern clipboard API
    return navigator.clipboard.writeText(text).then(() => {
        if (buttonElement) {
            showCopyFeedback(buttonElement);
        }
        return true;
    }).catch(err => {
        console.error('Clipboard write failed:', err);
        return false;
    });
}

// Show visual feedback when text is copied
function showCopyFeedback(buttonElement) {
    const originalText = buttonElement.innerHTML;
    const originalBackground = buttonElement.style.backgroundColor;
    
    buttonElement.innerHTML = '<span class="material-symbols-outlined" style="font-size: 16px;">check</span> Copied!';
    buttonElement.style.backgroundColor = '#4CAF50';
    
    setTimeout(() => {
        buttonElement.innerHTML = originalText;
        buttonElement.style.backgroundColor = originalBackground;
    }, 2000);
}

// Clear transcription functionality
function clearTranscription() {
    // Find the transcription result element
    const transcriptionResult = document.querySelector('.success-box');
    if (transcriptionResult) {
        transcriptionResult.style.opacity = '0.5';
        setTimeout(() => {
            transcriptionResult.remove();
            showNotification('Transcription cleared', 'success');
            
            // Also trigger the Streamlit clear button if it exists
            const clearButtons = document.querySelectorAll('button');
            clearButtons.forEach(btn => {
                if (btn.textContent.includes('Clear Transcription')) {
                    btn.click();
                }
            });
        }, 300);
    } else {
        showNotification('No transcription to clear', 'warning');
    }
}

// Add clear button to the transcription result section
function addClearButton() {
    // Check if we're on a page with transcription results
    const successBox = document.querySelector('.success-box');
    if (successBox) {
        // Check if clear button already exists
        if (!document.querySelector('.clear-transcription-button')) {
            const copyButton = document.querySelector('#copy_main_result');
            if (copyButton) {
                const clearButton = document.createElement('button');
                clearButton.className = 'clear-transcription-button';
                clearButton.innerHTML = '<span class="material-symbols-outlined" style="font-size: 18px;">delete</span> Clear Transcription';
                clearButton.style.cssText = `
                    background-color: #f44336 !important;
                    color: white !important;
                    border: none !important;
                    border-radius: 20px !important;
                    padding: 0.5rem 1rem !important;
                    font-size: 1rem !important;
                    font-weight: 600 !important;
                    cursor: pointer !important;
                    transition: all 0.3s ease !important;
                    margin: 0.2rem !important;
                    display: inline-flex !important;
                    align-items: center !important;
                    gap: 4px !important;
                    margin-left: 10px !important;
                `;
                
                clearButton.addEventListener('mouseenter', function() {
                    this.style.backgroundColor = '#d32f2f !important';
                    this.style.transform = 'translateY(-1px) !important';
                });
                
                clearButton.addEventListener('mouseleave', function() {
                    this.style.backgroundColor = '#f44336 !important';
                    this.style.transform = 'none !important';
                });
                
                clearButton.addEventListener('click', clearTranscription);
                
                // Insert after the copy button
                copyButton.parentNode.appendChild(clearButton);
            }
        }
    }
}

// Keyboard navigation enhancements
document.addEventListener('keydown', function(e) {
    // Alt + C focuses on the search input
    if (e.altKey && e.key === 'c') {
        const searchInput = document.querySelector('input[placeholder*="Search"]');
        if (searchInput) {
            searchInput.focus();
            e.preventDefault();
        }
    }
    
    // Escape key closes any open notifications
    if (e.key === 'Escape') {
        const notifications = document.querySelectorAll('.kasuku-notification');
        notifications.forEach(notification => {
            notification.style.opacity = '0';
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.parentNode.removeChild(notification);
                }
            }, 300);
        });
    }
});

// Check for transcription results periodically and add clear button
setInterval(addClearButton, 1000);

// Export functions for potential use in other scripts
window.KasukuASR = {
    showNotification,
    enhancedCopyToClipboard,
    clearTranscription,
    initializeKasukuASR
};