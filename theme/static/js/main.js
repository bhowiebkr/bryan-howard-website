/**
 * Bryan Howard Website - Main JavaScript
 * 
 * Features:
 * - Mobile navigation toggle
 * - Theme toggle functionality
 * - Smooth scrolling
 * - Search functionality
 * - Accessibility enhancements
 * - Performance optimizations
 */

'use strict';

(function() {
    // Utility functions
    const utils = {
        // Debounce function for performance
        debounce: function(func, wait) {
            let timeout;
            return function executedFunction(...args) {
                const later = () => {
                    clearTimeout(timeout);
                    func(...args);
                };
                clearTimeout(timeout);
                timeout = setTimeout(later, wait);
            };
        },
        
        // Throttle function for scroll events
        throttle: function(func, limit) {
            let inThrottle;
            return function() {
                const args = arguments;
                const context = this;
                if (!inThrottle) {
                    func.apply(context, args);
                    inThrottle = true;
                    setTimeout(() => inThrottle = false, limit);
                }
            };
        },
        
        // Check if element is in viewport
        isInViewport: function(element) {
            const rect = element.getBoundingClientRect();
            return (
                rect.top >= 0 &&
                rect.left >= 0 &&
                rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
                rect.right <= (window.innerWidth || document.documentElement.clientWidth)
            );
        },
        
        // Add focus trap for accessibility
        focusTrap: function(element) {
            const focusableElements = element.querySelectorAll(
                'a[href], button, textarea, input[type="text"], input[type="radio"], input[type="checkbox"], select'
            );
            const firstFocusableElement = focusableElements[0];
            const lastFocusableElement = focusableElements[focusableElements.length - 1];
            
            element.addEventListener('keydown', function(e) {
                if (e.key === 'Tab') {
                    if (e.shiftKey) {
                        if (document.activeElement === firstFocusableElement) {
                            lastFocusableElement.focus();
                            e.preventDefault();
                        }
                    } else {
                        if (document.activeElement === lastFocusableElement) {
                            firstFocusableElement.focus();
                            e.preventDefault();
                        }
                    }
                }
                
                if (e.key === 'Escape') {
                    element.style.display = 'none';
                    document.body.style.overflow = '';
                }
            });
        }
    };

    // Mobile Navigation
    class MobileNavigation {
        constructor() {
            this.toggle = document.querySelector('.mobile-menu-toggle');
            this.nav = document.querySelector('.main-nav');
            this.body = document.body;
            this.isOpen = false;
            
            if (this.toggle && this.nav) {
                this.init();
            }
        }
        
        init() {
            this.toggle.addEventListener('click', () => this.toggleMenu());
            this.nav.addEventListener('click', (e) => {
                if (e.target.classList.contains('nav-link')) {
                    this.closeMenu();
                }
            });
            
            // Close menu on escape key
            document.addEventListener('keydown', (e) => {
                if (e.key === 'Escape' && this.isOpen) {
                    this.closeMenu();
                }
            });
            
            // Close menu when clicking outside
            document.addEventListener('click', (e) => {
                if (this.isOpen && !this.nav.contains(e.target) && !this.toggle.contains(e.target)) {
                    this.closeMenu();
                }
            });
            
            // Handle resize
            window.addEventListener('resize', utils.throttle(() => {
                if (window.innerWidth > 768 && this.isOpen) {
                    this.closeMenu();
                }
            }, 250));
        }
        
        toggleMenu() {
            if (this.isOpen) {
                this.closeMenu();
            } else {
                this.openMenu();
            }
        }
        
        openMenu() {
            this.isOpen = true;
            this.nav.classList.add('active');
            this.toggle.setAttribute('aria-expanded', 'true');
            this.body.style.overflow = 'hidden';
            
            // Focus first nav link
            const firstLink = this.nav.querySelector('.nav-link');
            if (firstLink) {
                firstLink.focus();
            }
            
            // Add focus trap
            utils.focusTrap(this.nav);
        }
        
        closeMenu() {
            this.isOpen = false;
            this.nav.classList.remove('active');
            this.toggle.setAttribute('aria-expanded', 'false');
            this.body.style.overflow = '';
            this.toggle.focus();
        }
    }

    // Theme Toggle
    class ThemeToggle {
        constructor() {
            this.toggle = document.querySelector('.theme-toggle');
            this.html = document.documentElement;
            this.currentTheme = this.getStoredTheme() || 'dark';
            
            if (this.toggle) {
                this.init();
            }
        }
        
        init() {
            this.setTheme(this.currentTheme);
            this.updateToggleIcon();
            
            this.toggle.addEventListener('click', () => {
                this.currentTheme = this.currentTheme === 'dark' ? 'light' : 'dark';
                this.setTheme(this.currentTheme);
                this.updateToggleIcon();
                this.storeTheme(this.currentTheme);
            });
        }
        
        setTheme(theme) {
            this.html.className = this.html.className.replace(/theme-\w+/, `theme-${theme}`);
            if (!this.html.className.includes('theme-')) {
                this.html.classList.add(`theme-${theme}`);
            }
        }
        
        updateToggleIcon() {
            const icon = this.toggle.querySelector('i');
            if (icon) {
                icon.className = this.currentTheme === 'dark' ? 'fas fa-sun' : 'fas fa-moon';
            }
            this.toggle.setAttribute('aria-label', 
                `Switch to ${this.currentTheme === 'dark' ? 'light' : 'dark'} theme`);
        }
        
        getStoredTheme() {
            try {
                return localStorage.getItem('theme');
            } catch (e) {
                return null;
            }
        }
        
        storeTheme(theme) {
            try {
                localStorage.setItem('theme', theme);
            } catch (e) {
                // Local storage not available
            }
        }
    }

    // Smooth Scrolling
    class SmoothScrolling {
        constructor() {
            this.init();
        }
        
        init() {
            // Smooth scrolling for anchor links
            document.addEventListener('click', (e) => {
                const target = e.target.closest('a[href^="#"]');
                if (target && target.getAttribute('href') !== '#') {
                    e.preventDefault();
                    const href = target.getAttribute('href');
                    const element = document.querySelector(href);
                    
                    if (element) {
                        const offsetTop = element.offsetTop - 80; // Account for fixed header
                        window.scrollTo({
                            top: offsetTop,
                            behavior: 'smooth'
                        });
                        
                        // Update focus for accessibility
                        element.focus();
                        if (element.tabIndex < 0) {
                            element.tabIndex = -1;
                        }
                    }
                }
            });
        }
    }

    // Header Scroll Effects
    class HeaderEffects {
        constructor() {
            this.header = document.querySelector('.site-header');
            this.lastScrollY = window.scrollY;
            
            if (this.header) {
                this.init();
            }
        }
        
        init() {
            window.addEventListener('scroll', utils.throttle(() => {
                const currentScrollY = window.scrollY;
                
                // Add/remove scrolled class
                if (currentScrollY > 50) {
                    this.header.classList.add('scrolled');
                } else {
                    this.header.classList.remove('scrolled');
                }
                
                this.lastScrollY = currentScrollY;
            }, 10));
        }
    }

    // Lazy Loading Images
    class LazyLoading {
        constructor() {
            this.images = document.querySelectorAll('img[loading="lazy"]');
            this.init();
        }
        
        init() {
            if ('IntersectionObserver' in window) {
                this.observer = new IntersectionObserver((entries) => {
                    entries.forEach(entry => {
                        if (entry.isIntersecting) {
                            const img = entry.target;
                            img.classList.add('loaded');
                            this.observer.unobserve(img);
                        }
                    });
                }, {
                    rootMargin: '50px 0px'
                });
                
                this.images.forEach(img => {
                    this.observer.observe(img);
                });
            }
        }
    }

    // Copy Code Blocks
    class CodeCopyButtons {
        constructor() {
            this.codeBlocks = document.querySelectorAll('pre code');
            this.init();
        }
        
        init() {
            this.codeBlocks.forEach((codeBlock, index) => {
                const pre = codeBlock.parentElement;
                const button = this.createCopyButton(index);
                
                pre.style.position = 'relative';
                pre.appendChild(button);
                
                button.addEventListener('click', () => {
                    this.copyToClipboard(codeBlock.textContent, button);
                });
            });
        }
        
        createCopyButton(index) {
            const button = document.createElement('button');
            button.className = 'copy-code-btn';
            button.innerHTML = '<i class="fas fa-copy" aria-hidden="true"></i>';
            button.setAttribute('aria-label', `Copy code block ${index + 1}`);
            button.type = 'button';
            
            return button;
        }
        
        async copyToClipboard(text, button) {
            try {
                await navigator.clipboard.writeText(text);
                this.showCopySuccess(button);
            } catch (err) {
                // Fallback for older browsers
                this.fallbackCopyTextToClipboard(text, button);
            }
        }
        
        fallbackCopyTextToClipboard(text, button) {
            const textArea = document.createElement('textarea');
            textArea.value = text;
            textArea.style.position = 'fixed';
            textArea.style.left = '-999999px';
            textArea.style.top = '-999999px';
            document.body.appendChild(textArea);
            textArea.focus();
            textArea.select();
            
            try {
                document.execCommand('copy');
                this.showCopySuccess(button);
            } catch (err) {
                console.error('Fallback: Oops, unable to copy', err);
            }
            
            document.body.removeChild(textArea);
        }
        
        showCopySuccess(button) {
            const originalHTML = button.innerHTML;
            button.innerHTML = '<i class="fas fa-check" aria-hidden="true"></i>';
            button.classList.add('copied');
            
            setTimeout(() => {
                button.innerHTML = originalHTML;
                button.classList.remove('copied');
            }, 2000);
        }
    }

    // Form Enhancement
    class FormEnhancement {
        constructor() {
            this.forms = document.querySelectorAll('form');
            this.init();
        }
        
        init() {
            this.forms.forEach(form => {
                this.enhanceForm(form);
            });
        }
        
        enhanceForm(form) {
            const inputs = form.querySelectorAll('input, textarea');
            
            inputs.forEach(input => {
                // Add floating label effect
                this.addFloatingLabel(input);
                
                // Add validation
                this.addValidation(input);
            });
            
            // Form submission
            form.addEventListener('submit', (e) => {
                if (!this.validateForm(form)) {
                    e.preventDefault();
                }
            });
        }
        
        addFloatingLabel(input) {
            const wrapper = document.createElement('div');
            wrapper.className = 'input-wrapper';
            
            input.parentNode.insertBefore(wrapper, input);
            wrapper.appendChild(input);
            
            input.addEventListener('focus', () => {
                wrapper.classList.add('focused');
            });
            
            input.addEventListener('blur', () => {
                if (!input.value.trim()) {
                    wrapper.classList.remove('focused');
                }
            });
            
            if (input.value.trim()) {
                wrapper.classList.add('focused');
            }
        }
        
        addValidation(input) {
            input.addEventListener('blur', () => {
                this.validateField(input);
            });
            
            input.addEventListener('input', utils.debounce(() => {
                this.validateField(input);
            }, 300));
        }
        
        validateField(input) {
            const value = input.value.trim();
            let isValid = true;
            let message = '';
            
            // Required validation
            if (input.required && !value) {
                isValid = false;
                message = 'This field is required';
            }
            
            // Email validation
            if (input.type === 'email' && value) {
                const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
                if (!emailRegex.test(value)) {
                    isValid = false;
                    message = 'Please enter a valid email address';
                }
            }
            
            this.showValidation(input, isValid, message);
            return isValid;
        }
        
        showValidation(input, isValid, message) {
            const wrapper = input.closest('.form-group') || input.parentElement;
            let errorElement = wrapper.querySelector('.error-message');
            
            if (!errorElement) {
                errorElement = document.createElement('div');
                errorElement.className = 'error-message';
                wrapper.appendChild(errorElement);
            }
            
            if (isValid) {
                input.classList.remove('error');
                errorElement.textContent = '';
                errorElement.style.display = 'none';
            } else {
                input.classList.add('error');
                errorElement.textContent = message;
                errorElement.style.display = 'block';
            }
        }
        
        validateForm(form) {
            const inputs = form.querySelectorAll('input[required], textarea[required]');
            let isValid = true;
            
            inputs.forEach(input => {
                if (!this.validateField(input)) {
                    isValid = false;
                }
            });
            
            return isValid;
        }
    }

    // Analytics and Performance
    class Analytics {
        constructor() {
            this.init();
        }
        
        init() {
            // Track page performance
            if ('performance' in window) {
                window.addEventListener('load', () => {
                    const perfData = performance.getEntriesByType('navigation')[0];
                    console.log('Page load time:', perfData.loadEventEnd - perfData.loadEventStart, 'ms');
                });
            }
            
            // Track scroll depth
            this.trackScrollDepth();
        }
        
        trackScrollDepth() {
            let maxScroll = 0;
            const milestones = [25, 50, 75, 90, 100];
            const tracked = new Set();
            
            window.addEventListener('scroll', utils.throttle(() => {
                const scrollTop = window.pageYOffset;
                const documentHeight = document.documentElement.scrollHeight;
                const windowHeight = window.innerHeight;
                const scrollPercent = Math.round((scrollTop / (documentHeight - windowHeight)) * 100);
                
                if (scrollPercent > maxScroll) {
                    maxScroll = scrollPercent;
                    
                    milestones.forEach(milestone => {
                        if (scrollPercent >= milestone && !tracked.has(milestone)) {
                            tracked.add(milestone);
                            // Send to analytics if available
                            if (typeof gtag !== 'undefined') {
                                gtag('event', 'scroll_depth', {
                                    'custom_parameter': milestone
                                });
                            }
                        }
                    });
                }
            }, 500));
        }
    }

    // YouTube Video Cards Enhancement
    class YouTubeEnhancements {
        constructor() {
            this.videoCards = document.querySelectorAll('.video-card');
            this.init();
        }
        
        init() {
            this.videoCards.forEach(card => {
                this.enhanceVideoCard(card);
            });
        }
        
        enhanceVideoCard(card) {
            const thumbnail = card.querySelector('.video-thumbnail');
            const playOverlay = card.querySelector('.play-overlay');
            
            if (thumbnail && playOverlay) {
                // Add hover effects
                thumbnail.addEventListener('mouseenter', () => {
                    playOverlay.style.transform = 'scale(1.1)';
                    playOverlay.style.opacity = '0.9';
                });
                
                thumbnail.addEventListener('mouseleave', () => {
                    playOverlay.style.transform = 'scale(1)';
                    playOverlay.style.opacity = '0.8';
                });
                
                // Add keyboard navigation
                const link = thumbnail.querySelector('a');
                if (link) {
                    link.addEventListener('focus', () => {
                        thumbnail.style.transform = 'scale(1.02)';
                    });
                    
                    link.addEventListener('blur', () => {
                        thumbnail.style.transform = 'scale(1)';
                    });
                }
            }
        }
    }
    
    // GitHub Repository Cards Enhancement
    class GitHubEnhancements {
        constructor() {
            this.repoCards = document.querySelectorAll('.repository-card');
            this.init();
        }
        
        init() {
            this.repoCards.forEach(card => {
                this.enhanceRepoCard(card);
            });
        }
        
        enhanceRepoCard(card) {
            const repoLink = card.querySelector('.repo-name a');
            
            if (repoLink) {
                // Make entire card clickable
                card.style.cursor = 'pointer';
                card.setAttribute('tabindex', '0');
                card.setAttribute('role', 'button');
                card.setAttribute('aria-label', `View ${repoLink.textContent} repository`);
                
                // Handle click on card
                card.addEventListener('click', (e) => {
                    if (e.target.tagName !== 'A') {
                        repoLink.click();
                    }
                });
                
                // Handle keyboard navigation
                card.addEventListener('keydown', (e) => {
                    if (e.key === 'Enter' || e.key === ' ') {
                        e.preventDefault();
                        repoLink.click();
                    }
                });
                
                // Add focus styles
                card.addEventListener('focus', () => {
                    card.style.outline = '2px solid var(--color-primary)';
                    card.style.outlineOffset = '2px';
                });
                
                card.addEventListener('blur', () => {
                    card.style.outline = 'none';
                });
            }
        }
    }
    
    // Scroll to Top Button
    class ScrollToTop {
        constructor() {
            this.button = null;
            this.init();
        }
        
        init() {
            this.createButton();
            this.handleScroll();
        }
        
        createButton() {
            this.button = document.createElement('button');
            this.button.innerHTML = '<i class="fas fa-arrow-up" aria-hidden="true"></i>';
            this.button.className = 'scroll-to-top';
            this.button.setAttribute('aria-label', 'Scroll to top');
            this.button.style.cssText = `
                position: fixed;
                bottom: 2rem;
                right: 2rem;
                width: 3rem;
                height: 3rem;
                border: none;
                border-radius: 50%;
                background-color: var(--color-primary);
                color: white;
                cursor: pointer;
                opacity: 0;
                transform: translateY(100px);
                transition: all 0.3s ease;
                z-index: 1000;
                box-shadow: 0 4px 12px var(--shadow-md);
                display: flex;
                align-items: center;
                justify-content: center;
            `;
            
            document.body.appendChild(this.button);
            
            this.button.addEventListener('click', () => {
                window.scrollTo({
                    top: 0,
                    behavior: 'smooth'
                });
            });
        }
        
        handleScroll() {
            let ticking = false;
            
            const updateButton = () => {
                const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
                
                if (scrollTop > 500) {
                    this.button.style.opacity = '1';
                    this.button.style.transform = 'translateY(0)';
                } else {
                    this.button.style.opacity = '0';
                    this.button.style.transform = 'translateY(100px)';
                }
                
                ticking = false;
            };
            
            window.addEventListener('scroll', () => {
                if (!ticking) {
                    requestAnimationFrame(updateButton);
                    ticking = true;
                }
            }, { passive: true });
        }
    }

    // Initialize all modules when DOM is ready
    function init() {
        new MobileNavigation();
        new ThemeToggle();
        new SmoothScrolling();
        new HeaderEffects();
        new LazyLoading();
        new CodeCopyButtons();
        new FormEnhancement();
        new Analytics();
        new YouTubeEnhancements();
        new GitHubEnhancements();
        new ScrollToTop();
        
        // Add loaded class to body for CSS transitions
        document.body.classList.add('loaded');
    }

    // DOM Ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

    // Export for external use
    window.BryanHowardSite = {
        utils: utils
    };

})();