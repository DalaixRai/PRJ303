let items = document.querySelectorAll('.slider .item');
let next = document.getElementById('next');
let prev = document.getElementById('prev');

let active = 4;

function loadShow() {
  const viewportWidth = window.innerWidth;

  for (let i = 0; i < items.length; i++) {
    let distance = i - active;
    let stt = Math.abs(distance);

    if (distance === 0) {
      // Active slide
      items[i].style.transform = `none`;
      items[i].style.zIndex = 1;
      items[i].style.filter = 'none';
      items[i].style.opacity = 1;
    } else if (stt <= 3) {
      // Slides within 3 slides range from the active slide
      let direction = distance > 0 ? 1 : -1;
      let translateX = direction * (stt * getTranslateXFactor(viewportWidth));
      let scaleFactor = 1 - 0.2 * stt;

      items[i].style.transform = `translateX(${translateX}px) scale(${scaleFactor})`;
      items[i].style.zIndex = -stt;
      items[i].style.filter = 'blur(5px)';
      items[i].style.opacity = stt > 2 ? 0 : 0.6;
    } else {
      // Slides outside the 3 slides range from the active slide
      let direction = distance > 0 ? 1 : -1;
      let translateX = direction * (3 * getTranslateXFactor(viewportWidth));
      let scaleFactor = 1 - 0.2 * 3;

      // Decrease translateX distance for outer slides
      translateX = direction * (2.7 * getTranslateXFactor(viewportWidth)); // Adjust distance here

      items[i].style.transform = `translateX(${translateX}px) scale(${scaleFactor})`;
      items[i].style.zIndex = -4;
      items[i].style.filter = 'blur(2px)'; // Adjust blur effect here
      items[i].style.opacity = 0.4;
    }
  }
}

function getTranslateXFactor(viewportWidth) {
  // Adjust translateX factor based on viewport width
  if (viewportWidth >= 1400) {
    return 170; // Decrease by 6 units (pixels) from 176
  } else if (viewportWidth >= 1200) {
    return 140; // Decrease by 6 units (pixels) from 146
  } else if (viewportWidth >= 900) {
    return 110; // Decrease by 6 units (pixels) from 116
  } else if (viewportWidth >= 700) {
    return 80; // Decrease by 6 units (pixels) from 86
  } else if (viewportWidth >= 400) {
    return 50; // Decrease by 6 units (pixels) from 56
  } else if (viewportWidth >= 350) {
    return 35; // Decrease by 6 units (pixels) from 41
  } else if (viewportWidth >= 280) {
    return 20; // Decrease by 6 units (pixels) from 26
  } else {
    return 10; // Default value (can be adjusted as needed)
  }
}

// Initial load
loadShow();

// Event listener for next button
next.onclick = function () {
  active = Math.min(active + 1, items.length - 1);
  loadShow();
};

// Event listener for prev button
prev.onclick = function () {
  active = Math.max(active - 1, 0);
  loadShow();
};

// Resize event listener to handle changes in viewport width
window.addEventListener('resize', () => {
  loadShow(); // Reload slide layout on window resize
});

