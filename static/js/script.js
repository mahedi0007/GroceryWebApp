const sidebar = document.getElementById("sidebar");
const openBtn = document.getElementById("openSidebar");
const closeBtn = document.getElementById("closeSidebar");

openBtn.onclick = () => {
    sidebar.classList.add("active");
}

closeBtn.onclick = () => {
    sidebar.classList.remove("active");
}
