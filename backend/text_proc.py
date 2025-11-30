from backend.processing import process_transcript

# Sample Indian meeting transcript
test_transcript = """
Hi everyone, this is Rajesh speaking. Thanks for joining today's call. 
Priya, can you give us an update on the project status?

Sure Rajesh ji. We've completed 80% of the development work. 
Amit and I reviewed the code yesterday, and we found a few bugs that need fixing.

Okay, Priya. Amit, can you fix those bugs by Friday?

Yes, I'll handle it. I'll also prepare the deployment checklist.

Great! Sneha, please schedule a demo with the client for next Tuesday.

Sure thing, I'll send the calendar invite today itself.

Perfect. So to summarize - Amit will fix bugs by Friday, 
Sneha will schedule client demo for next Tuesday, 
and we'll do final testing over the weekend. Meeting adjourned!
"""

result = process_transcript(test_transcript)

print("📝 SUMMARY:")
print(result['summary'])
print("\n✅ ACTION ITEMS:")
for item in result['action_items']:
    print(f"  - {item}")
print("\n👥 PARTICIPANTS:")
for person in result['participants']:
    print(f"  - {person}")
print("\n🎯 KEY DECISIONS:")
for decision in result['key_decisions']:
    print(f"  - {decision}")

from backend.transcription import transcribe_audio

audio_file = "sample_meeting.mp3"
transcript = transcribe_audio(audio_file)

print("📄 TRANSCRIPT:")
print(transcript)