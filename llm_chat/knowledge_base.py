import glob
import os
from pathlib import Path

knowledge = {}

def load_knowledge(base_path=None):
    global knowledge
    
    if base_path is None:
        base_path = os.getenv("KNOWLEDGE_BASE_PATH", "knowledge_base")

    if knowledge:  # already loaded
        return

    # Load employees
    for filename in glob.glob(f"{base_path}/employees/*"):
        name = Path(filename).stem.split(' ')[-1]
        with open(filename, "r", encoding="utf-8") as f:
            knowledge[name.lower()] = f.read()

    # Load products
    for filename in glob.glob(f"{base_path}/products/*"):
        name = Path(filename).stem
        with open(filename, "r", encoding="utf-8") as f:
            knowledge[name.lower()] = f.read()


def get_relevant_context(message):
    if not knowledge:
        load_knowledge()

    text = ''.join(ch for ch in message if ch.isalpha() or ch.isspace())
    words = text.lower().split()

    return [knowledge[word] for word in words if word in knowledge]


def additional_context(message):
    relevant_context = get_relevant_context(message)

    if not relevant_context:
        return "There is no additional context relevant to the user's question."

    return (
        "The following additional context might be relevant in answering the user's question:\n\n"
        + "\n\n".join(relevant_context)
    )