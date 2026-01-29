import pandas as pd
import os
import csv

class TextProcessor:
    def __init__(self, input_file, use_ipa):
        self.input_file = input_file
        self.use_ipa = use_ipa

    def create_tts_metadata(self, output_path="data/processed/metadata.csv"):
        """
        Loads the input file, transliterates transcripts to IPA, 
        and saves as a pipe-delimited CSV.
        """
        # Load the spreadsheet
        if self.input_file.endswith('.xlsx'):
            df = pd.read_excel(self.input_file)
        else:
            df = pd.read_csv(self.input_file)

        # Standardizing columns
        # We assume the input has 'Filename' and 'Transcript'
        df = df[['Filename', 'Transcript']].copy()
        
        # Clean the text and apply transliteration
        df['Transcript'] = df['Transcript'].str.strip()
        
        print(">>> Transliterating Abkhaz Cyrillic to IPA...")
        # Apply the ab2ipa function to every row in the Transcript column
        df['IPA_Transcript'] = df['Transcript'].apply(self.ab2ipa)
        
        # Reorder or select columns for the final TTS format
        # Format: filename|original_text|ipa_text
        
        if self.use_ipa:
            final_df = df[['Filename', 'IPA_Transcript']]
        else:
            final_df = df[['Filename', 'Transcript']]
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        # Save with UTF-8 encoding to preserve IPA symbols
        final_df.to_csv(output_path, sep='|', index=False, header=False, encoding='utf-8', quoting=csv.QUOTE_NONE, escapechar='\\')

        print(f">>> Metadata created at {output_path} with {len(df)} entries.")

    def ab2ipa(self, text):
        """
        Transliterates Abkhaz Cyrillic text into IPA based on the standard
        literary alphabet and prosodic punctuation.
        """
        if not isinstance(text, str):
            return ""

        mapping = {
            # Trigraphs
            'Ӷь': 'ʁʲ', 'Ҕь': 'ʁʲ', 'Ӷә': 'ʁʷ', 'Ҕә': 'ʁʷ',
            'Ҟь': 'qʲʼ', 'Ҟә': 'qʷʼ',

            # Digraphs
            'Гь': 'ɡʲ', 'Гә': 'ɡʷ', 'Ӷ': 'ʁ', 'Ҕ': 'ʁ',
            'Дә': 'dʷ', 'Жь': 'ʒ', 'Жә': 'ʒʷ', 'Ӡә': 'd͡ʑʷ',
            'Кь': 'kʼʲ', 'Кә': 'kʷʼ', 'Қь': 'kʲʰ', 'Қә': 'kʷʰ',
            'Ҟ': 'qʼ', 'Ԥ': 'pʰ', 'Ҧ': 'pʰ', 'Тә': 'tʷʼ',
            'Ҭә': 'tʷʰ', 'Хь': 'χʲ', 'Хә': 'χʷ', 'Ҳә': 'ħʷ',
            'Цә': 't͡ɕʷ', 'Ҵә': 't͡ɕʷʼ', 'Шь': 'ʃ', 'Шә': 'ʃʷ',
            'Џь': 'd͡ʒ', 'Ҩ': 'ɥ',

            # Single Letters
            'А': 'a', 'Б': 'b', 'В': 'v', 'Г': 'ɡ', 'Д': 'd',
            'Е': 'e', 'Ж': 'ʐ', 'З': 'z', 'Ӡ': 'd͡z', 'И': 'i',
            'К': 'kʼ', 'Қ': 'kʰ', 'Л': 'l', 'М': 'm', 'Н': 'n',
            'О': 'o', 'П': 'pʼ', 'Р': 'r', 'С': 's', 'Т': 'tʼ',
            'Ҭ': 'tʰ', 'У': 'u', 'Ф': 'f', 'Х': 'χ', 'Ҳ': 'ħ',
            'Ц': 't͡sʰ', 'Ҵ': 't͡sʼ', 'Ч': 't͡ʃʰ', 'Ҷ': 't͡ʃʼ',
            'Ҽ': 't͡ʂʰ', 'Ҿ': 't͡ʂʼ', 'Ш': 'ʂ', 'Ы': 'ə',
            'Џ': 'd͡ʐ', 'Ь': 'ʲ', 'Ә': 'ʷ',

            # IPA Prosodic Punctuation
            # '.': ' ‖', ',': ' |', '?': ' ↗', '!': ' ↘', ' ': ' '
        }

        output = []
        i = 0
        while i < len(text):
            match = None
            for length in [3, 2, 1]:
                substring = text[i:i+length]
                # Capitalize handles most Abkhaz digraphs correctly for lookup
                lookup = substring.capitalize() if length > 1 else substring.upper()

                if lookup in mapping:
                    match = mapping[lookup]
                    i += length
                    break

            if match:
                output.append(match)
            else:
                output.append(text[i])
                i += 1

        return "".join(output).strip()