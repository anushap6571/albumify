document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('logout-button').addEventListener('click', function() {
        window.location.href = '/logout';
    });
});

document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('playlist-list').addEventListener('click', function() {
        window.location.href = '/get_album';
    });
});