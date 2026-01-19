const API = "http://127.0.0.1:8000"; // change after deployment

function login() {
  fetch(`${API}/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      phone: document.getElementById("phone").value,
      password: document.getElementById("password").value
    })
  })
  .then(res => res.json())
  .then(data => {
    localStorage.setItem("token", data.access_token);
    window.location.href = "dashboard.html";
  });
}

function authHeader() {
  return {
    "Authorization": "Bearer " + localStorage.getItem("token"),
    "Content-Type": "application/json"
  };
}

function loadRestaurants() {
  fetch(`${API}/restaurants`, { headers: authHeader() })
    .then(res => res.json())
    .then(data => {
      document.getElementById("restaurants").innerHTML =
        JSON.stringify(data, null, 2);
    });
}

function viewCart() {
  fetch(`${API}/cart`, { headers: authHeader() })
    .then(res => res.json())
    .then(data => {
      document.getElementById("cart").innerText =
        JSON.stringify(data, null, 2);
    });
}

function placeOrder() {
  fetch(`${API}/orders/place`, {
    method: "POST",
    headers: authHeader()
  })
  .then(res => res.json())
  .then(data => {
    alert("Order placed: " + data.id);
    localStorage.setItem("order_id", data.id);
  });
}

function trackOrder() {
  const orderId = document.getElementById("orderId").value;
  fetch(`${API}/tracking/${orderId}`, { headers: authHeader() })
    .then(res => res.json())
    .then(data => {
      document.getElementById("status").innerText =
        JSON.stringify(data, null, 2);
    });
}
