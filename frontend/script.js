const API_URL = 'http://localhost:8000';
// Real-Time Recording Variables
let mediaRecorder;
let audioChunks = [];
let recordingStartTime;
let timerInterval;

// Recording Functions
const startRecordBtn = document.getElementById('startRecordBtn');
const stopRecordBtn = document.getElementById('stopRecordBtn');
const recordingTimer = document.getElementById('recordingTimer');
const timerText = document.getElementById('timerText');
const recordingWave = document.getElementById('recordingWave');

startRecordBtn.addEventListener('click', startRecording);
stopRecordBtn.addEventListener('click', stopRecording);

async function startRecording() {
    try {
        // Request microphone access
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        
        // Create media recorder
        mediaRecorder = new MediaRecorder(stream);
        audioChunks = [];
        
        mediaRecorder.ondataavailable = (event) => {
            audioChunks.push(event.data);
        };
        
        mediaRecorder.onstop = async () => {
            // Stop all tracks
            stream.getTracks().forEach(track => track.stop());
            
            // Create audio blob
            const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
            
            // Convert to file
            const audioFile = new File([audioBlob], `recording-${Date.now()}.webm`, {
                type: 'audio/webm'
            });
            
            // Auto-process the recording
            await processRecordedAudio(audioFile);
        };
        
        // Start recording
        mediaRecorder.start();
        recordingStartTime = Date.now();
        
        // Update UI
        startRecordBtn.style.display = 'none';
        stopRecordBtn.style.display = 'flex';
        recordingTimer.style.display = 'flex';
        recordingWave.style.display = 'flex';
        
        // Start timer
        timerInterval = setInterval(updateTimer, 1000);
        
        console.log('🎙️ Recording started!');
        
    } catch (error) {
        console.error('Error accessing microphone:', error);
        alert('Could not access microphone. Please grant permission and try again.');
    }
}

function stopRecording() {
    if (mediaRecorder && mediaRecorder.state !== 'inactive') {
        mediaRecorder.stop();
        
        // Update UI
        startRecordBtn.style.display = 'flex';
        stopRecordBtn.style.display = 'none';
        recordingTimer.style.display = 'none';
        recordingWave.style.display = 'none';
        
        // Stop timer
        clearInterval(timerInterval);
        timerText.textContent = '00:00';
        
        console.log('⏹️ Recording stopped!');
    }
}

