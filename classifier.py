"""
IT Helpdesk Ticket Classification Module

This module provides a reusable classifier for IT helpdesk tickets.
It can be imported and used in other Python applications.
"""

import os
import json
from typing import Dict, Any, Optional
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# System configuration
DELIMITER = "####"

SYSTEM_PROMPT = f"""
You are an expert IT helpdesk classification system. Your role is to analyze incoming support requests 
and classify them accurately into appropriate categories.

You must classify each request into:
1. A primary category
2. A specific subcategory
3. A priority level (Critical, High, Medium, Low)
4. A confidence level (high, medium, low)

PRIMARY CATEGORIES AND SUBCATEGORIES:

1. Hardware Issues
   - Desktop/Laptop problems
   - Peripheral devices
   - Mobile devices
   - Printer issues

2. Network & Connectivity
   - Wi-Fi/LAN issues
   - VPN problems
   - Internet connectivity
   - Network speed

3. Software & Applications
   - Application errors
   - Installation/Updates
   - License issues
   - Performance problems

4. Account & Access
   - Password reset
   - Account locked
   - Access permissions
   - New account creation

5. Security
   - Suspicious activity
   - Malware/Virus
   - Phishing reports
   - Security policy questions

6. Email & Communication
   - Email access issues
   - Calendar problems
   - Video conferencing
   - Shared folders

PRIORITY ASSIGNMENT RULES:

Critical:
- Complete system outages
- Security breaches or active malware
- Data loss occurring
- Multiple users affected simultaneously
- Business-critical services down
- Physical safety concerns (burning smell, sparks, etc.)

High:
- Single user completely unable to work
- Suspected malware/virus
- Account locked preventing work
- Critical application errors
- Data loss risk
- Email access issues

Medium:
- Workarounds available
- Non-urgent productivity issues
- Minor connectivity problems
- Peripheral device issues
- Password resets (when not preventing work)

Low:
- General questions
- Feature requests
- Minor inconveniences
- Information requests
- How-to questions

SPECIAL HANDLING:

For vague or ambiguous requests:
- Set confidence to "low"
- Provide clarifying questions in the response
- Make best guess based on available information

For multi-issue requests:
- Classify based on the most urgent/critical issue
- Mention additional issues in suggested_action

For urgent language (URGENT, ASAP, HELP):
- Consider but don't solely rely on it for priority
- Assess actual business impact

OUTPUT FORMAT:

Always respond with valid JSON in this exact structure:
{{
  "primary_category": "string",
  "subcategory": "string",
  "priority": "Critical|High|Medium|Low",
  "confidence": "high|medium|low",
  "suggested_action": "string",
  "estimated_resolution_time": "string",
  "clarifying_questions": ["string"] (only if confidence is low)
}}

The user request will be delimited with {DELIMITER} characters.
"""


class ITHelpdeskClassifier:
    """
    IT Helpdesk Ticket Classifier using OpenAI's API.
    """
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        model: str = "gpt-4o-mini",
        temperature: float = 0
    ):
        """
        Initialize the classifier.
        
        Args:
            api_key: OpenAI API key (defaults to API_KEY env var)
            base_url: API base URL (defaults to AI_URL env var or OpenAI default)
            model: Model to use for classification
            temperature: Sampling temperature (0 = deterministic)
        """
        self.api_key = api_key or os.environ.get("API_KEY")
        self.base_url = base_url or os.environ.get("AI_URL", "https://api.openai.com/v1")
        self.model = model
        self.temperature = temperature
        
        if not self.api_key:
            raise ValueError("API key must be provided or set in API_KEY environment variable")
        
        self.client = OpenAI(
            base_url=self.base_url,
            api_key=self.api_key
        )
    
    def classify(self, ticket_text: str) -> Dict[str, Any]:
        """
        Classify an IT helpdesk ticket.
        
        Args:
            ticket_text: The ticket description to classify
            
        Returns:
            Dictionary containing classification results
        """
        try:
            messages = [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"{DELIMITER}{ticket_text}{DELIMITER}"}
            ]
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=self.temperature,
                response_format={"type": "json_object"}
            )
            
            result = json.loads(response.choices[0].message.content)
            result['input'] = ticket_text
            result['model'] = self.model
            
            return result
            
        except Exception as e:
            return {
                "error": str(e),
                "input": ticket_text,
                "primary_category": "Error",
                "subcategory": "Classification failed",
                "priority": "Medium",
                "confidence": "low",
                "suggested_action": "Please try again or contact support"
            }
    
    def classify_batch(self, tickets: list) -> list:
        """
        Classify multiple tickets.
        
        Args:
            tickets: List of ticket descriptions
            
        Returns:
            List of classification results
        """
        return [self.classify(ticket) for ticket in tickets]


def classify_ticket(
    ticket_text: str,
    model: str = "gpt-4o-mini",
    temperature: float = 0
) -> Dict[str, Any]:
    """
    Convenience function to classify a single ticket.
    
    Args:
        ticket_text: The ticket description to classify
        model: Model to use for classification
        temperature: Sampling temperature
        
    Returns:
        Dictionary containing classification results
    """
    classifier = ITHelpdeskClassifier(model=model, temperature=temperature)
    return classifier.classify(ticket_text)


def format_result(result: Dict[str, Any]) -> str:
    """
    Format classification result as a readable string.
    
    Args:
        result: Classification result dictionary
        
    Returns:
        Formatted string representation
    """
    priority_emoji = {
        'Critical': '🔴',
        'High': '🟠',
        'Medium': '🟡',
        'Low': '🟢'
    }
    
    confidence_emoji = {
        'high': '✅',
        'medium': '⚠️',
        'low': '❓'
    }
    
    output = []
    output.append("="*60)
    output.append("📝 TICKET CLASSIFICATION RESULT")
    output.append("="*60)
    
    if 'error' in result:
        output.append(f"\n❌ Error: {result['error']}")
        return "\n".join(output)
    
    output.append(f"\n📋 Input: {result.get('input', 'N/A')}")
    output.append(f"\n🏷️  Category: {result.get('primary_category', 'N/A')}")
    output.append(f"📌 Subcategory: {result.get('subcategory', 'N/A')}")
    
    priority = result.get('priority', 'N/A')
    output.append(f"{priority_emoji.get(priority, '⚪')} Priority: {priority}")
    
    confidence = result.get('confidence', 'N/A')
    output.append(f"{confidence_emoji.get(confidence, '⚪')} Confidence: {confidence}")
    
    output.append(f"\n💡 Suggested Action: {result.get('suggested_action', 'N/A')}")
    
    if 'estimated_resolution_time' in result:
        output.append(f"⏱️  Estimated Resolution: {result['estimated_resolution_time']}")
    
    if 'clarifying_questions' in result and result['clarifying_questions']:
        output.append(f"\n❓ Clarifying Questions Needed:")
        for i, question in enumerate(result['clarifying_questions'], 1):
            output.append(f"   {i}. {question}")
    
    output.append("\n" + "="*60)
    
    return "\n".join(output)


# Example usage
if __name__ == "__main__":
    # Example 1: Using the convenience function
    result = classify_ticket("My laptop is not connecting to the office Wi-Fi.")
    print(format_result(result))
    
    # Example 2: Using the classifier class
    classifier = ITHelpdeskClassifier()
    
    tickets = [
        "I forgot my password and need to reset it.",
        "Microsoft Word keeps crashing.",
        "I received a suspicious email asking for my password."
    ]
    
    results = classifier.classify_batch(tickets)
    
    for i, result in enumerate(results, 1):
        print(f"\n\nTicket {i}:")
        print(format_result(result))
