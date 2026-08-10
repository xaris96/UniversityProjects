// add new user
document.getElementById('addForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const name = document.getElementById('name').value;
    const age = document.getElementById('age').value;

    try {
        const response = await fetch('/add', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                name: name,
                age: age,
                test_data: false
            })
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Failed to add user');
        }
        
        await fetchResources();  // reload data
        document.getElementById('name').value = '';  // clear input
        document.getElementById('age').value = '';
        alert("User added successfully!");
    } catch (error) {
        alert(error.message);
    }
});

// load users from api
async function fetchResources() {
    try {
        const response = await fetch('/api/users');
        const users = await response.json();
        const tbody = document.querySelector('#resourceTable tbody');
        tbody.innerHTML = users.map(user => `
            <tr>
                <td>${user.id}</td>
                <td>${user.name}</td>
                <td>${user.age}</td>
                <td>
                    <button onclick="editResource(${user.id})">Edit</button>
                    <button onclick="deleteResource(${user.id})">Delete</button>
                </td>
            </tr>
        `).join('');
    } catch (error) {
        console.error('Error fetching data:', error);
    }
}

// edit user
async function editResource(id) {
    const newName = prompt("Enter new name:");
    const newAge = prompt("Enter new age:");

    if (!newName || !newAge) {
        alert("Name and age are required!");
        return;
    }

    try {
        const response = await fetch(`/edit`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ id: id, name: newName, age: newAge })
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Failed to edit user');
        }

        await fetchResources();  // reload data
        alert("User updated successfully!");
    } catch (error) {
        alert(error.message);
    }
}

// delete user
async function deleteResource(id) {
    if (!confirm("Are you sure you want to delete this user?")) {
        return;
    }

    try {
        const response = await fetch(`/delete`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ id: id })
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Failed to delete user');
        }

        await fetchResources();  // reload data
        alert("User deleted successfully!");
    } catch (error) {
        alert(error.message);
    }
}

// load initial data
fetchResources();
