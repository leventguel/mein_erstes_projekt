from poem_operations import add_poem, show_all_poems, delete_poem
from translations import MENU_TRANSLATIONS

def run_cli():
    language = "en"  # Default session language
    translations = MENU_TRANSLATIONS[language]

    while True:
        print("\n" + translations['menu_title'])
        print(translations['add_poem'])
        print(translations['show_all'])
        print(translations['delete_poem'])
        print(translations['change_language'])
        print(translations['exit'])

        choice = input(translations['choose_action'])

        if choice == '1':
            title = input(translations['add_poem'] + ": ")
            content = input("Enter poem content: ")
            add_poem(language, title, content)
        elif choice == '2':
            show_all_poems(language)
        elif choice == '3':
            poem_id = input("Enter poem ID to delete: ").strip()
            if poem_id.isdigit():
                delete_poem(language, int(poem_id))
            else:
                print("Invalid ID. Please try again.")
        elif choice == '4':
            print("Available languages:", ", ".join(MENU_TRANSLATIONS.keys()))
            new_language = input("Enter the language code (e.g., 'en', 'de', 'fr'): ").strip()
            if new_language in MENU_TRANSLATIONS:
                language = new_language
                translations = MENU_TRANSLATIONS[language]
                print(f"Language switched to {language}.")
            else:
                print("Invalid language code. Language remains unchanged.")
        elif choice == '5':
            print(translations['exit'])
            break
        else:
            print("Invalid choice. Please try again.")
