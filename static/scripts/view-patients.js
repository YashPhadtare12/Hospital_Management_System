function searchPatients() {
    const searchTerm = document.getElementById("search").value.toLowerCase();
    const rows = document.querySelectorAll("#patient-table tbody tr");

    rows.forEach((row) => {
        const patientName = row.querySelector("td[data-label='Name']").textContent.toLowerCase();
        const mobile = row.querySelector("td[data-label='Mobile']").textContent.toLowerCase();
        if (patientName.includes(searchTerm) || mobile.includes(searchTerm)) {
            row.style.display = "";
        } else {
            row.style.display = "none";
        }
    });
}