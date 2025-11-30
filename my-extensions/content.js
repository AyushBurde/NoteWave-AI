if (
  window.location.href.includes("meet.google.com") ||
  window.location.href.includes("zoom.us")
) {
  const btn = document.createElement("div");
  btn.innerText = "🇮🇳 IndianMeet AI – Capture Meeting";
  btn.style.cssText = `
    position: fixed;
    bottom: 20px;
    right: 20px;
    background: linear-gradient(135deg, #182848, #4b6cb7);
    color: white;
    padding: 14px 20px;
    font-weight: bold;
    border-radius: 20px;
    cursor: pointer;
    z-index: 999999;
    box-shadow: 0 4px 12px rgba(0,0,0,0.3);
  `;

  btn.onclick = () => {
    window.open("http://localhost:3000", "_blank");
  };

  document.body.appendChild(btn);
}
