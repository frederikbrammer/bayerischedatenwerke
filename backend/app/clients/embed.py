import torch
import torch.nn.functional as F
from torch import Tensor
from transformers import AutoTokenizer, AutoModel
import json
import os
import numpy as np
from typing import List, Dict, Any, Tuple
from app.db.database import get_all_cases

def average_pool(last_hidden_states: Tensor, attention_mask: Tensor) -> Tensor:
    last_hidden = last_hidden_states.masked_fill(~attention_mask[..., None].bool(), 0.0)
    return last_hidden.sum(dim=1) / attention_mask.sum(dim=1)[..., None]

def find_similar(query_case: Dict[str, Any], threshold: float = 0.5, top_k: int = 5) -> Dict[str, Any]:
    """
    Find the most similar cases to a query case, write them into the case, and return the case
    
    Args:
        query_case: The case to find similar cases for
        threshold: Minimum similarity score to include a case
        top_k: Maximum number of similar cases to return
        
    Returns:
        The query case with similar case IDs added
    """
    # Get all cases
    case_database = get_all_cases()
    
    # Get query embedding
    if "caseEmbedding" not in query_case:
        query_case = embed(query_case)
    
    query_embedding = query_case["caseEmbedding"]
    query_embedding_tensor = torch.tensor(query_embedding)
    
    # Calculate similarity scores
    similarities = []
    for case in case_database:
        # Skip the query case itself if it's in the database
        if case.get("caseId") == query_case.get("caseId"):
            continue
            
        # Add embedding to case if it doesn't have one
        if "caseEmbedding" not in case:
            case = embed(case)
            
        case_embedding = case["caseEmbedding"]
        case_embedding_tensor = torch.tensor(case_embedding)
        
        # Calculate cosine similarity
        similarity = torch.nn.functional.cosine_similarity(
            query_embedding_tensor.unsqueeze(0), 
            case_embedding_tensor.unsqueeze(0)
        ).item()
        
        # Only include cases above the threshold
        if similarity >= threshold:
            similarities.append((case.get("caseId"), similarity))
    
    # Sort by similarity (highest first)
    similarities.sort(key=lambda x: x[1], reverse=True)
    
    # Get top k similar case IDs
    similar_case_ids = [case_id for case_id, _ in similarities[:top_k]]
    
    # Add similar case IDs to the query case
    query_case["similarCases"] = similar_case_ids
    
    return query_case

def embed(case_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Add embedding to a case and return it
    
    Args:
        case_data: The case data to embed
        
    Returns:
        The case data with embedding added
    """
    # Use MPS (Metal Performance Shaders) if available, otherwise use CPU or CUDA
    device = torch.device("cuda" if torch.cuda.is_available() else 
                         "mps" if torch.backends.mps.is_available() else "cpu")
    
    # Extract case components
    laws_affected = case_data.get("lawsAffected", [])
    plaintiff_arguments = case_data.get("plaintiffArgumentation", [])
    evidence_items = case_data.get("evidence", [])
    
    # Format the input text for embedding
    laws_text = "Laws: " + "; ".join(laws_affected) if laws_affected else ""
    arguments_text = "Arguments: " + "; ".join(plaintiff_arguments) if plaintiff_arguments else ""
    
    evidence_text = "Evidence: "
    for item in evidence_items:
        evidence_text += f"{item.get('text', '')}; "
    
    # Combine all components into a single query text
    case_text = f"query: {laws_text} {arguments_text} {evidence_text}"
    
    # Load the model and tokenizer
    tokenizer = AutoTokenizer.from_pretrained('intfloat/multilingual-e5-large')
    model = AutoModel.from_pretrained('intfloat/multilingual-e5-large').to(device)
    
    # Tokenize the input text
    inputs = tokenizer([case_text], max_length=512, padding=True, truncation=True, return_tensors='pt')
    inputs = {k: v.to(device) for k, v in inputs.items()}
    
    # Generate embeddings
    with torch.no_grad():
        outputs = model(**inputs)
    
    # Average pool and normalize
    embedding = average_pool(outputs.last_hidden_state, inputs["attention_mask"])
    embedding = F.normalize(embedding, p=2, dim=1)
    
    # Convert embedding to list for storage
    embedding_list = embedding[0].cpu().numpy().tolist()
    
    # Add embedding to case data
    case_data["caseEmbedding"] = embedding_list
    
    return case_data
