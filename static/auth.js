const API_URL = "/auth";

// -- Helper Functions --
function showSpinner(btnId) {
    const btn = document.querySelector(`#${btnId}`);
    if (btn) {
        const spinner = btn.querySelector('.spinner-sm');
        const text = btn.querySelector('#btn-text');
        if (spinner) spinner.style.display = 'block';
        if (text) text.style.opacity = '0';
        btn.disabled = true;
    }
}

function hideSpinner(btnId) {
    const btn = document.querySelector(`#${btnId}`);
    if (btn) {
        const spinner = btn.querySelector('.spinner-sm');
        const text = btn.querySelector('#btn-text');
        if (spinner) spinner.style.display = 'none';
        if (text) text.style.opacity = '1';
        btn.disabled = false;
    }
}

function showError(msg) {
    const el = document.getElementById('error-msg');
    if (el) el.textContent = msg;
}

function saveToken(token) {
    localStorage.setItem('access_token', token);
}

function getToken() {
    return localStorage.getItem('access_token');
}

function logout() {
    localStorage.removeItem('access_token');
    window.location.href = '/login';
}

// -- Page Specific Logic --

// REGISTER
const registerForm = document.getElementById('register-form');
if (registerForm) {
    registerForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        showSpinner('register-form button');
        showError('');

        const name = document.getElementById('name').value;
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;

        try {
            const response = await fetch(`${API_URL}/register`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ name, email, password })
            });

            // Handle non-JSON responses gracefully
            const textHTML = await response.text();
            let data;
            try {
                data = JSON.parse(textHTML);
            } catch (err) {
                console.error("Server returned non-JSON:", textHTML);
                // Try to infer error from status code if JSON parse fails
                if (response.status === 500) throw new Error("Internal Server Error. Please try again later.");
                throw new Error(`Server error (${response.status})`);
            }

            if (!response.ok || !data.success) {
                throw new Error(data.message || 'Registration failed');
            }

            // Success
            alert(data.message);
            window.location.href = '/login';

        } catch (err) {
            showError(err.message);
        } finally {
            hideSpinner('register-form button');
        }
    });
}

// LOGIN
const loginForm = document.getElementById('login-form');
if (loginForm) {
    loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        showSpinner('login-form button');
        showError('');

        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;

        try {
            const response = await fetch(`${API_URL}/login`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, password })
            });

            // Handle non-JSON responses gracefully
            const textHTML = await response.text();
            let data;
            try {
                data = JSON.parse(textHTML);
            } catch (err) {
                console.error("Server returned non-JSON:", textHTML);
                if (response.status === 500) throw new Error("Internal Server Error. Please try again later.");
                throw new Error(`Server error (${response.status})`);
            }

            if (!response.ok || !data.success) {
                throw new Error(data.message || 'Login failed');
            }

            // Success
            if (data.access_token) {
                saveToken(data.access_token);
                window.location.href = '/dashboard';
            } else {
                throw new Error("Login successful but no token received");
            }

        } catch (err) {
            showError(err.message);
        } finally {
            hideSpinner('login-form button');
        }
    });
}

// DASHBOARD CHECK
const userGreeting = document.getElementById('user-greeting');
if (userGreeting) {
    const token = getToken();
    if (!token) {
        window.location.href = '/login';
    } else {
        // Fetch User Info
        fetch(`${API_URL}/me`, {
            headers: { 'Authorization': `Bearer ${token}` }
        })
            .then(res => {
                if (!res.ok) throw new Error();
                return res.json();
            })
            .then(user => {
                userGreeting.textContent = `Welcome, ${user.name}`;
            })
            .catch(() => {
                // Silently fail or redirect if token clearly invalid
                // logout(); 
                console.log("Session invalid or expired");
            });
    }
}

// LOGOUT
const logoutBtn = document.getElementById('logout-btn');
if (logoutBtn) {
    logoutBtn.addEventListener('click', logout);
}
