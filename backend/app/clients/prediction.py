import os
import json
from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field
import requests
from dotenv import load_dotenv

load_dotenv()

class EvidenceItem(BaseModel):
    text: str
    relevance: str
    strength: str

class WinLikelihoodResponse(BaseModel):
    win_likelihood_percent: float = Field(description="Likelihood of winning the case as a percentage")
    explanation: str = Field(description="Detailed explanation of the win likelihood assessment")
    key_factors: List[Dict[str, str]] = Field(description="Key factors affecting the win likelihood")
    defense_arguments: List[str] = Field(description="Recommended lines of argument against the plaintiff")

def predict_case_win_likelihood(
    evidence: List[Dict[str, str]],
    plaintiff_argumentation: List[str],
    court_jurisdiction: str,
    state_jurisdiction: str,
    timeline_events: List[Dict[str, str]],
    case_type: str,
    harm_type: str,
    cause: str
) -> WinLikelihoodResponse:
    """
    Predicts the likelihood of winning a case based on evidence, plaintiff's argumentation,
    court information, and timeline events using Azure OpenAI's o3-mini model.
    
    Args:
        evidence: List of evidence items with text, relevance, and strength
        plaintiff_argumentation: List of plaintiff's key arguments
        court_jurisdiction: The court jurisdiction handling the case
        state_jurisdiction: The state jurisdiction for the case
        timeline_events: List of timeline events with dates and descriptions
        case_type: The primary legal case type
        harm_type: The type of harm caused
        cause: The specific cause of the harm
        
    Returns:
        WinLikelihoodResponse: Structured response with win likelihood percentage and explanation
    """
    # Azure OpenAI API configuration for o3-mini
    api_key = os.environ.get("AZURE_OPENAI_API_KEY")
    endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT")
    o3_mini_deployment = os.environ.get("AZURE_OPENAI_O3_MINI_DEPLOYMENT", "o3-mini")
    api_version = os.environ.get("AZURE_OPENAI_API_VERSION", "2023-12-01-preview")
    
    if not api_key or not endpoint:
        raise ValueError("Azure OpenAI API key and endpoint must be set as environment variables")
    
    # Format the evidence for the prompt
    evidence_text = ""
    for i, item in enumerate(evidence, 1):
        evidence_text += f"Evidence {i}:\n"
        evidence_text += f"- Text: {item.get('text', '')}\n"
        evidence_text += f"- Relevance: {item.get('relevance', '')}\n"
        evidence_text += f"- Strength: {item.get('strength', '')}\n\n"
    
    # Format plaintiff argumentation
    plaintiff_args = "\n".join([f"- {arg}" for arg in plaintiff_argumentation])
    
    # Format timeline events
    timeline_text = ""
    for event in timeline_events:
        date = event.get('date', 'Unknown')
        event_desc = event.get('event', '')
        timeline_text += f"- {date}: {event_desc}\n"
    
    # Prepare the prompt for o3-mini
    prompt = f"""
    As a legal expert representing the defense, analyze this case and predict the likelihood of winning (as a percentage) based on the following information:

    CASE OVERVIEW:
    - Case Type: {case_type}
    - Harm Type: {harm_type}
    - Cause: {cause}
    - Court Jurisdiction: {court_jurisdiction}
    - State Jurisdiction: {state_jurisdiction}

    EVIDENCE:
    {evidence_text}

    PLAINTIFF'S ARGUMENTATION:
    {plaintiff_args}

    TIMELINE OF EVENTS:
    {timeline_text}

    Based on the above information, provide:
    1. A specific percentage representing the likelihood of winning this case from the defense perspective (e.g., 65%)
    2. A concise explanation of your assessment (2-3 sentences)
    3. Three key factors that influenced your assessment (positive and negative)
    4. Three specific lines of argument against the plaintiff's case (focus on weaknesses in their evidence and arguments)

    Consider:
    - Weaknesses in the plaintiff's evidence
    - Potential alternative causes for the harm
    - Procedural or jurisdictional issues
    - Timeline inconsistencies

    Return your analysis in this JSON structure:
    {{
      "win_likelihood_percent": 75.5,
      "explanation": "Concise explanation of the win likelihood assessment...",
      "key_factors": [
        {{
          "factor": "Weak causal connection in evidence",
          "impact": "positive for defense"
        }},
        {{
          "factor": "Strong documentary evidence from plaintiff",
          "impact": "negative for defense"
        }},
        {{
          "factor": "Jurisdiction typically favors defendants in similar cases",
          "impact": "positive for defense"
        }}
      ],
      "defense_arguments": [
        "Challenge causation by presenting alternative explanations for the harm",
        "Argue contributory negligence based on plaintiff's actions",
        "Question the admissibility of key evidence due to chain of custody issues"
      ]
    }}
    """

    try:
        # Prepare the API request
        headers = {
            "Content-Type": "application/json",
            "api-key": api_key
        }
        
        # Azure OpenAI API request body
        request_body = {
            "messages": [
                {"role": "system", "content": "You are a legal analysis assistant specializing in defense strategy."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.2,
            "response_format": {"type": "json_object"}
        }
        
        # Make the API request to Azure OpenAI o3-mini
        response = requests.post(
            f"{endpoint}",
            headers=headers,
            json=request_body
        )
        
        response.raise_for_status()
        result = response.json()
        
        # Extract the generated content from Azure OpenAI response
        generated_text = result["choices"][0]["message"]["content"]
        
        # Parse the JSON response
        try:
            prediction = json.loads(generated_text)
            return WinLikelihoodResponse(**prediction)
        except json.JSONDecodeError:
            # If direct parsing fails, try to extract JSON from the text
            import re
            json_match = re.search(r'(\{.*\})', generated_text, re.DOTALL)
            if json_match:
                prediction = json.loads(json_match.group(1))
                return WinLikelihoodResponse(**prediction)
            else:
                raise ValueError("Could not extract valid JSON from model response")
                
    except Exception as e:
        print(f"Error calling Azure OpenAI o3-mini API: {e}")
        return WinLikelihoodResponse(
            win_likelihood_percent=50.0,
            explanation=f"Error in prediction: {str(e)}",
            key_factors=[{"factor": "Error in analysis", "impact": "negative"}],
            defense_arguments=["Review case data and try again"]
        )

def generate_defense_reasoning(
    evidence: List[Dict[str, str]],
    plaintiff_argumentation: List[str],
    case_type: str,
    harm_type: str,
    cause: str,
    defense_arguments: List[str]
) -> str:
    """
    Generates detailed reasoning for defense arguments using Azure OpenAI's o3-mini model.
    Returns the reasoning as a formatted string.
    
    Args:
        evidence: List of evidence items
        plaintiff_argumentation: List of plaintiff's arguments
        case_type: The primary legal case type
        harm_type: The type of harm caused
        cause: The specific cause of the harm
        defense_arguments: List of defense arguments to elaborate on
        
    Returns:
        str: Formatted string with defense arguments and reasoning
    """
    # Azure OpenAI API configuration for o3-mini
    api_key = os.environ.get("AZURE_OPENAI_API_KEY")
    endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT")
    
    if not api_key or not endpoint:
        raise ValueError("Azure OpenAI API key and endpoint must be set as environment variables")
    
    # Format the evidence for the prompt
    evidence_text = ""
    for i, item in enumerate(evidence, 1):
        evidence_text += f"Evidence {i}: {item.get('text', '')}\n"
    
    # Format plaintiff argumentation
    plaintiff_args = "\n".join([f"- {arg}" for arg in plaintiff_argumentation])
    
    # Format defense arguments
    defense_args = "\n".join([f"- {arg}" for arg in defense_arguments])
    
    # Prepare the prompt for o3-mini
    prompt = f"""
    As a legal expert, provide concise reasoning for each of these defense arguments:

    CASE OVERVIEW:
    - Case Type: {case_type}
    - Harm Type: {harm_type}
    - Cause: {cause}

    PLAINTIFF'S EVIDENCE SUMMARY:
    {evidence_text}

    PLAINTIFF'S ARGUMENTS:
    {plaintiff_args}

    DEFENSE ARGUMENTS TO ELABORATE:
    {defense_args}

    For each defense argument, provide:
    1. Brief legal reasoning (1-2 sentences)
    2. Which specific plaintiff claim this counters

    Return your analysis as a formatted text with each argument and its reasoning clearly separated.
    """

    try:
        # Prepare the API request
        headers = {
            "Content-Type": "application/json",
            "api-key": api_key
        }
        
        # Azure OpenAI API request body
        request_body = {
            "messages": [
                {"role": "system", "content": "You are a legal reasoning assistant specializing in defense strategy."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.3
        }
        
        # Make the API request to Azure OpenAI o3-mini
        response = requests.post(
            f"{endpoint}",
            headers=headers,
            json=request_body
        )
        
        response.raise_for_status()
        result = response.json()
        
        # Extract the generated content from Azure OpenAI response
        generated_text = result["choices"][0]["message"]["content"]
        
        # Return the text directly
        return generated_text
                
    except Exception as e:
        print(f"Error calling Azure OpenAI o3-mini API: {e}")
        # Create a basic formatted string with the defense arguments
        defense_text = "Defense Arguments:\n\n"
        for i, arg in enumerate(defense_arguments, 1):
            defense_text += f"{i}. {arg}\n"
            defense_text += "   Reasoning: Unable to generate detailed reasoning due to an error.\n\n"
        return defense_text

# Function to integrate with the case creation process
def add_win_likelihood_to_case(case_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Adds win likelihood prediction and defense arguments with reasoning to an existing case data structure.
    Uses o3-mini for both prediction and reasoning.
    
    Args:
        case_data: The case data dictionary
        
    Returns:
        Dict[str, Any]: Updated case data with win likelihood prediction and defense reasoning
    """
    try:
        # Extract required data from case
        evidence = case_data.get("evidence", [])
        plaintiff_argumentation = case_data.get("plaintiffArgumentation", [])
        court_jurisdiction = case_data.get("courtJurisdiction", "")
        state_jurisdiction = case_data.get("stateJurisdiction", "")
        timeline_events = case_data.get("timeline", [])
        case_type = case_data.get("caseType", "")
        harm_type = case_data.get("harmType", "")
        cause = case_data.get("cause", "")
        
        # Get prediction with defense arguments using o3-mini
        prediction = predict_case_win_likelihood(
            evidence=evidence,
            plaintiff_argumentation=plaintiff_argumentation,
            court_jurisdiction=court_jurisdiction,
            state_jurisdiction=state_jurisdiction,
            timeline_events=timeline_events,
            case_type=case_type,
            harm_type=harm_type,
            cause=cause
        )
        
        # Generate detailed reasoning for defense arguments using o3-mini as a string
        defense_reasoning_text = generate_defense_reasoning(
            evidence=evidence,
            plaintiff_argumentation=plaintiff_argumentation,
            case_type=case_type,
            harm_type=harm_type,
            cause=cause,
            defense_arguments=prediction.defense_arguments
        )
        
        # Add prediction and defense reasoning to case data
        case_data["caseWinLikelihood"] = {
            "percentage": prediction.win_likelihood_percent,
            "explanation": prediction.explanation,
            "keyFactors": prediction.key_factors,
            "defenseArguments": prediction.defense_arguments
        }
        
        # Add defense reasoning as a string
        case_data["defenseArgumentation"] = defense_reasoning_text
        
        return case_data
    
    except Exception as e:
        print(f"Error adding win likelihood prediction: {e}")
        # Return original case data if prediction fails
        return case_data

# Example usage
if __name__ == "__main__":
    # Example case data for testing
    test_case = {
        "evidence": [
            {
                "text": "Internal memo dated June 15, 2024 acknowledging brake system defect",
                "relevance": "Shows company knowledge of defect prior to accident",
                "strength": "strong"
            },
            {
                "text": "Customer complaint records showing 15 similar incidents reported",
                "relevance": "Establishes pattern of issues and notice to manufacturer",
                "strength": "moderate"
            }
        ],
        "plaintiffArgumentation": [
            "Manufacturer knew about defect for 6 months before recall",
            "Failed to properly test braking system in wet conditions",
            "Did not include adequate warnings in owner's manual"
        ],
        "courtJurisdiction": "Federal District Court",
        "stateJurisdiction": "California",
        "timeline": [
            {
                "date": "2024-01-10",
                "event": "Initial defect discovered in internal testing"
            },
            {
                "date": "2024-03-22",
                "event": "First customer accident reported"
            },
            {
                "date": "2024-06-15",
                "event": "Internal memo discussing potential recall"
            },
            {
                "date": "2024-07-01",
                "event": "Plaintiff's accident occurred"
            }
        ],
        "caseType": "Product Liability",
        "harmType": "Physical harm",
        "cause": "Defective Vehicle Component",
    }
    
    # Add win likelihood prediction
    updated_case = add_win_likelihood_to_case(test_case)
    
    # Print the prediction
    print("Case Win Likelihood Prediction:")
    print(f"Percentage: {updated_case['caseWinLikelihood']['percentage']}%")
    print(f"Explanation: {updated_case['caseWinLikelihood']['explanation']}")
    print("\nKey Factors:")
    for factor in updated_case['caseWinLikelihood']['keyFactors']:
        print(f"- {factor['factor']} ({factor['impact']})")
    print("\nDefense Arguments:")
    for arg in updated_case['caseWinLikelihood']['defenseArguments']:
        print(f"- {arg}")
    
    print("\nDetailed Defense Reasoning:")
    print(updated_case['defenseArgumentation'])
