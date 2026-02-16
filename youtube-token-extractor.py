"""
YouTube Token Extractor
-----------------------
This script helps you extract the po_token and visitor_data from YouTube.

INSTRUCTIONS:
1. Open YouTube in your browser (Chrome, Firefox, Edge, etc.)
2. Make sure you're logged in
3. Press F12 to open Developer Tools
4. Go to the "Console" tab
5. Copy and paste the code below into the console and press Enter

COPY THIS CODE INTO BROWSER CONSOLE:
====================================

// Extract tokens from YouTube
(function() {
    const cookies = document.cookie.split(';').reduce((acc, cookie) => {
        const [key, value] = cookie.trim().split('=');
        acc[key] = value;
        return acc;
    }, {});
    
    const po_token = cookies['__Secure-1PAPISID'] || cookies['SAPISID'] || 'Not found';
    const visitor_data = cookies['VISITOR_INFO1_LIVE'] || cookies['VISITOR_PRIVACY_METADATA'] || 'Not found';
    
    console.log('=====================================');
    console.log('YouTube Tokens:');
    console.log('=====================================');
    console.log('po_token:', po_token);
    console.log('visitor_data:', visitor_data);
    console.log('=====================================');
    console.log('Copy these values into your downloader!');
    
    // Also try to get from localStorage
    try {
        const ytCfg = window.ytcfg?.data_;
        if (ytCfg) {
            console.log('\nAlternative method:');
            console.log('DELEGATED_SESSION_ID:', ytCfg.DELEGATED_SESSION_ID || 'Not found');
            console.log('INNERTUBE_CONTEXT:', ytCfg.INNERTUBE_CONTEXT?.client?.visitorData || 'Not found');
        }
    } catch(e) {
        console.log('Could not extract from ytcfg');
    }
})();

====================================

ALTERNATIVE METHOD (if above doesn't work):
==========================================

1. In Developer Tools, go to "Application" tab (Chrome) or "Storage" tab (Firefox)
2. Click on "Cookies" in the left sidebar
3. Click on "https://www.youtube.com"
4. Look for these cookies:
   - __Secure-1PAPISID (use as po_token)
   - VISITOR_INFO1_LIVE (use as visitor_data)
5. Copy their values

====================================

NOTE: These tokens expire after some time. If downloads start failing again,
you'll need to extract fresh tokens.
"""

print(__doc__)