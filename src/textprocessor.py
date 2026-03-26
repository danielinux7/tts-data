import pandas as pd
import os
import csv
import unicodedata
import json

class TextProcessor:
    def __init__(self, input_file, use_ipa, mapping_file="src/ab2ipa.json"):
        self.input_file = input_file + "/metadata.xlsx"
        self.use_ipa = use_ipa
        
        # Initialize mapping with the static punctuation rule from the original code
        self.mapping = {'…': '.'}
        
        if self.use_ipa:
            if os.path.exists(mapping_file):
                with open(mapping_file, 'r', encoding='utf-8') as f:
                    file_mapping = json.load(f)
                    self.mapping.update(file_mapping)
            else:
                print(f"Warning: {mapping_file} not found. IPA transliteration may fail.")

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
        print(f">>> Checking for audio files in: {output_dir+'/wavs'}")
        
        def file_exists(f_name):
            # Construct path: output_dir/filename
            full_audio_path = os.path.join(output_dir+"/wavs", str(f_name))
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
        Transliterates Abkhaz Cyrillic to IPA using external JSON mapping.
        """
        if not isinstance(text, str):
            return ""

        output = []
        i = 0
        while i < len(text):
            match = None
            # Iterate through possible token lengths (trigraphs -> digraphs -> single)
            for length in [3, 2, 1]:
                substring = text[i:i+length]
                
                # Maintain original logic: Capitalize digraphs/trigraphs, Uppercase single letters
                # This ensures we hit the keys in the JSON (e.g. "Гь", "А")
                lookup = substring.capitalize() if length > 1 else substring.upper()

                if lookup in self.mapping:
                    match = self.mapping[lookup]
                    i += length
                    break

            if match:
                output.append(match)
            else:
                output.append(text[i])
                i += 1
        return unicodedata.normalize("NFD", "".join(output).strip())
