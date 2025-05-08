/**
 * Discord Messages Dump - Main JavaScript
 * Handles interactive elements and functionality for the documentation website
 */

/**
 * Debounce function to limit how often a function can be called
 * @param {Function} func - The function to debounce
 * @param {number} wait - The time to wait in milliseconds
 * @returns {Function} - The debounced function
 */
function debounce(func, wait) {
    let timeout;
    return function() {
        const context = this;
        const args = arguments;
        clearTimeout(timeout);
        timeout = setTimeout(() => {
            func.apply(context, args);
        }, wait);
    };
}

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all components
    initNavbar();
    initArchitectureDiagram();
    initCodeHighlighting();
    initScrollSpy();
    initTooltips();
    initCopyButtons();
    initThemeToggle();
    initMobileMenu();
});

/**
 * Initialize navbar functionality
 * - Adds active class to current page link
 * - Handles navbar scrolling behavior
 */
function initNavbar() {
    // Get current page path
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.nav-link');

    // Add active class to current page link
    navLinks.forEach(link => {
        const linkPath = link.getAttribute('href');
        if (linkPath === currentPath ||
            (currentPath.endsWith('/') && linkPath === currentPath + 'index.html') ||
            (linkPath === '/index.html' && (currentPath === '/' || currentPath === ''))) {
            link.classList.add('active');
        }
    });

    // Navbar scrolling behavior
    const navbar = document.querySelector('.navbar');
    let lastScrollTop = 0;

    window.addEventListener('scroll', function() {
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;

        if (scrollTop > 100) {
            navbar.classList.add('navbar-scrolled');
        } else {
            navbar.classList.remove('navbar-scrolled');
        }

        if (scrollTop > lastScrollTop && scrollTop > 200) {
            // Scrolling down
            navbar.classList.add('navbar-hidden');
        } else {
            // Scrolling up
            navbar.classList.remove('navbar-hidden');
        }

        lastScrollTop = scrollTop;
    });
}

/**
 * Initialize the architecture diagram
 * - Sets up tooltips for the static SVG
 * - Implements zoom functionality
 */
function initArchitectureDiagram() {
    const diagramContainer = document.getElementById('diagram-container');
    if (!diagramContainer) return;

    // Create tooltip container if it doesn't exist
    if (!document.getElementById('component-tooltip')) {
        const tooltip = document.createElement('div');
        tooltip.id = 'component-tooltip';
        tooltip.className = 'component-tooltip';
        tooltip.style.display = 'none';
        document.body.appendChild(tooltip);
    }

    // Set up tooltips for the SVG once it's loaded
    const svgObject = document.querySelector('.architecture-svg');
    if (svgObject) {
        // For object tag, we need to wait for the SVG to load
        svgObject.addEventListener('load', function() {
            // Access the SVG document inside the object
            const svgDoc = svgObject.contentDocument;
            if (!svgDoc) return;

            // Add tooltip functionality to components
            const components = svgDoc.querySelectorAll('.component');
            setupSVGTooltips(components);
        });
    }

    // Set up zoom controls with active state
    const zoomButtons = document.querySelectorAll('.zoom-controls button');
    zoomButtons.forEach(btn => {
        btn.addEventListener('click', function() {
            const scale = parseFloat(this.textContent.replace('%', '')) / 100;

            // Update active state
            zoomButtons.forEach(b => b.classList.remove('btn-primary'));
            zoomButtons.forEach(b => b.classList.add('btn-outline-primary'));
            this.classList.remove('btn-outline-primary');
            this.classList.add('btn-primary');

            zoomDiagram(scale);
        });
    });

    // Auto-select appropriate zoom level based on screen size
    function setInitialZoom() {
        let initialScale = 1; // Default 100%
        const screenWidth = window.innerWidth;

        if (screenWidth < 576) {
            initialScale = 0.5; // 50% for mobile
            zoomButtons[0].click(); // Click the 50% button
        } else if (screenWidth < 992) {
            initialScale = 0.75; // 75% for tablets
            // Since we don't have a 75% button, we'll just set the zoom directly
            zoomDiagram(initialScale);
        } else {
            zoomButtons[1].click(); // Click the 100% button for larger screens
        }
    }

    // Set initial zoom on load
    setInitialZoom();

    // Update zoom on window resize
    window.addEventListener('resize', debounce(setInitialZoom, 250));
}

/**
 * Set up tooltips for SVG components
 * @param {NodeList} components - The SVG component elements
 */
