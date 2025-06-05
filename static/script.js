// Schema Validator Frontend JavaScript

class SchemaValidator {
    constructor() {
        this.baseUrl = window.location.origin;
        this.initializeEventListeners();
        this.loadExampleSchemas();
    }

    initializeEventListeners() {
        const validateBtn = document.getElementById('validate-btn');
        const schemaTypeSelect = document.getElementById('schema-type');
        const platformSelect = document.getElementById('platform-select');

        validateBtn.addEventListener('click', () => this.validateSchema());
        
        // Auto-populate schema type based on platform selection
        platformSelect.addEventListener('change', () => this.updateSchemaTypeOptions());
        
        // User menu dropdown functionality
        this.initializeUserMenu();
        
        // Enable Enter key submission
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && e.ctrlKey) {
                this.validateSchema();
            }
        });
    }

    initializeUserMenu() {
        const userMenuToggle = document.getElementById('user-menu-toggle');
        const dropdownMenu = document.getElementById('user-dropdown-menu');

        if (userMenuToggle && dropdownMenu) {
            userMenuToggle.addEventListener('click', (e) => {
                e.stopPropagation();
                dropdownMenu.classList.toggle('show');
            });

            // Close dropdown when clicking outside
            document.addEventListener('click', (e) => {
                if (!e.target.closest('.user-dropdown')) {
                    dropdownMenu.classList.remove('show');
                }
            });

            // Prevent dropdown from closing when clicking inside it
            dropdownMenu.addEventListener('click', (e) => {
                e.stopPropagation();
            });
        }
    }

    updateSchemaTypeOptions() {
        const platform = document.getElementById('platform-select').value;
        const schemaTypeSelect = document.getElementById('schema-type');
        const options = schemaTypeSelect.querySelectorAll('option');

        // Reset schema type selection
        schemaTypeSelect.value = '';

        // Show/hide options based on platform selection
        options.forEach(option => {
            if (option.value === '') {
                // Always show the placeholder option
                option.style.display = 'block';
                option.disabled = false;
                return;
            }

            const supportedPlatforms = option.getAttribute('data-platforms');
            
            if (!platform) {
                // If no platform selected, show all options
                option.style.display = 'block';
                option.disabled = false;
            } else if (supportedPlatforms && supportedPlatforms.includes(platform)) {
                // Show if platform is supported
                option.style.display = 'block';
                option.disabled = false;
            } else {
                // Hide if platform is not supported
                option.style.display = 'none';
                option.disabled = true;
            }
        });

        // Auto-select if only one option is available for the platform
        if (platform) {
            const availableOptions = Array.from(options).filter(option => 
                option.value !== '' && 
                option.getAttribute('data-platforms') && 
                option.getAttribute('data-platforms').includes(platform)
            );
            
            if (availableOptions.length === 1) {
                schemaTypeSelect.value = availableOptions[0].value;
            }
        }
    }

    async loadExampleSchemas() {
        try {
            const response = await fetch(`${this.baseUrl}/api/v1/examples`);
            const examples = await response.json();
            
            // Store examples for potential use
            this.examples = examples;
        } catch (error) {
            console.log('Could not load examples:', error);
        }
    }

    async validateSchema() {
        const platform = document.getElementById('platform-select').value;
        const schemaType = document.getElementById('schema-type').value;
        const schemaContent = document.getElementById('schema-input').value.trim();
        const context = document.getElementById('context-input').value.trim();

        // Validation
        if (!schemaType) {
            this.showError('Please select a schema type');
            return;
        }

        if (!schemaContent) {
            this.showError('Please enter your schema content');
            return;
        }

        // Show loading state
        this.showLoading(true);
        this.hideResults();

        try {
            const requestBody = {
                schema_content: schemaContent,
                schema_type: schemaType,
                context: context || `${platform} schema validation`,
                include_best_practices: true,
                platform: platform // Add platform info for backend
            };

            const response = await fetch(`${this.baseUrl}/api/v1/validate`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(requestBody)
            });

            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }

            const result = await response.json();
            this.displayResults(result);

        } catch (error) {
            console.error('Validation error:', error);
            this.showError(`Validation failed: ${error.message}`);
        } finally {
            this.showLoading(false);
        }
    }

    displayResults(result) {
        const resultsSection = document.getElementById('results-section');
        const resultsContent = document.getElementById('results-content');
        const overallScore = document.getElementById('overall-score');

        // Show results section
        resultsSection.style.display = 'block';
        resultsSection.scrollIntoView({ behavior: 'smooth' });

        // Display overall score
        this.displayOverallScore(overallScore, result.overall_score);

        // Build results HTML
        let html = '';

        // Summary section
        if (result.summary) {
            html += `
                <div class="summary-section">
                    <h3><i class="fas fa-clipboard-list"></i> Summary</h3>
                    <p>${result.summary}</p>
                </div>
            `;
        }

        // Recommendations
        if (result.recommendations && result.recommendations.length > 0) {
            html += '<h3 style="margin-bottom: 20px;"><i class="fas fa-lightbulb"></i> Recommendations</h3>';
            
            result.recommendations.forEach(rec => {
                html += this.createRecommendationCard(rec);
            });
        }

        // Best practices section
        if (result.best_practices_applied || result.missing_best_practices) {
            html += this.createBestPracticesSection(result);
        }

        // Processing time
        if (result.processing_time) {
            html += `
                <div class="processing-time">
                    <i class="fas fa-clock"></i> 
                    Analysis completed in ${result.processing_time.toFixed(2)} seconds
                </div>
            `;
        }

        resultsContent.innerHTML = html;
    }

    displayOverallScore(element, score) {
        let scoreClass, scoreText, cuteMessage;
        
        if (score >= 8) {
            scoreClass = 'score-excellent';
            scoreText = 'Excellent';
            cuteMessage = 'Your schema has amazing vibes! ✨';
        } else if (score >= 6) {
            scoreClass = 'score-good';
            scoreText = 'Good';
            cuteMessage = 'Your schema has good vibes! 😊';
        } else if (score >= 4) {
            scoreClass = 'score-fair';
            scoreText = 'Fair';
            cuteMessage = 'Your schema has mixed vibes 🤔';
        } else {
            scoreClass = 'score-poor';
            scoreText = 'Needs Work';
            cuteMessage = 'Your schema did not pass the vibe check 😬';
        }

        element.className = `score-badge ${scoreClass}`;
        element.innerHTML = `
            <div class="score-display">
                <div class="score-number">Vibe Score: ${score}/10 - ${scoreText}</div>
                <div class="cute-message">${cuteMessage}</div>
            </div>
        `;
    }

    createRecommendationCard(recommendation) {
        const severityClass = `severity-${recommendation.severity}`;
        const categoryIcon = this.getCategoryIcon(recommendation.category);

        return `
            <div class="recommendation">
                <div class="recommendation-header">
                    <div class="recommendation-category">
                        <i class="${categoryIcon}"></i>
                        ${recommendation.category}
                    </div>
                    <span class="severity-badge ${severityClass}">
                        ${recommendation.severity}
                    </span>
                </div>
                <div class="recommendation-description">
                    ${recommendation.description}
                </div>
                <div class="recommendation-suggestion">
                    <strong>Suggestion:</strong> ${recommendation.suggestion}
                </div>
                <div class="recommendation-impact">
                    <strong>Impact:</strong> ${recommendation.impact}
                </div>
            </div>
        `;
    }

    createBestPracticesSection(result) {
        let html = '<h3 style="margin: 30px 0 20px 0;"><i class="fas fa-star"></i> Best Practices</h3>';
        html += '<div class="best-practices">';

        if (result.best_practices_applied && result.best_practices_applied.length > 0) {
            html += `
                <div class="practice-list applied">
                    <h4><i class="fas fa-check-circle"></i> Applied</h4>
                    <ul>
                        ${result.best_practices_applied.map(practice => `<li>${practice}</li>`).join('')}
                    </ul>
                </div>
            `;
        }

        if (result.missing_best_practices && result.missing_best_practices.length > 0) {
            html += `
                <div class="practice-list missing">
                    <h4><i class="fas fa-exclamation-circle"></i> Missing</h4>
                    <ul>
                        ${result.missing_best_practices.map(practice => `<li>${practice}</li>`).join('')}
                    </ul>
                </div>
            `;
        }

        html += '</div>';
        return html;
    }

    getCategoryIcon(category) {
        const iconMap = {
            'Naming Conventions': 'fas fa-tag',
            'Data Types': 'fas fa-database',
            'Constraints': 'fas fa-lock',
            'Indexing': 'fas fa-search',
            'Normalization': 'fas fa-project-diagram',
            'Scalability': 'fas fa-expand-arrows-alt',
            'Security': 'fas fa-shield-alt',
            'Documentation': 'fas fa-book',
            'Performance': 'fas fa-tachometer-alt',
            'error': 'fas fa-exclamation-triangle'
        };

        return iconMap[category] || 'fas fa-info-circle';
    }

    showLoading(show) {
        const loadingElement = document.getElementById('loading');
        const validateBtn = document.getElementById('validate-btn');
        
        if (show) {
            loadingElement.style.display = 'block';
            validateBtn.disabled = true;
            validateBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Analyzing...';
            loadingElement.scrollIntoView({ behavior: 'smooth' });
        } else {
            loadingElement.style.display = 'none';
            validateBtn.disabled = false;
            validateBtn.innerHTML = '<i class="fas fa-check-circle"></i> Validate Schema';
        }
    }

    hideResults() {
        document.getElementById('results-section').style.display = 'none';
    }

    showError(message) {
        // Create temporary error message
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error-message';
        errorDiv.style.cssText = `
            background: #f8d7da;
            color: #721c24;
            padding: 15px;
            border-radius: 8px;
            margin: 15px 0;
            border: 1px solid #f5c6cb;
            display: flex;
            align-items: center;
            gap: 10px;
        `;
        errorDiv.innerHTML = `<i class="fas fa-exclamation-triangle"></i> ${message}`;

        // Insert after form
        const inputSection = document.querySelector('.input-section');
        inputSection.appendChild(errorDiv);

        // Auto-remove after 5 seconds
        setTimeout(() => {
            if (errorDiv.parentNode) {
                errorDiv.parentNode.removeChild(errorDiv);
            }
        }, 5000);
    }

    // Utility methods for examples
    loadExample(type) {
        const schemaInput = document.getElementById('schema-input');
        const schemaTypeSelect = document.getElementById('schema-type');
        
        if (this.examples && this.examples[type]) {
            schemaInput.value = this.examples[type].content;
            schemaTypeSelect.value = type;
        }
    }
}

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new SchemaValidator();
});

// Export for potential external use
window.SchemaValidator = SchemaValidator; 