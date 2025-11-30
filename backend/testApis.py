import os
from dotenv import load_dotenv

load_dotenv()

print("🔍 Testing API Keys...\n")

# Test 1: Check if .env is loaded
deepgram_key = os.getenv("DEEPGRAM_API_KEY")
groq_key = os.getenv("GROQ_API_KEY")

if deepgram_key:
    print(f"✅ Deepgram API Key found: {deepgram_key[:20]}...")
else:
    print("❌ Deepgram API Key NOT found!")

if groq_key:
    print(f"✅ Groq API Key found: {groq_key[:20]}...")
else:
    print("❌ Groq API Key NOT found!")

print("\n" + "="*50 + "\n")

# Test 2: Test Groq API (Processing)
print("🤖 Testing Groq API (AI Processing)...\n")

try:
    from backend.processing import process_transcript
    
    test_text = """
    Hi everyone, this is Rajesh. Priya, can you send the report by Friday?
    Yes Rajesh ji, I'll send it. Amit will help me with the data analysis.
    """
    
    result = process_transcript(test_text)
    
    print("✅ Groq API Working!\n")
    print(f"Summary: {result['summary']}")
    print(f"Action Items: {result['action_items']}")
    print(f"Participants: {result['participants']}")
    
except Exception as e:
    print(f"❌ Groq API Error: {str(e)}")

print("\n" + "="*50 + "\n")

# Test 3: Test Deepgram API (Transcription)
print("🎤 Testing Deepgram API (Transcription)...\n")
print("⚠️ This needs an actual audio file to test.")
print("We'll test this in the full app.\n")

print("="*50)
print("\n✅ Basic API tests complete!")
print("If you see ✅ above, you're ready to run the full app!\n")