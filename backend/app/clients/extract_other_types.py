import json
import concurrent.futures
import time
import requests
import os
from dotenv import load_dotenv
from typing import List, Dict, Optional, Any, Union
from pydantic import BaseModel, Field

load_dotenv()
class CaseInformation(BaseModel):
    Case_ID: Optional[str] = None
    Filing_Date: Optional[str] = None
    Jurisdiction: Optional[Dict[str, str]] = None  # Changed to dictionary with state and court jurisdiction
    Defect_Type: Optional[List[str]] = None
    Number_of_Claimants: Optional[str] = None
    Media_Coverage_Level: Optional[Dict[str, str]] = None
    Outcome: Optional[str] = None
    Status: Optional[str] = None
    Case_Summary: Optional[str] = None
    Time_to_Resolution_Months: Optional[str] = None
    Settlement_Amount: Optional[str] = None
    Defense_Cost_Estimate: Optional[str] = None
    Expected_Brand_Impact: Optional[Dict[str, str]] = None
    Affected_Car: Optional[str] = None
    Affected_Part: Optional[str] = None
    Brand_Impact_Estimate: Optional[Dict[str, str]] = None
    Case_Win_Likelihood: Optional[Dict[str, str]] = None
    Plaintiff_Argumentation: Optional[List[str]] = None
    Timeline_of_Events: Optional[List[str]] = None  # New field
    Relevant_Laws: Optional[List[str]] = None  # New field
    Reputation_Impact: Optional[Dict[str, Dict[str, str]]] = None  # New field for separated reputation impact

