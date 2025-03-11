/**
 * Vanilla JSU Parallax
 * A lightweight parallax scrolling effect library for modern websites
 * Customized for Rechtsanwalt Matusewicz website
 */
class vanillaJsuParallax {
    constructor(options) {
        // Default settings
        this.settings = {
            items: document.querySelectorAll('.parallax-item'),
            minViewportWidth: 0,
            minViewportHeight: 0,
            scrollSpeed: 0.5,
            backgroundSpeed: 0.2
        };

        // Override with user settings
        Object.assign(this.settings, options);

        // Initialize
        this.init();
    }

    init() {
        // Check viewport size
        if (window.innerWidth <= this.settings.minViewportWidth ||
            window.innerHeight <= this.settings.minViewportHeight) {
            return;
        }

        // Initialize parallax effect on each item
        this.items = Array.from(this.settings.items);

        // Set initial positions
        this.updatePositions();

        // Add scroll event listener
        window.addEventListener('scroll', this.handleScroll.bind(this));

        // Add resize event listener
        window.addEventListener('resize', this.handleResize.bind(this));
    }

    handleScroll() {
        // Update positions on scroll
        window.requestAnimationFrame(this.updatePositions.bind(this));
    }

    handleResize() {
        // Check viewport size on resize
        if (window.innerWidth <= this.settings.minViewportWidth ||
            window.innerHeight <= this.settings.minViewportHeight) {
            // Reset styles
            this.items.forEach(item => {
                const target = item.querySelector('.parallax-target') || item;
                target.style.transform = '';
            });
            return;
        }

        // Update positions
        this.updatePositions();
    }

    updatePositions() {
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;

        this.items.forEach(item => {
            // Get element data
            const direction = item.dataset.jsuplxdir || 'top';
            const mode = item.dataset.jsuplxmode || 'vertical';
            const perspective = parseInt(item.dataset.jsuplxperspective) || 200;

            // Apply different speeds based on class
            let speed;
            if (item.classList.contains('parallax-bg')) {
                speed = this.settings.backgroundSpeed; // Much slower for background
            } else {
                speed = this.settings.scrollSpeed;
            }

            // Get element position
            const rect = item.getBoundingClientRect();
            const elemTop = rect.top + scrollTop;
            const elemHeight = rect.height;

            // Check if element is in viewport or nearby
            if (scrollTop + window.innerHeight + 100 > elemTop &&
                scrollTop - 100 < elemTop + elemHeight) {

                // Calculate parallax offset
                const offset = (scrollTop - elemTop) * speed;
                const target = item.querySelector('.parallax-target') || item;

                // Apply parallax effect based on mode and direction
                if (mode === 'horizontal') {
                    if (direction === 'left') {
                        target.style.transform = `translateX(${-offset}px)`;
                    } else {
                        target.style.transform = `translateX(${offset}px)`;
                    }
                } else {
                    if (direction === 'bottom') {
                        target.style.transform = `translateY(${-offset}px)`;
                    } else {
                        target.style.transform = `translateY(${offset}px)`;
                    }
                }
            }
        });
    }
}