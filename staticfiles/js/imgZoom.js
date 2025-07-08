const img = document.getElementById("mainImage");

function zoom(e) {
  const rect = e.currentTarget.getBoundingClientRect();
  const x = ((e.clientX - rect.left) / rect.width) * 100;
  const y = ((e.clientY - rect.top) / rect.height) * 100;
  img.style.transformOrigin = `${x}% ${y}%`;
  img.style.transform = "scale(2)";
}

function resetZoom() {
  img.style.transformOrigin = "center center";
  img.style.transform = "scale(1)";
}