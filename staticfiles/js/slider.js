function slide(direction) {
  const slider = document.getElementById('slider');
  const scrollAmount = slider.offsetWidth * 0.6; // pomeri za ~60% širine
  if (direction === 'left') {
    slider.scrollBy({ left: -scrollAmount, behavior: 'smooth' });
  } else {
    slider.scrollBy({ left: scrollAmount, behavior: 'smooth' });
  }
}