def call_azure_openai_flashlight(chunk, chunk_number, chunk_size):
    """
    Calls the Azure OpenAI API with GPT-4o to process the text chunk.

    Args:
        chunk (str): The text chunk to process.
        chunk_number (int): The chunk number for debugging.
        chunk_size (int): The size of the chunk for logging.

    Returns:
        dict: The extracted case information from this chunk.
    """
    # Azure OpenAI API configuration
    api_key = os.environ.get("AZURE_OPENAI_API_KEY")
    endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT")
    deployment_name = os.environ.get("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-4o")
    api_version = os.environ.get("AZURE_OPENAI_API_VERSION", "2023-12-01-preview")
    
    if not api_key or not endpoint:
        raise ValueError("Azure OpenAI API key and endpoint must be set as environment variables")
    
    prompt = (
        "Extract the following information from the legal case text provided. "
        "All fields are optional - include information that is explicitly mentioned in the text. "
        "For certain fields like Expected_Brand_Impact, Brand_Impact_Estimate, Media_Coverage_Level, and Case_Win_Likelihood, make a reasonable inference based on the context and provide a detailed explanation for your assessment. "
        "If a piece of information appears multiple times, include all instances in a list. "
        "If information is not found for a field, use the exact string 'Not specified' as the value. "
        "For list fields like Defect_Type and Plaintiff_Argumentation, if no information is found, include a single item with value 'Not specified'. "
        "For the Status field, use ONLY one of the following values: 'In favour of defendant', 'In favour of plaintiff', 'Settled', 'In Progress first instance', 'Dismissed', 'In Progress appeal', 'In Progress Supreme Court'. If the status cannot be determined, use 'Not specified'."
        "Return the output as a JSON object with the following structure and descriptions:\n\n"
        "To determine the brand impact, consider if someone died and if the defendant maybe did something intentionally or knowingly use low and medium often, high if number of claimants is high and or death is mentioned\n"
        "{\n"
        "  'Case_ID': 'A unique identifier assigned to each legal case for tracking and reference purposes',\n"
        "  'Filing_Date': 'The date on which the case was officially filed with the court',\n"
        "  'Jurisdiction': {'state_jurisdiction': 'State or federal court system where the case is being heard', 'court_jurisdiction': 'Specific court where the case is being heard'},\n"
        "  'Defect_Type': ['The specific kind of product flaw alleged in the case, such as design defect, manufacturing defect, or failure to warn'],\n"
        "  'Number_of_Claimants': 'The total number of plaintiffs or parties bringing the case against the company',\n"
        "  'Media_Coverage_Level': {'level': 'None/Low/Medium/High', 'explanation': 'Detailed explanation of why this level was assigned based on the text'},\n"
        "  'Outcome': 'The final resolution of the case, such as Dismissed, Settled, Plaintiff Win, or Defense Win',\n"
        "  'Status': 'The current status of the case: In favour of defendant, In favour of plaintiff, Settled, In Progress first instance, Dismissed, In Progress appeal, In Progress Supreme Court',\n"
        "  'Case_Summary': 'A concise summary of what the case is about, including key allegations and context',\n"
        "  'Time_to_Resolution_Months': 'The total duration, measured in months, from the case's filing date to its conclusion',\n"
        "  'Settlement_Amount': 'The amount of money paid by the defendant to the plaintiff(s) if the case was resolved through a settlement agreement',\n"
        "  'Defense_Cost_Estimate': 'The estimated total cost incurred by the defense, including legal fees, expert witness fees, and other litigation expenses',\n"
        "  'Expected_Brand_Impact': {'impact': 'Low/Medium/High', 'explanation': 'Detailed explanation of why this impact level was assigned based on the case details'},\n"
        "  'Affected_Car': 'The specific car model or vehicle type that is involved in the case',\n"
        "  'Affected_Part': 'The specific component or part of the vehicle that is alleged to be defective',\n"
        "  'Brand_Impact_Estimate': {'impact': 'Low/Medium/High', 'explanation': 'Detailed assessment of how this case might affect the company's brand reputation'},\n"
        "  'Case_Win_Likelihood': {'likelihood': 'Low/Medium/High', 'explanation': 'Assessment of how likely the defendant will win the case based on available information'},\n"
        "  'Plaintiff_Argumentation': ['Key arguments made by the plaintiff in support of their case, in exhaustive key points'],\n"
        "  'Timeline_of_Events': ['Chronological list of key events related to the case'],\n"
        "  'Relevant_Laws': ['Laws, statutes, regulations, or legal precedents relevant to the case'],\n"
        "  'Reputation_Impact': {'case_outcome': {'impact': 'Low/Medium/High', 'explanation': 'Impact on reputation based on the case outcome'}, 'media_coverage': {'impact': 'Low/Medium/High', 'explanation': 'Impact on reputation from media coverage regardless of case outcome'}}\n"
        "}\n\n"
        "Important: For any field where information is not available in the text, use the exact string 'Not specified'. "
        "Do not break down strings into individual characters. For example, if Defect_Type is not specified, return ['Not specified'] not ['N','o','t',' ','s','p','e','c','i','f','i','e','d']. "
        "For Expected_Brand_Impact, Brand_Impact_Estimate, Media_Coverage_Level, Case_Win_Likelihood, and Reputation_Impact, provide a detailed explanation for your assessment. "
        "If you cannot make a reasonable assessment, use {'level': 'Not specified', 'explanation': 'Insufficient information to determine'} or similar.\n\n"
        + chunk
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
                {"role": "system", "content": "You are a legal information extraction assistant that provides structured JSON responses."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0,
            "response_format": {"type": "json_object"}
        }
        
        # Make the API request to Azure OpenAI
        response = requests.post(
            f"{endpoint}",
            headers=headers,
            json=request_body,
            timeout=60  # Add timeout to prevent hanging
        )
        
        response.raise_for_status()
        result = response.json()
        
        # Extract the generated content from Azure OpenAI response
        response_text = result["choices"][0]["message"]["content"]

        # Print the raw response for debugging problematic chunks
        if chunk_number == 1:
            print(f"Raw API response for chunk 1 (size {chunk_size}): {response_text[:200]}...")

        # Try to parse the JSON response
        try:
            # First try direct parsing
            response_json = json.loads(response_text)
            
            # If response_json is a list, handle it appropriately
            if isinstance(response_json, list):
                print(f"API returned a list for chunk {chunk_number} (size {chunk_size}) instead of a dictionary")
                # Try to extract a dictionary from the list if possible
                dict_items = [item for item in response_json if isinstance(item, dict)]
                if dict_items:
                    response_json = dict_items[0]  # Use the first dictionary
                else:
                    # Create an empty dictionary if no dictionaries found
                    response_json = {}
                    
        except json.JSONDecodeError:
            # If direct parsing fails, try to extract JSON from the text
            import re
            json_match = re.search(r'(\{.*\})', response_text, re.DOTALL)
            if json_match:
                try:
                    response_json = json.loads(json_match.group(1))
                except:
                    print(f"Failed to parse extracted JSON for chunk {chunk_number}")
                    response_json = {}
            else:
                print(f"No JSON found in response for chunk {chunk_number}")
                response_json = {}

        # Fix potential issues with the response format
        fixed_response = {}

        # Process each field in the response
        for key, value in response_json.items():
            # Handle list of single characters
            if isinstance(value, list) and all(isinstance(item, str) and len(item) == 1 for item in value):
                fixed_response[key] = [''.join(value)]
            # Handle dictionary fields
            elif key in ['Media_Coverage_Level', 'Expected_Brand_Impact', 'Brand_Impact_Estimate', 'Case_Win_Likelihood', 'Reputation_Impact']:
                if isinstance(value, str):
                    if key == 'Case_Win_Likelihood':
                        level_key = "likelihood"
                    elif key in ['Expected_Brand_Impact', 'Brand_Impact_Estimate']:
                        level_key = "impact"
                    else:
                        level_key = "level"
                    
                    fixed_response[key] = {
                        level_key: value,
                        "explanation": f"No detailed explanation provided for the {level_key}."
                    }
                else:
                    fixed_response[key] = value
            # Handle all other fields
            else:
                fixed_response[key] = value

        print(f"Successfully processed chunk {chunk_number} (size {chunk_size})")
        return fixed_response

    except Exception as e:
        print(f"An error occurred while calling Azure OpenAI for chunk {chunk_number} (size {chunk_size}): {e}")
        # Return a valid empty response
        return {}

def split_text_into_chunks(text, chunk_size=2000):
    """
    Splits text into smaller chunks.

    Args:
        text (str): The text to split.
        chunk_size (int): The maximum size of each chunk.

    Returns:
        list: A list of text chunks.
    """
    return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]

