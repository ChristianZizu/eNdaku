const fileInput = document.getElementById('fileImage');
const thumbnail = document.getElementById('thumbnail');
const readerFile = new FileReader()
fileInput.addEventListener('change', (event) => {
    const file = event.target.files[0];
    if (file) {
        readerFile.onload = (event) => {
            thumbnail.setAttribute('src', event.target.result)
        }
        readerFile.readAsDataURL(file);
    } else {
        thumbnail.setAttribute('src', "{% static 'image/avatar.PNG' %}");
    }
});