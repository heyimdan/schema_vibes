// Admin Panel JavaScript

class AdminPanel {
    constructor() {
        this.baseUrl = window.location.origin;
        this.currentSection = 'dashboard';
        this.bestPractices = [];
        this.schemaTypes = [];
        this.platforms = [];
        this.currentEditId = null;
        this.isAuthenticated = false;
        
        this.checkAuthentication();
    }

    async checkAuthentication() {
        try {
            const response = await fetch(`${this.baseUrl}/api/v1/auth/status`);
            const data = await response.json();
            this.isAuthenticated = data.authenticated;
            
            if (this.isAuthenticated) {
                this.showAdminPanel();
                this.initializeEventListeners();
                this.loadInitialData();
            } else {
                this.showLogin();
            }
        } catch (error) {
            console.error('Auth check failed:', error);
            this.showLogin();
        }
        
        // Check for login error in URL
        const urlParams = new URLSearchParams(window.location.search);
        if (urlParams.get('error') === 'invalid') {
            this.showLoginError('Invalid password. Please try again.');
        } else if (urlParams.get('error') === 'server') {
            this.showLoginError('Server error. Please try again.');
        }
    }

    showLogin() {
        document.getElementById('login-container').style.display = 'flex';
        document.getElementById('admin-container').style.display = 'none';
        this.setupLoginForm();
    }

    showAdminPanel() {
        document.getElementById('login-container').style.display = 'none';
        document.getElementById('admin-container').style.display = 'flex';
    }

    setupLoginForm() {
        const loginForm = document.getElementById('login-form');
        if (loginForm) {
            // Focus on password field
            document.getElementById('password').focus();
            
            // Handle enter key
            document.getElementById('password').addEventListener('keypress', (e) => {
                if (e.key === 'Enter') {
                    loginForm.submit();
                }
            });
        }
    }

    showLoginError(message) {
        const errorDiv = document.getElementById('login-error');
        if (errorDiv) {
            errorDiv.textContent = message;
            errorDiv.style.display = 'block';
        }
    }

    async logout() {
        try {
            const response = await fetch(`${this.baseUrl}/api/v1/auth/logout`, {
                method: 'POST'
            });
            
            if (response.ok) {
                this.isAuthenticated = false;
                this.showLogin();
                
                // Clear any cached data
                this.bestPractices = [];
                this.schemaTypes = [];
                this.platforms = [];
            }
        } catch (error) {
            console.error('Logout failed:', error);
            this.showToast('Logout failed', 'error');
        }
    }

    initializeEventListeners() {
        // Navigation
        document.querySelectorAll('.nav-item[data-section]').forEach(item => {
            item.addEventListener('click', (e) => {
                e.preventDefault();
                const section = item.dataset.section;
                this.switchSection(section);
            });
        });

        // Refresh button
        document.getElementById('refresh-btn').addEventListener('click', () => {
            this.loadInitialData();
        });

        // Logout button
        document.getElementById('logout-btn').addEventListener('click', () => {
            this.logout();
        });

        // Form submissions
        document.getElementById('add-practice-form').addEventListener('submit', (e) => {
            e.preventDefault();
            this.handleAddPractice();
        });

        document.getElementById('edit-practice-form').addEventListener('submit', (e) => {
            e.preventDefault();
            this.handleEditPractice();
        });

        // Form controls
        document.getElementById('clear-form-btn').addEventListener('click', () => {
            this.clearAddForm();
        });

        // Modal controls
        document.querySelectorAll('.modal-close').forEach(btn => {
            btn.addEventListener('click', () => {
                this.closeModals();
            });
        });

        document.getElementById('cancel-edit').addEventListener('click', () => {
            this.closeModals();
        });

        document.getElementById('cancel-delete').addEventListener('click', () => {
            this.closeModals();
        });

        document.getElementById('confirm-delete').addEventListener('click', () => {
            this.handleDeletePractice();
        });

        // Filters
        document.getElementById('filter-schema-type').addEventListener('change', () => {
            this.applyFilters();
        });

        document.getElementById('filter-platform').addEventListener('change', () => {
            this.applyFilters();
        });

        document.getElementById('filter-category').addEventListener('change', () => {
            this.applyFilters();
        });

        // Model configuration events
        document.getElementById('update-model-btn').addEventListener('click', () => {
            this.updateGPTModel();
        });

        // Close modals when clicking outside
        document.querySelectorAll('.modal').forEach(modal => {
            modal.addEventListener('click', (e) => {
                if (e.target === modal) {
                    this.closeModals();
                }
            });
        });
    }

