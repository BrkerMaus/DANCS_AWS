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
    const tableBody = document.getElementById("inventory-table");
    const addItemBtn = document.getElementById("add-item-btn");

    addItemBtn.addEventListener("click", function () {
        const newRow = document.createElement("tr");

        newRow.innerHTML = `
            <td><input type="text" class="item-name" placeholder="Enter Name"></td>
            <td><input type="text" class="item-category" placeholder="Enter Category"></td>
            <td><input type="number" class="item-quantity" placeholder="Enter Quantity"></td>
            <td><input type="number" class="item-price" placeholder="Enter Unit Price"></td>
            <td>
                <select class="item-status">
                    <option value="Available">Available</option>
                    <option value="Low Stock">Low Stock</option>
                    <option value="Out of Stock">Out of Stock</option>
                </select>
            </td>
            <td>
                <button class="save-btn">Save</button>
                <button class="cancel-btn">Cancel</button>
            </td>
        `;

        tableBody.appendChild(newRow);
        newRow.querySelector(".save-btn").addEventListener("click", function () {
            const name = newRow.querySelector(".item-name").value;
            const category = newRow.querySelector(".item-category").value;
            const quantity = newRow.querySelector(".item-quantity").value;
            const price = newRow.querySelector(".item-price").value;
            const status = newRow.querySelector(".item-status").value;

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
                    price: parseFloat(price),
                    status: status
                })
            })
            .then(res => res.json())
            .then(data => {
                alert(data.message);
                location.reload();
            })
            .catch(error => console.error("Error:", error));
        });

        newRow.querySelector(".cancel-btn").addEventListener("click", function () {
            newRow.remove();
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