function setupSVGTooltips(components) {
    const tooltip = document.getElementById('component-tooltip');
    if (!tooltip || !components.length) return;

    // Add CSS for tooltip if not already in stylesheet
    if (!document.getElementById('tooltip-styles')) {
        const style = document.createElement('style');
        style.id = 'tooltip-styles';
        style.textContent = `
            .component-tooltip {
                position: absolute;
                background-color: rgba(255, 255, 255, 0.95);
                border: 1px solid #ccc;
                border-radius: 4px;
                padding: 8px 12px;
                font-size: 14px;
                max-width: 300px;
                box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
                z-index: 1000;
                pointer-events: none;
                transition: opacity 0.2s ease;
            }

            .component-tooltip strong {
                display: block;
                margin-bottom: 5px;
                color: #5865F2;
                border-bottom: 1px solid #eee;
                padding-bottom: 3px;
            }
        `;
        document.head.appendChild(style);
    }

    components.forEach(comp => {
        comp.addEventListener('mouseover', function(e) {
            const name = this.getAttribute('data-name');
            const description = this.getAttribute('data-description');

            tooltip.innerHTML = `<strong>${name}</strong>${description}`;
            tooltip.style.display = 'block';
            tooltip.style.opacity = '0';

            // Position tooltip
            const rect = this.getBoundingClientRect();
            const tooltipWidth = 300; // max-width from CSS

            // Position tooltip centered above the component
            let left = rect.left + (rect.width / 2) - (tooltipWidth / 2);
            let top = rect.top - tooltip.offsetHeight - 10 + window.scrollY;

            // Make sure tooltip stays within viewport
            if (left < 10) left = 10;
            if (left + tooltipWidth > window.innerWidth - 10) {
                left = window.innerWidth - tooltipWidth - 10;
            }

            // If tooltip would go off the top of the screen, position it below the component
            if (top < window.scrollY + 10) {
                top = rect.bottom + 10 + window.scrollY;
            }

            tooltip.style.left = `${left}px`;
            tooltip.style.top = `${top}px`;

            // Fade in
            setTimeout(() => {
                tooltip.style.opacity = '1';
            }, 10);
        });

        comp.addEventListener('mouseout', function() {
            tooltip.style.opacity = '0';
            setTimeout(() => {
                if (tooltip.style.opacity === '0') {
                    tooltip.style.display = 'none';
                }
            }, 200);
        });
    });
}



/**
 * Zoom the architecture diagram
 * @param {number} scale - The zoom scale (0.5, 1, 1.5, 2)
 */
function zoomDiagram(scale) {
    // Get the SVG object element
    const svgObject = document.querySelector('.architecture-svg');
    if (!svgObject) return;

    // Set the width and height based on scale
    const width = 1000 * scale;
    const height = 700 * scale;

    svgObject.style.width = `${width}px`;
    svgObject.style.height = `${height}px`;

    // Center the diagram in the container
    const diagramContainer = document.getElementById('diagram-container');
    if (diagramContainer) {
        diagramContainer.style.display = 'flex';
        diagramContainer.style.justifyContent = 'center';
        diagramContainer.style.alignItems = 'center';
        diagramContainer.style.overflow = 'auto';
    }

    // Update active button
    const zoomButtons = document.querySelectorAll('.zoom-controls button');
    zoomButtons.forEach(btn => {
        const btnScale = parseFloat(btn.textContent.replace('%', '')) / 100;
        if (btnScale === scale) {
            btn.classList.remove('btn-outline-primary');
            btn.classList.add('btn-primary');
        } else {
            btn.classList.remove('btn-primary');
            btn.classList.add('btn-outline-primary');
        }
    });
}

/**
 * Initialize code highlighting
 * Uses Prism.js if available
 */
function initCodeHighlighting() {
    // Check if Prism is available
    if (typeof Prism !== 'undefined') {
        Prism.highlightAll();
    }
}

/**
 * Initialize scroll spy functionality
 * Highlights navigation items based on scroll position
 */
function initScrollSpy() {
    const sections = document.querySelectorAll('section[id]');
    const navLinks = document.querySelectorAll('.nav-link');

    if (!sections.length || !navLinks.length) return;

    window.addEventListener('scroll', function() {
        let current = '';
        const scrollPosition = window.scrollY + 100; // Offset for navbar

        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            const sectionHeight = section.offsetHeight;

            if (scrollPosition >= sectionTop && scrollPosition < sectionTop + sectionHeight) {
                current = section.getAttribute('id');
            }
        });

        navLinks.forEach(link => {
            link.classList.remove('active');
            const href = link.getAttribute('href');
            if (href && href.includes(current)) {
                link.classList.add('active');
            }
        });
    });
}

/**
 * Initialize tooltips
 */
