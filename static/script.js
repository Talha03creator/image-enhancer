// --- CONFIG ---
const API_BASE = window.location.origin;

// --- STATE ---
let currentFile = null;
let currentFilter = 'auto';

// --- ELEMENTS ---
const dropZone = document.getElementById('drop-zone');
const fileInput = document.getElementById('file-input');
const browseBtn = document.getElementById('browse-btn');
const enhanceBtn = document.getElementById('enhance-btn');
const filterSelect = document.getElementById('filter-select');
const previewSection = document.getElementById('preview-section');
const originalPreview = document.getElementById('original-preview');
const enhancedPreview = document.getElementById('enhanced-preview');
const loader = document.getElementById('loader');
const downloadBtn = document.getElementById('download-btn');
const resetBtn = document.getElementById('reset-btn');

const toastVal = document.getElementById('toast');
const historyGrid = document.getElementById('history-grid');
const resizeOptions = document.getElementById('resize-options');

// --- AUTH CHECK ---
const token = localStorage.getItem('access_token');
if (!token) {
    window.location.href = '/login';
}

// --- INIT ---
document.addEventListener('DOMContentLoaded', () => {
    initTabs();
    initDragDrop();
    loadHistory();

    // Greeting
    const user = JSON.parse(localStorage.getItem('user'));
    if (user && document.getElementById('user-greeting')) {
        document.getElementById('user-greeting').textContent = user.name;
    }
});

// --- TABS & SIDEBAR ---
function initTabs() {
    const buttons = document.querySelectorAll('.dash-nav-item');
    const tabs = document.querySelectorAll('.tab-content');

    buttons.forEach(btn => {
        btn.addEventListener('click', () => {
            if (btn.getAttribute('onclick')) return; // Skip logout
            if (!btn.dataset.tab) return; // Skip items without tab data (like Welcome text)

            // Remove active
            buttons.forEach(b => b.classList.remove('active'));
            tabs.forEach(t => t.classList.remove('active'));

            // Set active
            btn.classList.add('active');
            const tabId = `tab-${btn.dataset.tab}`;
            const tabEl = document.getElementById(tabId);
            if (tabEl) tabEl.classList.add('active');

            if (btn.dataset.tab === 'history') {
                loadHistory();
            }
        });
    });
}

// --- DRAG & DROP ---
function initDragDrop() {
    if (!dropZone) return;

    browseBtn.addEventListener('click', () => fileInput.click());

    fileInput.addEventListener('change', (e) => handleFile(e.target.files[0]));

    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.style.borderColor = 'var(--primary-color)';
        dropZone.style.background = 'rgba(59, 130, 246, 0.1)';
    });

    dropZone.addEventListener('dragleave', (e) => {
        e.preventDefault();
        dropZone.style.borderColor = 'var(--border-color)';
        dropZone.style.background = 'rgba(15, 23, 42, 0.5)';
    });

    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.style.borderColor = 'var(--border-color)';
        dropZone.style.background = 'rgba(15, 23, 42, 0.5)';

        if (e.dataTransfer.files.length) {
            handleFile(e.dataTransfer.files[0]);
        }
    });
}

function handleFile(file) {
    if (!file.type.startsWith('image/')) {
        showToast('Please upload a valid image file (JPG, PNG).');
        return;
    }

    currentFile = file;

    // Show Preview
    const reader = new FileReader();
    reader.onload = (e) => {
        originalPreview.src = e.target.result;
        previewSection.style.display = 'block';

        // Hide upload, show controls
        dropZone.style.display = 'none';

        showToast('Image uploaded successfully.');
    };
    reader.readAsDataURL(file);
}

// --- FILTER CHANGE LOGIC ---
if (filterSelect) {
    filterSelect.addEventListener('change', () => {
        if (filterSelect.value === 'resize') {
            resizeOptions.style.display = 'flex';
        } else {
            resizeOptions.style.display = 'none';
        }
    });
}

// --- ENHANCE LOGIC ---
if (enhanceBtn) {
    enhanceBtn.addEventListener('click', async () => {
        if (!currentFile) return;

        // UI State
        enhanceBtn.disabled = true;
        enhanceBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Enhancing...';
        loader.style.display = 'flex';
        enhancedPreview.style.opacity = '0.5';

        const formData = new FormData();
        formData.append('file', currentFile);
        formData.append('filter_type', filterSelect.value);

        if (filterSelect.value === 'resize') {
            const w = document.getElementById('resize-width').value;
            const h = document.getElementById('resize-height').value;
            if (w) formData.append('width', w);
            if (h) formData.append('height', h);
        }

        try {
            const res = await fetch('/enhance', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`
                },
                body: formData
            });

            if (!res.ok) throw new Error('Enhancement failed');

            const blob = await res.blob();
            const url = URL.createObjectURL(blob);

            enhancedPreview.src = url;
            enhancedPreview.style.opacity = '1';
            loader.style.display = 'none';
            downloadBtn.href = url;
            downloadBtn.classList.remove('disabled');

            showToast('Enhancement complete!');
            loadHistory(); // Refresh history

        } catch (err) {
            showToast('Error enhancing image. Please try again.');
            console.error(err);
            enhancedPreview.style.opacity = '1';
            loader.style.display = 'none';
        } finally {
            enhanceBtn.disabled = false;
            enhanceBtn.innerHTML = 'Enhance Image <i class="fas fa-arrow-right"></i>';
        }
    });

    resetBtn.addEventListener('click', () => {
        currentFile = null;
        dropZone.style.display = 'block';
        previewSection.style.display = 'none';
        enhancedPreview.src = '';
        downloadBtn.classList.add('disabled');
        fileInput.value = '';
    });
}

// --- HISTORY LOGIC ---
async function loadHistory() {
    if (!historyGrid) return;

    try {
        const res = await fetch('/history', {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        const data = await res.json();

        historyGrid.innerHTML = '';

        if (data.length === 0) {
            historyGrid.innerHTML = '<p class="text-muted" style="grid-column: 1/-1; text-align: center;">No history found. Enhance an image to get started.</p>';
            return;
        }

        data.forEach(item => {
            const card = document.createElement('div');
            card.className = 'history-card';
            const date = new Date(item.timestamp).toLocaleDateString();

            card.innerHTML = `
                <img src="/outputs/${item.enhanced_filename}" class="history-img" alt="Enhanced">
                <div class="history-info">
                    <p class="history-date">${date}</p>
                    <div class="history-actions">
                        <a href="/outputs/${item.enhanced_filename}" download class="btn-sm btn-outline-light" style="color:white; text-decoration:none;">
                            <i class="fas fa-download"></i> Download
                        </a>
                    </div>
                </div>
            `;
            historyGrid.appendChild(card);
        });
    } catch (err) {
        console.error('Failed to load history', err);
    }
}

// --- UTILS ---
function showToast(msg) {
    const toast = document.getElementById('toast');
    toast.textContent = msg;
    toast.classList.remove('hidden');
    setTimeout(() => toast.classList.add('hidden'), 3000);
}

function logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    window.location.href = '/login';
}
