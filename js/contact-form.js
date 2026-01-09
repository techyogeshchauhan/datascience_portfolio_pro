// Contact Form Handler with Python Flask Backend
// Uses Gmail SMTP for email delivery

document.addEventListener('DOMContentLoaded', function() {
    const contactForm = document.getElementById('contactForm');
    
    if (contactForm) {
        contactForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            // Show loading state
            const submitButton = contactForm.querySelector('button[type="submit"]');
            const originalButtonText = submitButton.innerHTML;
            submitButton.disabled = true;
            submitButton.innerHTML = `
                <svg class="animate-spin h-5 w-5 mr-2 inline" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Sending...
            `;
            
            try {
                // Get form data
                const formData = new FormData(contactForm);
                
                // Send to Python backend
                const response = await fetch('/send-email', {
                    method: 'POST',
                    body: formData
                });
                
                const result = await response.json();
                
                if (result.success) {
                    // Show success message
                    showNotification('✅ Success! ' + result.message, 'success');
                    
                    // Reset form
                    contactForm.reset();
                    
                    // Scroll to top
                    window.scrollTo({ top: 0, behavior: 'smooth' });
                } else {
                    throw new Error(result.message || 'Failed to send message');
                }
            } catch (error) {
                console.error('Error:', error);
                showNotification('❌ Oops! Failed to send message. Please try again or email directly at soni6102000@gmail.com', 'error');
            } finally {
                // Restore button
                submitButton.disabled = false;
                submitButton.innerHTML = originalButtonText;
            }
        });
    }
});

// Show notification
function showNotification(message, type) {
    // Remove any existing notifications
    const existingNotifications = document.querySelectorAll('.notification-popup');
    existingNotifications.forEach(n => n.remove());
    
    const notification = document.createElement('div');
    notification.className = `notification-popup fixed top-20 left-1/2 transform -translate-x-1/2 z-50 p-6 rounded-lg shadow-2xl max-w-md w-full mx-4 ${
        type === 'success' ? 'bg-green-500 text-white' : 'bg-red-500 text-white'
    }`;
    notification.style.animation = 'slideDown 0.5s ease-out';
    notification.innerHTML = `
        <div class="flex items-start">
            <svg class="w-6 h-6 mr-3 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                ${type === 'success' 
                    ? '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>'
                    : '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z"></path>'
                }
            </svg>
            <div class="flex-1">
                <p class="font-semibold mb-1">${type === 'success' ? 'Message Sent!' : 'Error'}</p>
                <p class="text-sm">${message}</p>
            </div>
            <button onclick="this.parentElement.parentElement.remove()" class="ml-4 text-white hover:text-gray-200">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                </svg>
            </button>
        </div>
    `;
    
    // Add animation styles
    const style = document.createElement('style');
    style.textContent = `
        @keyframes slideDown {
            from {
                opacity: 0;
                transform: translate(-50%, -100%);
            }
            to {
                opacity: 1;
                transform: translate(-50%, 0);
            }
        }
    `;
    document.head.appendChild(style);
    
    document.body.appendChild(notification);
    
    // Remove after 8 seconds
    setTimeout(() => {
        notification.style.animation = 'slideDown 0.5s ease-out reverse';
        setTimeout(() => notification.remove(), 500);
    }, 8000);
}

// Dynamic field updates based on inquiry type
function updateFormFields() {
    const inquiryType = document.getElementById('inquiryType');
    const dynamicFields = document.getElementById('dynamicFields');
    
    if (!inquiryType || !dynamicFields) return;
    
    const type = inquiryType.value;
    let fieldsHTML = '';
    
    switch(type) {
        case 'research':
            fieldsHTML = `
                <div>
                    <label for="researchArea" class="block text-sm font-semibold text-text-primary mb-2">Research Area</label>
                    <input type="text" id="researchArea" name="researchArea" class="input-field" placeholder="e.g., Machine Learning, AI, Data Mining" />
                </div>
                <div>
                    <label for="timeline" class="block text-sm font-semibold text-text-primary mb-2">Proposed Timeline</label>
                    <input type="text" id="timeline" name="timeline" class="input-field" placeholder="e.g., 6 months, 1 year" />
                </div>
            `;
            break;
        case 'teaching':
            fieldsHTML = `
                <div>
                    <label for="eventDate" class="block text-sm font-semibold text-text-primary mb-2">Event Date</label>
                    <input type="date" id="eventDate" name="eventDate" class="input-field" />
                </div>
                <div>
                    <label for="audienceSize" class="block text-sm font-semibold text-text-primary mb-2">Expected Audience Size</label>
                    <input type="number" id="audienceSize" name="audienceSize" class="input-field" placeholder="e.g., 50" />
                </div>
            `;
            break;
        case 'speaking':
            fieldsHTML = `
                <div>
                    <label for="eventType" class="block text-sm font-semibold text-text-primary mb-2">Event Type</label>
                    <select id="eventType" name="eventType" class="input-field">
                        <option value="">Select event type...</option>
                        <option value="conference">Conference</option>
                        <option value="workshop">Workshop</option>
                        <option value="webinar">Webinar</option>
                        <option value="podcast">Podcast</option>
                    </select>
                </div>
            `;
            break;
        case 'mentorship':
            fieldsHTML = `
                <div>
                    <label for="currentLevel" class="block text-sm font-semibold text-text-primary mb-2">Current Academic Level</label>
                    <select id="currentLevel" name="currentLevel" class="input-field">
                        <option value="">Select level...</option>
                        <option value="undergraduate">Undergraduate</option>
                        <option value="masters">Master's Student</option>
                        <option value="phd">PhD Candidate</option>
                        <option value="professional">Working Professional</option>
                    </select>
                </div>
            `;
            break;
    }
    
    dynamicFields.innerHTML = fieldsHTML;
}

// Show/hide phone field based on response method
document.addEventListener('DOMContentLoaded', function() {
    const responseMethodRadios = document.querySelectorAll('input[name="responseMethod"]');
    const phoneField = document.getElementById('phoneField');
    
    if (responseMethodRadios && phoneField) {
        responseMethodRadios.forEach(radio => {
            radio.addEventListener('change', function() {
                if (this.value === 'phone') {
                    phoneField.classList.remove('hidden');
                } else {
                    phoneField.classList.add('hidden');
                }
            });
        });
    }
});
