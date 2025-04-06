function showRegister() {
    document.getElementById('auth-container').style.display = 'none';
    document.getElementById('register-container').style.display = 'block';
}

function showLogin() {
    document.getElementById('auth-container').style.display = 'block';
    document.getElementById('register-container').style.display = 'none';
}

function login() {
    let username = document.getElementById('login-username').value;
    let password = document.getElementById('login-password').value;
    
    if (username && password) {
        localStorage.setItem('user', username);
        document.getElementById('auth-container').style.display = 'none';
        document.getElementById('book-container').style.display = 'block';
    } else {
        alert('Please enter valid credentials!');
    }
}

function register() {
    let username = document.getElementById('register-username').value;
    let password = document.getElementById('register-password').value;
    
    if (username && password) {
        alert('Registration successful! Please login.');
        showLogin();
    } else {
        alert('All fields are required!');
    }
}

function logout() {
    localStorage.removeItem('user');
    document.getElementById('book-container').style.display = 'none';
    document.getElementById('auth-container').style.display = 'block';
}

function uploadBook() {
    let title = document.getElementById('book-title').value;
    let author = document.getElementById('book-author').value;
    let genre = document.getElementById('book-genre').value;
    let fileInput = document.getElementById('book-file');
    let file = fileInput.files[0];

    if (title && author && genre && file) {
        let reader = new FileReader();
        reader.onload = function(event) {
            let fileData = event.target.result;

            let list = document.getElementById('book-list');
            let li = document.createElement('li');
            li.innerHTML = `${title} by ${author} 
                <button onclick='readBook("${fileData}")'>Read</button>
                <button onclick='downloadBook("${file.name}", "${fileData}")'>Download</button>`;
            list.appendChild(li);
        };
        reader.readAsDataURL(file); // Convert file to Base64 for reading
    } else {
        alert('All fields are required!');
    }
}

function readBook(fileData) {
    let newWindow = window.open();
    newWindow.document.write(`<iframe src="${fileData}" width="100%" height="100%"></iframe>`);
}

function downloadBook(fileName, fileData) {
    let link = document.createElement('a');
    link.href = fileData;
    link.download = fileName;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

