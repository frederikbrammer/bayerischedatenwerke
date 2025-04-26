import json
from typing import List, Dict, Optional
from pydantic import BaseModel, Field
import requests
from dotenv import load_dotenv
import os
import re

load_dotenv()

# Define the data model for case analysis with evidence extraction
class Evidence(BaseModel):
    text: str = Field(description="The specific text from the document that serves as evidence")
    relevance: str = Field(description="Why this evidence is relevant to the case analysis")
    strength: str = Field(description="Assessment of the evidence strength (strong, moderate, weak)")

class CaseAnalysis(BaseModel):
    case_type: str = Field(description="The primary legal case type")
    harm_type: str = Field(
        description="The type of harm caused (physical, financial, environmental, employment)")
    cause: str = Field(description="The specific cause of the harm")
    description: str = Field(
        description="Legal analysis of the case with relevant precedents and statutes")
    secondary_types: Optional[List[str]] = Field(
        default=None, description="Additional relevant case types")
    evidence: Optional[List[Evidence]] = Field(
        default=None, description="Key evidence extracted from the document")

class CaseAnalysisResponse(BaseModel):
    primary_analysis: CaseAnalysis
    possible_alternatives: Optional[List[CaseAnalysis]] = None

def call_azure_openai_analyzer(chunk):
    """
    Analyzes legal text using Azure OpenAI API with GPT-4o to identify case type, harm, cause, and extract evidence.

    Args:
        chunk (str): The text chunk to process.

    Returns:
        str: The structured case analysis in JSON format.
    """
    # Azure OpenAI API configuration
    api_key = os.environ.get("AZURE_OPENAI_API_KEY")
    endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT")
    deployment_name = os.environ.get("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-4o")
    api_version = os.environ.get("AZURE_OPENAI_API_VERSION", "2023-12-01-preview")
    
    if not api_key or not endpoint:
        raise ValueError("Azure OpenAI API key and endpoint must be set as environment variables")
    
    prompt = (
        "Analyze the following legal text and classify it based on case type, harm, and cause. "
        "Also extract key evidence from the text. "
        "Return a structured analysis in JSON format according to these guidelines:\n\n"

        "HARM CLASSIFICATION:\n"
        "- Physical harm: Injury\n"
        "- Wrongful Death: Fatalities caused by the product\n"
        "- Financial harm: Monetary loss, property damage\n"
        "- Privacy/data harm: Unauthorized data use, privacy violations\n"
        "- Environmental harm: Pollution, emissions violations\n"
        "- Employment harm: Discrimination, wrongful termination, harassment\n\n"

        "CASE TYPE CLASSIFICATION:\n"
        "- Product Liability: Defect existed when product was sold (strict liability even without knowledge)\n"
        "- Negligence in Recalls: Company discovered defect later but failed to act responsibly\n"
        "- False Advertising: Misleading claims about product features or performance\n"
        "- Breach of Contract: Failure to fulfill agreed terms in vehicle purchase/warranty\n"
        "- Misuse of Personal Data: Improper handling of driver/customer data\n"
        "- Environmental Violations: Non-compliance with emissions or pollution regulations\n"
        "- IP Disputes: Unauthorized use of patented technology\n"
        "- Employment Disputes: Workplace issues like discrimination or wrongful termination\n\n"
        "If the liability is based on a defect present at the time of sale, classify as Product Liability. If the liability is based on failure to act after discovering a danger post-sale, classify as Negligence in Recall."

        "CAUSE CLASSIFICATION:\n"
        "- Defective Vehicle Component: A car part fails causing harm\n"
        "- Failure to Recall Known Defect: Company knew about issue but delayed action\n"
        "- Misleading Claims: Exaggerated or false safety/efficiency claims\n"
        "- Non-compliant Systems: Systems that violate regulations (e.g., emissions)\n"
        "- Contract Breach: Breaking terms of sales, lease, or warranty agreements\n"
        "- Unauthorized Data Sharing: Selling driver data without proper consent\n"
        "- Improper Recall Execution: Failed to properly fix issue after recall notice\n"
        "- Unlicensed Technology Use: Using patented tech without permission\n"
        "- Workplace Misconduct: Discrimination, harassment, or unlawful termination\n\n"

        "EVIDENCE EXTRACTION:\n"
        "- Identify 3-5 key pieces of evidence from the text that support your analysis\n"
        "- For each piece of evidence, extract the exact text, explain its relevance, and assess its strength\n"
        "- Evidence strength should be categorized as 'strong', 'moderate', or 'weak'\n"
        "- Focus on facts, dates, statements, or descriptions that directly support the case classification\n\n"

        "DECISION FLOW:\n"
        "1. First identify the type of harm (physical, financial, privacy, environmental, employment)\n"
        "2. Based on harm type, determine the most likely case type:\n"
        "   - If physical harm → check Product Liability or Negligence in Recalls\n"
        "   - If financial/privacy harm → check Misuse of Data, Breach of Contract, False Advertising, IP Disputes\n"
        "   - If environmental harm → check Environmental Violations\n"
        "   - If employment harm → check Employment Disputes\n"
        "3. For Product Liability vs. Negligence in Recalls:\n"
        "   - Product Liability: Defect existed when sold (focus on unsafe product from beginning)\n"
        "   - Negligence in Recalls: Bad behavior after product sold (focus on response to discovered defect)\n"
        "   - Note: Both can apply in some cases\n\n"

        "DESCRIPTION STYLE:\n"
        "The description should be written in formal legal language, citing relevant legal standards, potential "
        "applicable statutes, and precedent cases where appropriate. Use precise legal terminology and avoid "
        "colloquial expressions. Include references to elements of claims that would need to be proven, potential "
        "defenses, and burden of proof considerations. The tone should be analytical, authoritative, and "
        "objective, similar to a legal brief or memorandum.\n\n"

        "Return the analysis in this JSON structure:\n"
        "{\n"
        "  'primary_analysis': {\n"
        "    'case_type': 'Primary case type',\n"
        "    'harm_type': 'Type of harm caused',\n"
        "    'cause': 'Specific cause of the harm',\n"
        "    'description': 'Legal analysis with relevant standards and precedents',\n"
        "    'secondary_types': ['Additional relevant case types'],\n"
        "    'evidence': [\n"
        "      {\n"
        "        'text': 'Extracted text from document',\n"
        "        'relevance': 'Why this evidence matters',\n"
        "        'strength': 'strong/moderate/weak'\n"
        "      }\n"
        "    ]\n"
        "  },\n"
        "  'possible_alternatives': [\n"
        "    {\n"
        "      'case_type': 'Alternative case type',\n"
        "      'harm_type': 'Alternative harm type',\n"
        "      'cause': 'Alternative cause',\n"
        "      'description': 'Legal analysis of why this might also apply',\n"
        "      'evidence': [\n"
        "        {\n"
        "          'text': 'Extracted text from document',\n"
        "          'relevance': 'Why this evidence matters',\n"
        "          'strength': 'strong/moderate/weak'\n"
        "        }\n"
        "      ]\n"
        "    }\n"
        "  ]\n"
        "}\n\n"
        "Text to analyze:\n" + chunk
    )

    try:
        # Prepare the API request
        headers = {
            "Content-Type": "application/json",
            "api-key": api_key
        }
        
        # Azure OpenAI API request body
        request_body = {
            "messages": [
                {"role": "system", "content": "You are a legal analysis assistant that provides structured JSON responses."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0,
            "response_format": {"type": "json_object"}
        }
        
        # Make the API request to Azure OpenAI
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
            case_analysis = json.loads(generated_text)
            return json.dumps(case_analysis)
        except json.JSONDecodeError:
            # If direct parsing fails, try to extract JSON from the text
            json_match = re.search(r'(\{.*\})', generated_text, re.DOTALL)
            if json_match:
                case_analysis = json.loads(json_match.group(1))
                return json.dumps(case_analysis)
            else:
                raise ValueError("Could not extract valid JSON from model response")
                
    except Exception as e:
        print(f"Error calling Azure OpenAI API: {e}")
        return json.dumps({
            "primary_analysis": {
                "case_type": "Error",
                "harm_type": "Unknown",
                "cause": "Processing error",
                "description": f"Failed to analyze: {str(e)}",
                "evidence": []
            }
        })

def split_text_into_chunks(text, chunk_size=2000):
    """Splits text into smaller chunks for processing."""
    return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]

def extract_case_type(extracted_text: str) -> CaseAnalysisResponse:
    """
    Extracts case type, related information, and evidence from the provided text.

    Args:
        extracted_text (str): The text to analyze.

    Returns:
        CaseAnalysisResponse: The structured case analysis with evidence.
    """
    # Split the text into manageable chunks
    chunks = split_text_into_chunks(extracted_text)

    # Process each chunk and collect results
    results = []
    if chunks:
        result = call_azure_openai_analyzer(chunks[0])
        results.append(result)

    parsed_results = [json.loads(result) for result in results]
    print(parsed_results)
    
    # Combine results into a single response
    combined_response = {
        "primary_analysis": parsed_results[0]["primary_analysis"],
        "possible_alternatives": [result["primary_analysis"] for result in parsed_results[1:]]
    }

    return CaseAnalysisResponse(**combined_response)

# Example usage
if __name__ == "__main__":
    # Make sure to set these environment variables before running:
    # export AZURE_OPENAI_API_KEY="your-api-key"
    # export AZURE_OPENAI_ENDPOINT="https://your-resource-name.openai.azure.com"
    # export AZURE_OPENAI_DEPLOYMENT_NAME="your-gpt4o-deployment-name"
    # export AZURE_OPENAI_API_VERSION="2023-12-01-preview"
    
    sample_text = "Your legal text here..."
    result = extract_case_type(sample_text)
    print(result.model_dump_json(indent=2))
