document.addEventListener("DOMContentLoaded", function () {
    applyStockStatusStyles();

    document.querySelectorAll(".dropdown-btn").forEach(btn => {
        btn.addEventListener("click", function (event) {
            event.stopPropagation();
            closeAllDropdowns();
            this.nextElementSibling.classList.toggle("show");
        });
    });

    document.addEventListener("click", closeAllDropdowns);

    function closeAllDropdowns() {
        document.querySelectorAll(".dropdown-content").forEach(dropdown => {
            dropdown.classList.remove("show");
        });
    }

    document.querySelectorAll(".edit-btn").forEach(button => {
        button.addEventListener("click", function () {
            const row = this.closest("tr");
            if (this.textContent === "Edit") {
                makeRowEditable(row, this);
            } else {
                saveRowData(row, this);
            }
        });
    });

    document.querySelectorAll(".delete-btn").forEach(btn => {
        btn.addEventListener("click", function () {
            const productId = this.dataset.id;
            fetch("/delete-product", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ id: productId })
            }).then(res => res.json()).then(data => {
                alert(data.message);
                location.reload();
            });
        });
    });
});

function applyStockStatusStyles() {
    document.querySelectorAll(".editable.status").forEach(cell => {
        const statusText = cell.dataset.status || cell.textContent.trim();
        cell.innerHTML = `<span class="status-badge">${statusText}</span>`;
        const badge = cell.querySelector(".status-badge");

        badge.classList.remove("in-stock", "low-stock", "out-of-stock");

        if (statusText.toLowerCase() === "available") {
            badge.classList.add("in-stock");
        } else if (statusText.toLowerCase() === "low stock") {
            badge.classList.add("low-stock");
        } else if (statusText.toLowerCase() === "out of stock") {
            badge.classList.add("out-of-stock");
        }
    });
}

function makeRowEditable(row, button) {
    const cells = row.querySelectorAll("td:not(:last-child)");

    cells.forEach((cell, index) => {
        if (index > 0 && !cell.classList.contains("status")) {
            const input = document.createElement("input");
            input.type = "text";
            input.value = cell.innerText;
            cell.innerText = "";
            cell.appendChild(input);
        }
    });

    button.textContent = "Save";
}


function saveRowData(row, button) {
    const inputs = row.querySelectorAll("input");

    const updatedData = {
        id: row.cells[0].innerText,
        name: inputs[0].value,
        category: inputs[1].value,
        quantity: parseInt(inputs[2].value),
        price: parseFloat(inputs[3].value)
    };

    fetch("/edit-product", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(updatedData)
    })
    .then(response => response.json())
    .then(data => {
        inputs.forEach((input, index) => {
            input.parentElement.innerText = input.value;
        });

        updateStockStatusUI();

        button.textContent = "Edit";
    })
    .catch(error => {
        console.error("Error updating product:", error);
        alert("Failed to update product.");
    });
}



document.addEventListener("DOMContentLoaded", function () {
    const addItemBtn = document.getElementById("add-item-btn");
    const modal = document.getElementById("addItemModal");
    const closeModal = document.querySelector(".close-modal");
    const saveItemBtn = document.getElementById("save-item-btn");

    addItemBtn.addEventListener("click", function () {
        modal.style.display = "flex";
    });

    closeModal.addEventListener("click", function () {
        modal.style.display = "none";
    });

    window.addEventListener("click", function (event) {
        if (event.target === modal) {
            modal.style.display = "none";
        }
    });


    saveItemBtn.addEventListener("click", function () {
        const nameInput = document.getElementById("item-name");
        const categoryInput = document.getElementById("item-category");
        const quantityInput = document.getElementById("item-quantity");
        const priceInput = document.getElementById("item-price");

        const name = nameInput ? nameInput.value.trim() : "";
        const category = categoryInput ? categoryInput.value.trim() : "";
        const quantity = quantityInput ? quantityInput.value.trim() : "";
        const price = priceInput ? priceInput.value.trim() : "";

        if (!name || !category || !quantity || !price) {
            alert("All fields are required!");
            return;
        }

        fetch("/add-product", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                name: name,
                category: category,
                quantity: parseInt(quantity),
                price: parseFloat(price)
            })
        })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                alert(data.message);
                modal.style.display = "none";
                location.reload();
            } else {
                alert("Error: " + data.message);
            }
        })
        .catch(error => {
            console.error("Error:", error);
            alert("Failed to add item.");
        });
    });
});




document.addEventListener("DOMContentLoaded", function () {
    updateStockStatusUI();
});

function updateStockStatusUI() {
    document.querySelectorAll(".editable.quantity").forEach(cell => {
        let quantity = parseInt(cell.textContent.trim());
        let statusCell = cell.parentElement.querySelector(".editable.status");

        if (quantity > 20) {
            statusCell.innerHTML = '<span class="status-badge in-stock">Available</span>';
        } else if (quantity > 0) {
            statusCell.innerHTML = '<span class="status-badge low-stock">Low Stock</span>';
        } else {
            statusCell.innerHTML = '<span class="status-badge out-of-stock">Out of Stock</span>';
        }
    });
}

document.addEventListener("DOMContentLoaded", function () {
    const profileIcon = document.querySelector(".profile-icon");
    const profileMenu = document.querySelector(".profile-menu");

    profileIcon.addEventListener("mouseenter", function () {
        profileMenu.style.display = "block";
        fetchUserInfo();
    });

    profileIcon.addEventListener("mouseleave", function () {
        setTimeout(() => profileMenu.style.display = "none", 3000);
    });

    function fetchUserInfo() {
        let osName = "Unknown OS";
        const userAgent = navigator.userAgent;

        if (userAgent.includes("Windows NT 10.0")) {
            osName = "Windows 10";
        } else if (userAgent.includes("Windows NT 11.0") || userAgent.includes("Windows NT 10.0; Win64")) {
            osName = "Windows 11";
        } else if (userAgent.includes("Mac OS X")) {
            osName = "macOS";
        } else if (userAgent.includes("Linux")) {
            osName = "Linux";
        }

        let browserName = "Unknown Browser";
        if (userAgent.includes("Chrome") && !userAgent.includes("Edg")) {
            browserName = "Google Chrome";
        } else if (userAgent.includes("Firefox")) {
            browserName = "Mozilla Firefox";
        } else if (userAgent.includes("Safari") && !userAgent.includes("Chrome")) {
            browserName = "Safari";
        } else if (userAgent.includes("Edg")) {
            browserName = "Microsoft Edge";
        } else if (userAgent.includes("Opera") || userAgent.includes("OPR")) {
            browserName = "Opera";
        }

        document.getElementById("os-info").textContent = `OS: ${osName}`;
        document.getElementById("browser-info").textContent = `Browser: ${browserName}`;

        fetch("/user-info")
            .then(response => response.json())
            .then(data => {
                document.getElementById("ip-info").textContent = `IP: ${data.ip}`;
                document.getElementById("location-info").textContent = `Location: ${data.location}`;
                document.getElementById("process-info").textContent = `Processor: ${data.processor}`;
            })
            .catch(error => console.error("Error fetching user info:", error));
    }
});
