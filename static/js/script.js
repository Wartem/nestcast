// This is static/js/script.js

let volumeValue = 0.5;

document.addEventListener('DOMContentLoaded', function() {
    const deviceList = document.getElementById('deviceList');
    const audioForm = document.getElementById('audioForm');
    const discoverBtn = document.getElementById('discoverBtn');
    const sendBtn = document.getElementById('sendBtn');
    const pauseAllBtn = document.getElementById('pauseAllBtn');
    const stopAllBtn = document.getElementById('stopAllBtn');
    const loadingDevices = document.getElementById('loadingDevices');
    const audioFile = document.getElementById('audioFile');
    const streamUrl = document.getElementById('streamUrl');
    const streamBtn = document.getElementById('streamBtn');
    const playAudioBtn = document.getElementById('playAudioBtn');
    const volumeInput = document.getElementById('volume');
    const volumeValueSpan = document.getElementById('volume-value');

    // Initialize device list on page load
    updateDeviceList();
    populate_tts_languages();
    setButtonState(false);

    // Event Listeners
    audioForm.addEventListener('submit', handleMessageSubmit);
    discoverBtn.addEventListener('click', handleDiscoverDevices);
    pauseAllBtn.addEventListener('click', handlePauseAll);
    stopAllBtn.addEventListener('click', handleStopAll);
    streamBtn.addEventListener('click', handleStreamMedia);
    playAudioBtn.addEventListener('click', () => handleAudioAction('play', '/api/play_audio'));
    volumeInput.addEventListener('input', handleVolumeChange);

    // Functions
    function setButtonState(isDisabled) {
        sendBtn.disabled = isDisabled;
        streamBtn.disabled = isDisabled;
        playAudioBtn.disabled = isDisabled;
        pauseAllBtn.disabled = isDisabled;
        stopAllBtn.disabled = isDisabled;
    }

    function getSelectedDevices() {
        return Array.from(document.querySelectorAll('input[name="devices"]:checked')).map(input => input.value);
    }

    function updateDeviceList() {   
        loadingDevices.style.display = 'block';
        axios.get('/api/devices')
            .then(response => {
                loadingDevices.style.display = 'none';
                if (response.data.length > 0) {
                    deviceList.innerHTML = `
                        <div class="device-list">
                            ${response.data.map(device => `
                                <div class="device-item">
                                    <input type="checkbox" name="devices" value="${device.name}" id="${device.name}">
                                    <label for="${device.name}">
                                        <span class="device-name">${device.name}</span>
                                        <span class="device-ip">${device.ip}</span>
                                    </label>
                                </div>
                            `).join('')}
                        </div>
                    `;
                    setButtonState(false);
                } else {
                    deviceList.innerHTML = '<p class="no-devices">No devices available.</p>';
                    setButtonState(true);
                }
            })
            .catch(error => {
                console.error('Error fetching devices:', error);
                deviceList.innerHTML = '<p class="error-message">Error retrieving devices. Please try again later.</p>';
                setButtonState(true);
            });
    }

    function populate_tts_languages() {
        console.log('Attempting to fetch tts_languages.txt');
        fetch('/static/txt/tts_languages.txt')  // or .html if you kept it as HTML
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.text();
            })
            .then(data => {
                console.log('Successfully loaded tts_languages.txt');
                const languageSelect = document.getElementById('language');
                if (languageSelect) {
                    languageSelect.innerHTML = data;
                    console.log('Populated language select');
                } else {
                    console.error('Language select element not found');
                }
            })
            .catch(error => {
                console.error('Error loading languages:', error);
                console.error('Error details:', error.message);
            });
    }

    function handleMessageSubmit(e) {
        e.preventDefault();
        sendBtn.textContent = 'Sending...';
        sendBtn.disabled = true;
        const message = document.getElementById('message').value;
        const language = document.getElementById('language').value;
        const selectedDevices = getSelectedDevices();
        const formData = new FormData();
        formData.append('message', message);
        formData.append('language', language);
        formData.append('volume', volumeValue);
        formData.append('devices', JSON.stringify(selectedDevices));
        axios.post('/api/send_message', formData)
            .then(response => {
                if (response.data.results) {
                    const messages = response.data.results.map(result =>
                        `${result.device}: ${result.status}${result.message ? ' - ' + result.message : ''}`
                    );
                    alert(messages.join('\n'));
                } else {
                    alert('Message sent!');
                }
            })
            .catch(error => {
                console.error('Error sending message:', error);
                alert('Failed to send message: ' + (error.response?.data?.message || 'Unknown error'));
            })
            .finally(() => {
                sendBtn.textContent = 'Send Message';
                sendBtn.disabled = false;
            });
    }

    function handleDiscoverDevices() {
        discoverBtn.textContent = 'Discovering...';
        discoverBtn.disabled = true;

        axios.post('/api/discover')
            .then(response => {
                alert('Device discovery is complete!');
                updateDeviceList();
            })
            .catch(error => {
                console.error('Error discovering devices:', error);
                alert(`Failed to discover devices: ${error.response?.data?.message || error.message || 'Unknown error'}`);
            })
            .finally(() => {
                discoverBtn.textContent = 'Discover Devices';
                discoverBtn.disabled = false;
            });
    }

    function handlePauseAll() {
        const selectedDevices = getSelectedDevices();
        if (selectedDevices.length === 0) {
            alert('Please select at least one device to pause.');
            return;
        }
        axios.post('/api/pause_audio', { devices: selectedDevices })
            .then(response => {
                if (response.data.status === "Error") {
                    alert(`Failed to pause message: ${response.data.message}`);
                } else {
                    alert('Message paused on selected devices.');
                }
            })
            .catch(error => {
                console.error('Error pausing message:', error);
                alert('Failed to pause message. Please try again.');
            });
    }

    function handleStopAll() {
        const selectedDevices = getSelectedDevices();
        if (selectedDevices.length === 0) {
            alert('Please select at least one device to stop.');
            return;
        }
        axios.post('/api/stop_audio', { devices: selectedDevices })
            .then(response => {
                if (response.data.status === "Error") {
                    alert(`Failed to stop message: ${response.data.message}`);
                } else {
                    alert('Message stopped on selected devices.');
                }
            })
            .catch(error => {
                console.error('Error stopping message:', error);
                alert('Failed to stop message. Please try again.');
            });
    }

    function getContentType(url) {
        const extension = url.split('.').pop().toLowerCase();
        if (!extension) {
            alert('Could not determine the file type. Please ensure the URL points to a valid media file.');
        }
        const contentTypes = {
            'mp4': 'video/mp4',
            'mp3': 'audio/mpeg',
            'wav': 'audio/wav',
            'ogg': 'audio/ogg',
            'webm': 'video/webm',
            'aac': 'audio/aac',
            'flac': 'audio/flac',
            'm4a': 'audio/mp4',
            'avi': 'video/x-msvideo',
            'mov': 'video/quicktime',
            'wmv': 'video/x-ms-wmv',
            'mpeg': 'video/mpeg',
            'mpg': 'video/mpeg',
            'jpg': 'image/jpeg',
            'jpeg': 'image/jpeg',
            'png': 'image/png',
            'gif': 'image/gif',
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
        return contentTypes[extension] || 'application/octet-stream';
    }

    async function handleStreamMedia() {
        const url = streamUrl.value.trim();
        if (!url) {
            alert('Please enter a valid streaming URL.');
            return;
        }

        const selectedDevices = getSelectedDevices();
        if (selectedDevices.length === 0) {
            alert('Please select at least one device.');
            return;
        }

        streamBtn.textContent = 'Streaming...';
        streamBtn.disabled = true;

        try {
            await determineContentTypeAndCast(url, selectedDevices);
            alert('Media streaming started!');
        } catch (error) {
            console.error('Error streaming media:', error);
            alert('Failed to start media streaming: ' + error.message);
        } finally {
            streamBtn.textContent = 'Stream Media';
            streamBtn.disabled = false;
        }
    }

    async function determineContentTypeAndCast(url, selectedDevices) {
        if (isYouTubeUrl(url)) {
            await castYouTubeVideo(url, selectedDevices);
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
                await castMedia(url, contentType, selectedDevices);
            } else {
                // If content-type header is not found, try guessing from URL
                const guessedType = guessMimeTypeFromUrl(url);
                if (guessedType) {
                    await castMedia(url, guessedType, selectedDevices);
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
                await castMedia(url, guessedType, selectedDevices);
            } else {
                throw new Error("Unable to determine content type");
            }
        }
    }

    function isYouTubeUrl(url) {
        return url.includes('youtube.com') || url.includes('youtu.be');
    }

    async function castYouTubeVideo(url, selectedDevices) {
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
            await castMedia(youtubeEmbedUrl, 'video/youtube', selectedDevices);
        } else {
            throw new Error("Unable to extract YouTube video ID");
        }
    }

    function guessMimeTypeFromUrl(url) {
        // Check for known CDN patterns first
        if (url.includes('cloudfront.net') && url.includes('_fullscreen')) {
            return 'image/jpeg';  // Assume JPEG for Bukowskis-like URLs
        }

        // Then check for file extensions
        return getContentType(url);
    }

    async function castMedia(mediaUrl, contentType, selectedDevices) {
        const formData = new FormData();
        formData.append('media_url', mediaUrl);
        formData.append('content_type', contentType);
        formData.append('volume', volumeValue);
        formData.append('devices', JSON.stringify(selectedDevices));

        try {
            const response = await axios.post('/api/stream_media', formData);
            console.log(response.data);
        } catch (error) {
            console.error('Error:', error);
            throw error;
        }
    }

    function handleAudioAction(action, url) {
        const file = audioFile.files[0];
        if (!file) {
            alert('Please select an audio file first.');
            return;
        }

        const selectedDevices = getSelectedDevices();
        if (selectedDevices.length === 0) {
            alert('Please select at least one device.');
            return;
        }

        console.log("Volume from button click", volumeValue);

        const formData = new FormData();
        formData.append('audio', file);
        formData.append('devices', JSON.stringify(selectedDevices));
        formData.append('volume', volumeValue);

        const button = action === 'play' ? playAudioBtn : streamBtn;
        button.textContent = `${action === 'play' ? 'Playing' : 'Streaming'}...`;
        button.disabled = true;

        axios.post(url, formData, {
            headers: {
                'Content-Type': 'multipart/form-data'
            }
        })
        .then(response => {
            console.log('Response:', response);
            if (response.data.results) {
                const messages = response.data.results.map(result => 
                    `${result.device}: ${result.status}${result.message ? ' - ' + result.message : ''}`
                );
                alert(messages.join('\n'));
            } else {
                alert(`Audio ${action} started!`);
            }
        })
        .catch(error => {
            console.error(`Error ${action}ing audio:`, error);
            if (error.response) {
                console.error('Response data:', error.response.data);
                console.error('Response status:', error.response.status);
                console.error('Response headers:', error.response.headers);
            } else if (error.request) {
                console.error('Request:', error.request);
            } else {
                console.error('Error message:', error.message);
            }
            alert(`Failed to start audio ${action}. ${error.response?.data?.message || error.message || 'Unknown error'}`);
        })
        .finally(() => {
            button.textContent = `${action === 'play' ? 'Play' : 'Stream'} Audio`;
            button.disabled = false;
        });
    }

    function handleVolumeChange(e) {
        volumeValue = e.target.value / 100;
        volumeValueSpan.textContent = `${e.target.value}%`;
    }
});