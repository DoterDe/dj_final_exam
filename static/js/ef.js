const container = document.getElementById('container');
const registerBtn = document.getElementById('register');
const loginBtn = document.getElementById('login');

registerBtn.addEventListener('click', () => {
    container.classList.add("active");
});

loginBtn.addEventListener('click', () => {
    container.classList.remove("active");
});
function previewAvatar(event) {
    const avatarPreview = document.getElementById('avatar-preview');
    const file = event.target.files[0];
    
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            avatarPreview.src = e.target.result;
        }
        reader.readAsDataURL(file);
    }
}

document.getElementById('edit-profile-btn').onclick = function() {
    document.getElementById('edit-profile-modal').style.display = 'block';
}

