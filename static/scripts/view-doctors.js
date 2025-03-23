function searchDoctors() {
    const searchTerm = document.getElementById("search").value.toLowerCase();
    const rows = document.querySelectorAll("#doctor-table tbody tr");
  
    rows.forEach((row) => {
      const doctorName = row.querySelector("td[data-label='Name']").textContent.toLowerCase();
      const specialization = row.querySelector("td[data-label='Specialization']").textContent.toLowerCase();
      if (doctorName.includes(searchTerm) || specialization.includes(searchTerm)) {
        row.style.display = "";
      } else {
        row.style.display = "none";
      }
    });
  }
  
  // Function to convert 24-hour time to 12-hour format
  function formatTime(time) {
    let [hours, minutes] = time.split(":");
    let period = "AM";
    if (hours >= 12) {
      period = "PM";
      if (hours > 12) hours -= 12;
    }
    if (hours === "00") hours = "12";
    return `${hours}:${minutes} ${period}`;
  }
  
  // Modal functionality
  const modal = document.getElementById("availabilityModal");
  const span = document.getElementsByClassName("close")[0];
  const doctorNameSpan = document.getElementById("doctorName");
  const availabilityForm = document.getElementById("availabilityForm");
  
  let currentDoctor = "";
  
  function setAvailability(doctorName) {
    currentDoctor = doctorName;
    doctorNameSpan.textContent = doctorName;
    modal.style.display = "block";
  }
  
  span.onclick = function () {
    modal.style.display = "none";
  };
  
  window.onclick = function (event) {
    if (event.target == modal) {
      modal.style.display = "none";
    }
  };
  
  availabilityForm.onsubmit = function (event) {
    event.preventDefault();
  
    const startTime = document.getElementById("start-time").value;
    const breakStart = document.getElementById("break-start").value;
    const breakEnd = document.getElementById("break-end").value;
    const endTime = document.getElementById("end-time").value;
  
    fetch("/set-availability", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        doctorName: currentDoctor,
        startTime,
        breakStart,
        breakEnd,
        endTime,
      }),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.success) {
          alert("Availability set successfully!");
          modal.style.display = "none";
        } else {
          alert("Failed to set availability.");
        }
      });
  };