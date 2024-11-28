from datetime import datetime
from langdetect import detect, LangDetectException
from helpers import insert_poem, fetch_all_poems, delete_poem_by_id

def detect_language(content):
    try:
        return detect(content)
    except LangDetectException:
        return "en"  # Default to English if detection fails

def add_poem(language, title, content):
    date_added = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    insert_poem(language, title.strip(), content.strip(), date_added)
    print(f"Poem '{title}' added to {language} database successfully!")

def show_all_poems(language):
    poems = fetch_all_poems(language)
    poem_list = []
    
    if poems:
        for poem in poems:
            poem_dict = {
                'id': poem[0],
                'title': poem[1],
                'content': poem[2],
                'date_added': poem[3],
                'language': poem[4]
            }
            poem_list.append(poem_dict)
            
        return poem_list
    else:
        print("No poems found for language:", language)  # Debugging line
        return []  # Ensure this returns an empty list if no poems found

def delete_poem(language, poem_id):
    affected_rows = delete_poem_by_id(language, poem_id)
    if affected_rows > 0:
        print(f"Poem with ID {poem_id} deleted successfully.")
    else:
        print(f"No poem found with ID {poem_id}.")
