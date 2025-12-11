document.getElementById("categoriesForm").addEventListener("submit", async function(e){
    e.preventDefault();

    let name = document.getElementById("category_name").value.trim();
    let message = document.getElementById("message");

    if(name === ""){
        message.style.color = "red";
        message.textContent = "Failed! Category name cannot be empty.";
        return;
    }

    // Send request to FastAPI
    let response = await fetch("admin/categories/add", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ category_name: name })
    });

    let result = await response.json();

    if(result.status === "success"){
        message.style.color = "green";
        message.textContent = result.message + " ✔";
        document.getElementById("categoriesForm").reset();
    } else {
        message.style.color = "red";
        message.textContent = result.message + " ✖";
    }
});
