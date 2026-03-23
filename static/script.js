// ========================================
// GLOBAL CLICK HANDLER
// ========================================
document.addEventListener("click", (e) => {
    // SEARCH TOGGLE
    if (e.target.closest(".header-search-icon")) {
        const input = document.querySelector(".header-search-box-input");
        input.classList.toggle("active");
        if (input.classList.contains("active")) {
            input.focus();
        }
    }
});

// ========================================
// CARD NAVIGATION
// ========================================
document.querySelectorAll(".item-card").forEach(card => {
    card.addEventListener("click", (e) => {
        // Don't navigate if clicking on interactive elements
        if (!e.target.closest(".wishlist") && 
            !e.target.closest(".add-cart") && 
            !e.target.closest("button")) {
            const link = card.dataset.link;
            if (link) {
                window.location.href = link;
            }
        }
    });
});

document.querySelectorAll(".category-card").forEach(card => {
    card.addEventListener("click", () => {
        const link = card.dataset.link;
        if (link) {
            window.location.href = link;
        }
    });
});

// Wait until page loads
document.addEventListener("DOMContentLoaded", function () {

    const hamburger = document.getElementById("hamburger");
    const headerLinks = document.getElementById("headerLinks");

    // =========================
    // HAMBURGER MENU
    // =========================
    if (hamburger && headerLinks) {
        hamburger.addEventListener("click", function (e) {
            e.stopPropagation();

            hamburger.classList.toggle("active");
            headerLinks.classList.toggle("active");
        });
    }

    // =========================
    // MOBILE DROPDOWN
    // =========================
    const navLinks = document.querySelectorAll(".nav-dropdown .nav-link");

    navLinks.forEach(function (link) {
        link.addEventListener("click", function (e) {

            if (window.innerWidth <= 1024) {
                e.preventDefault();

                const dropdown = link.closest(".nav-dropdown");
                dropdown.classList.toggle("active");
            }

        });
    });

    // =========================
    // CLOSE MENU WHEN CLICK OUTSIDE
    // =========================
    document.addEventListener("click", function (e) {

        if (window.innerWidth <= 1024) {

            if (!e.target.closest(".header-links") &&
                !e.target.closest(".hamburger")) {

                hamburger.classList.remove("active");
                headerLinks.classList.remove("active");

                document.querySelectorAll(".nav-dropdown").forEach(function (dropdown) {
                    dropdown.classList.remove("active");
                });

            }

        }

    });

    // =========================
    // RESET ON RESIZE
    // =========================
    window.addEventListener("resize", function () {

        if (window.innerWidth > 1024) {

            hamburger.classList.remove("active");
            headerLinks.classList.remove("active");

            document.querySelectorAll(".nav-dropdown").forEach(function (dropdown) {
                dropdown.classList.remove("active");
            });

        }

    });

});

// ========================================
// INITIALIZE ON PAGE LOAD
// ========================================
document.addEventListener('DOMContentLoaded', () => {
    console.log('ÉVARA - Website initialized');
    
    // Test button functionality
    const testBtn = document.querySelector('.add-cart');
    if (testBtn) {
        console.log('Add to Cart buttons found:', document.querySelectorAll('.add-cart').length);
    }
});

// Auto-hide flash messages after 3 seconds
document.addEventListener("DOMContentLoaded", function() {
    const flashes = document.querySelectorAll(".flash-message");

    flashes.forEach(flash => {
      setTimeout(() => {
        flash.style.opacity = "0";
        flash.style.transform = "translateY(-20px)";
        setTimeout(() => flash.remove(), 300);
      }, 3000);

      flash.querySelector(".close-flash").addEventListener("click", () => {
        flash.remove();
      });
    });
  });
  
// ===================================
// QUANTITY + / -
// ===================================
document.addEventListener("click", function(e){

    if(e.target.classList.contains("plus") ||
       e.target.classList.contains("minus")){

        const wrapper = e.target.closest(".qty-wrapper");
        const input = wrapper.querySelector(".qty-input");

        let value = parseInt(input.value);

        if(e.target.classList.contains("plus")){
            value++;
        }

        if(e.target.classList.contains("minus")){
            if(value > 1){
                value--;
            }
        }

        input.value = value;
    }

});

document.addEventListener("DOMContentLoaded", function() {
    const cards = document.querySelectorAll(".cart-card");

    cards.forEach(card => {
        card.addEventListener("click", function(e) {

            if (e.target.closest("button, select, input, label, .size-wrapper, .quantity-controls")) {
                return;
            }

            const link = this.dataset.link;
            if (link) {
                window.location.href = link;
            }
        });
    });
});

// =======================
// ADDRESS FORM TOGGLE
// =======================

document.addEventListener("DOMContentLoaded", function () {

    const showBtn = document.getElementById("showAddressForm");
    const addressForm = document.getElementById("newAddressForm");

    if (showBtn && addressForm) {

        showBtn.addEventListener("click", function () {

            addressForm.classList.toggle("hidden");

        });

    }

});

document.addEventListener("DOMContentLoaded", function () {
  const rows = document.querySelectorAll(".clickable-row");

  rows.forEach(row => {
    row.addEventListener("click", function () {
      const link = this.dataset.link;
      if (link) {
        window.location.href = link;
      }
    });
  });
});