def merge_case_information(info_list):
    """
    Merges multiple case information dictionaries into a single comprehensive one.

    Args:
        info_list (list): List of dictionaries containing case information.

    Returns:
        dict: A merged dictionary with all case information.
    """
    merged_info = {}

    # Fields that should be lists of unique items
    list_fields = ['Defect_Type', 'Plaintiff_Argumentation', 'Timeline_of_Events', 'Relevant_Laws']

    # Fields that are dictionaries with explanations
    dict_fields = ['Media_Coverage_Level', 'Expected_Brand_Impact', 'Brand_Impact_Estimate', 'Case_Win_Likelihood', 'Reputation_Impact']

    # Fields that should take the first non-empty value
    single_value_fields = [
        'Case_ID', 'Filing_Date', 'Number_of_Claimants', 'Outcome', 'Status', 'Case_Summary',
        'Time_to_Resolution_Months', 'Settlement_Amount', 'Defense_Cost_Estimate', 'Affected_Car', 'Affected_Part'
    ]
    
    # Handle Jurisdiction separately as it's now a dictionary
    jurisdiction_field = 'Jurisdiction'

    for info in info_list:
        if not info:
            continue

        # Process list fields
        for field in list_fields:
            if field in info and info[field]:
                if field not in merged_info:
                    merged_info[field] = []

                # Add new unique items that are not "Not specified"
                for item in info[field]:
                    if item != "Not specified" and item not in merged_info[field]:
                        merged_info[field].append(item)

        # Process dictionary fields with the most detailed explanation
        for field in dict_fields:
            if field in info and info[field]:
                # If the field is a string, convert it to a dictionary
                if isinstance(info[field], str):
                    if field == 'Case_Win_Likelihood':
                        level_key = "likelihood"
                    elif field in ['Expected_Brand_Impact', 'Brand_Impact_Estimate']:
                        level_key = "impact"
                    else:
                        level_key = "level"
                        
                    info[field] = {
                        level_key: info[field],
                        "explanation": f"No detailed explanation provided for the {level_key}."
                    }

                # Special handling for Reputation_Impact which has nested dictionaries
                if field == 'Reputation_Impact':
                    if field not in merged_info:
                        merged_info[field] = {
                            'case_outcome': {'impact': 'Not specified', 'explanation': 'Insufficient information to determine'},
                            'media_coverage': {'impact': 'Not specified', 'explanation': 'Insufficient information to determine'}
                        }
                    
                    # Update case_outcome if it has better information
                    if 'case_outcome' in info[field] and (
                        info[field]['case_outcome'].get('impact') != 'Not specified' or
                        len(info[field]['case_outcome'].get('explanation', '')) > len(merged_info[field]['case_outcome'].get('explanation', ''))
                    ):
                        merged_info[field]['case_outcome'] = info[field]['case_outcome']
                    
                    # Update media_coverage if it has better information
                    if 'media_coverage' in info[field] and (
                        info[field]['media_coverage'].get('impact') != 'Not specified' or
                        len(info[field]['media_coverage'].get('explanation', '')) > len(merged_info[field]['media_coverage'].get('explanation', ''))
                    ):
                        merged_info[field]['media_coverage'] = info[field]['media_coverage']
                else:
                    # Handle other dictionary fields
                    level_key = "likelihood" if field == 'Case_Win_Likelihood' else "impact" if field in ['Expected_Brand_Impact', 'Brand_Impact_Estimate'] else "level"
                    
                    if (field not in merged_info or
                        isinstance(merged_info[field], str) or
                        merged_info[field].get(level_key) == 'Not specified' or
                        (len(info[field].get('explanation', '')) > len(merged_info[field].get('explanation', '')))):
                        merged_info[field] = info[field]

        # Process single value fields
        for field in single_value_fields:
            if field in info and info[field] and info[field] != "Not specified" and (field not in merged_info or merged_info[field] == "Not specified"):
                merged_info[field] = info[field]
        
        # Process Jurisdiction field (now a dictionary)
        if jurisdiction_field in info and info[jurisdiction_field]:
            if jurisdiction_field not in merged_info:
                merged_info[jurisdiction_field] = {
                    'state_jurisdiction': 'Not specified',
                    'court_jurisdiction': 'Not specified'
                }
            
            # Handle if Jurisdiction is still a string in some chunks
            if isinstance(info[jurisdiction_field], str) and info[jurisdiction_field] != "Not specified":
                # Try to intelligently split into state and court
                if "federal" in info[jurisdiction_field].lower():
                    merged_info[jurisdiction_field]['state_jurisdiction'] = "Federal"
                    merged_info[jurisdiction_field]['court_jurisdiction'] = info[jurisdiction_field]
                else:
                    merged_info[jurisdiction_field]['state_jurisdiction'] = info[jurisdiction_field]
                    merged_info[jurisdiction_field]['court_jurisdiction'] = 'Not specified'
            elif isinstance(info[jurisdiction_field], dict):
                # Update state_jurisdiction if better info available
                if 'state_jurisdiction' in info[jurisdiction_field] and info[jurisdiction_field]['state_jurisdiction'] != "Not specified":
                    merged_info[jurisdiction_field]['state_jurisdiction'] = info[jurisdiction_field]['state_jurisdiction']
                
                # Update court_jurisdiction if better info available
                if 'court_jurisdiction' in info[jurisdiction_field] and info[jurisdiction_field]['court_jurisdiction'] != "Not specified":
                    merged_info[jurisdiction_field]['court_jurisdiction'] = info[jurisdiction_field]['court_jurisdiction']

    # Add "Not specified" for any missing fields
    all_fields = list_fields + single_value_fields
    for field in all_fields:
        if field not in merged_info or not merged_info[field]:
            if field in list_fields:
                merged_info[field] = ["Not specified"]
            else:
                merged_info[field] = "Not specified"

    # Add default dictionaries for missing dict fields
    for field in dict_fields:
        if field not in merged_info:
            if field == 'Reputation_Impact':
                merged_info[field] = {
                    'case_outcome': {'impact': 'Not specified', 'explanation': 'Insufficient information to determine'},
                    'media_coverage': {'impact': 'Not specified', 'explanation': 'Insufficient information to determine'}
                }
            else:
                if field == 'Case_Win_Likelihood':
                    level_key = "likelihood"
                elif field in ['Expected_Brand_Impact', 'Brand_Impact_Estimate']:
                    level_key = "impact"
                else:
                    level_key = "level"
                    
                merged_info[field] = {
                    level_key: "Not specified",
                    "explanation": "Insufficient information to determine"
                }
        elif isinstance(merged_info[field], str) and field != 'Reputation_Impact':
            if field == 'Case_Win_Likelihood':
                level_key = "likelihood"
            elif field in ['Expected_Brand_Impact', 'Brand_Impact_Estimate']:
                level_key = "impact"
            else:
                level_key = "level"
                
            merged_info[field] = {
                level_key: merged_info[field],
                "explanation": f"No detailed explanation provided for the {level_key}."
            }
    
    # Ensure Jurisdiction is properly formatted
    if jurisdiction_field not in merged_info:
        merged_info[jurisdiction_field] = {
            'state_jurisdiction': 'Not specified',
            'court_jurisdiction': 'Not specified'
        }

    return merged_info

