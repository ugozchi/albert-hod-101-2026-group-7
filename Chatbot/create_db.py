"""
create_vector_db.py - Vector Database Generator for Othello RAG

This script reads the Othello text file, chunks it into smaller segments,
generates embeddings, and stores them in ChromaDB.

Usage:
    python create_vector_db.py
"""

import os
os.environ["ANONYMIZED_TELEMETRY"] = "False"

import re
from chroma_manager import create_collection, get_collection_stats

# Configuration
OTHELLO_FILE = os.path.join("source", "Othello.txt")
CHUNK_SIZE = 400  # Target chunk size in words
CHUNK_OVERLAP = 50  # Overlap between chunks in words


def load_othello_text(filepath: str) -> str:
    """
    Load the Othello text from a file.
    
    Args:
        filepath: Path to the Othello text file
        
    Returns:
        str: The full text content
        
    Raises:
        FileNotFoundError: If the file doesn't exist
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(
            f"❌ File '{filepath}' not found.\n"
            f"Please download Othello from https://www.gutenberg.org/ "
            f"and save it as '{filepath}'"
        )
    
    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()
    
    print(f"📖 Loaded {len(text)} characters from {filepath}")
    return text


def clean_text(text: str) -> str:
    """
    Clean and normalize the text.
    
    Args:
        text: Raw text content
        
    Returns:
        str: Cleaned text
    """
    # Remove Gutenberg header/footer
    start_markers = ["*** START OF", "***START OF"]
    end_markers = ["*** END OF", "***END OF", "End of Project Gutenberg"]
    
    for marker in start_markers:
        if marker in text:
            text = text.split(marker, 1)[-1]
            text = text.split("\n", 1)[-1] if "\n" in text else text
    
    for marker in end_markers:
        if marker in text:
            text = text.split(marker, 1)[0]
    
    # Normalize whitespace
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r' +', ' ', text)
    
    return text.strip()


def extract_scenes(text: str) -> list:
    """
    Extract scenes from the play for metadata.
    
    Args:
        text: The cleaned play text
        
    Returns:
        list: List of (scene_marker, start_position) tuples
    """
    scene_pattern = r'(ACT [IVX]+[.,]?\s*SCENE [IVX0-9]+)'
    
    scenes = []
    for match in re.finditer(scene_pattern, text, re.IGNORECASE):
        scenes.append((match.group(1).strip(), match.start()))
    
    return scenes


def get_scene_for_position(position: int, scenes: list) -> str:
    """
    Get the scene name for a given text position.
    
    Args:
        position: Character position in text
        scenes: List of (scene_marker, start_position) tuples
        
    Returns:
        str: Scene name (e.g., "ACT I, SCENE 1")
    """
    current_scene = "Prologue"
    
    for scene_name, scene_start in scenes:
        if position >= scene_start:
            current_scene = scene_name
        else:
            break
    
    return current_scene


def split_into_chunks(text: str, chunk_size: int = CHUNK_SIZE, 
                      overlap: int = CHUNK_OVERLAP) -> list:
    """
    Split text into overlapping chunks by word count.
    
    Args:
        text: The text to chunk
        chunk_size: Target number of words per chunk
        overlap: Number of overlapping words between chunks
        
    Returns:
        list: List of (chunk_text, start_char, end_char) tuples
    """
    words = text.split()
    chunks = []
    
    if len(words) == 0:
        return chunks
    
    start_word = 0
    while start_word < len(words):
        end_word = min(start_word + chunk_size, len(words))
        chunk_words = words[start_word:end_word]
        chunk_content = " ".join(chunk_words)
        
        # Calculate character positions (approximate)
        start_char = len(" ".join(words[:start_word])) + (1 if start_word > 0 else 0)
        end_char = start_char + len(chunk_content)
        
        chunks.append((chunk_content, start_char, end_char))
        
        # Move to next chunk with overlap
        start_word += chunk_size - overlap
        
        if end_word >= len(words):
            break
    
    return chunks


def create_database():
    """
    Main function to create the ChromaDB vector database.
    
    This function:
    1. Loads and cleans the Othello text
    2. Extracts scene information
    3. Chunks the text
    4. Creates embeddings and stores in ChromaDB
    """
    print("=" * 60)
    print("🎭 Othello RAG - Vector Database Generator")
    print("=" * 60)
    
    # Load text
    print("\n📚 Loading Othello text...")
    raw_text = load_othello_text(OTHELLO_FILE)
    
    # Check if file has content
    if len(raw_text) == 0:
        print("❌ ERROR: The file is empty!")
        print(f"   Please download Othello from: https://www.gutenberg.org/cache/epub/1531/pg1531.txt")
        print(f"   And save it to: {OTHELLO_FILE}")
        return
    
    # Clean text
    print("🧹 Cleaning text...")
    cleaned_text = clean_text(raw_text)
    print(f"   Cleaned text: {len(cleaned_text)} characters")
    
    if len(cleaned_text) == 0:
        print("❌ ERROR: Text is empty after cleaning!")
        return
    
    # Extract scenes
    print("🎬 Extracting scenes...")
    scenes = extract_scenes(cleaned_text)
    print(f"   Found {len(scenes)} scenes")
    
    # Chunk text
    print(f"✂️ Chunking text (size={CHUNK_SIZE}, overlap={CHUNK_OVERLAP})...")
    chunks = split_into_chunks(cleaned_text, CHUNK_SIZE, CHUNK_OVERLAP)
    print(f"   Created {len(chunks)} chunks")
    
    if len(chunks) == 0:
        print("❌ ERROR: No chunks created!")
        return
    
    # Prepare data for ChromaDB
    print("📦 Preparing data for ChromaDB...")
    documents = []
    metadatas = []
    ids = []
    
    for i, (text_chunk, start_char, end_char) in enumerate(chunks):
        scene = get_scene_for_position(start_char, scenes)
        
        documents.append(text_chunk)
        metadatas.append({
            "source": "Othello",
            "author": "William Shakespeare",
            "scene": scene,
            "chunk_index": i,
            "start_char": start_char,
            "end_char": end_char,
            "word_count": len(text_chunk.split())
        })
        ids.append(f"othello_chunk_{i:04d}")
    
    # Create ChromaDB collection
    print("\n🧠 Creating ChromaDB collection with embeddings...")
    print("   (This may take a moment...)")
    
    create_collection(documents, metadatas, ids)
    
    # Verify
    print("\n✅ Database created successfully!")
    stats = get_collection_stats()
    if stats:
        print(f"   Collection: {stats['name']}")
        print(f"   Total chunks: {stats['count']}")
    
    print("\n" + "=" * 60)
    print("🎉 Done! You can now run the Streamlit app.")
    print("   Command: streamlit run main.py")
    print("=" * 60)


if __name__ == "__main__":
    create_database()