# Navigation Data Processor for RAG Integration

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List, Tuple


NAVIGATION_DATA_PATH = Path(__file__).resolve().parents[1] / "dataset" / "navigation" / "navigation_data.json"
OUTPUT_DIR = Path(__file__).resolve().parents[1] / "dataset" / "processed"


def load_navigation_data(path: Path = NAVIGATION_DATA_PATH) -> Dict:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def format_list_or_value(value) -> str:
    if isinstance(value, list):
        return "\n".join(f"  • {item}" for item in value)
    elif isinstance(value, dict):
        lines = []
        for k, v in value.items():
            if isinstance(v, dict):
                lines.append(f"  {k}:")
                for kk, vv in v.items():
                    lines.append(f"    - {kk}: {vv}")
            elif isinstance(v, list):
                lines.append(f"  {k}: {', '.join(str(i) for i in v)}")
            else:
                lines.append(f"  {k}: {v}")
        return "\n".join(lines)
    else:
        return str(value) if value else "Not specified"


def format_steps(steps: List[str]) -> str:
    formatted = []
    for i, step in enumerate(steps, 1):
        # Handle indented sub-steps
        if step.strip().startswith(("1.", "2.", "3.", "4.", "5.", "6.", "7.", "8.", "9.")):
            formatted.append(f"     {step.strip()}")
        else:
            formatted.append(f"  {i}. {step}")
    return "\n".join(formatted)


def service_to_text(service: Dict) -> str:
    
    parts = []
    
    # Title and Category
    parts.append(f"SERVICE: {service.get('service_name', 'Unknown Service')}")
    parts.append(f"Category: {service.get('category', 'General')}")
    
    # Description
    if service.get('description'):
        parts.append(f"\nDescription: {service['description']}")
    
    # Keywords for better search matching
    if service.get('keywords'):
        keywords = service['keywords']
        if isinstance(keywords, list):
            parts.append(f"Keywords: {', '.join(keywords)}")
    
    # Department and Contact Info
    parts.append(f"\nDepartment: {service.get('department', 'Not specified')}")
    
    if service.get('office_address'):
        parts.append(f"Office Address: {service['office_address']}")
    
    phone = service.get('phone_number')
    if phone:
        if isinstance(phone, list):
            parts.append(f"Phone: {', '.join(phone)}")
        elif phone != "NIL":
            parts.append(f"Phone: {phone}")
    
    if service.get('online_link') and service['online_link'] != "NIL":
        parts.append(f"Online Portal: {service['online_link']}")
    
    # Steps - Most important for navigation queries
    if service.get('steps'):
        parts.append(f"\nHow to Apply / Process Steps:")
        parts.append(format_steps(service['steps']))
    
    # Alternative methods if available
    if service.get('alternative_method'):
        alt = service['alternative_method']
        parts.append(f"\nAlternative Method ({alt.get('method', 'Other')}):")
        if alt.get('steps'):
            parts.append(format_steps(alt['steps']))
    
    if service.get('alternative_methods'):
        for alt in service['alternative_methods']:
            parts.append(f"\nAlternative Method ({alt.get('method', 'Other')}):")
            if alt.get('steps'):
                parts.append(format_steps(alt['steps']))
    
    # Documents Required
    if service.get('documents_required'):
        parts.append(f"\nDocuments Required:")
        parts.append(format_list_or_value(service['documents_required']))
    
    # Cost
    if service.get('cost'):
        parts.append(f"\nCost/Fees:")
        parts.append(format_list_or_value(service['cost']))
    
    # Time Required
    if service.get('time_required'):
        parts.append(f"\nTime Required: {service['time_required']}")
    
    # Notes
    if service.get('notes'):
        parts.append(f"\nImportant Notes:")
        parts.append(format_list_or_value(service['notes']))
    
    return "\n".join(parts)


def service_to_metadata(service: Dict) -> Dict:
    return {
        "type": "navigation",
        "service_name": service.get("service_name", "Unknown"),
        "category": service.get("category", "General"),
        "department": service.get("department", ""),
        "keywords": service.get("keywords", []),
        "online_link": service.get("online_link", ""),
        "phone_number": service.get("phone_number", ""),
        "office_address": service.get("office_address", ""),
        "filename": "navigation_data.json",
        "title": service.get("service_name", "Unknown Service"),
    }


def process_navigation_data() -> Tuple[List[str], List[Dict]]:

    data = load_navigation_data()
    services = data.get("services", [])
    
    texts = []
    metadatas = []
    
    for service in services:
        text = service_to_text(service)
        metadata = service_to_metadata(service)
        texts.append(text)
        metadatas.append(metadata)
    
    return texts, metadatas


def save_navigation_chunks(output_dir: Path = OUTPUT_DIR) -> None:

    texts, metadatas = process_navigation_data()
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Save in similar format to legal chunks
    chunks_data = {
        "metadata": {
            "type": "navigation",
            "filename": "navigation_data.json",
            "title": "Nepal Government Services Navigation Guide",
            "country": "Nepal",
        },
        "chunks": texts,
        "chunk_metadata": metadatas,  # Per-chunk metadata
    }
    
    output_path = output_dir / "navigation_data_chunks.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(chunks_data, f, ensure_ascii=False, indent=2)
    
    print(f" Saved {len(texts)} navigation chunks to {output_path}")
    return output_path


if __name__ == "__main__":
    print("Processing navigation data...")
    texts, metas = process_navigation_data()
    print(f"Processed {len(texts)} services")
    
    # Preview first service
    if texts:
        print("\ Sample Chunk ---")
        print(texts[0][:1000])
        print("...")
    
    # Save chunks
    save_navigation_chunks()