def clean_response(response_dict):
    """
    Cleans the response dictionary to ensure consistent formatting.

    Args:
        response_dict (dict): The dictionary to clean.

    Returns:
        dict: The cleaned dictionary.
    """
    # Convert any string values that look like numbers to actual numbers
    if "Number_of_Claimants" in response_dict and isinstance(response_dict["Number_of_Claimants"], str):
        try:
            if response_dict["Number_of_Claimants"].isdigit():
                response_dict["Number_of_Claimants"] = response_dict["Number_of_Claimants"]
        except:
            pass

    # Ensure dictionary fields have the correct structure
    dict_fields = ['Media_Coverage_Level', 'Expected_Brand_Impact', 'Brand_Impact_Estimate', 'Case_Win_Likelihood']
    for field in dict_fields:
        if field in response_dict:
            if isinstance(response_dict[field], str):
                if field == 'Case_Win_Likelihood':
                    level_key = "likelihood"
                elif field in ['Expected_Brand_Impact', 'Brand_Impact_Estimate']:
                    level_key = "impact"
                else:
                    level_key = "level"
                
                response_dict[field] = {
                    level_key: response_dict[field],
                    "explanation": f"No detailed explanation provided for the {level_key}."
                }
    
    # Ensure Reputation_Impact has the correct structure
    if 'Reputation_Impact' in response_dict:
        if isinstance(response_dict['Reputation_Impact'], str):
            response_dict['Reputation_Impact'] = {
                'case_outcome': {'impact': response_dict['Reputation_Impact'], 'explanation': 'No detailed explanation provided.'},
                'media_coverage': {'impact': 'Not specified', 'explanation': 'Insufficient information to determine'}
            }
        elif isinstance(response_dict['Reputation_Impact'], dict) and not ('case_outcome' in response_dict['Reputation_Impact'] and 'media_coverage' in response_dict['Reputation_Impact']):
            # If it's a dict but doesn't have the right structure
            temp_impact = response_dict['Reputation_Impact'].get('impact', 'Not specified')
            temp_explanation = response_dict['Reputation_Impact'].get('explanation', 'No detailed explanation provided.')
            
            response_dict['Reputation_Impact'] = {
                'case_outcome': {'impact': temp_impact, 'explanation': temp_explanation},
                'media_coverage': {'impact': 'Not specified', 'explanation': 'Insufficient information to determine'}
            }
    else:
        response_dict['Reputation_Impact'] = {
            'case_outcome': {'impact': 'Not specified', 'explanation': 'Insufficient information to determine'},
            'media_coverage': {'impact': 'Not specified', 'explanation': 'Insufficient information to determine'}
        }
    
    # Ensure list fields have the correct structure
    list_fields = ['Defect_Type', 'Plaintiff_Argumentation', 'Timeline_of_Events', 'Relevant_Laws']
    for field in list_fields:
        if field in response_dict:
            if not isinstance(response_dict[field], list):
                if response_dict[field] == "Not specified":
                    response_dict[field] = ["Not specified"]
                else:
                    response_dict[field] = [response_dict[field]]
            elif len(response_dict[field]) == 0:
                response_dict[field] = ["Not specified"]
        else:
            response_dict[field] = ["Not specified"]
    
    # Ensure Status field has a valid value
    valid_statuses = ["In favour of defendant", "In favour of plaintiff", "Settled", "In Progress first instance", "Dismissed", "In Progress appeal", "In Progress Supreme Court"]
    
    if "Status" in response_dict:
        if response_dict["Status"] not in valid_statuses and response_dict["Status"] != "Not specified":
            # Map old status values to new valid statuses
            status_mapping = {
                "Won": "In favour of defendant",
                "Lost": "In favour of plaintiff",
                "Settled": "Settled",
                "In Progress": "In Progress first instance"
            }
            
            # Try to map the status to a valid one
            if response_dict["Status"] in status_mapping:
                response_dict["Status"] = status_mapping[response_dict["Status"]]
            else:
                # Try to infer status from Outcome if possible
                if "Outcome" in response_dict:
                    if response_dict["Outcome"] == "Plaintiff Win":
                        response_dict["Status"] = "In favour of plaintiff"
                    elif response_dict["Outcome"] == "Defense Win":
                        response_dict["Status"] = "In favour of defendant"
                    elif response_dict["Outcome"] == "Settled":
                        response_dict["Status"] = "Settled"
                    elif response_dict["Outcome"] == "Dismissed":
                        response_dict["Status"] = "Dismissed"
                    else:
                        response_dict["Status"] = "In Progress first instance"
                else:
                    response_dict["Status"] = "In Progress first instance"
    elif "Outcome" in response_dict and response_dict["Outcome"] != "Not specified":
        # If Status is missing but Outcome is present, infer Status
        if response_dict["Outcome"] == "Plaintiff Win":
            response_dict["Status"] = "In favour of plaintiff"
        elif response_dict["Outcome"] == "Defense Win":
            response_dict["Status"] = "In favour of defendant"
        elif response_dict["Outcome"] == "Settled":
            response_dict["Status"] = "Settled"
        elif response_dict["Outcome"] == "Dismissed":
            response_dict["Status"] = "Dismissed"
        else:
            response_dict["Status"] = "In Progress first instance"
    else:
        response_dict["Status"] = "Not specified"

    # Ensure Case_Summary is present
    if "Case_Summary" not in response_dict or not response_dict["Case_Summary"]:
        # Try to create a summary from other fields if possible
        if "Defect_Type" in response_dict and response_dict["Defect_Type"] != ["Not specified"]:
            defect_types = ", ".join(response_dict["Defect_Type"])
            affected_car = response_dict.get("Affected_Car", "unspecified vehicle")
            if affected_car == "Not specified":
                affected_car = "unspecified vehicle"
            affected_part = response_dict.get("Affected_Part", "unspecified part")
            if affected_part == "Not specified":
                affected_part = "unspecified part"
            
            response_dict["Case_Summary"] = f"This case involves allegations of {defect_types} related to {affected_part} in {affected_car}."
        else:
            response_dict["Case_Summary"] = "Not specified"
    
    # Ensure Jurisdiction is properly formatted
    if "Jurisdiction" not in response_dict:
        response_dict["Jurisdiction"] = {
            'state_jurisdiction': 'Not specified',
            'court_jurisdiction': 'Not specified'
        }
    elif isinstance(response_dict["Jurisdiction"], str) and response_dict["Jurisdiction"] != "Not specified":
        # Convert string to dictionary format
        jurisdiction_text = response_dict["Jurisdiction"]
        response_dict["Jurisdiction"] = {
            'state_jurisdiction': 'Not specified',
            'court_jurisdiction': 'Not specified'
        }
        
        # Try to intelligently split into state and court
        if "federal" in jurisdiction_text.lower():
            response_dict["Jurisdiction"]['state_jurisdiction'] = "Federal"
            response_dict["Jurisdiction"]['court_jurisdiction'] = jurisdiction_text
        else:
            response_dict["Jurisdiction"]['state_jurisdiction'] = jurisdiction_text
    
    return response_dict

