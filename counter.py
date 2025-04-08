import os

def count_files_filtered_by_number(root_folder, max_number):
    total_files = 0
    
    for folder in os.listdir(root_folder):
        folder_path = os.path.join(root_folder, folder)
        
        # Ensure it's a directory and extract the number prefix
        if os.path.isdir(folder_path):
            try:
                folder_number = int(folder.split('_')[0])  # Extract number before '_'
                if folder_number < max_number:
                    # Count files in this folder
                    total_files += len([f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))])
            except ValueError:
                pass  # Skip if folder name doesn't start with a number
    
    return total_files

# Example usage
root_folder = "."
max_number = 13  # Change this to the threshold number
print("Total number of files in folders with number < {}: {}".format(max_number, count_files_filtered_by_number(root_folder, max_number)))

