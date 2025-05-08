/**
 * Discord Messages Dump - Main JavaScript
 * Handles interactive elements and functionality for the documentation website
 */

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
 * - Creates SVG diagram
 * - Adds interactive elements
 * - Implements zoom functionality
 */
function initArchitectureDiagram() {
    const diagramContainer = document.getElementById('diagram-container');
    if (!diagramContainer) return;

    // Create SVG element
    const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    svg.setAttribute('width', '800');
    svg.setAttribute('height', '600');
    svg.setAttribute('viewBox', '0 0 800 600');
    svg.id = 'architecture-diagram';
    svg.setAttribute('aria-labelledby', 'diagram-title');
    svg.setAttribute('role', 'img');

    // Add title for accessibility
    const title = document.createElementNS('http://www.w3.org/2000/svg', 'title');
    title.id = 'diagram-title';
    title.textContent = 'Discord Messages Dump Architecture Diagram';
    svg.appendChild(title);

    // Add description for accessibility
    const desc = document.createElementNS('http://www.w3.org/2000/svg', 'desc');
    desc.textContent = 'Architecture diagram showing the components of the Discord Messages Dump package and their relationships.';
    svg.appendChild(desc);

    // Add legend
    const legend = document.createElementNS('http://www.w3.org/2000/svg', 'g');
    legend.setAttribute('transform', 'translate(20, 20)');

    const legendTitle = document.createElementNS('http://www.w3.org/2000/svg', 'text');
    legendTitle.setAttribute('x', '0');
    legendTitle.setAttribute('y', '0');
    legendTitle.setAttribute('font-weight', 'bold');
    legendTitle.textContent = 'Legend:';
    legend.appendChild(legendTitle);

    const legendItems = [
        { color: '#5865F2', text: 'Core Components' },
        { color: '#EB459E', text: 'User Interfaces' },
        { color: '#9B84EC', text: 'Supporting Components' }
    ];

    legendItems.forEach((item, index) => {
        const y = 25 * (index + 1);

        const rect = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
        rect.setAttribute('x', '0');
        rect.setAttribute('y', y - 15);
        rect.setAttribute('width', '15');
        rect.setAttribute('height', '15');
        rect.setAttribute('fill', item.color);
        rect.setAttribute('stroke', '#333');
        rect.setAttribute('stroke-width', '1');

        const text = document.createElementNS('http://www.w3.org/2000/svg', 'text');
        text.setAttribute('x', '25');
        text.setAttribute('y', y);
        text.textContent = item.text;

        legend.appendChild(rect);
        legend.appendChild(text);
    });

    svg.appendChild(legend);

    // Define components with consistent naming and styling
    const components = [
        { id: 'api', x: 150, y: 150, width: 180, height: 80, color: '#5865F2', name: 'Discord API Client', description: 'Handles communication with Discord API, fetches messages, and manages rate limits.' },
        { id: 'processor', x: 400, y: 150, width: 180, height: 80, color: '#5865F2', name: 'Message Processor', description: 'Processes raw message data and formats it into various output formats (text, JSON, CSV, Markdown).' },
        { id: 'file_processor', x: 650, y: 150, width: 180, height: 80, color: '#5865F2', name: 'File Processor', description: 'Manages file operations, including opening file dialogs and saving content to files.' },
        { id: 'cli', x: 275, y: 300, width: 180, height: 80, color: '#EB459E', name: 'Command Line Interface', description: 'Provides a CLI using Click with various options for fetching and saving messages.' },
        { id: 'gui', x: 525, y: 300, width: 180, height: 80, color: '#EB459E', name: 'GUI Application', description: 'Provides a graphical interface for selecting output format and file location.' },
        { id: 'config', x: 400, y: 450, width: 180, height: 80, color: '#9B84EC', name: 'Configuration', description: 'Manages environment variables, validates input, and provides default values.' },
        { id: 'error', x: 650, y: 450, width: 180, height: 80, color: '#9B84EC', name: 'Error Handling', description: 'Manages error handling and provides fallback mechanisms.' }
    ];

    // Define connections with consistent styling
    const connections = [
        { from: 'cli', to: 'api', label: 'uses', type: 'main' },
        { from: 'cli', to: 'processor', label: 'uses', type: 'main' },
        { from: 'cli', to: 'file_processor', label: 'uses', type: 'main' },
        { from: 'gui', to: 'api', label: 'uses', type: 'main' },
        { from: 'gui', to: 'processor', label: 'uses', type: 'main' },
        { from: 'gui', to: 'file_processor', label: 'uses', type: 'main' },
        { from: 'processor', to: 'api', label: 'receives data', type: 'data' },
        { from: 'cli', to: 'config', label: 'loads', type: 'config' },
        { from: 'gui', to: 'config', label: 'loads', type: 'config' },
        { from: 'cli', to: 'error', label: 'reports', type: 'error' },
        { from: 'gui', to: 'error', label: 'reports', type: 'error' }
    ];

    // Add arrowhead markers with different colors
    const defs = document.createElementNS('http://www.w3.org/2000/svg', 'defs');

    const markerTypes = [
        { id: 'arrowhead-main', color: '#333' },
        { id: 'arrowhead-data', color: '#0066cc' },
        { id: 'arrowhead-config', color: '#009933' },
        { id: 'arrowhead-error', color: '#cc0000' }
    ];

    markerTypes.forEach(markerType => {
        const marker = document.createElementNS('http://www.w3.org/2000/svg', 'marker');
        marker.id = markerType.id;
        marker.setAttribute('viewBox', '0 0 10 10');
        marker.setAttribute('refX', '5');
        marker.setAttribute('refY', '5');
        marker.setAttribute('markerWidth', '6');
        marker.setAttribute('markerHeight', '6');
        marker.setAttribute('orient', 'auto');

        const markerPath = document.createElementNS('http://www.w3.org/2000/svg', 'path');
        markerPath.setAttribute('d', 'M 0 0 L 10 5 L 0 10 z');
        markerPath.setAttribute('fill', markerType.color);

        marker.appendChild(markerPath);
        defs.appendChild(marker);
    });

    svg.appendChild(defs);

    // Draw connections with improved styling
    connections.forEach(conn => {
        const fromComp = components.find(c => c.id === conn.from);
        const toComp = components.find(c => c.id === conn.to);

        if (!fromComp || !toComp) return;

        // Calculate start and end points
        const startX = fromComp.x + fromComp.width / 2;
        const startY = fromComp.y;
        const endX = toComp.x + toComp.width / 2;
        const endY = toComp.y + toComp.height;

        // Set connection style based on type
        let strokeColor, strokeWidth, dashArray;

        switch(conn.type) {
            case 'data':
                strokeColor = '#0066cc';
                strokeWidth = 2.5;
                dashArray = '';
                break;
            case 'config':
                strokeColor = '#009933';
                strokeWidth = 2;
                dashArray = '';
                break;
            case 'error':
                strokeColor = '#cc0000';
                strokeWidth = 2;
                dashArray = '5,3';
                break;
            default:
                strokeColor = '#333';
                strokeWidth = 2;
                dashArray = '';
        }

        // Draw arrow
        const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
        const d = `M${startX},${startY} C${startX},${startY - 50} ${endX},${endY + 50} ${endX},${endY}`;
        path.setAttribute('d', d);
        path.setAttribute('fill', 'none');
        path.setAttribute('stroke', strokeColor);
        path.setAttribute('stroke-width', strokeWidth);
        path.setAttribute('marker-end', `url(#arrowhead-${conn.type})`);

        if (dashArray) {
            path.setAttribute('stroke-dasharray', dashArray);
        }

        // Add label with improved visibility
        const textPath = document.createElementNS('http://www.w3.org/2000/svg', 'text');
        const pathId = `path-${conn.from}-${conn.to}`;
        path.id = pathId;

        const textPathElement = document.createElementNS('http://www.w3.org/2000/svg', 'textPath');
        textPathElement.setAttribute('href', `#${pathId}`);
        textPathElement.setAttribute('startOffset', '50%');
        textPathElement.textContent = conn.label;

        // Add background to text for better readability
        const textBackground = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
        textBackground.setAttribute('fill', 'white');
        textBackground.setAttribute('fill-opacity', '0.8');
        textBackground.setAttribute('rx', '3');
        textBackground.setAttribute('ry', '3');

        textPath.setAttribute('text-anchor', 'middle');
        textPath.setAttribute('fill', strokeColor);
        textPath.setAttribute('font-weight', 'bold');
        textPath.setAttribute('dy', '-5');
        textPath.appendChild(textPathElement);

        svg.appendChild(path);
        svg.appendChild(textPath);
    });

    // Draw components with consistent styling
    components.forEach(comp => {
        const group = document.createElementNS('http://www.w3.org/2000/svg', 'g');
        group.classList.add('component');
        group.setAttribute('data-id', comp.id);
        group.setAttribute('data-name', comp.name);
        group.setAttribute('data-description', comp.description);

        const rect = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
        rect.setAttribute('x', comp.x);
        rect.setAttribute('y', comp.y);
        rect.setAttribute('width', comp.width);
        rect.setAttribute('height', comp.height);
        rect.setAttribute('rx', '8');
        rect.setAttribute('ry', '8');
        rect.setAttribute('fill', comp.color);
        rect.setAttribute('stroke', '#333');
        rect.setAttribute('stroke-width', '2');

        const text = document.createElementNS('http://www.w3.org/2000/svg', 'text');
        text.setAttribute('x', comp.x + comp.width / 2);
        text.setAttribute('y', comp.y + comp.height / 2);
        text.setAttribute('text-anchor', 'middle');
        text.setAttribute('dominant-baseline', 'middle');
        text.setAttribute('fill', '#fff');
        text.setAttribute('font-weight', 'bold');
        text.textContent = comp.name;

        group.appendChild(rect);
        group.appendChild(text);
        svg.appendChild(group);
    });

    diagramContainer.appendChild(svg);

    // Create tooltip container if it doesn't exist
    if (!document.getElementById('component-tooltip')) {
        const tooltip = document.createElement('div');
        tooltip.id = 'component-tooltip';
        tooltip.className = 'component-tooltip';
        tooltip.style.display = 'none';
        document.body.appendChild(tooltip);
    }

    // Set up tooltips
    setupDiagramTooltips();

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
}