    async loadInitialData() {
        this.showLoading(true);
        
        try {
            await Promise.all([
                this.loadStats(),
                this.loadSchemaTypes(),
                this.loadBestPractices(),
                this.loadCurrentModel()
            ]);
            
            this.populateFilters();
            this.updateDashboard();
            this.updateAnalytics();
            this.renderBestPracticesTable();
            
        } catch (error) {
            console.error('Error loading initial data:', error);
            this.showToast('Failed to load data', 'error');
        } finally {
            this.showLoading(false);
        }
    }

    async loadStats() {
        try {
            const response = await fetch(`${this.baseUrl}/api/v1/stats`);
            if (!response.ok) throw new Error('Failed to load stats');
            this.stats = await response.json();
        } catch (error) {
            console.error('Error loading stats:', error);
            this.stats = {};
        }
    }

    async loadSchemaTypes() {
        try {
            const response = await fetch(`${this.baseUrl}/api/v1/schema-types`);
            if (!response.ok) throw new Error('Failed to load schema types');
            this.schemaTypes = await response.json();
        } catch (error) {
            console.error('Error loading schema types:', error);
            this.schemaTypes = [];
        }
    }

    async loadBestPractices() {
        try {
            const response = await fetch(`${this.baseUrl}/api/v1/best-practices`);
            if (!response.ok) throw new Error('Failed to load best practices');
            this.bestPractices = await response.json();
        } catch (error) {
            console.error('Error loading best practices:', error);
            this.bestPractices = [];
        }
    }

    switchSection(section) {
        // Update navigation
        document.querySelectorAll('.nav-item').forEach(item => {
            item.classList.remove('active');
        });
        document.querySelector(`[data-section="${section}"]`).classList.add('active');

        // Update content sections
        document.querySelectorAll('.content-section').forEach(section => {
            section.classList.remove('active');
        });
        document.getElementById(`${section}-section`).classList.add('active');

        // Update page title
        const titles = {
            'dashboard': 'Dashboard',
            'best-practices': 'Best Practices',
            'add-practice': 'Add Practice',
            'analytics': 'Analytics'
        };
        document.getElementById('page-title').textContent = titles[section] || section;

        this.currentSection = section;

        // Load section-specific data
        if (section === 'add-practice') {
            this.setupAddForm();
        }
    }

    updateDashboard() {
        // Update stats cards
        document.getElementById('total-practices').textContent = this.stats.total_best_practices || 0;
        document.getElementById('schema-types-count').textContent = this.stats.supported_schema_types || 0;
        document.getElementById('ai-status').textContent = this.stats.ai_service_status || 'Unknown';
        
        // Count unique platforms from best practices
        const platforms = new Set();
        this.bestPractices.forEach(practice => {
            if (practice.metadata.platforms) {
                try {
                    const practicesPlatforms = JSON.parse(practice.metadata.platforms);
                    practicesPlatforms.forEach(p => platforms.add(p));
                } catch (e) {
                    // Ignore parsing errors
                }
            }
        });
        document.getElementById('platform-count').textContent = platforms.size;

        // Update charts
        this.updateCharts();
    }

