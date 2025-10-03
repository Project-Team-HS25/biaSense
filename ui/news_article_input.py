# ui/user_input.py

from business_logic.text_cleaner import TextCleaner

def main():
    cleaner = TextCleaner()
    user_text = input("Bitte gib deinen Text ein: ")
    cleaned_text = cleaner.remove_stopwords(user_text)
    print("\nBereinigter Text:")
    print(cleaned_text)

if __name__ == "__main__":
    main()