/**
 * Set up tooltips for the architecture diagram
 */
function setupDiagramTooltips() {
    const components = document.querySelectorAll('.component');
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

            .component {
                cursor: pointer;
                transition: opacity 0.3s ease;
            }

            .component:hover {
                opacity: 0.9;
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
    const svg = document.getElementById('architecture-diagram');
    if (!svg) return;

    const width = 800 * scale;
    const height = 600 * scale;

    svg.setAttribute('width', width);
    svg.setAttribute('height', height);

    // Center the diagram in the container
    const diagramContainer = document.getElementById('diagram-container');
    if (diagramContainer) {
        diagramContainer.style.display = 'flex';
        diagramContainer.style.justifyContent = 'center';
        diagramContainer.style.alignItems = 'center';
    }

    // Add version information
    const versionText = svg.querySelector('#version-text');
    if (!versionText) {
        const versionGroup = document.createElementNS('http://www.w3.org/2000/svg', 'g');
        versionGroup.setAttribute('transform', 'translate(700, 580)');

        const versionTextElement = document.createElementNS('http://www.w3.org/2000/svg', 'text');
        versionTextElement.id = 'version-text';
        versionTextElement.setAttribute('text-anchor', 'end');
        versionTextElement.setAttribute('font-size', '12');
        versionTextElement.setAttribute('fill', '#666');
        versionTextElement.textContent = 'v1.0.0 - Last updated: ' + new Date().toLocaleDateString();

        versionGroup.appendChild(versionTextElement);
        svg.appendChild(versionGroup);
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
