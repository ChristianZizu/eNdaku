// Message time out transition
const messageContainers = document.querySelectorAll('.message-container');
messageContainers.forEach(container => {
    setTimeout(() => {
        container.classList.add('fade-out');
    }, 3000);
    setTimeout(() => {
        container.remove();
    }, 4000);
});


