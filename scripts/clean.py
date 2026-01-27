import argparse
import json
import os
import re
from pathlib import Path
from typing import Dict, List, Optional

# Primary extractor
from pypdf import PdfReader

try:
    import fitz  # PyMuPDF
    HAS_PYMUPDF = True
except Exception:
    HAS_PYMUPDF = False


def extract_text_pypdf(pdf_path: Path) -> str:
    # Extracts text from a PDF using pypdf.
    # Returns an empty string if no extractable text.
    
    try:
        reader = PdfReader(str(pdf_path))
        parts: List[str] = []
        for page in reader.pages:
            txt = page.extract_text() or ""
            if txt:
                parts.append(txt)
        return "\n".join(parts)
    except Exception as e:
        raise RuntimeError(f"Failed to read {pdf_path}: {e}")


def extract_text_pymupdf(pdf_path: Path) -> str:
    # Extract text via PyMuPDF.
    if not HAS_PYMUPDF:
        return ""
    try:
        doc = fitz.open(str(pdf_path))
        parts: List[str] = []
        for page in doc:
            parts.append(page.get_text("text") or "")
        return "\n".join(parts)
    except Exception:
        return ""


def extract_metadata(text: str, filename: str) -> Dict[str, str]:
    # Extract metadata from legal documents (Act name, number, date, etc.)
    metadata = {"filename": filename}
    
    # Extract Act name from title (first few lines)
    lines = text.split("\n")[:10]
    for line in lines:
        # Match Act titles
        if "Act" in line and len(line.strip()) > 10:
            metadata["title"] = line.strip()
            break
    
    # Extract Act number
    act_num = re.search(r"Act number\s+(\d+)\s+of\s+the\s+year\s+(\d+)", text, re.IGNORECASE)
    if act_num:
        metadata["act_number"] = act_num.group(1)
        metadata["year"] = act_num.group(2)
    
    # Extract date
    date_match = re.search(r"Date of (Authentication|Publication)[^\n]*\n([^\n]+)", text, re.IGNORECASE)
    if date_match:
        metadata["date"] = date_match.group(2).strip()
    
    return metadata


def clean_text_minimal(text: str) -> str:
    # Minimal cleaning: trim lines and remove empty ones.
    cleaned = "\n".join(line.strip() for line in text.splitlines())
    cleaned = "\n".join([l for l in cleaned.split("\n") if l.strip()])
    return cleaned.strip()


