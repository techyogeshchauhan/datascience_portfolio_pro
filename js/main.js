// Mobile Menu Toggle
function toggleMobileMenu() {
    const mobileMenu = document.getElementById('mobile-menu');
    if (mobileMenu) {
        mobileMenu.classList.toggle('hidden');
    }
}

// Filter functionality for research projects
function filterProjects(category) {
    const projects = document.querySelectorAll('.research-project');
    const filterBtns = document.querySelectorAll('.filter-btn');
    
    // Update active filter button
    filterBtns.forEach(btn => btn.classList.remove('active'));
    event.target.classList.add('active');
    
    // Show/hide projects based on category
    projects.forEach(project => {
        if (category === 'all' || project.classList.contains(category)) {
            project.style.display = 'block';
            project.style.opacity = '1';
        } else {
            project.style.display = 'none';
            project.style.opacity = '0';
        }
    });
}

// Search functionality for research projects
function searchProjects(searchTerm) {
    const projects = document.querySelectorAll('.research-project');
    const term = searchTerm.toLowerCase();
    
    projects.forEach(project => {
        const title = project.querySelector('h3').textContent.toLowerCase();
        const description = project.querySelector('p').textContent.toLowerCase();
        
        if (title.includes(term) || description.includes(term)) {
            project.style.display = 'block';
            project.style.opacity = '1';
        } else {
            project.style.display = 'none';
            project.style.opacity = '0';
        }
    });
}

// Reset filters
function resetFilters() {
    const projects = document.querySelectorAll('.research-project');
    const filterBtns = document.querySelectorAll('.filter-btn');
    const searchInput = document.querySelector('input[type="text"]');
    
    // Reset filter buttons
    filterBtns.forEach(btn => btn.classList.remove('active'));
    document.querySelector('[data-filter="all"]')?.classList.add('active');
    
    // Clear search
    if (searchInput) searchInput.value = '';
    
    // Show all projects
    projects.forEach(project => {
        project.style.display = 'block';
        project.style.opacity = '1';
    });
}

// Publication filters
function filterPublications(type) {
    const publications = document.querySelectorAll('.publication-item');
    const filterBtns = document.querySelectorAll('.filter-btn');
    
    // Update active filter button
    filterBtns.forEach(btn => btn.classList.remove('active'));
    event.target.classList.add('active');
    
    // Show/hide publications based on type
    publications.forEach(publication => {
        if (type === 'all' || publication.dataset.type === type) {
            publication.style.display = 'block';
            publication.style.opacity = '1';
        } else {
            publication.style.display = 'none';
            publication.style.opacity = '0';
        }
    });
}

// Course expansion functionality
function expandCourse(courseId) {
    // This would typically open a modal or navigate to a detailed course page
    console.log(`Expanding course: ${courseId}`);
    // For now, we'll just scroll to the course section
    document.getElementById('courses')?.scrollIntoView({ behavior: 'smooth' });
}

// Form handling
function handleFormSubmit(event) {
    event.preventDefault();
    
    // Get form data
    const formData = new FormData(event.target);
    const data = Object.fromEntries(formData);
    
    // Basic validation
    if (!data.fullName || !data.email || !data.subject || !data.message) {
        alert('Please fill in all required fields.');
        return;
    }
    
    // Show success message (in a real app, this would submit to a server)
    alert('Thank you for your message! I will get back to you within 2-3 business days.');
    
    // Reset form
    event.target.reset();
}