function initTooltips() {
    const tooltips = document.querySelectorAll('[data-tooltip]');

    tooltips.forEach(element => {
        const tooltipText = element.getAttribute('data-tooltip');

        element.addEventListener('mouseenter', function(e) {
            const tooltip = document.createElement('div');
            tooltip.className = 'tooltip';
            tooltip.textContent = tooltipText;
            document.body.appendChild(tooltip);

            const rect = element.getBoundingClientRect();
            tooltip.style.left = `${rect.left + rect.width / 2 - tooltip.offsetWidth / 2}px`;
            tooltip.style.top = `${rect.top - tooltip.offsetHeight - 10 + window.scrollY}px`;

            tooltip.classList.add('tooltip-visible');

            element.addEventListener('mouseleave', function() {
                tooltip.remove();
            });
        });
    });
}

/**
 * Initialize copy buttons for code blocks and command boxes
 */
function initCopyButtons() {
    // Add copy buttons to code blocks
    const codeBlocks = document.querySelectorAll('pre code');

    codeBlocks.forEach(block => {
        const pre = block.parentNode;

        // Skip if already has a copy button
        if (pre.querySelector('.copy-button')) return;

        // Create copy button
        const copyButton = document.createElement('button');
        copyButton.className = 'copy-button';
        copyButton.textContent = 'Copy';
        copyButton.setAttribute('aria-label', 'Copy code to clipboard');

        // Add button to pre element
        pre.appendChild(copyButton);

        // Add click event
        copyButton.addEventListener('click', function() {
            const code = block.textContent;
            navigator.clipboard.writeText(code).then(() => {
                copyButton.textContent = 'Copied!';
                setTimeout(() => {
                    copyButton.textContent = 'Copy';
                }, 2000);
            }).catch(err => {
                console.error('Failed to copy: ', err);
                copyButton.textContent = 'Failed';
                setTimeout(() => {
                    copyButton.textContent = 'Copy';
                }, 2000);
            });
        });
    });

    // Convert inline code blocks with command class to command boxes with copy buttons
    const commandBlocks = document.querySelectorAll('code.command');

    commandBlocks.forEach(block => {
        // Create command box
        const commandBox = document.createElement('div');
        commandBox.className = 'command-box';

        // Move content to command box
        commandBox.textContent = block.textContent;

        // Create copy button
        const copyButton = document.createElement('button');
        copyButton.className = 'copy-button';
        copyButton.textContent = 'Copy';
        copyButton.setAttribute('aria-label', 'Copy command to clipboard');

        // Add button to command box
        commandBox.appendChild(copyButton);

        // Replace original code element with command box
        block.parentNode.replaceChild(commandBox, block);

        // Add click event
        copyButton.addEventListener('click', function() {
            const command = commandBox.textContent.replace('Copy', '').trim();
            navigator.clipboard.writeText(command).then(() => {
                copyButton.textContent = 'Copied!';
                setTimeout(() => {
                    copyButton.textContent = 'Copy';
                }, 2000);
            }).catch(err => {
                console.error('Failed to copy: ', err);
                copyButton.textContent = 'Failed';
                setTimeout(() => {
                    copyButton.textContent = 'Copy';
                }, 2000);
            });
        });
    });
}

/**
 * Initialize theme toggle functionality
 */
function initThemeToggle() {
    const themeToggle = document.getElementById('theme-toggle');
    if (!themeToggle) return;

    // Check for saved theme preference
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
        document.documentElement.setAttribute('data-theme', savedTheme);
        if (savedTheme === 'dark') {
            themeToggle.checked = true;
        }
    }

    // Add event listener
    themeToggle.addEventListener('change', function() {
        if (this.checked) {
            document.documentElement.setAttribute('data-theme', 'dark');
            localStorage.setItem('theme', 'dark');
        } else {
            document.documentElement.setAttribute('data-theme', 'light');
            localStorage.setItem('theme', 'light');
        }
    });
}

/**
 * Initialize mobile menu functionality
 */
function initMobileMenu() {
    const menuToggle = document.getElementById('menu-toggle');
    const mobileMenu = document.getElementById('mobile-menu');

    if (!menuToggle || !mobileMenu) return;

    menuToggle.addEventListener('click', function() {
        mobileMenu.classList.toggle('active');
        menuToggle.classList.toggle('active');
    });

    // Close menu when clicking outside
    document.addEventListener('click', function(event) {
        if (!mobileMenu.contains(event.target) && !menuToggle.contains(event.target)) {
            mobileMenu.classList.remove('active');
            menuToggle.classList.remove('active');
        }
    });

    // Close menu when clicking on a link
    const mobileLinks = mobileMenu.querySelectorAll('a');
    mobileLinks.forEach(link => {
        link.addEventListener('click', function() {
            mobileMenu.classList.remove('active');
            menuToggle.classList.remove('active');
        });
    });
}