def fix_broken_words(text: str) -> str:
    # Fix words broken by PDF extraction with spaces in wrong places.
   
    fixes = {
        # Words with space before last 1-3 letters
        r'\bA ct\b': 'Act',
        r'\bof fence': 'offence',
        r'\bOf fence': 'Offence',
        r'\ba ct\b': 'act',
        r'\bth is\b': 'this',
        r'\bTh is\b': 'This',
        r'\bth at\b': 'that',
        r'\bTh at\b': 'That',
        r'\bth e\b': 'the',
        r'\bTh e\b': 'The',
        r'\bwh ich\b': 'which',
        r'\bWh ich\b': 'Which',
        r'\bsh all\b': 'shall',
        r'\bSh all\b': 'Shall',
        r'\bwh o\b': 'who',
        r'\bWh o\b': 'Who',
        r'\ba nd\b': 'and',
        r'\bA nd\b': 'And',
        r'\bor der\b': 'order',
        r'\bOr der\b': 'Order',
        r'\bin to\b': 'into',
        r'\bIn to\b': 'Into',
        r'\bhe lp': 'help',
        r'\bHe lp': 'Help',
        r'\bshe lter': 'shelter',
        r'\bShe lter': 'Shelter',
        r'\ba ny\b': 'any',
        r'\bA ny\b': 'Any',
        r'\bma y\b': 'may',
        r'\bMa y\b': 'May',
        r'\bbe ing\b': 'being',
        r'\bBe ing\b': 'Being',
        r'\ba lso\b': 'also',
        r'\bA lso\b': 'Also',
        r'\bin cludes?\b': 'include',
        r'\bIn cludes?\b': 'Include',
        r'\ba uthoriz': 'authoriz',
        r'\bA uthoriz': 'Authoriz',
        r'\ba uthority': 'authority',
        r'\bA uthority': 'Authority',
        r'\ba pprehension': 'apprehension',
        r'\bA pprehension': 'Apprehension',
        r'\ba ssist': 'assist',
        r'\bA ssist': 'Assist',
        r'\ba mend': 'amend',
        r'\bA mend': 'Amend',
        r'\ba mong': 'among',
        r'\bA mong': 'Among',
        r'\ba pplic': 'applic',
        r'\bA pplic': 'Applic',
        r'\ba rticle': 'article',
        r'\bA rticle': 'Article',
        r'\ba rms\b': 'arms',
        r'\bA rms\b': 'Arms',
        r'\ba mmunition': 'ammunition',
        r'\bA mmunition': 'Ammunition',
        r'\ba ircraft': 'aircraft',
        r'\bA ircraft': 'Aircraft',
        r'\ba bandon': 'abandon',
        r'\bA bandon': 'Abandon',
        r'\ba betment': 'abetment',
        r'\bA betment': 'Abetment',
        r'\ba gainst': 'against',
        r'\bA gainst': 'Against',
        r'\ba djudic': 'adjudic',
        r'\bA djudic': 'Adjudic',
        r'\ba dult': 'adult',
        r'\bA dult': 'Adult',
        r'\bfor gery': 'forgery',
        r'\bFor gery': 'Forgery',
        r'\bimprison ment': 'imprisonment',
        r'\bImprison ment': 'Imprisonment',
        r'\bhe inous': 'heinous',
        r'\bHe inous': 'Heinous',
        r'\bat tempt': 'attempt',
        r'\bAt tempt': 'Attempt',
        r'\bin cest': 'incest',
        r'\bIn cest': 'Incest',
        r'\bin terest': 'interest',
        r'\bIn terest': 'Interest',
        r'\bin tent': 'intent',
        r'\bIn tent': 'Intent',
        r'\bmainta in\b': 'maintain',
        r'\bMainta in\b': 'Maintain',
        r'\bsup ply': 'supply',
        r'\bSup ply': 'Supply',
        r'\bthe refore': 'therefore',
        r'\bThe refore': 'Therefore',
        r'\bharb or': 'harbor',
        r'\bHarb or': 'Harbor',
        r'\bExtr a': 'Extra',
        r'\bextr a': 'extra',
        r'\bL evel': 'Level',
        r'\bl evel': 'level',
        r'\bL ocal': 'Local',
        r'\bl ocal': 'local',

        # Common concatenations
        r'\bofthe\b': 'of the',
        r'\btothe\b': 'to the',
        r'\binthe\b': 'in the',
        r'\bforthe\b': 'for the',
        r'\bandthe\b': 'and the',
        r'\borthe\b': 'or the',
        r'\bbythe\b': 'by the',
        r'\bonthe\b': 'on the',
        r'\batthe\b': 'at the',
        r'\basthe\b': 'as the',
        r'\bifthe\b': 'if the',
    }
    
    for pattern, replacement in fixes.items():
        text = re.sub(pattern, replacement, text)
    
    return text


def clean_text_aggressive(text: str) -> str:
    # Aggressive cleaning: remove headers/footers, URLs, fix hyphenation and spacing.


    # Remove URLs
    text = re.sub(r"www\.[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", "", text)
    text = re.sub(r"https?://[^\s]+", "", text)
    
    # Remove explicit "Page X of Y" markers
    text = re.sub(r"Page \d+ of \d+", "", text, flags=re.IGNORECASE)
    
    # Fix broken hyphenated words split across lines
    text = re.sub(r"(\w)-\s*\n\s*(\w)", r"\1\2", text)
    text = re.sub(r"(\w)-\s+(\w)", r"\1\2", text)
    
    # Apply word fixes
    text = fix_broken_words(text)
    
    # Fix concatenated words with capital letters (CamelCase to separate words)
    text = re.sub(r"([a-z])([A-Z])", r"\1 \2", text)
    
    # Process line by line to drop likely headers/footers and TOC-like lines
    lines = text.split("\n")
    cleaned_lines: List[str] = []
    for line in lines:
        s = line.strip()
        if len(s) < 5:
            continue
        # Skip lines that look like TOC entries with dots
        if re.match(r"^.*\.{3,}.*\d+$", s):
            continue
        # Skip lines that are just page numbers
        if re.match(r"^\d+$", s):
            continue
        # Skip repeated dashes or underscores (page separators)
        if re.match(r"^[-_=]{3,}$", s):
            continue
        cleaned_lines.append(s)
    
    text = "\n".join(cleaned_lines)
    
    # Fix multiple spaces
    text = re.sub(r" {2,}", " ", text)
    
    # Normalize multiple blank lines to max 2
    text = re.sub(r"\n{3,}", "\n\n", text)
    
    return text.strip()


def normalize_whitespace_single_space(text: str) -> str:
    # Normalize all whitespace to single spaces (loses line breaks).
    return re.sub(r"\s+", " ", text).strip()


