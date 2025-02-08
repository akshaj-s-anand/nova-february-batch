
// Get search input element
const searchInput = document.getElementById('searchInput');
const tableBody = document.getElementById('complaintTableBody');

// Event listener for search input
searchInput.addEventListener('input', function () {
    const searchQuery = searchInput.value.toLowerCase();

    // Get all rows in the table
    const rows = tableBody.getElementsByTagName('tr');

    // Loop through rows and filter based on search query
    for (let row of rows) {
        const cells = row.getElementsByTagName('td');
        let matchFound = false;

        // Check if any cell contains the search query
        for (let cell of cells) {
            if (cell.textContent.toLowerCase().includes(searchQuery)) {
                matchFound = true;
                break;
            }
        }

        // Show/hide row based on whether a match is found
        if (matchFound) {
            row.style.display = '';
        } else {
            row.style.display = 'none';
        }
    }
});

// user table sort function
new Tablesort(document.getElementById('userTable'));

// complaint table sort function
new Tablesort(document.getElementById('complaintsTable'));