import os
from groq import Groq
from dotenv import load_dotenv
import re

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)

def process_transcript(transcript: str) -> dict:
    """
    Process transcript using Groq + Llama 3 (FREE!)
    Optimized for Indian business meetings
    """
    
    # Create specialized prompt for Indian context
    prompt = f"""You are an expert meeting assistant specialized in analyzing Indian business meetings. You understand Indian English, Hinglish (Hindi-English mix), and Indian names perfectly.

TRANSCRIPT:
{transcript}

Analyze this meeting transcript and provide:

1. SUMMARY: Write a concise 3-4 sentence summary of the key discussion points and outcomes.

2. ACTION ITEMS: Extract all tasks, action items, or to-dos mentioned. Format each as:
   - [Person's Name]: [Specific task/action] - [Deadline/timeframe if mentioned]
   
   Examples:
   - Rajesh: Complete the project report by Friday
   - Priya: Schedule follow-up meeting with client next week
   - Team: Review the proposal and provide feedback

3. PARTICIPANTS: List all participant names mentioned in the conversation. Common Indian names include Rajesh, Priya, Amit, Sneha, Arjun, Rohan, Neha, Vikram, Ananya, etc.

4. KEY DECISIONS: List any important decisions, conclusions, or agreements reached during the meeting.

IMPORTANT NOTES:
- Understand that "ji" is a respectful suffix (e.g., "Amit ji" = "Mr. Amit")
- Recognize Hindi words mixed in English (Hinglish)
- Be accurate with Indian names and their various spellings
- If no specific items found in a category, write "None identified"

Format your response EXACTLY like this:

SUMMARY:
[Your 3-4 sentence summary here]

ACTION ITEMS:
- [Action item 1]
- [Action item 2]
(or write "None identified" if no action items)

PARTICIPANTS:
- [Name 1]
- [Name 2]
(or write "None identified" if no clear participants)

KEY DECISIONS:
- [Decision 1]
- [Decision 2]
(or write "None identified" if no key decisions)"""

    try:
        # Call Groq API with Llama 3.3
        print("🤖 Processing with Llama 3.3...")
        
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert meeting assistant who specializes in Indian business contexts. You understand Indian English accents, Hinglish, and Indian names perfectly. You provide accurate, well-formatted meeting summaries."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            model="llama-3.3-70b-versatile",  # UPDATED MODEL ✅
            temperature=0.3,
            max_tokens=2000,
            top_p=0.9,
        )
        
        result_text = chat_completion.choices[0].message.content
        
        print("✅ Processing complete!")
        
        # Parse the response
        parsed_result = parse_ai_response(result_text)
        
        return parsed_result
        
    except Exception as e:
        print(f"❌ Processing error: {str(e)}")
        import traceback
        traceback.print_exc()
        raise Exception(f"Failed to process transcript: {str(e)}")


def parse_ai_response(response_text: str) -> dict:
    """
    Parse the AI response into structured format
    """
    result = {
        "summary": "",
        "action_items": [],
        "participants": [],
        "key_decisions": []
    }
    
    try:
        # Extract SUMMARY
        summary_match = re.search(
            r'SUMMARY:\s*(.*?)(?=ACTION ITEMS:|PARTICIPANTS:|KEY DECISIONS:|$)', 
            response_text, 
            re.DOTALL | re.IGNORECASE
        )
        if summary_match:
            result["summary"] = summary_match.group(1).strip()
        
        # Extract ACTION ITEMS
        action_items_match = re.search(
            r'ACTION ITEMS:\s*(.*?)(?=PARTICIPANTS:|KEY DECISIONS:|$)', 
            response_text, 
            re.DOTALL | re.IGNORECASE
        )
        if action_items_match:
            items_text = action_items_match.group(1).strip()
            if "none identified" not in items_text.lower():
                items = items_text.split('\n')
                result["action_items"] = [
                    item.strip('- ').strip() 
                    for item in items 
                    if item.strip() and item.strip() != '-'
                ]
        
        # Extract PARTICIPANTS
        participants_match = re.search(
            r'PARTICIPANTS:\s*(.*?)(?=KEY DECISIONS:|$)', 
            response_text, 
            re.DOTALL | re.IGNORECASE
        )
        if participants_match:
            participants_text = participants_match.group(1).strip()
            if "none identified" not in participants_text.lower():
                participants = participants_text.split('\n')
                result["participants"] = [
                    p.strip('- ').strip() 
                    for p in participants 
                    if p.strip() and p.strip() != '-'
                ]
        
        # Extract KEY DECISIONS
        decisions_match = re.search(
            r'KEY DECISIONS:\s*(.*?)$', 
            response_text, 
            re.DOTALL | re.IGNORECASE
        )
        if decisions_match:
            decisions_text = decisions_match.group(1).strip()
            if "none identified" not in decisions_text.lower():
                decisions = decisions_text.split('\n')
                result["key_decisions"] = [
                    d.strip('- ').strip() 
                    for d in decisions 
                    if d.strip() and d.strip() != '-'
                ]
        
        return result
        
    except Exception as e:
        print(f"⚠️ Parsing warning: {str(e)}")
        # Return whatever we managed to extract
        return result


def quick_summary(transcript: str) -> str:
    """
    Generate a quick one-line summary (useful for testing)
    """
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": f"Summarize this meeting in one sentence:\n\n{transcript[:2000]}"
                }
            ],
            model="llama-3.3-70b-versatile",  # UPDATED MODEL ✅
            temperature=0.5,
            max_tokens=100,
        )
        
        return chat_completion.choices[0].message.content
        
    except Exception as e:
        return f"Error generating summary: {str(e)}"