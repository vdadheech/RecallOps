import os
import json
from groq import Groq
from dotenv import load_dotenv

# Ensure environment variables are loaded
load_dotenv()

def get_groq_client():
    """l
    Returns an initialized Groq client. Raises ValueError if api key is missing.
    """
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY is not set in environment variables.")
    return Groq(api_key=api_key)

def extract_structure(raw_text: str) -> dict:
    """
    Extracts structured incident data from messy text using Groq LLM.
    Returns a dictionary with keys:
    - service_affected
    - symptom_pattern
    - root_cause
    - fix_applied
    - time_to_resolve_minutes (int)
    """
    client = get_groq_client()
    system_prompt = (
        "You are an expert site reliability engineer (SRE). Your task is to analyze raw, messy incident notes, "
        "Slack threads, or post-mortem text and extract structured incident information. "
        "You MUST return a JSON object with the following keys:\n"
        "- service_affected: Name of the microservice or component affected (string)\n"
        "- symptom_pattern: High-level symptom pattern (string)\n"
        "- root_cause: Detailed root cause of the incident (string)\n"
        "- fix_applied: The fix applied to resolve the incident (string)\n"
        "- time_to_resolve_minutes: The duration of the incident in minutes (must be an integer, default to 0 if not found)\n\n"
        "Do not include any chat filler, markdown formatting, or notes outside the JSON object. Output ONLY valid JSON."
    )
    
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Raw incident notes:\n{raw_text}"}
        ],
        response_format={"type": "json_object"},
        temperature=0.1
    )
    
    response_text = response.choices[0].message.content
    try:
        data = json.loads(response_text)
        # Validate and clean up data types
        data["time_to_resolve_minutes"] = int(data.get("time_to_resolve_minutes", 0))
        return data
    except (json.JSONDecodeError, ValueError) as e:
        return {
            "service_affected": "Unknown",
            "symptom_pattern": "Failed to parse LLM response",
            "root_cause": f"JSON decode error: {str(e)}",
            "fix_applied": "Manual inspection required",
            "time_to_resolve_minutes": 0,
            "raw_response": response_text
        }

def generate_triage_brief(alert_text: str, similar_incidents: list) -> str:
    """
    Synthesizes similar incidents into an actionable brief for an incoming alert.
    """
    client = get_groq_client()
    
    # Format the similar incidents for the prompt context
    incidents_context = ""
    for idx, inc in enumerate(similar_incidents, 1):
        content_val = inc.get("content", "")
        relevance = inc.get("relevance_score", 0.0)
        incidents_context += f"--- Incident #{idx} (Relevance: {relevance:.2f}) ---\n{content_val}\n\n"
        
    system_prompt = (
        "You are an expert SRE triage agent. You are given an incoming alert and a list of historical "
        "incidents that are semantically similar. Your job is to analyze this context and generate a "
        "concise, highly actionable triage brief in Markdown.\n\n"
        "The brief should contain:\n"
        "1. **Analysis**: Why this alert is firing, comparing it to the historical incidents.\n"
        "2. **Most Likely Cause**: A clear hypothesis of the root cause.\n"
        "3. **Recommended Actions**: Step-by-step instructions on what the engineer should check or do immediately to fix the issue.\n\n"
        "Be extremely direct, professional, and practical. Avoid hand-wavy advice."
    )
    
    user_content = (
        f"Incoming Alert:\n{alert_text}\n\n"
        f"Similar Historical Incidents in Memory:\n{incidents_context}"
    )
    
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content}
        ],
        temperature=0.3
    )
    
    return response.choices[0].message.content
