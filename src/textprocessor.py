import pandas as pd
import os

class TextProcessor:
    def __init__(self, input_file):
        self.input_file = input_file

    def create_tts_metadata(self, output_path="data/processed/metadata.csv"):
        # Load the spreadsheet (works for .csv or .xlsx)
        if self.input_file.endswith('.xlsx'):
            df = pd.read_excel(self.input_file)
        else:
            df = pd.read_csv(self.input_file)

        # Standardizing columns: We need 'audio_file' and 'text'
        # Adjust 'Filename' and 'Transcript' to match your spreadsheet headers
        df = df[['Filename', 'Transcript']] 
        
        # Clean the text: remove extra whitespace, handle special characters
        df['Transcript'] = df['Transcript'].str.strip()
        
        # TTS formats (like LJSpeech) often use a pipe '|' delimiter
        df.to_csv(output_path, sep='|', index=False, header=False)
        print(f">>> Metadata created at {output_path} with {len(df)} entries.")