// Dynamic form fields based on inquiry type
function updateFormFields() {
    const inquiryType = document.getElementById('inquiryType')?.value;
    const dynamicFields = document.getElementById('dynamicFields');
    const phoneField = document.getElementById('phoneField');
    
    if (!dynamicFields) return;
    
    // Clear existing dynamic fields
    dynamicFields.innerHTML = '';
    
    // Add specific fields based on inquiry type
    switch (inquiryType) {
        case 'research':
            dynamicFields.innerHTML = `
                <div>
                    <label for="researchArea" class="block text-sm font-semibold text-text-primary mb-2">Research Area</label>
                    <select id="researchArea" name="researchArea" class="input-field">
                        <option value="">Select research area...</option>
                        <option value="machine-learning">Machine Learning</option>
                        <option value="educational-analytics">Educational Analytics</option>
                        <option value="data-mining">Data Mining</option>
                        <option value="ai-applications">AI Applications</option>
                    </select>
                </div>
                <div>
                    <label for="timeline" class="block text-sm font-semibold text-text-primary mb-2">Project Timeline</label>
                    <input type="text" id="timeline" name="timeline" class="input-field" placeholder="e.g., 6 months, 1 year" />
                </div>
            `;
            break;
        case 'teaching':
            dynamicFields.innerHTML = `
                <div>
                    <label for="eventType" class="block text-sm font-semibold text-text-primary mb-2">Event Type</label>
                    <select id="eventType" name="eventType" class="input-field">
                        <option value="">Select event type...</option>
                        <option value="guest-lecture">Guest Lecture</option>
                        <option value="workshop">Workshop</option>
                        <option value="curriculum-development">Curriculum Development</option>
                        <option value="consulting">Educational Consulting</option>
                    </select>
                </div>
                <div>
                    <label for="audienceSize" class="block text-sm font-semibold text-text-primary mb-2">Expected Audience Size</label>
                    <input type="number" id="audienceSize" name="audienceSize" class="input-field" placeholder="e.g., 50" />
                </div>
            `;
            break;
        case 'speaking':
            dynamicFields.innerHTML = `
                <div>
                    <label for="eventDate" class="block text-sm font-semibold text-text-primary mb-2">Event Date</label>
                    <input type="date" id="eventDate" name="eventDate" class="input-field" />
                </div>
                <div>
                    <label for="speakingTopic" class="block text-sm font-semibold text-text-primary mb-2">Preferred Topics</label>
                    <textarea id="speakingTopic" name="speakingTopic" rows="3" class="input-field" placeholder="Data science education, machine learning applications, etc."></textarea>
                </div>
            `;
            break;
    }
}

// Show/hide phone field based on response method
document.addEventListener('DOMContentLoaded', function() {
    const responseMethodInputs = document.querySelectorAll('input[name="responseMethod"]');
    const phoneField = document.getElementById('phoneField');
    
    responseMethodInputs.forEach(input => {
        input.addEventListener('change', function() {
            if (phoneField) {
                if (this.value === 'phone') {
                    phoneField.classList.remove('hidden');
                } else {
                    phoneField.classList.add('hidden');
                }
            }
        });
    });
});

// Load more publications functionality
function loadMorePublications() {
    // This would typically load more publications from a server
    console.log('Loading more publications...');
    // For demo purposes, just show a message
    alert('More publications would be loaded here in a real application.');
}

// Smooth scrolling for anchor links
document.addEventListener('DOMContentLoaded', function() {
    const anchorLinks = document.querySelectorAll('a[href^="#"]');
    
    anchorLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href').substring(1);
            const targetElement = document.getElementById(targetId);
            
            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
});

// Add loading states for buttons
function addLoadingState(button) {
    const originalText = button.textContent;
    button.textContent = 'Loading...';
    button.disabled = true;
    
    // Simulate loading time
    setTimeout(() => {
        button.textContent = originalText;
        button.disabled = false;
    }, 2000);
}

// Initialize page functionality
document.addEventListener('DOMContentLoaded', function() {
    // Add click handlers for buttons that need loading states
    const actionButtons = document.querySelectorAll('.btn-primary, .btn-secondary, .btn-accent');
    
    actionButtons.forEach(button => {
        if (button.textContent.includes('Download') || button.textContent.includes('Load')) {
            button.addEventListener('click', function() {
                addLoadingState(this);
            });
        }
    });
    
    // Initialize any other page-specific functionality
    console.log('Academic portfolio initialized successfully');
});