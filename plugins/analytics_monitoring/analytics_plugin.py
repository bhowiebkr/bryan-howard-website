"""
Analytics and Monitoring Plugin for Pelican
Adds Google Analytics, performance monitoring, and privacy-compliant tracking
"""

import os
import logging
from pelican import signals

logger = logging.getLogger(__name__)

def add_analytics_context(generator):
    """Add analytics configuration to template context"""
    if not hasattr(generator, 'context'):
        return
    
    analytics_config = {
        'google_analytics_id': generator.settings.get('GOOGLE_ANALYTICS', ''),
        'gtag_id': generator.settings.get('GTAG_ID', ''),
        'privacy_mode': generator.settings.get('PRIVACY_MODE', True),
        'cookie_consent': generator.settings.get('COOKIE_CONSENT', True),
        'performance_monitoring': generator.settings.get('PERFORMANCE_MONITORING', True),
        'error_tracking': generator.settings.get('ERROR_TRACKING', True)
    }
    
    generator.context['analytics'] = analytics_config

def generate_analytics_scripts(generator, writer):
    """Generate analytics scripts for inclusion in templates"""
    if not hasattr(generator, 'context'):
        return
    
    # Google Analytics 4 (gtag.js) script
    if generator.settings.get('GTAG_ID'):
        gtag_script = f"""
<!-- Google Analytics 4 -->
<script async src="https://www.googletagmanager.com/gtag/js?id={generator.settings.get('GTAG_ID')}"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
  
  gtag('config', '{generator.settings.get('GTAG_ID')}', {{
    'anonymize_ip': {'true' if generator.settings.get('PRIVACY_MODE', True) else 'false'},
    'respect_dnt': {'true' if generator.settings.get('PRIVACY_MODE', True) else 'false'},
    'allow_google_signals': {'false' if generator.settings.get('PRIVACY_MODE', True) else 'true'},
    'allow_ad_personalization_signals': {'false' if generator.settings.get('PRIVACY_MODE', True) else 'true'}
  }});
</script>
"""
        generator.context['gtag_script'] = gtag_script
    
    # Performance monitoring script
    if generator.settings.get('PERFORMANCE_MONITORING', True):
        performance_script = """
<script>
  // Performance monitoring
  (function() {
    'use strict';
    
    // Core Web Vitals tracking
    function trackWebVitals() {
      // Track Largest Contentful Paint (LCP)
      new PerformanceObserver((entryList) => {
        for (const entry of entryList.getEntries()) {
          if (entry.entryType === 'largest-contentful-paint') {
            const lcp = entry.startTime;
            if (typeof gtag !== 'undefined') {
              gtag('event', 'web_vitals', {
                'metric_name': 'LCP',
                'metric_value': Math.round(lcp),
                'metric_rating': lcp > 4000 ? 'poor' : lcp > 2500 ? 'needs_improvement' : 'good'
              });
            }
          }
        }
      }).observe({entryTypes: ['largest-contentful-paint']});
      
      // Track First Input Delay (FID)
      new PerformanceObserver((entryList) => {
        for (const entry of entryList.getEntries()) {
          const fid = entry.processingStart - entry.startTime;
          if (typeof gtag !== 'undefined') {
            gtag('event', 'web_vitals', {
              'metric_name': 'FID',
              'metric_value': Math.round(fid),
              'metric_rating': fid > 300 ? 'poor' : fid > 100 ? 'needs_improvement' : 'good'
            });
          }
        }
      }).observe({entryTypes: ['first-input']});
      
      // Track Cumulative Layout Shift (CLS)
      let clsValue = 0;
      let clsEntries = [];
      let sessionValue = 0;
      let sessionEntries = [];
      
      new PerformanceObserver((entryList) => {
        for (const entry of entryList.getEntries()) {
          if (!entry.hadRecentInput) {
            const firstSessionEntry = sessionEntries[0];
            const lastSessionEntry = sessionEntries[sessionEntries.length - 1];
            
            if (sessionValue && 
                entry.startTime - lastSessionEntry.startTime < 1000 &&
                entry.startTime - firstSessionEntry.startTime < 5000) {
              sessionValue += entry.value;
              sessionEntries.push(entry);
            } else {
              sessionValue = entry.value;
              sessionEntries = [entry];
            }
            
            if (sessionValue > clsValue) {
              clsValue = sessionValue;
              clsEntries = [...sessionEntries];
              
              if (typeof gtag !== 'undefined') {
                gtag('event', 'web_vitals', {
                  'metric_name': 'CLS',
                  'metric_value': Math.round(clsValue * 1000) / 1000,
                  'metric_rating': clsValue > 0.25 ? 'poor' : clsValue > 0.1 ? 'needs_improvement' : 'good'
                });
              }
            }
          }
        }
      }).observe({entryTypes: ['layout-shift']});
    }
    
    // Page load performance
    function trackPagePerformance() {
      window.addEventListener('load', function() {
        setTimeout(function() {
          const perfData = performance.getEntriesByType('navigation')[0];
          
          if (perfData && typeof gtag !== 'undefined') {
            gtag('event', 'page_performance', {
              'load_time': Math.round(perfData.loadEventEnd - perfData.loadEventStart),
              'dom_content_loaded': Math.round(perfData.domContentLoadedEventEnd - perfData.domContentLoadedEventStart),
              'first_paint': Math.round(performance.getEntriesByName('first-paint')[0]?.startTime || 0),
              'first_contentful_paint': Math.round(performance.getEntriesByName('first-contentful-paint')[0]?.startTime || 0)
            });
          }
        }, 1000);
      });
    }
    
    // Error tracking
    function trackErrors() {
      window.addEventListener('error', function(e) {
        if (typeof gtag !== 'undefined') {
          gtag('event', 'javascript_error', {
            'error_message': e.message,
            'error_filename': e.filename,
            'error_lineno': e.lineno,
            'error_colno': e.colno
          });
        }
      });
      
      window.addEventListener('unhandledrejection', function(e) {
        if (typeof gtag !== 'undefined') {
          gtag('event', 'promise_rejection', {
            'error_reason': e.reason
          });
        }
      });
    }
    
    // Initialize tracking
    if ('PerformanceObserver' in window) {
      trackWebVitals();
    }
    trackPagePerformance();
    trackErrors();
    
  })();
</script>
"""
        generator.context['performance_script'] = performance_script
    
    # Cookie consent script
    if generator.settings.get('COOKIE_CONSENT', True):
        cookie_consent_script = """
<script>
  // Simple cookie consent
  (function() {
    'use strict';
    
    function showCookieConsent() {
      if (localStorage.getItem('cookieConsent') === 'accepted') {
        return;
      }
      
      const banner = document.createElement('div');
      banner.innerHTML = `
        <div style="position: fixed; bottom: 0; left: 0; right: 0; background: var(--bg-secondary); border-top: 1px solid var(--border-primary); padding: 1rem; z-index: 10000; box-shadow: 0 -2px 10px rgba(0,0,0,0.1);">
          <div style="max-width: 1200px; margin: 0 auto; display: flex; align-items: center; justify-content: space-between; gap: 1rem; flex-wrap: wrap;">
            <p style="margin: 0; color: var(--text-primary); font-size: 0.9rem;">
              This website uses cookies to enhance your experience and analyze site usage. 
              <a href="/privacy-policy/" style="color: var(--color-primary); text-decoration: underline;">Learn more</a>
            </p>
            <div style="display: flex; gap: 0.5rem;">
              <button id="acceptCookies" style="background: var(--color-primary); color: white; border: none; padding: 0.5rem 1rem; border-radius: 0.25rem; cursor: pointer; font-size: 0.9rem;">
                Accept
              </button>
              <button id="declineCookies" style="background: transparent; color: var(--text-primary); border: 1px solid var(--border-primary); padding: 0.5rem 1rem; border-radius: 0.25rem; cursor: pointer; font-size: 0.9rem;">
                Decline
              </button>
            </div>
          </div>
        </div>
      `;
      
      document.body.appendChild(banner);
      
      document.getElementById('acceptCookies').onclick = function() {
        localStorage.setItem('cookieConsent', 'accepted');
        document.body.removeChild(banner);
        // Initialize analytics here if needed
        if (typeof gtag !== 'undefined') {
          gtag('consent', 'update', {
            'analytics_storage': 'granted'
          });
        }
      };
      
      document.getElementById('declineCookies').onclick = function() {
        localStorage.setItem('cookieConsent', 'declined');
        document.body.removeChild(banner);
        // Disable analytics
        if (typeof gtag !== 'undefined') {
          gtag('consent', 'update', {
            'analytics_storage': 'denied'
          });
        }
      };
    }
    
    // Show consent banner after page load
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', showCookieConsent);
    } else {
      showCookieConsent();
    }
    
  })();
</script>
"""
        generator.context['cookie_consent_script'] = cookie_consent_script

def register():
    """Register the plugin"""
    signals.generator_init.connect(add_analytics_context)
    signals.writer_finalized.connect(generate_analytics_scripts)