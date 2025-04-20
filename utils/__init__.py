import json
import os

def load_story_data(json_path: str = None):
    """
    Load the story pages from story.json and normalize image paths.
    
    By default, looks for data/story.json in the project root.
    Ensures that page["image"] always begins with "imagess/".
    """
    # Determine default path to story.json
    if json_path is None:
        # __file__ is utils/__init__.py; go up to the project root
        project_root = os.path.dirname(os.path.dirname(__file__))
        json_path = os.path.join(project_root, "data", "story.json")

    # Load JSON
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Normalize image paths
    for page in data:
        img = page.get("image", "")
        # If it's just a filename (no folder), prefix with imagess/
        if os.path.basename(img) == img:
            page["image"] = os.path.join("imagess", img)

    return data
