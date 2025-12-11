const BASE_URL = "http://127.0.0.1:8000";

console.log('add.js loaded');
const formEl = document.getElementById("productForm");
if (!formEl) console.warn('productForm element not found');
else console.log('productForm element found');


formEl && formEl.addEventListener("submit", async function(e) {
      e.preventDefault();

    // Create FormData object from form
    const formData = new FormData(formEl);

    console.log("Submitting formData...");

    try {
        const response = await fetch(`${BASE_URL}/admin/products`, {
            method: "POST",
            body: formData
        });

        // Case 1: FastAPI returns redirect (303)
        if (response.redirected) {
            alert("Product added successfully!");
            window.location.href = response.url;
            return;
        }

        // Case 2: FastAPI returns JSON
        let result = {};
        try {
            result = await response.json();
        } catch (err) {
            // Non-JSON response (e.g., HTML redirect) – ignore
            console.warn("Non-JSON response received");
        }

        if (!response.ok) {
            alert("Error: " + (result.detail || "Unknown error"));
            return;
        }

        // Success
        alert(result.message || "Product added successfully!");
        console.log(result);

    } catch (error) {
        alert("Failed to add product");
        console.error(error);
    }

   
});
