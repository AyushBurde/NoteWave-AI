import os
import requests
from dotenv import load_dotenv

load_dotenv()

DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")

def transcribe_audio(audio_file_path: str) -> str:
    """
    Transcribe audio using Deepgram REST API directly (FREE!)
    This bypasses SDK version issues
    """
    try:
        print(f"🎤 Starting Deepgram transcription...")
        
        # Read audio file
        with open(audio_file_path, "rb") as audio_file:
            audio_data = audio_file.read()
        
        print(f"📦 Audio size: {len(audio_data)} bytes")
        
        # Deepgram API endpoint
        url = "https://api.deepgram.com/v1/listen"
        
        # Parameters optimized for Indian English
        params = {
            "model": "nova-2",
            "language": "en",
            "smart_format": "true",
            "punctuate": "true",
            "paragraphs": "true",
            "diarize": "true",
            "filler_words": "false"
        }
        
        # Headers
        headers = {
            "Authorization": f"Token {DEEPGRAM_API_KEY}",
            "Content-Type": "audio/wav"  # Will work for most audio formats
        }
        
        print("🚀 Sending to Deepgram API...")
        
        # Make request
        response = requests.post(
            url,
            params=params,
            headers=headers,
            data=audio_data,
            timeout=120  # 2 minute timeout
        )
        
        if response.status_code != 200:
            raise Exception(f"Deepgram API error: {response.status_code} - {response.text}")
        
        result = response.json()
        
        # Extract transcript
        transcript = result['results']['channels'][0]['alternatives'][0]['transcript']
        
        print(f"✅ Transcription complete! Length: {len(transcript)} characters")
        
        return transcript
        
    except Exception as e:
        print(f"❌ Transcription error: {str(e)}")
        import traceback
        traceback.print_exc()
        raise Exception(f"Failed to transcribe audio: {str(e)}")


def transcribe_with_speakers(audio_file_path: str) -> dict:
    """
    Get transcription with speaker identification
    """
    try:
        with open(audio_file_path, "rb") as audio_file:
            audio_data = audio_file.read()
        
        url = "https://api.deepgram.com/v1/listen"
        params = {
            "model": "nova-2",
            "language": "en",
            "smart_format": "true",
            "punctuate": "true",
            "diarize": "true",
            "utterances": "true"
        }
        
        headers = {
            "Authorization": f"Token {DEEPGRAM_API_KEY}",
            "Content-Type": "audio/wav"
        }
        
        response = requests.post(url, params=params, headers=headers, data=audio_data, timeout=120)
        result = response.json()
        
        # Extract speaker info
        utterances = result.get('results', {}).get('utterances', [])
        speaker_transcript = []
        
        for utterance in utterances:
            speaker_transcript.append({
                'speaker': f"Speaker {utterance.get('speaker', 'Unknown')}",
                'text': utterance.get('transcript', ''),
                'start': utterance.get('start', 0),
                'end': utterance.get('end', 0)
            })
        
        full_transcript = result['results']['channels'][0]['alternatives'][0]['transcript']
        
        return {
            'full_transcript': full_transcript,
            'speakers': speaker_transcript
        }
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        raise Exception(f"Failed to transcribe: {str(e)}")