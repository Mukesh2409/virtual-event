// Livestream functionality for virtual events

// Global variables
let eventId;
let streamActive = false;
let controlsTimeout;
let viewerCount = 0;
let isMuted = false;
let simulatedQuality = "720p"; // For mocked quality selector

// Initialize the livestream functionality
function initLivestream(id) {
    eventId = id;
    const videoContainer = document.getElementById('livestream-container');
    const mockVideo = document.getElementById('mock-video');
    const controlsOverlay = document.getElementById('stream-controls');
    const playButton = document.getElementById('play-button');
    const muteButton = document.getElementById('mute-button');
    const fullscreenButton = document.getElementById('fullscreen-button');
    const qualitySelector = document.getElementById('quality-selector');
    const viewerCounter = document.getElementById('viewer-count');
    
    if (!videoContainer || !mockVideo) {
        console.error('Livestream elements not found');
        return;
    }
    
    // Simulate stream loading
    simulateStreamLoading();
    
    // Handle play/pause
    if (playButton) {
        playButton.addEventListener('click', function() {
            togglePlayPause();
        });
        
        // Also allow clicking on the video to play/pause
        mockVideo.addEventListener('click', function() {
            togglePlayPause();
        });
    }
    
    // Handle mute/unmute
    if (muteButton) {
        muteButton.addEventListener('click', function() {
            toggleMute();
        });
    }
    
    // Handle fullscreen
    if (fullscreenButton) {
        fullscreenButton.addEventListener('click', function() {
            toggleFullscreen(videoContainer);
        });
    }
    
    // Handle quality selection
    if (qualitySelector) {
        qualitySelector.addEventListener('change', function() {
            changeQuality(this.value);
        });
    }
    
    // Show/hide controls on hover
    if (videoContainer && controlsOverlay) {
        videoContainer.addEventListener('mousemove', function() {
            showControls();
            clearTimeout(controlsTimeout);
            controlsTimeout = setTimeout(hideControls, 3000);
        });
        
        videoContainer.addEventListener('mouseleave', function() {
            hideControls();
        });
    }
    
    // Simulate viewer count updates
    if (viewerCounter) {
        simulateViewerCount();
        setInterval(simulateViewerCount, 10000);
    }
}

// Simulate stream loading
function simulateStreamLoading() {
    const mockVideo = document.getElementById('mock-video');
    const loadingIndicator = document.getElementById('loading-indicator');
    
    if (mockVideo && loadingIndicator) {
        // Show loading state
        loadingIndicator.style.display = 'flex';
        mockVideo.classList.add('opacity-50');
        
        // Simulate buffering
        setTimeout(function() {
            loadingIndicator.style.display = 'none';
            mockVideo.classList.remove('opacity-50');
            streamActive = true;
            
            // Update UI to reflect playing state
            const playButton = document.getElementById('play-button');
            if (playButton) {
                playButton.innerHTML = '<i class="fas fa-pause"></i>';
            }
        }, 2000);
    }
}

// Toggle play/pause
function togglePlayPause() {
    const playButton = document.getElementById('play-button');
    const mockVideo = document.getElementById('mock-video');
    const loadingIndicator = document.getElementById('loading-indicator');
    
    if (streamActive) {
        // Pause the "stream"
        streamActive = false;
        if (playButton) {
            playButton.innerHTML = '<i class="fas fa-play"></i>';
        }
        if (mockVideo) {
            mockVideo.classList.add('opacity-75');
        }
    } else {
        // Simulate short buffering
        if (loadingIndicator) {
            loadingIndicator.style.display = 'flex';
        }
        
        setTimeout(function() {
            streamActive = true;
            if (playButton) {
                playButton.innerHTML = '<i class="fas fa-pause"></i>';
            }
            if (mockVideo) {
                mockVideo.classList.remove('opacity-75');
            }
            if (loadingIndicator) {
                loadingIndicator.style.display = 'none';
            }
        }, 1000);
    }
}

// Toggle mute/unmute
function toggleMute() {
    const muteButton = document.getElementById('mute-button');
    isMuted = !isMuted;
    
    if (muteButton) {
        if (isMuted) {
            muteButton.innerHTML = '<i class="fas fa-volume-mute"></i>';
            // Would actually mute a real video here
        } else {
            muteButton.innerHTML = '<i class="fas fa-volume-up"></i>';
            // Would unmute a real video here
        }
    }
}

// Toggle fullscreen
function toggleFullscreen(element) {
    if (!document.fullscreenElement &&    // Standard property
        !document.mozFullScreenElement && // Firefox
        !document.webkitFullscreenElement && // Chrome, Safari and Opera
        !document.msFullscreenElement) {  // IE/Edge
        
        // Enter fullscreen
        if (element.requestFullscreen) {
            element.requestFullscreen();
        } else if (element.mozRequestFullScreen) {
            element.mozRequestFullScreen();
        } else if (element.webkitRequestFullscreen) {
            element.webkitRequestFullscreen();
        } else if (element.msRequestFullscreen) {
            element.msRequestFullscreen();
        }
    } else {
        // Exit fullscreen
        if (document.exitFullscreen) {
            document.exitFullscreen();
        } else if (document.mozCancelFullScreen) {
            document.mozCancelFullScreen();
        } else if (document.webkitExitFullscreen) {
            document.webkitExitFullscreen();
        } else if (document.msExitFullscreen) {
            document.msExitFullscreen();
        }
    }
}

