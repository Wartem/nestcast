chrome.runtime.onInstalled.addListener(() => {
  chrome.contextMenus.create({
    id: "castMedia",
    title: "Chromecast Media Mini TV",
    contexts: ["image", "video", "audio", "link"]
  });
});

chrome.contextMenus.onClicked.addListener((info, tab) => {
  if (info.menuItemId === "castMedia") {
    let mediaUrl = info.srcUrl || info.linkUrl;
    
    if (mediaUrl) {
      determineContentTypeAndCast(mediaUrl);
    } else {
      console.error("Unable to determine media URL");
    }
  }
});

async function determineContentTypeAndCast(url) {
  if (isYouTubeUrl(url)) {
    castYouTubeVideo(url);
    return;
  }

  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), 5000); // 5 second timeout

  try {
    const response = await fetch(url, { 
      method: 'HEAD', 
      signal: controller.signal 
    });
    clearTimeout(timeoutId);

    let contentType = response.headers.get('content-type');
    if (contentType) {
      castMedia(url, contentType);
    } else {
      // If content-type header is not found, try guessing from URL
      const guessedType = guessMimeTypeFromUrl(url);
      if (guessedType) {
        castMedia(url, guessedType);
      } else {
        throw new Error("Unable to determine content type");
      }
    }
  } catch (error) {
    clearTimeout(timeoutId);
    console.error('Error determining content type:', error);
    
    // Fallback to guessing content type from URL
    const guessedType = guessMimeTypeFromUrl(url);
    if (guessedType) {
      castMedia(url, guessedType);
    } else {
      console.error("Unable to determine content type");
    }
  }
}

function isYouTubeUrl(url) {
  return url.includes('youtube.com') || url.includes('youtu.be');
}

function castYouTubeVideo(url) {
  let videoId = '';
  const parsedUrl = new URL(url);
  
  if (parsedUrl.hostname === 'youtu.be') {
    videoId = parsedUrl.pathname.slice(1);
  } else if (parsedUrl.hostname.includes('youtube.com')) {
    if (parsedUrl.searchParams.has('v')) {
      videoId = parsedUrl.searchParams.get('v');
    } else if (parsedUrl.pathname.startsWith('/embed/')) {
      videoId = parsedUrl.pathname.split('/')[2];
    } else if (parsedUrl.pathname.includes('/video/')) {
      videoId = parsedUrl.pathname.split('/video/')[1];
    }
  }

  if (videoId) {
    const youtubeEmbedUrl = `https://www.youtube.com/embed/${videoId}`;
    castMedia(youtubeEmbedUrl, 'video/youtube');
  } else {
    console.error("Unable to extract YouTube video ID");
  }
}

function guessMimeTypeFromUrl(url) {
  // Check for known CDN patterns first
  if (url.includes('cloudfront.net') && url.includes('_fullscreen')) {
    return 'image/jpeg';  // Assume JPEG for Bukowskis-like URLs
  }

  // Then check for file extensions
  return getContentTypeFromUrl(url);
}

function getContentTypeFromUrl(url) {
  const extension = url.split('.').pop().toLowerCase().split(/[?#]/)[0];
  const mimeTypes = {
    // Highly Compatible
    'mp4': 'video/mp4',
    'mp3': 'audio/mpeg',
    'webm': 'video/webm',
    'jpg': 'image/jpeg',
    'jpeg': 'image/jpeg',
    'png': 'image/png',
    'gif': 'image/gif',
    // Potentially Compatible
    'wav': 'audio/wav',
    'ogg': 'audio/ogg',
    'aac': 'audio/aac',
    'm4a': 'audio/mp4',
    'flac': 'audio/flac',
    // Limited Compatibility
    'avi': 'video/x-msvideo',
    'mov': 'video/quicktime',
    'wmv': 'video/x-ms-wmv',
    'mpeg': 'video/mpeg',
    'mpg': 'video/mpeg',
    // Non-Media (for potential other uses)
    'bmp': 'image/bmp',
    'svg': 'image/svg+xml',
    'pdf': 'application/pdf',
    'txt': 'text/plain',
    'html': 'text/html',
    'css': 'text/css',
    'js': 'application/javascript',
    'json': 'application/json',
    'xml': 'application/xml'
  };
  return mimeTypes[extension] || null;
}

async function castMedia(mediaUrl, contentType) {
  const formData = new FormData();
  formData.append('media_url', mediaUrl);
  formData.append('content_type', contentType);
  formData.append('volume', '0.6');
  formData.append('devices', JSON.stringify(['Mini TV']));

  try {
    const response = await fetch('http://192.168.68.201:5030/api/stream_media', {
      method: 'POST',
      body: formData
    });
    const data = await response.json();
    console.log(data);
  } catch (error) {
    console.error('Error:', error);
  }
}