import os

def sum_files(root_folder):
    data = []
    
    for folder in os.listdir(root_folder):
        folder_path = os.path.join(root_folder, folder)
        
        # Ensure it's a directory and extract the number prefix
        if os.path.isdir(folder_path):
            try:
                # Count files in this folder
                dir_files = len([f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))])
                # print("Folder: {} - {} files".format(folder, dir_files))
                # book_name = folder.split('_')[1]
                data.append((folder, dir_files))
            except ValueError:
                pass  # Skip if folder name doesn't start with a number
    data.sort(key=lambda x: getBookParts(x)[0])
    lengths = open("lengths.csv", "w")
    for dataum in data:
        parts = getBookParts(dataum)
        lengths.write(str(parts[0]) + "," + str(parts[1]) + "," + str(dataum[1]) + "\n")
    lengths.close()

def getBookParts(book):
    number = int(book[0].split('_')[0])
    name = ' '.join(book[0].split('_')[1:])
    return (number, name)

def count_files_filtered_by_number(root_folder, max_number):
    total_files = 0
    # file_lengths = []
    # file_names = []
    
    for folder in os.listdir(root_folder):
        folder_path = os.path.join(root_folder, folder)
        
        # Ensure it's a directory and extract the number prefix
        if os.path.isdir(folder_path):
            try:
                folder_number = int(folder.split('_')[0])  # Extract number before '_'
                if folder_number < max_number:
                    # Count files in this folder
                    dir_files = len([f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))])
                    total_files += dir_files
                    print("Folder: {} - {} files".format(folder, dir_files))
                    book_name = folder.split('_')[1]
                    # file_lengths.append(dir_files)
                    # file_names.append(folder)
            except ValueError:
                pass  # Skip if folder name doesn't start with a number
    
    return total_files

# Example usage
root_folder = "."
# max_number = 13  # Change this to the threshold number
max_number = int(input("Enter the book you are on (ls .): "))
sum_files(root_folder)
print("Total number of files in folders with number < {}: {}".format(max_number, count_files_filtered_by_number(root_folder, max_number)))

