function signup() {
  const name = document.getElementById("name").value;
  const email = document.getElementById("email").value;
  const username = document.getElementById("username").value;
  const password = document.getElementById("password").value;

  if (!name || !email || !username || !password) {
      alert("Please fill in all fields.");
      return;
  }

  fetch("/signup", {
      method: "POST",
      headers: {
          "Content-Type": "application/json",
      },
      body: JSON.stringify({ name, email, username, password }),
  })
  .then((response) => response.json())
  .then((data) => {
      if (data.success) {
          window.location.href = "/login";
      } else {
          alert(data.message || "Signup failed. Please try again.");
      }
  })
  .catch((error) => {
      console.error("Error:", error);
      alert("An error occurred. Please try again.");
  });
}