def process_chunk(args):
    """
    Process a single chunk (for parallel processing).

    Args:
        args (tuple): A tuple containing (chunk, chunk_number, chunk_size).

    Returns:
        dict: The extracted case information.
    """
    chunk, chunk_number, chunk_size = args
    try:
        # Add a small delay to avoid overwhelming the API
        if chunk_number > 1:
            time.sleep(1)
        return call_azure_openai_flashlight(chunk, chunk_number, chunk_size)
    except Exception as e:
        print(f"Error in process_chunk for chunk {chunk_number} (size {chunk_size}): {e}")
        return {}

def process_with_chunk_size(text, chunk_size, max_workers=2):
    """
    Process the text with a specific chunk size using parallel processing.
    Using fewer workers to avoid overwhelming the API.

    Args:
        text (str): The text to process.
        chunk_size (int): The chunk size to use.
        max_workers (int): Maximum number of parallel workers.

    Returns:
        dict: The merged case information from all chunks.
    """
    chunks = split_text_into_chunks(text, chunk_size)
    print(f"Processing {len(chunks)} chunks of size {chunk_size} in parallel (max {max_workers} workers)...")

    # Prepare arguments for parallel processing
    chunk_args = [(chunk, i+1, chunk_size) for i, chunk in enumerate(chunks)]

    # Process chunks in parallel
    all_chunk_info = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all tasks
        future_to_chunk = {executor.submit(process_chunk, arg): arg[1] for arg in chunk_args}

        # Collect results as they complete
        for future in concurrent.futures.as_completed(future_to_chunk):
            chunk_number = future_to_chunk[future]
            try:
                chunk_info = future.result()
                all_chunk_info.append(chunk_info)
                print(f"Completed chunk {chunk_number}/{len(chunks)} (size {chunk_size})")
            except Exception as e:
                print(f"Exception processing chunk {chunk_number} (size {chunk_size}): {e}")
                all_chunk_info.append({})

    # Merge information from all chunks
    merged_case_info = merge_case_information(all_chunk_info)
    return merged_case_info

def extract_other_types(extracted_text: str) -> CaseInformation:
    """
    Extracts case type and related information from the provided text.

    Args:
        extracted_text (str): The text to analyze.

    Returns:
        CaseInformation: The structured case analysis.
    """
    # Process the text with a specific chunk size
    chunk_size = 5000
    # Using fewer workers to avoid overwhelming the API
    merged_case_info = process_with_chunk_size(extracted_text, chunk_size, max_workers=2)

    print("merged_case_info")
    # Clean the response
    cleaned_response = clean_response(merged_case_info)

    print("cleaned_response")
    # Convert to CaseInformation model
    case_info = CaseInformation(**cleaned_response)
    return case_info
