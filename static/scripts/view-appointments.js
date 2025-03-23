function searchAppointments() {
    const searchTerm = document.getElementById("search").value.toLowerCase();
    const rows = document.querySelectorAll("#appointment-table tbody tr");
  
    rows.forEach((row) => {
        const patientName = row.querySelector("td[data-label='Patient Name']").textContent.toLowerCase();
        if (patientName.includes(searchTerm)) {
            row.style.display = "";
        } else {
            row.style.display = "none";
        }
    });
  }
  
  function deleteAppointment(patientName, date, time) {
    if (confirm("Are you sure you want to delete this appointment?")) {
        fetch("/delete-appointment", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ patientName, date, time }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                location.reload(); // Refresh the page to reflect changes
            } else {
                alert("Failed to delete appointment.");
            }
        })
        .catch((error) => {
            console.error("Error:", error);
            alert("An error occurred while deleting the appointment.");
        });
    }
  }
  
  function exportAppointments() {
    const rows = document.querySelectorAll("#appointment-table tbody tr");
    let csvContent = "Patient Name,Doctor,Date,Time,Status\n";
  
    rows.forEach((row) => {
        const patientName = row.querySelector("td[data-label='Patient Name']").textContent;
        const doctor = row.querySelector("td[data-label='Doctor']").textContent;
        const date = row.querySelector("td[data-label='Date']").textContent;
        const time = row.querySelector("td[data-label='Time']").textContent;
        const status = row.querySelector("td[data-label='Status']").textContent;
        csvContent += `${patientName},${doctor},${date},${time},${status}\n`;
    });
  
    const blob = new Blob([csvContent], { type: "text/csv" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "appointments.csv";
    a.click();
    URL.revokeObjectURL(url);
  }