def preserve_legal_structure(text: str) -> str:
    # Preserve legal document structure (sections, subsections, clauses).
    lines = text.split("\n")
    structured_lines = []
    
    for line in lines:
        s = line.strip()
        
        # Add extra spacing before major sections
        if re.match(r"^(Part|Chapter|Section|Article)\s*[-:]?\s*\d+", s, re.IGNORECASE):
            structured_lines.append("\n" + s)
        # Preserve subsections with proper formatting
        elif re.match(r"^\(?\d+\)?\.?\s+", s) or re.match(r"^\([a-z]\)", s):
            structured_lines.append(s)
        else:
            structured_lines.append(s)
    
    return "\n".join(structured_lines).strip()


def prepare_for_rag(text: str, chunk_size: int = 2000, overlap: int = 400, min_chunk_size: int = 100) -> List[str]:
    # Split text into overlapping chunks suitable for RAG embedding.
    # Larger chunks preserve more context for better retrieval.

    # Split by major sections first to keep context together
    major_sections = re.split(r"\n(?=(?:Part|Chapter|Section|Article)\s*[-:]?\s*\d+)", text)
    
    chunks = []
    current_accumulated = ""
    
    for section in major_sections:
        section = section.strip()
        if not section:
            continue
            
        # If section is very small, accumulate with next section
        if len(section) < min_chunk_size:
            current_accumulated += "\n" + section if current_accumulated else section
            continue
        
        # Add any accumulated small sections to this section
        if current_accumulated:
            section = current_accumulated + "\n" + section
            current_accumulated = ""
        
        if len(section) <= chunk_size:
            chunks.append(section)
        else:
            # Split large sections into smaller chunks with overlap
            words = section.split()
            current_chunk = []
            current_length = 0
            
            for word in words:
                current_chunk.append(word)
                current_length += len(word) + 1
                
                if current_length >= chunk_size:
                    chunk_text = " ".join(current_chunk)
                    chunks.append(chunk_text)
                    # Keep last part for overlap
                    overlap_words = int(len(current_chunk) * (overlap / chunk_size))
                    current_chunk = current_chunk[-overlap_words:]
                    current_length = sum(len(w) + 1 for w in current_chunk)
            
            if current_chunk:
                remaining = " ".join(current_chunk)
                # Only add if it's substantial enough
                if len(remaining) >= min_chunk_size:
                    chunks.append(remaining)
                elif chunks:
                    # Append to previous chunk if too small
                    chunks[-1] = chunks[-1] + " " + remaining
    
    # Handle any remaining accumulated content
    if current_accumulated and len(current_accumulated) >= min_chunk_size:
        if chunks:
            chunks[-1] = chunks[-1] + "\n" + current_accumulated
        else:
            chunks.append(current_accumulated)
    
    # Filter out any chunks that are still too small or are just headers/TOC
    filtered_chunks = []
    for c in chunks:
        c = c.strip()
        if len(c) >= min_chunk_size and not _is_toc_or_header_only(c):
            filtered_chunks.append(c)
    
    return filtered_chunks


def _is_toc_or_header_only(text: str) -> bool:
    # Check if text is just table of contents or headers without substantive content.
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    if not lines:
        return True
    
    # If most lines are short (likely headers), it's probably TOC
    short_lines = sum(1 for l in lines if len(l) < 50)
    if len(lines) > 3 and short_lines / len(lines) > 0.8:
        return True
    
    # Check for common TOC patterns
    toc_patterns = [
        r"^(Part|Chapter|Section|Article|Schedule)\s*[-:]?\s*\d*\s*$",
        r"^Table of Contents$",
    ]
    toc_line_count = 0
    for line in lines:
        for pattern in toc_patterns:
            if re.match(pattern, line, re.IGNORECASE):
                toc_line_count += 1
                break
    
    if len(lines) > 0 and toc_line_count / len(lines) > 0.5:
        return True
    
    return False


def save_text(output_path: Path, text: str) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(text, encoding="utf-8")


def extract_text_with_engine(pdf: Path, engine: str) -> str:
    # Extract text using the selected engine: pypdf, pymupdf, or auto fallback.
    engine = engine.lower()
    if engine == "pypdf":
        return extract_text_pypdf(pdf)
    if engine == "pymupdf":
        if not HAS_PYMUPDF:
            raise RuntimeError("fitz not installed;")
        return extract_text_pymupdf(pdf)

    raw = extract_text_pypdf(pdf)
    if raw.strip():
        return raw
    if HAS_PYMUPDF:
        return extract_text_pymupdf(pdf)
    return raw


