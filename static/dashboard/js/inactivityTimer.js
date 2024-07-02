let inactivityTime = 0;
let warningTimeout;
let logoutTimeout;

document.addEventListener('mousemove', resetInactivityTimer);
document.addEventListener('keydown', resetInactivityTimer);

function resetInactivityTimer() {
    clearTimeouts();
    inactivityTime = 0;
}

function handleLogout() {
    // Redirect the user to the logout page or perform any other necessary actions
    window.location.href = "{% url 'BINA_healthcare_workers:healthcare-user-logout' %}";
}

function showWarningMessage() {
    const warningElement = document.querySelector('.inactivity-warning');
    warningElement.textContent = 'You will be logged out due to inactivity in 3 minutes.';
    warningElement.style.display = 'inline';
}

function startInactivityTimer() {
    clearTimeouts();

    warningTimeout = setTimeout(showWarningMessage, 12 * 60 * 1000); // 12 minutes (15 - 3)
    logoutTimeout = setTimeout(handleLogout, 15 * 60 * 1000); // 15 minutes
}

function clearTimeouts() {
    clearTimeout(warningTimeout);
    clearTimeout(logoutTimeout);
}

window.addEventListener('load', startInactivityTimer);