function updateTimer() {
    const elapsed = Math.floor((Date.now() - recordingStartTime) / 1000);
    const minutes = Math.floor(elapsed / 60);
    const seconds = elapsed % 60;
    timerText.textContent = `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
}

async function processRecordedAudio(audioFile) {
    // Hide recording section, show loading
    document.querySelector('.recording-section').style.display = 'none';
    document.querySelector('.upload-section').style.display = 'none';
    resultsSection.style.display = 'none';
    loadingSection.style.display = 'block';
    
    try {
        loadingText.textContent = 'Processing your recording...';
        
        const formData = new FormData();
        formData.append('file', audioFile);
        
        loadingText.textContent = 'Transcribing (this may take 1-2 minutes)...';
        
        const response = await fetch(`${API_URL}/upload-audio`, {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            throw new Error('Failed to process recording');
        }
        
        loadingText.textContent = 'Extracting insights...';
        
        const result = await response.json();
        currentResults = result;
        
        // Display results
        displayResults(result);
        
    } catch (error) {
        console.error('Error:', error);
        alert('Failed to process recording. Please try again.');
        resetUI();
    }
}

let selectedFile = null;
let currentResults = null;

// DOM Elements
const uploadArea = document.getElementById('uploadArea');
const audioFile = document.getElementById('audioFile');
const processBtn = document.getElementById('processBtn');
const loadingSection = document.getElementById('loadingSection');
const resultsSection = document.getElementById('resultsSection');
const loadingText = document.getElementById('loadingText');

// Upload area interactions
uploadArea.addEventListener('click', () => {
    audioFile.click();
});

uploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadArea.classList.add('active');
});

uploadArea.addEventListener('dragleave', () => {
    uploadArea.classList.remove('active');
});

uploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadArea.classList.remove('active');
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        handleFileSelect(files[0]);
    }
});

audioFile.addEventListener('change', (e) => {
    if (e.target.files.length > 0) {
        handleFileSelect(e.target.files[0]);
    }
});

function handleFileSelect(file) {
    // Validate file type
    const validTypes = ['audio/mpeg', 'audio/wav', 'audio/mp4', 'audio/webm', 'audio/m4a'];
    if (!validTypes.includes(file.type) && !file.name.match(/\.(mp3|wav|m4a|webm)$/i)) {
        alert('Please select a valid audio file (MP3, WAV, M4A, WebM)');
        return;
    }
    
    // Validate file size (25MB limit)
    if (file.size > 25 * 1024 * 1024) {
        alert('File size must be less than 25MB');
        return;
    }
    
    selectedFile = file;
    uploadArea.querySelector('p').textContent = `Selected: ${file.name}`;
    processBtn.disabled = false;
}

// Process meeting
processBtn.addEventListener('click', async () => {
    if (!selectedFile) return;
    
    // Hide upload section, show loading
    document.querySelector('.upload-section').style.display = 'none';
    resultsSection.style.display = 'none';
    loadingSection.style.display = 'block';
    
    try {
        // Upload and process
        loadingText.textContent = 'Uploading audio file...';
        
        const formData = new FormData();
        formData.append('file', selectedFile);
        
        loadingText.textContent = 'Transcribing (this may take 1-2 minutes)...';
        
        const response = await fetch(`${API_URL}/upload-audio`, {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            throw new Error('Failed to process audio');
        }
        
        loadingText.textContent = 'Extracting insights...';
        
        const result = await response.json();
        currentResults = result;
        
        // Display results
        displayResults(result);
        
    } catch (error) {
        console.error('Error:', error);
        alert('Failed to process meeting. Please try again.');
        resetUI();
    }
});

function displayResults(result) {
    loadingSection.style.display = 'none';
    resultsSection.style.display = 'block';
    
    // Summary
    document.getElementById('summaryContent').innerHTML = `<p>${result.summary}</p>`;
    
    // Action Items
    if (result.action_items && result.action_items.length > 0) {
        const actionItemsHTML = '<ul>' + result.action_items.map(item => 
            `<li>${item}</li>`
        ).join('') + '</ul>';
        document.getElementById('actionItemsContent').innerHTML = actionItemsHTML;
    } else {
        document.getElementById('actionItemsContent').innerHTML = '<p>No action items identified</p>';
    }
    
    // Participants
    if (result.participants && result.participants.length > 0) {
        const participantsHTML = '<ul>' + result.participants.map(participant => 
            `<li>${participant}</li>`
        ).join('') + '</ul>';
        document.getElementById('participantsContent').innerHTML = participantsHTML;
    } else {
        document.getElementById('participantsContent').innerHTML = '<p>No participants identified</p>';
    }
    
    // Key Decisions
    if (result.key_decisions && result.key_decisions.length > 0) {
        const decisionsHTML = '<ul>' + result.key_decisions.map(decision => 
            `<li>${decision}</li>`
        ).join('') + '</ul>';
        document.getElementById('decisionsContent').innerHTML = decisionsHTML;
    } else {
        document.getElementById('decisionsContent').innerHTML = '<p>No key decisions identified</p>';
    }
    
    // Transcript
    document.getElementById('transcriptContent').innerHTML = `<p>${result.transcript}</p>`;
}

// Export functions
document.getElementById('exportTxtBtn').addEventListener('click', () => {
    if (!currentResults) return;
    
    const text = `
INDIANMEET AI - MEETING NOTES
==============================

SUMMARY:
${currentResults.summary}

ACTION ITEMS:
${currentResults.action_items.map(item => `- ${item}`).join('\n')}

PARTICIPANTS:
${currentResults.participants.map(p => `- ${p}`).join('\n')}

KEY DECISIONS:
${currentResults.key_decisions ? currentResults.key_decisions.map(d => `- ${d}`).join('\n') : 'None'}

FULL TRANSCRIPT:
${currentResults.transcript}
    `;
    
    const blob = new Blob([text], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `meeting-notes-${Date.now()}.txt`;
    a.click();
});

document.getElementById('exportPdfBtn').addEventListener('click', () => {
    alert('PDF export feature coming soon! For now, use the Text export option.');
});

document.getElementById('newMeetingBtn').addEventListener('click', () => {
    resetUI();
});

function resetUI() {
    selectedFile = null;
    currentResults = null;
    audioFile.value = '';
    uploadArea.querySelector('p').textContent = 'Drop audio file here or click to browse';
    processBtn.disabled = true;
    document.querySelector('.recording-section').style.display = 'block';
    document.querySelector('.upload-section').style.display = 'block';
    loadingSection.style.display = 'none';
    resultsSection.style.display = 'none';
}