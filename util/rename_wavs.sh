#!/bin/bash

# 1. Ask the user for the prefix
read -p "Enter the prefix you'd like to add: " prefix

# 2. Check if any .wav files actually exist to avoid errors
shopt -s nullglob
files=(*.wav)

if [ ${#files[@]} -eq 0 ]; then
    echo "No .wav files found in this directory."
    exit 0
fi

# 3. Loop through the files and rename them
echo "Renaming files..."
for file in "${files[@]}"; do
    # This 'mv' command adds the prefix to the original filename
    mv "$file" "${prefix}${file}"
    echo "Renamed: $file -> ${prefix}${file}"
done

echo "---"
echo "All done! Your files have been updated."
