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
    
    // Define components
    const components = [
        { id: 'api', x: 150, y: 150, width: 180, height: 80, color: '#5865F2', name: 'Discord API Client', description: 'Handles communication with Discord API, fetches messages, and manages rate limits.' },
        { id: 'processor', x: 400, y: 150, width: 180, height: 80, color: '#57F287', name: 'Message Processor', description: 'Processes raw message data and formats it into various output formats (text, JSON, CSV, Markdown).' },
        { id: 'file_handler', x: 650, y: 150, width: 180, height: 80, color: '#FEE75C', name: 'File Handler', description: 'Manages file operations, including opening file dialogs and saving content to files.' },
        { id: 'cli', x: 275, y: 300, width: 180, height: 80, color: '#EB459E', name: 'Command-Line Interface', description: 'Provides a CLI using Click with various options for fetching and saving messages.' },
        { id: 'gui', x: 525, y: 300, width: 180, height: 80, color: '#ED4245', name: 'GUI Script', description: 'Provides a graphical interface for selecting output format and file location.' },
        { id: 'config', x: 400, y: 450, width: 180, height: 80, color: '#9B84EC', name: 'Configuration', description: 'Manages environment variables, validates input, and provides default values.' }
    ];
    
    // Define connections
    const connections = [
        { from: 'cli', to: 'api', label: 'uses' },
        { from: 'cli', to: 'processor', label: 'uses' },
        { from: 'cli', to: 'file_handler', label: 'uses' },
        { from: 'gui', to: 'api', label: 'uses' },
        { from: 'gui', to: 'processor', label: 'uses' },
        { from: 'gui', to: 'file_handler', label: 'uses' },
        { from: 'processor', to: 'api', label: 'receives data' },
        { from: 'cli', to: 'config', label: 'loads' },
        { from: 'gui', to: 'config', label: 'loads' }
    ];
    
    // Add arrowhead marker
    const defs = document.createElementNS('http://www.w3.org/2000/svg', 'defs');
    const marker = document.createElementNS('http://www.w3.org/2000/svg', 'marker');
    marker.id = 'arrowhead';
    marker.setAttribute('viewBox', '0 0 10 10');
    marker.setAttribute('refX', '5');
    marker.setAttribute('refY', '5');
    marker.setAttribute('markerWidth', '6');
    marker.setAttribute('markerHeight', '6');
    marker.setAttribute('orient', 'auto');
    
    const markerPath = document.createElementNS('http://www.w3.org/2000/svg', 'path');
    markerPath.setAttribute('d', 'M 0 0 L 10 5 L 0 10 z');
    markerPath.setAttribute('fill', '#333');
    
    marker.appendChild(markerPath);
    defs.appendChild(marker);
    svg.appendChild(defs);
    
    // Draw connections
    connections.forEach(conn => {
        const fromComp = components.find(c => c.id === conn.from);
        const toComp = components.find(c => c.id === conn.to);
        
        // Calculate start and end points
        const startX = fromComp.x + fromComp.width / 2;
        const startY = fromComp.y;
        const endX = toComp.x + toComp.width / 2;
        const endY = toComp.y + toComp.height;
        
        // Draw arrow
        const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
        const d = `M${startX},${startY} C${startX},${startY - 50} ${endX},${endY + 50} ${endX},${endY}`;
        path.setAttribute('d', d);
        path.setAttribute('fill', 'none');
        path.setAttribute('stroke', '#333');
        path.setAttribute('stroke-width', '2');
        path.setAttribute('marker-end', 'url(#arrowhead)');
        
        // Add label
        const textPath = document.createElementNS('http://www.w3.org/2000/svg', 'text');
        const pathId = `path-${conn.from}-${conn.to}`;
        path.id = pathId;
        
        const textPathElement = document.createElementNS('http://www.w3.org/2000/svg', 'textPath');
        textPathElement.setAttribute('href', `#${pathId}`);
        textPathElement.setAttribute('startOffset', '50%');
        textPathElement.textContent = conn.label;
        
        textPath.setAttribute('text-anchor', 'middle');
        textPath.setAttribute('fill', '#333');
        textPath.appendChild(textPathElement);
        
        svg.appendChild(path);
        svg.appendChild(textPath);
    });
    
    // Draw components
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
        rect.setAttribute('rx', '10');
        rect.setAttribute('ry', '10');
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
    
    // Set up tooltips
    setupDiagramTooltips();
    
    // Set up zoom controls
    const zoomControls = document.querySelectorAll('.zoom-btn');
    zoomControls.forEach(btn => {
        btn.addEventListener('click', function() {
            const scale = parseFloat(this.getAttribute('data-scale'));
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
    
    components.forEach(comp => {
        comp.addEventListener('mouseover', function(e) {
            const name = this.getAttribute('data-name');
            const description = this.getAttribute('data-description');
            
            tooltip.innerHTML = `<strong>${name}</strong><br>${description}`;
            tooltip.style.display = 'block';
            tooltip.style.left = `${e.pageX + 10}px`;
            tooltip.style.top = `${e.pageY + 10}px`;
        });
        
        comp.addEventListener('mousemove', function(e) {
            tooltip.style.left = `${e.pageX + 10}px`;
            tooltip.style.top = `${e.pageY + 10}px`;
        });
        
        comp.addEventListener('mouseout', function() {
            tooltip.style.display = 'none';
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
    
    // Update active button
    const zoomButtons = document.querySelectorAll('.zoom-btn');
    zoomButtons.forEach(btn => {
        const btnScale = parseFloat(btn.getAttribute('data-scale'));
        if (btnScale === scale) {
            btn.classList.add('active');
        } else {
            btn.classList.remove('active');
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
 * Initialize copy buttons for code blocks
 */
function initCopyButtons() {
    const codeBlocks = document.querySelectorAll('pre code');
    
    codeBlocks.forEach(block => {
        const pre = block.parentNode;
        
        // Create copy button
        const copyButton = document.createElement('button');
        copyButton.className = 'copy-button';
        copyButton.textContent = 'Copy';
        
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
