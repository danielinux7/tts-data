import pandas as pd
import os, re
import csv

class TextProcessor:
    def __init__(self, input_file, use_ipa):
        self.input_file = input_file
        self.use_ipa = use_ipa

    def create_tts_metadata(self, output_dir):
        """
        Refactored to validate audio file existence in output_dir.
        Only rows with existing audio files are saved to metadata.csv.
        """
        output_path = os.path.join(output_dir, "metadata.csv")
        
        # Load the spreadsheet
        if self.input_file.endswith('.xlsx'):
            df = pd.read_excel(self.input_file)
        else:
            df = pd.read_csv(self.input_file)

        # Standardizing columns
        df = df[['Filename', 'Transcript']].copy()
        df['Transcript'] = df['Transcript'].str.strip()
        
        # 1. Check for audio file existence
        # We assume the 'Filename' column contains the name (e.g., "audio1.wav")
        print(f">>> Checking for audio files in: {output_dir}")
        
        def file_exists(f_name):
            # Construct path: output_dir/filename
            full_audio_path = os.path.join(output_dir, str(f_name))
            return os.path.isfile(full_audio_path)

        # Create a mask for existing files
        exists_mask = df['Filename'].apply(file_exists)
        
        # Log how many files are missing
        missing_count = len(df) - exists_mask.sum()
        if missing_count > 0:
            print(f"--- Warning: {missing_count} audio files not found. Removing from metadata.")

        # Filter the dataframe
        df = df[exists_mask].copy()

        # 2. Process Transliteration if requested
        if self.use_ipa:
            print(">>> Transliterating Abkhaz Cyrillic to IPA...")
            df['IPA_Transcript'] = df['Transcript'].apply(self.ab2ipa)
            final_df = df[['Filename', 'IPA_Transcript']]
        else:
            final_df = df[['Filename', 'Transcript']]
        
        # 3. Save the validated metadata
        os.makedirs(output_dir, exist_ok=True)

        final_df.to_csv(
            output_path, 
            sep='|', 
            index=False, 
            header=False, 
            encoding='utf-8', 
            quoting=csv.QUOTE_NONE, 
            escapechar='\\'
        )

        print(f">>> Metadata created at {output_path} with {len(final_df)} validated entries.")

    def ab2ipa(self, text):
        """
        Transliterates Abkhaz Cyrillic to IPA using prosodic punctuation.
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
            '…':'.'
        }

        output = []
        i = 0
        while i < len(text):
            match = None
            for length in [3, 2, 1]:
                substring = text[i:i+length]
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
        output = "".join(output).strip()
        # To make it Piper compatabile, I need to remove these.
        output = re.sub(r'd͡', 'd', output)
        output = re.sub(r't͡', 't', output)
        output = re.sub(r'ʼ', '', output)
        return output