def process_pdfs(
    input_dir: Path,
    output_dir: Path,
    merge: bool,
    engine: str,
    aggressive: bool,
    normalize_ws: bool,
    preserve_structure: bool = True,
    create_chunks: bool = False,
    chunk_size: int = 1000,
) -> Path:
    pdf_files = sorted([p for p in input_dir.glob("**/*.pdf") if p.is_file()])
    if not pdf_files:
        print(f"No PDFs found in {input_dir}")
        return output_dir / "combined.txt"

    combined_parts: List[str] = []
    all_metadata: List[Dict] = []

    for pdf in pdf_files:
        print(f"Extracting: {pdf}")
        raw = extract_text_with_engine(pdf, engine)
        if not raw.strip():
            print(f"Warning: No text extracted  {pdf}")
            continue

        # Extract metadata
        metadata = extract_metadata(raw, pdf.name)
        all_metadata.append(metadata)

        # Clean text
        cleaned = clean_text_aggressive(raw) if aggressive else clean_text_minimal(raw)
        
        if preserve_structure and not normalize_ws:
            cleaned = preserve_legal_structure(cleaned)
        
        if normalize_ws:
            cleaned = normalize_whitespace_single_space(cleaned)

        # Save main text file
        out_path = output_dir / (pdf.stem + ".txt")
        save_text(out_path, cleaned)
        print(f"Saved: {out_path}")

        # Save metadata
        metadata_path = output_dir / (pdf.stem + "_metadata.json")
        with open(metadata_path, "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)

        # Create chunks for RAG if requested
        if create_chunks:
            chunks = prepare_for_rag(cleaned, chunk_size=chunk_size)
            chunks_path = output_dir / (pdf.stem + "_chunks.json")
            with open(chunks_path, "w", encoding="utf-8") as f:
                json.dump({
                    "metadata": metadata,
                    "chunks": chunks,
                    "total_chunks": len(chunks)
                }, f, indent=2, ensure_ascii=False)
            print(f"Created {len(chunks)} chunks: {chunks_path}")

        if merge:
            header = f"===== SOURCE: {pdf.name} ====="
            combined_parts.append(header)
            combined_parts.append(cleaned)

    # Save combined metadata
    if all_metadata:
        metadata_summary_path = output_dir / "all_metadata.json"
        with open(metadata_summary_path, "w", encoding="utf-8") as f:
            json.dump(all_metadata, f, indent=2, ensure_ascii=False)
        print(f"Saved metadata summary: {metadata_summary_path}")

    combined_path = output_dir / "combined.txt"
    if merge:
        save_text(combined_path, "\n\n".join(combined_parts))
        print(f"Merged file: {combined_path}")

    return combined_path


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Extract and clean text from legal PDFs for RAG chatbot.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
       
    )
    parser.add_argument("--input", default=str(Path("dataset") / "raw"))
    parser.add_argument("--output", default=str(Path("dataset") / "processed"))
    parser.add_argument("--merge", action="store_true")
    parser.add_argument(
        "--engine",
        choices=["auto", "pypdf", "pymupdf"],
        default="auto",
        help="Text extraction engine",
    )
    parser.add_argument(
        "--aggressive-clean",
        action="store_true",
        help="Apply aggressive cleaning",
    )
    parser.add_argument(
        "--normalize-whitespace",
        action="store_true",
        help="Normalize all whitespace",
    )
    parser.add_argument(
        "--no-preserve-structure",
        action="store_true",
        help="Disable legal structure preservation (Parts, Chapters, Sections)",
    )
    parser.add_argument(
        "--create-chunks",
        action="store_true",
        help="Create JSON files",
    )
    parser.add_argument(
        "--chunk-size",
        type=int,
        default=2000,
        help="Character size for RAG chunks (default: 2000)",
    )

    args = parser.parse_args()

    input_dir = Path(args.input)
    output_dir = Path(args.output)

    if not input_dir.exists():
        raise FileNotFoundError(f"Input folder not found: {input_dir}")


    print(f"Input: {input_dir}")
    print(f"Output: {output_dir}")
    print(f"Aggressive cleaning: {args.aggressive_clean}")
    print(f"Create chunks: {args.create_chunks}")
    if args.create_chunks:
        print(f"Chunk size: {args.chunk_size} characters")
    print()

    process_pdfs(
        input_dir=input_dir,
        output_dir=output_dir,
        merge=args.merge,
        engine=args.engine,
        aggressive=args.aggressive_clean,
        normalize_ws=args.normalize_whitespace,
        preserve_structure=not args.no_preserve_structure,
        create_chunks=args.create_chunks,
        chunk_size=args.chunk_size,
    )
    
    print("\n Processing complete!")


if __name__ == "__main__":
    main()