    updateCharts() {
        // Category chart
        const categories = {};
        this.bestPractices.forEach(practice => {
            const category = practice.metadata.category || 'Other';
            categories[category] = (categories[category] || 0) + 1;
        });

        const categoryChart = document.getElementById('category-chart');
        categoryChart.innerHTML = this.createSimpleBarChart(categories);

        // Platform chart
        const platforms = {};
        this.bestPractices.forEach(practice => {
            if (practice.metadata.platforms) {
                try {
                    const practicesPlatforms = JSON.parse(practice.metadata.platforms);
                    if (practicesPlatforms.length === 0) {
                        platforms['All Platforms'] = (platforms['All Platforms'] || 0) + 1;
                    } else {
                        practicesPlatforms.forEach(p => {
                            platforms[p] = (platforms[p] || 0) + 1;
                        });
                    }
                } catch (e) {
                    platforms['All Platforms'] = (platforms['All Platforms'] || 0) + 1;
                }
            } else {
                platforms['All Platforms'] = (platforms['All Platforms'] || 0) + 1;
            }
        });

        const platformChart = document.getElementById('platform-chart');
        platformChart.innerHTML = this.createSimpleBarChart(platforms);
    }

    createSimpleBarChart(data) {
        if (Object.keys(data).length === 0) {
            return '<p class="text-center text-muted">No data available</p>';
        }

        const maxValue = Math.max(...Object.values(data));
        let html = '<div class="simple-chart">';
        
        Object.entries(data).forEach(([label, value]) => {
            const percentage = (value / maxValue) * 100;
            html += `
                <div class="chart-item" style="margin-bottom: 0.5rem;">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 0.25rem;">
                        <span style="font-size: 0.8rem;">${label}</span>
                        <span style="font-size: 0.8rem; font-weight: 600;">${value}</span>
                    </div>
                    <div style="background: #e2e8f0; height: 8px; border-radius: 4px; overflow: hidden;">
                        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); height: 100%; width: ${percentage}%; transition: width 0.3s ease;"></div>
                    </div>
                </div>
            `;
        });
        
        html += '</div>';
        return html;
    }

    updateAnalytics() {
        // Category analytics
        const categories = {};
        this.bestPractices.forEach(practice => {
            const category = practice.metadata.category || 'Other';
            categories[category] = (categories[category] || 0) + 1;
        });

        const categoryAnalytics = document.getElementById('category-analytics');
        categoryAnalytics.innerHTML = this.createAnalyticsItems(categories);

        // Severity analytics
        const severities = {};
        this.bestPractices.forEach(practice => {
            const severity = practice.metadata.severity || 'unknown';
            severities[severity] = (severities[severity] || 0) + 1;
        });

        const severityAnalytics = document.getElementById('severity-analytics');
        severityAnalytics.innerHTML = this.createAnalyticsItems(severities);

        // Schema coverage analytics
        const schemaTypeCoverage = {};
        this.schemaTypes.forEach(type => {
            schemaTypeCoverage[type] = 0;
        });

        this.bestPractices.forEach(practice => {
            if (practice.metadata.schema_types) {
                try {
                    const types = JSON.parse(practice.metadata.schema_types);
                    types.forEach(type => {
                        if (schemaTypeCoverage.hasOwnProperty(type)) {
                            schemaTypeCoverage[type]++;
                        }
                    });
                } catch (e) {
                    // Ignore parsing errors
                }
            }
        });

        const schemaAnalytics = document.getElementById('schema-coverage-analytics');
        schemaAnalytics.innerHTML = this.createAnalyticsItems(schemaTypeCoverage);
    }

    createAnalyticsItems(data) {
        if (Object.keys(data).length === 0) {
            return '<p class="text-muted">No data available</p>';
        }

        return Object.entries(data)
            .sort(([,a], [,b]) => b - a)
            .map(([label, value]) => `
                <div class="analytics-item">
                    <span class="analytics-label">${label}</span>
                    <span class="analytics-value">${value}</span>
                </div>
            `).join('');
    }