// Change video quality (mock function)
function changeQuality(quality) {
    const qualityIndicator = document.getElementById('quality-indicator');
    
    simulatedQuality = quality;
    
    if (qualityIndicator) {
        qualityIndicator.textContent = quality;
    }
    
    // Simulate buffering when changing quality
    const loadingIndicator = document.getElementById('loading-indicator');
    const mockVideo = document.getElementById('mock-video');
    
    if (loadingIndicator && mockVideo) {
        loadingIndicator.style.display = 'flex';
        mockVideo.classList.add('opacity-50');
        
        setTimeout(function() {
            loadingIndicator.style.display = 'none';
            mockVideo.classList.remove('opacity-50');
        }, 1500);
    }
}

// Show stream controls
function showControls() {
    const controlsOverlay = document.getElementById('stream-controls');
    if (controlsOverlay) {
        controlsOverlay.classList.remove('opacity-0');
        controlsOverlay.classList.add('opacity-100');
    }
}

// Hide stream controls
function hideControls() {
    const controlsOverlay = document.getElementById('stream-controls');
    if (controlsOverlay) {
        controlsOverlay.classList.remove('opacity-100');
        controlsOverlay.classList.add('opacity-0');
    }
}

// Simulate viewer count (for demonstration purposes)
function simulateViewerCount() {
    const viewerCounter = document.getElementById('viewer-count');
    
    // Generate a random change in viewer count (-5 to +10)
    const change = Math.floor(Math.random() * 16) - 5;
    viewerCount = Math.max(10, viewerCount + change);
    
    if (viewerCounter) {
        viewerCounter.textContent = viewerCount;
    }
}

// Add stream reaction (like, heart, etc.)
function addStreamReaction(type) {
    const streamContainer = document.getElementById('livestream-container');
    
    if (!streamContainer) return;
    
    const reaction = document.createElement('div');
    reaction.className = 'absolute text-3xl pointer-events-none animate-reaction';
    
    // Set random position at the bottom of the container
    const randomX = Math.floor(Math.random() * 90) + 5; // 5% to 95% width
    reaction.style.left = `${randomX}%`;
    reaction.style.bottom = '10%';
    
    // Set icon based on reaction type
    switch(type) {
        case 'like':
            reaction.innerHTML = '<i class="fas fa-thumbs-up text-blue-500"></i>';
            break;
        case 'heart':
            reaction.innerHTML = '<i class="fas fa-heart text-red-500"></i>';
            break;
        case 'laugh':
            reaction.innerHTML = '<i class="fas fa-laugh text-yellow-500"></i>';
            break;
        case 'clap':
            reaction.innerHTML = '<i class="fas fa-hands-clapping text-green-500"></i>';
            break;
        default:
            reaction.innerHTML = '<i class="fas fa-star text-purple-500"></i>';
    }
    
    streamContainer.appendChild(reaction);
    
    // Remove the element after animation completes
    setTimeout(() => {
        streamContainer.removeChild(reaction);
    }, 3000);
}

// Simulate stream error
function simulateStreamError() {
    const mockVideo = document.getElementById('mock-video');
    const errorOverlay = document.getElementById('error-overlay');
    
    if (mockVideo && errorOverlay) {
        mockVideo.classList.add('opacity-50');
        errorOverlay.classList.remove('hidden');
        
        // Auto-retry after 5 seconds
        setTimeout(function() {
            mockVideo.classList.remove('opacity-50');
            errorOverlay.classList.add('hidden');
        }, 5000);
    }
}

// CSS Animation for reactions
document.addEventListener('DOMContentLoaded', function() {
    // Add the reaction animation CSS if it doesn't exist
    if (!document.getElementById('reaction-animation-css')) {
        const style = document.createElement('style');
        style.id = 'reaction-animation-css';
        style.textContent = `
            @keyframes float-up {
                0% {
                    transform: translateY(0) scale(1);
                    opacity: 1;
                }
                100% {
                    transform: translateY(-100px) scale(1.5);
                    opacity: 0;
                }
            }
            .animate-reaction {
                animation: float-up 3s ease-out forwards;
            }
        `;
        document.head.appendChild(style);
    }
    
    // Add event listeners for reaction buttons
    const reactionButtons = document.querySelectorAll('.reaction-button');
    reactionButtons.forEach(button => {
        button.addEventListener('click', function() {
            const reactionType = this.dataset.reaction;
            addStreamReaction(reactionType);
        });
    });
});
