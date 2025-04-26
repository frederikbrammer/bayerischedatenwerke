import PyPDF2
import ollama
import requests
import json
import concurrent.futures
import time
from typing import List, Dict, Optional, Any, Union
from key import api_key
from google import genai
from pydantic import BaseModel, Field


class CaseInformation(BaseModel):
    Case_ID: Optional[str] = None
    Filing_Date: Optional[str] = None
    Jurisdiction: Optional[str] = None
    Defect_Type: Optional[List[str]] = None
    Number_of_Claimants: Optional[int] = None
    Media_Coverage_Level: Optional[Dict[str, str]] = None
    Outcome: Optional[str] = None
    Time_to_Resolution_Months: Optional[str] = None
    Settlement_Amount: Optional[str] = None
    Defense_Cost_Estimate: Optional[str] = None
    Expected_Brand_Impact: Optional[Dict[str, str]] = None


client = genai.Client(api_key=api_key)


def call_gemini_flashlight(chunk, chunk_number, chunk_size):
    """
    Calls the Google Gemini 2.0 Flashlight API to process the text chunk.

    Args:
        chunk (str): The text chunk to process.
        chunk_number (int): The chunk number for debugging.
        chunk_size (int): The size of the chunk for logging.

    Returns:
        dict: The extracted case information from this chunk.
    """
    prompt = (
        "Extract the following information from the legal case text provided. "
        "All fields are optional - include information that is explicitly mentioned in the text. "
        "For certain fields like Expected_Brand_Impact and Media_Coverage_Level, make a reasonable inference based on the context and provide a detailed explanation for your assessment. "
        "If a piece of information appears multiple times, include all instances in a list. "
        "If information is not found for a field, use the exact string 'Not specified' as the value. "
        "For list fields like Defect_Type, if no information is found, include a single item with value 'Not specified'. "
        "Return the output as a JSON object with the following structure and descriptions:\n\n"
        "{\n"
        "  'Case_ID': 'A unique identifier assigned to each legal case for tracking and reference purposes',\n"
        "  'Filing_Date': 'The date on which the case was officially filed with the court',\n"
        "  'Jurisdiction': 'The geographic location and legal authority (court, region, or country) where the case is being heard',\n"
        "  'Defect_Type': ['The specific kind of product flaw alleged in the case, such as design defect, manufacturing defect, or failure to warn'],\n"
        "  'Number_of_Claimants': 'The total number of plaintiffs or parties bringing the case against the company',\n"
        "  'Media_Coverage_Level': {'level': 'None/Low/Medium/High', 'explanation': 'Detailed explanation of why this level was assigned based on the text'},\n"
        "  'Outcome': 'The final resolution of the case, such as Dismissed, Settled, Plaintiff Win, or Defense Win',\n"
        "  'Time_to_Resolution_Months': 'The total duration, measured in months, from the case's filing date to its conclusion',\n"
        "  'Settlement_Amount': 'The amount of money paid by the defendant to the plaintiff(s) if the case was resolved through a settlement agreement',\n"
        "  'Defense_Cost_Estimate': 'The estimated total cost incurred by the defense, including legal fees, expert witness fees, and other litigation expenses',\n"
        "  'Expected_Brand_Impact': {'impact': 'Low/Medium/High', 'explanation': 'Detailed explanation of why this impact level was assigned based on the case details'}\n"
        "}\n\n"
        "Important: For any field where information is not available in the text, use the exact string 'Not specified'. "
        "Do not break down strings into individual characters. For example, if Defect_Type is not specified, return ['Not specified'] not ['N','o','t',' ','s','p','e','c','i','f','i','e','d']. "
        "For Expected_Brand_Impact and Media_Coverage_Level, provide a detailed explanation for your assessment. For example, if you assess Media_Coverage_Level as 'Low', explain why (e.g., 'The case appears to be a routine legal proceeding with limited public interest'). "
        "If you cannot make a reasonable assessment, use {'level': 'Not specified', 'explanation': 'Insufficient information to determine media coverage'} or similar.\n\n"
        + chunk
    )

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
            config={
                "response_mime_type": "application/json",
            },
        )

        # Parse the response text as JSON
        response_text = response.text

        # Print the raw response for debugging problematic chunks
        if chunk_number == 1:
            print(
                f"Raw API response for chunk 1 (size {chunk_size}): {response_text[:200]}...")

        # Handle potential list response
        try:
            response_json = json.loads(response_text)

            # If response_json is a list, handle it appropriately
            if isinstance(response_json, list):
                print(
                    f"API returned a list for chunk {chunk_number} (size {chunk_size}) instead of a dictionary")
                # Try to extract a dictionary from the list if possible
                dict_items = [
                    item for item in response_json if isinstance(item, dict)]
                if dict_items:
                    response_json = dict_items[0]  # Use the first dictionary
                else:
                    # Create an empty dictionary if no dictionaries found
                    response_json = {}

            # Fix potential issues with the response format
            fixed_response = {}

            # Process each field in the response
            for key, value in response_json.items():
                # Handle list of single characters
                if isinstance(value, list) and all(isinstance(item, str) and len(item) == 1 for item in value):
                    fixed_response[key] = [''.join(value)]
                # Handle dictionary fields
                elif key in ['Media_Coverage_Level', 'Expected_Brand_Impact']:
                    if isinstance(value, str):
                        level_key = "level" if key == "Media_Coverage_Level" else "impact"
                        fixed_response[key] = {
                            level_key: value,
                            "explanation": f"No detailed explanation provided for the {level_key}."
                        }
                    else:
                        fixed_response[key] = value
                # Handle all other fields
                else:
                    fixed_response[key] = value

            print(
                f"Successfully processed chunk {chunk_number} (size {chunk_size})")
            return fixed_response

        except json.JSONDecodeError:
            print(
                f"Invalid JSON response for chunk {chunk_number} (size {chunk_size})")
            return {}

    except Exception as e:
        print(
            f"An error occurred while calling the API for chunk {chunk_number} (size {chunk_size}): {e}")
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
    list_fields = ['Defect_Type']

    # Fields that are dictionaries with explanations
    dict_fields = ['Media_Coverage_Level', 'Expected_Brand_Impact']

    # Fields that should take the first non-empty value
    single_value_fields = [
        'Case_ID', 'Filing_Date', 'Jurisdiction',
        'Number_of_Claimants', 'Outcome',
        'Time_to_Resolution_Months', 'Settlement_Amount',
        'Defense_Cost_Estimate'
    ]

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
                    level_key = "level" if field == "Media_Coverage_Level" else "impact"
                    info[field] = {
                        level_key: info[field],
                        "explanation": f"No detailed explanation provided for the {level_key}."
                    }

                # If this is the first instance or has a better explanation
                if (field not in merged_info or
                    isinstance(merged_info[field], str) or
                    merged_info[field].get('level' if field == 'Media_Coverage_Level' else 'impact') == 'Not specified' or
                        (len(info[field].get('explanation', '')) > len(merged_info[field].get('explanation', '')))):
                    merged_info[field] = info[field]

        # Process single value fields
        for field in single_value_fields:
            if field in info and info[field] and info[field] != "Not specified" and (field not in merged_info or merged_info[field] == "Not specified"):
                merged_info[field] = info[field]

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
            level_key = "level" if field == "Media_Coverage_Level" else "impact"
            merged_info[field] = {
                level_key: "Not specified",
                "explanation": "Insufficient information to determine"
            }
        elif isinstance(merged_info[field], str):
            level_key = "level" if field == "Media_Coverage_Level" else "impact"
            merged_info[field] = {
                level_key: merged_info[field],
                "explanation": f"No detailed explanation provided for the {level_key}."
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
                response_dict["Number_of_Claimants"] = int(
                    response_dict["Number_of_Claimants"])
        except:
            pass

    # Ensure Media_Coverage_Level and Expected_Brand_Impact have the correct structure
    for field in ['Media_Coverage_Level', 'Expected_Brand_Impact']:
        if field in response_dict:
            if isinstance(response_dict[field], str):
                level_key = "level" if field == "Media_Coverage_Level" else "impact"
                response_dict[field] = {
                    level_key: response_dict[field],
                    "explanation": f"No detailed explanation provided for the {level_key}."
                }

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
        # Add a small delay to avoid rate limiting
        if chunk_number > 1:
            time.sleep(0.5)
        return call_gemini_flashlight(chunk, chunk_number, chunk_size)
    except Exception as e:
        print(
            f"Error in process_chunk for chunk {chunk_number} (size {chunk_size}): {e}")
        return {}


def process_with_chunk_size(text, chunk_size, max_workers=4):
    """
    Process the text with a specific chunk size using parallel processing.

    Args:
        text (str): The text to process.
        chunk_size (int): The chunk size to use.
        max_workers (int): Maximum number of parallel workers.

    Returns:
        dict: The merged case information from all chunks.
    """
    chunks = split_text_into_chunks(text, chunk_size)
    print(
        f"Processing {len(chunks)} chunks of size {chunk_size} in parallel (max {max_workers} workers)...")

    # Prepare arguments for parallel processing
    chunk_args = [(chunk, i+1, chunk_size) for i, chunk in enumerate(chunks)]

    # Process chunks in parallel
    all_chunk_info = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all tasks
        future_to_chunk = {executor.submit(
            process_chunk, arg): arg[1] for arg in chunk_args}

        # Collect results as they complete
        for future in concurrent.futures.as_completed(future_to_chunk):
            chunk_number = future_to_chunk[future]
            try:
                chunk_info = future.result()
                all_chunk_info.append(chunk_info)
                print(
                    f"Completed chunk {chunk_number}/{len(chunks)} (size {chunk_size})")
            except Exception as e:
                print(
                    f"Exception processing chunk {chunk_number} (size {chunk_size}): {e}")
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
    chunk_size = 2000
    merged_case_info = process_with_chunk_size(
        extracted_text, chunk_size, max_workers=4)

    # Clean the response
    cleaned_response = clean_response(merged_case_info)

    # Convert to CaseInformation model
    case_info = CaseInformation(**cleaned_response)
    return case_info