    populateFilters() {
        // Schema type filter
        const schemaFilter = document.getElementById('filter-schema-type');
        schemaFilter.innerHTML = '<option value="">All Schema Types</option>';
        this.schemaTypes.forEach(type => {
            schemaFilter.innerHTML += `<option value="${type}">${type}</option>`;
        });

        // Platform filter
        const platforms = new Set();
        this.bestPractices.forEach(practice => {
            if (practice.metadata.platforms) {
                try {
                    const practicesPlatforms = JSON.parse(practice.metadata.platforms);
                    practicesPlatforms.forEach(p => platforms.add(p));
                } catch (e) {
                    // Ignore parsing errors
                }
            }
        });

        const platformFilter = document.getElementById('filter-platform');
        platformFilter.innerHTML = '<option value="">All Platforms</option>';
        Array.from(platforms).sort().forEach(platform => {
            platformFilter.innerHTML += `<option value="${platform}">${platform}</option>`;
        });

        // Category filter
        const categories = new Set();
        this.bestPractices.forEach(practice => {
            if (practice.metadata.category) {
                categories.add(practice.metadata.category);
            }
        });

        const categoryFilter = document.getElementById('filter-category');
        categoryFilter.innerHTML = '<option value="">All Categories</option>';
        Array.from(categories).sort().forEach(category => {
            categoryFilter.innerHTML += `<option value="${category}">${category}</option>`;
        });
    }

    applyFilters() {
        const schemaTypeFilter = document.getElementById('filter-schema-type').value;
        const platformFilter = document.getElementById('filter-platform').value;
        const categoryFilter = document.getElementById('filter-category').value;

        const filteredPractices = this.bestPractices.filter(practice => {
            // Schema type filter
            if (schemaTypeFilter) {
                try {
                    const schemaTypes = JSON.parse(practice.metadata.schema_types || '[]');
                    if (!schemaTypes.includes(schemaTypeFilter)) {
                        return false;
                    }
                } catch (e) {
                    return false;
                }
            }

            // Platform filter
            if (platformFilter) {
                try {
                    const platforms = JSON.parse(practice.metadata.platforms || '[]');
                    if (platforms.length > 0 && !platforms.includes(platformFilter)) {
                        return false;
                    }
                } catch (e) {
                    return false;
                }
            }

            // Category filter
            if (categoryFilter && practice.metadata.category !== categoryFilter) {
                return false;
            }

            return true;
        });

        this.renderBestPracticesTable(filteredPractices);
    }

    renderBestPracticesTable(practices = null) {
        const practicesData = practices || this.bestPractices;
        const tbody = document.getElementById('practices-tbody');
        
        if (practicesData.length === 0) {
            tbody.innerHTML = `
                <tr>
                    <td colspan="7" class="text-center text-muted" style="padding: 2rem;">
                        No best practices found
                    </td>
                </tr>
            `;
            return;
        }

        tbody.innerHTML = practicesData.map(practice => {
            const metadata = practice.metadata;
            
            // Parse schema types
            let schemaTypes = [];
            try {
                schemaTypes = JSON.parse(metadata.schema_types || '[]');
            } catch (e) {
                schemaTypes = [];
            }

            // Parse platforms
            let platforms = [];
            try {
                platforms = JSON.parse(metadata.platforms || '[]');
            } catch (e) {
                platforms = [];
            }

            return `
                <tr>
                    <td><code>${practice.id}</code></td>
                    <td>
                        <div style="max-width: 200px;">
                            <strong>${this.extractTitle(practice.content)}</strong>
                        </div>
                    </td>
                    <td>
                        <span class="badge badge-schema">${metadata.category || 'N/A'}</span>
                    </td>
                    <td>
                        <div style="max-width: 150px;">
                            ${schemaTypes.map(type => 
                                `<span class="badge badge-schema">${type}</span>`
                            ).join(' ')}
                        </div>
                    </td>
                    <td>
                        <div style="max-width: 150px;">
                            ${platforms.length === 0 ? 
                                '<span class="badge badge-platform">All</span>' :
                                platforms.map(platform => 
                                    `<span class="badge badge-platform">${platform}</span>`
                                ).join(' ')
                            }
                        </div>
                    </td>
                    <td>
                        <span class="badge badge-severity-${metadata.severity || 'medium'}">
                            ${metadata.severity || 'Medium'}
                        </span>
                    </td>
                    <td>
                        <div style="display: flex; gap: 0.5rem;">
                            <button class="btn btn-secondary btn-small" onclick="adminPanel.editPractice('${practice.id}')">
                                <i class="fas fa-edit"></i>
                            </button>
                            <button class="btn btn-danger btn-small" onclick="adminPanel.deletePractice('${practice.id}')">
                                <i class="fas fa-trash"></i>
                            </button>
                        </div>
                    </td>
                </tr>
            `;
        }).join('');
    }

