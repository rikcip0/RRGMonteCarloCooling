import os
import shutil
import re

def check_subfolder_existence(parent_folder, subfolder_name):
    # Check if the parent folder exists
    if not os.path.exists(parent_folder):
        print(f"The folder '{parent_folder}' doesn't exist.")
        return False

    subfolder_path = os.path.join(parent_folder, subfolder_name)
    # Check for subfolders with the distinguishing string
    run_count = 1
    while True:
        run_subfolder = f"{subfolder_name}_run{run_count}"
        run_subfolder_path = os.path.join(parent_folder, run_subfolder)

        if not os.path.exists(subfolder_path):
            break
        else:
            if not os.path.exists(run_subfolder_path):
                break 
            run_count += 1

        if run_count > 20:
            print(f"There already many runs for '{subfolder_name}' in the folder '{parent_folder}'.")
            break

    return run_subfolder_path


def move_folder_content(source_folder, destination_folder):
    # Verifica se la cartella di origine esiste
    if not os.path.exists(source_folder):
        print(f"The source folder '{source_folder}' doesn't exist.")
        return

    # Verifica se la cartella di destinazione esiste
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)
        print(f"The destination folder '{destination_folder}' has been created.")

    # Sposta il contenuto della cartella di origine nella cartella di destinazione
    for item in os.listdir(source_folder):
        item_path = os.path.join(source_folder, item)
        if os.path.isfile(item_path):
            shutil.move(item_path, destination_folder)
        elif os.path.isdir(item_path):
            shutil.move(item_path, os.path.join(destination_folder, item))

    print("Content moved successfully.")

def get_title_line(Info_path):
    with open(Info_path, "r") as file:
        # Read the content of the file
        content = file.read()

        # Find the line starting with "#"
        params_line = next((line for line in content.split("\n") if line.startswith("#")), None)

        if params_line is not None:
            # Extract the symType
            symType = re.search(r"#(\w+)", params_line).group(1)

            # Search for parameters and values using regular expressions
            params = re.findall(r"\b(\w+)\s*=\s*([^\s#]+)", params_line)
            return symType, ''.join([f"{key}{value}" for key, value in params])
    return None


file_path = "..\\Data\\ThisRun\\Info.txt"
symTypeString, inputParamsString= get_title_line(file_path)
formatFolder_name = os.path.join(symTypeString, inputParamsString)

archive_folder = "..\\Data\\Archive"
destination_folder = check_subfolder_existence(archive_folder, formatFolder_name)

source_folder = "..\\Data\\ThisRun"
move_folder_content(source_folder, destination_folder)