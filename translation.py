from googletrans import Translator

def translate_text_file(input_path, output_path, target_language='es'):
    """Translate the content of a text file to the target language and save it."""
    translator = Translator()
    
    with open(input_path, 'r', encoding='utf-8') as file:
        text = file.read()
    
    # Translate the text
    translated = translator.translate(text, dest=target_language)
    
    # Save the translated text to the output file
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(translated.text)

    print(f"Translation complete. Translated text saved to {output_path}")