    extractTitle(content) {
        // Extract title from content (before the first colon)
        const colonIndex = content.indexOf(':');
        if (colonIndex > 0) {
            return content.substring(0, colonIndex).trim();
        }
        return content.substring(0, 50) + (content.length > 50 ? '...' : '');
    }

    setupAddForm() {
        // Populate schema types checkboxes
        const schemaTypesContainer = document.getElementById('schema-types-checkboxes');
        schemaTypesContainer.innerHTML = this.schemaTypes.map(type => `
            <div class="checkbox-item">
                <input type="checkbox" id="schema-${type}" name="schema_types" value="${type}">
                <label for="schema-${type}">${type}</label>
            </div>
        `).join('');

        // Populate platforms checkboxes
        const platformsList = ['venice', 'espresso', 'kafka', 'pinot', 'mysql', 'tidb'];
        const platformsContainer = document.getElementById('platforms-checkboxes');
        platformsContainer.innerHTML = platformsList.map(platform => `
            <div class="checkbox-item">
                <input type="checkbox" id="platform-${platform}" name="platforms" value="${platform}">
                <label for="platform-${platform}">${platform}</label>
            </div>
        `).join('');
    }

    async handleAddPractice() {
        const formData = this.getFormData('add-practice-form');
        
        if (!this.validatePracticeForm(formData)) {
            return;
        }

        this.showLoading(true);

        try {
            const response = await fetch(`${this.baseUrl}/api/v1/best-practices`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            });

            if (response.ok) {
                this.showToast('Best practice added successfully!', 'success');
                this.clearAddForm();
                await this.loadBestPractices();
                this.renderBestPracticesTable();
                this.updateDashboard();
                this.switchSection('best-practices');
            } else {
                const error = await response.json();
                throw new Error(error.detail || 'Failed to add best practice');
            }
        } catch (error) {
            console.error('Error adding practice:', error);
            this.showToast(`Failed to add practice: ${error.message}`, 'error');
        } finally {
            this.showLoading(false);
        }
    }

    editPractice(practiceId) {
        const practice = this.bestPractices.find(p => p.id === practiceId);
        if (!practice) {
            this.showToast('Practice not found', 'error');
            return;
        }

        this.currentEditId = practiceId;
        
        // Extract data from practice
        const title = this.extractTitle(practice.content);
        const description = practice.content.substring(practice.content.indexOf(':') + 1).trim();
        
        let schemaTypes = [];
        let platforms = [];
        let examples = [];

        try {
            schemaTypes = JSON.parse(practice.metadata.schema_types || '[]');
            platforms = JSON.parse(practice.metadata.platforms || '[]');
            examples = JSON.parse(practice.metadata.examples || '[]');
        } catch (e) {
            console.error('Error parsing practice metadata:', e);
        }

        // Create edit form
        const editForm = document.getElementById('edit-practice-form');
        editForm.innerHTML = `
            <div class="form-row">
                <div class="form-group">
                    <label for="edit-practice-id">Practice ID *</label>
                    <input type="text" id="edit-practice-id" name="id" value="${practice.id}" readonly>
                </div>
                <div class="form-group">
                    <label for="edit-practice-title">Title *</label>
                    <input type="text" id="edit-practice-title" name="title" value="${title}" required>
                </div>
            </div>
            <div class="form-group">
                <label for="edit-practice-description">Description *</label>
                <textarea id="edit-practice-description" name="description" required rows="3">${description}</textarea>
            </div>
            <div class="form-row">
                <div class="form-group">
                    <label for="edit-practice-category">Category *</label>
                    <input type="text" id="edit-practice-category" name="category" value="${practice.metadata.category || ''}" required>
                </div>
                <div class="form-group">
                    <label for="edit-practice-severity">Severity *</label>
                    <select id="edit-practice-severity" name="severity" required>
                        <option value="">Select Severity</option>
                        <option value="low" ${practice.metadata.severity === 'low' ? 'selected' : ''}>Low</option>
                        <option value="medium" ${practice.metadata.severity === 'medium' ? 'selected' : ''}>Medium</option>
                        <option value="high" ${practice.metadata.severity === 'high' ? 'selected' : ''}>High</option>
                    </select>
                </div>
            </div>
            <div class="form-row">
                <div class="form-group">
                    <label>Applicable Schema Types *</label>
                    <div class="checkbox-group">
                        ${this.schemaTypes.map(type => `
                            <div class="checkbox-item">
                                <input type="checkbox" id="edit-schema-${type}" name="schema_types" value="${type}" 
                                       ${schemaTypes.includes(type) ? 'checked' : ''}>
                                <label for="edit-schema-${type}">${type}</label>
                            </div>
                        `).join('')}
                    </div>
                </div>
                <div class="form-group">
                    <label>Applicable Platforms</label>
                    <div class="checkbox-group">
                        ${['venice', 'espresso', 'kafka', 'pinot', 'mysql', 'tidb'].map(platform => `
                            <div class="checkbox-item">
                                <input type="checkbox" id="edit-platform-${platform}" name="platforms" value="${platform}"
                                       ${platforms.includes(platform) ? 'checked' : ''}>
                                <label for="edit-platform-${platform}">${platform}</label>
                            </div>
                        `).join('')}
                    </div>
                </div>
            </div>
            <div class="form-group">
                <label for="edit-practice-examples">Examples (separate with "---" on a new line)</label>
                <textarea id="edit-practice-examples" name="examples" rows="6">${examples.join('\n---\n')}</textarea>
            </div>
        `;

        // Show edit modal
        document.getElementById('edit-modal').classList.add('active');
    }

    async handleEditPractice() {
        const formData = this.getFormData('edit-practice-form');
        formData.id = this.currentEditId;
        
        if (!this.validatePracticeForm(formData)) {
            return;
        }

        this.showLoading(true);

        try {
            const response = await fetch(`${this.baseUrl}/api/v1/best-practices/${this.currentEditId}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            });

            if (response.ok) {
                this.showToast('Best practice updated successfully!', 'success');
                this.closeModals();
                await this.loadBestPractices();
                this.renderBestPracticesTable();
                this.updateDashboard();
            } else {
                const error = await response.json();
                throw new Error(error.detail || 'Failed to update best practice');
            }
        } catch (error) {
            console.error('Error updating practice:', error);
            this.showToast(`Failed to update practice: ${error.message}`, 'error');
        } finally {
            this.showLoading(false);
        }
    }

    deletePractice(practiceId) {
        const practice = this.bestPractices.find(p => p.id === practiceId);
        if (!practice) {
            this.showToast('Practice not found', 'error');
            return;
        }

        this.currentEditId = practiceId;
        const title = this.extractTitle(practice.content);
        document.getElementById('delete-practice-title').textContent = title;
        document.getElementById('delete-modal').classList.add('active');
    }

    async handleDeletePractice() {
        this.showLoading(true);

        try {
            const response = await fetch(`${this.baseUrl}/api/v1/best-practices/${this.currentEditId}`, {
                method: 'DELETE'
            });

            if (response.ok) {
                this.showToast('Best practice deleted successfully!', 'success');
                this.closeModals();
                await this.loadBestPractices();
                this.renderBestPracticesTable();
                this.updateDashboard();
            } else {
                const error = await response.json();
                throw new Error(error.detail || 'Failed to delete best practice');
            }
        } catch (error) {
            console.error('Error deleting practice:', error);
            this.showToast(`Failed to delete practice: ${error.message}`, 'error');
        } finally {
            this.showLoading(false);
        }
    }

    getFormData(formId) {
        const form = document.getElementById(formId);
        const formData = new FormData(form);
        
        const data = {
            id: formData.get('id'),
            title: formData.get('title'),
            description: formData.get('description'),
            category: formData.get('category'),
            severity_if_missing: formData.get('severity'),
            applicable_schema_types: formData.getAll('schema_types'),
            applicable_platforms: formData.getAll('platforms'),
            examples: formData.get('examples') ? 
                formData.get('examples').split('---').map(ex => ex.trim()).filter(ex => ex.length > 0) : []
        };

        return data;
    }

    validatePracticeForm(data) {
        if (!data.id || !data.title || !data.description || !data.category || !data.severity_if_missing) {
            this.showToast('Please fill in all required fields', 'error');
            return false;
        }

        if (data.applicable_schema_types.length === 0) {
            this.showToast('Please select at least one schema type', 'error');
            return false;
        }

        return true;
    }

    clearAddForm() {
        document.getElementById('add-practice-form').reset();
        // Uncheck all checkboxes
        document.querySelectorAll('#add-practice-form input[type="checkbox"]').forEach(cb => {
            cb.checked = false;
        });
    }

    closeModals() {
        document.querySelectorAll('.modal').forEach(modal => {
            modal.classList.remove('active');
        });
        this.currentEditId = null;
    }

    async updateGPTModel() {
        const selectedModel = document.getElementById('gpt-model-select').value;
        
        if (!selectedModel) {
            this.showToast('Please select a model', 'error');
            return;
        }

        this.showLoading(true);

        try {
            const response = await fetch(`${this.baseUrl}/api/v1/config/model`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ model: selectedModel })
            });

            if (response.ok) {
                const result = await response.json();
                this.showToast('Model updated successfully!', 'success');
                document.getElementById('current-model').textContent = selectedModel;
            } else {
                const error = await response.json();
                throw new Error(error.detail || 'Failed to update model');
            }
        } catch (error) {
            console.error('Error updating model:', error);
            this.showToast(`Failed to update model: ${error.message}`, 'error');
        } finally {
            this.showLoading(false);
        }
    }

    async loadCurrentModel() {
        try {
            const response = await fetch(`${this.baseUrl}/api/v1/config/model`);
            if (response.ok) {
                const result = await response.json();
                const currentModel = result.current_model || 'gpt-4o-mini';
                document.getElementById('current-model').textContent = currentModel;
                document.getElementById('gpt-model-select').value = currentModel;
            }
        } catch (error) {
            console.error('Error loading current model:', error);
            // Use default if can't load
        }
    }

    showLoading(show) {
        const overlay = document.getElementById('loading-overlay');
        if (show) {
            overlay.classList.add('active');
        } else {
            overlay.classList.remove('active');
        }
    }

    showToast(message, type = 'info') {
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.textContent = message;

        const container = document.getElementById('toast-container');
        container.appendChild(toast);

        // Trigger animation
        setTimeout(() => {
            toast.classList.add('show');
        }, 100);

        // Remove after 4 seconds
        setTimeout(() => {
            toast.classList.remove('show');
            setTimeout(() => {
                if (toast.parentNode) {
                    toast.parentNode.removeChild(toast);
                }
            }, 300);
        }, 4000);
    }
}

// Initialize admin panel when DOM is loaded
let adminPanel;
document.addEventListener('DOMContentLoaded', () => {
    adminPanel = new AdminPanel();
});

// Export for global access
window.adminPanel = adminPanel; 