window.addEventListener("DOMContentLoaded", () => {
  const firstSlide = document.querySelector(".story-slide");
  const firstOverlay = firstSlide.querySelector(".overlay-stories");

  if (firstOverlay) {
    firstOverlay.classList.add("active");
    firstSlide.classList.remove("active-slide");
    const slides = document.querySelectorAll(".story-slide");
    slides.forEach((slide) => {
      if (slide !== firstSlide) {
        const overlay = slide.querySelector(".overlay-stories");
        if (overlay) {
          overlay.classList.remove("active");
          slide.classList.add("active-slide");
        }
      }
    });
  }
});
const swiper = new Swiper(".swiper", {
  direction: "horizontal",
  loop: false,
  effect: "slide",
  crossFade: true,
  centeredSlides: true,
  slidesPerView: 4,
  spaceBetween: 30,

  navigation: {
    nextEl: ".swiper-button-next",
    prevEl: ".swiper-button-prev",
  },
  on: { slideChangeTransitionEnd: function () {
    const slides = document.querySelectorAll(".story-slide");
    let firstSlideActivated = false;
    slides.forEach((slide) => {
      const overlay = slide.querySelector(".overlay-stories");
      if (overlay) {
        if (
          slide.classList.contains("swiper-slide-active") &&
          !firstSlideActivated
        ) {
          overlay.classList.add("active");
          slide.classList.remove("active-slide");
          firstSlideActivated = true;
        } else {
          overlay.classList.remove("active");
          slide.classList.add("active-slide");
        }
      }
    });
    },
  },
});

// document.addEventListener("DOMContentLoaded", function () {
//   var cubeSwipers = document.querySelectorAll('.cube-swiper');

//   cubeSwipers.forEach(function (cubeSwiper) {
//     new Swiper(cubeSwiper, {
//       effect: 'fade',
//       slidesPerView: 1,
//       direction: "horizontal",
//       loop: false,
//       cubeEffect: {
//         slideShadows: true,
//         shadow: true,
//         shadowOffset: 20,
//         shadowScale: 0.4,
//       },
//       autoplay: {
//         delay: 3000, 
//         disableOnInteraction: false, 
//       },
//       on: {
//         progress: function(progress) {
//           var progressBar = cubeSwiper.querySelector('.swiper-progress-bar');
//           progressBar.style.width = progress * 100 + '%';
//         },
//       },
//     });
//   });
// });

// Function to open modal
function openModal(id) {
  var modal = document.getElementById(id);
  modal.style.display = "block";
}

// Function to close modal
function closeModal(id) {
  var modal = document.getElementById(id);
  modal.style.display = "none";
}

// Close the modal when clicking outside of it
document.addEventListener("click", function (event) {
  var modals = document.getElementsByClassName("modal");
  for (var i = 0; i < modals.length; i++) {
    var modal = modals[i];
    if (event.target == modal) {
      modal.style.display = "none";
    }
  }
});
let marqueeContent = document.getElementById("marqueeContent");
let stepSize = 40; // Adjust the step size as needed

function moveLeft() {
  let currentLeft = parseFloat(getComputedStyle(marqueeContent).left);
  let newLeft = currentLeft + stepSize;
  let containerWidth = document.querySelector(".marquee-container").offsetWidth;
  let contentWidth = marqueeContent.scrollWidth;

  if (newLeft > 0) {
    newLeft = 0;
  } else if (newLeft < containerWidth - contentWidth) {
    newLeft = containerWidth - contentWidth;
  }

  marqueeContent.style.left = newLeft + "px";
}

function moveRight() {
  let currentLeft = parseFloat(getComputedStyle(marqueeContent).left);
  let newLeft = currentLeft - stepSize;
  let containerWidth = document.querySelector(".marquee-container").offsetWidth;
  let contentWidth = marqueeContent.scrollWidth;

  if (newLeft < containerWidth - contentWidth) {
    newLeft = containerWidth - contentWidth;
  } else if (newLeft > 0) {
    newLeft = 0;
  }

  marqueeContent.style.left = newLeft + "px";
}
