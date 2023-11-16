import subprocess
import os
import shutil
import time
import zipfile

# Get the directory where the script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# Find the Godot project file in the script directory
project_file = None
for file in os.listdir(script_dir):
    if file.lower() == "project.godot":
        project_file = os.path.join(script_dir, file)
        break

if project_file is None:
    print("Error: Project file (project.godot) not found in the script directory.")
    exit(1)

def get_game_name():
    # Function to get the game name from project.godot
    project_file = os.path.join(script_dir, "project.godot")
    with open(project_file, "r") as f:
        for line in f:
            if line.strip().startswith("config/name"):
                return line.split("=")[1].strip(' "\n')

game_name = get_game_name()

source_dir = os.path.join(script_dir, "exports\\web")
zip_dir = os.path.join(script_dir, "exports")
export_preset = "Web"  # Change this to your desired export preset
zip_filename = os.path.join(zip_dir, f"{get_game_name()}_{export_preset}.zip")

# Tests to run before starting the export process
project_file = None
for file in os.listdir(script_dir):
    if file.lower() == "project.godot":
        project_file = os.path.join(script_dir, file)
        break
if project_file is None:
    print("Error: Project file (project.godot) not found in the script directory.")
    exit(1)

if game_name is None:
    print("Failed to get the game name from project.godot.")
    input("Press Enter to exit...")
    exit(1)

def run_export():
    print("Exporting the game... (This may take a moment)")
    try:
        process = subprocess.Popen(["godot", "--headless", "--export-release", export_preset, os.path.join(script_dir, "exports", "web", "index")], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        while True:
            time.sleep(1)  # Wait for 1 second
            return_code = process.poll()  # Check if the subprocess has completed
            if return_code is not None:
                break
            print(".", end="", flush=True)  # Print a dot to indicate progress
        print()  # Print a newline to end the progress indicator
        if return_code != 0:
            print(f"Error during export: {process.stderr.read().decode('utf-8')}")
            exit(1)
    except subprocess.CalledProcessError as e:
        print(f"Error during export: {e}")
        exit(1)
      
def print_compression_info():
    # Print information about the source directory
    print(f"Source Directory: {source_dir}")

    # Get the list of files to be compressed
    files_to_compress = []
    for foldername, _, filenames in os.walk(source_dir):
        print(f"Processing folder: {foldername}")  # Debug line
        for filename in filenames:
            file_path = os.path.join(foldername, filename)
            files_to_compress.append(file_path)

    # Print the list of files to be compressed
    print("\nFiles to be Compressed:")
    for file_path in files_to_compress:
        print(file_path)

    # Print the name of the ZIP file to be created
    print(f"\nZIP File to be Created: {zip_filename}\n")

def compress_files_to_zip():
    # Directory containing the files you want to compress
    source_dir = os.path.join(script_dir, "exports/web")
    print_compression_info()
    try:
        # Create a ZIP file in write mode
        with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Walk through the source directory and its subdirectories
            for foldername, subfolders, filenames in os.walk(source_dir):
                for filename in filenames:
                    # Get the full path of the file
                    file_path = os.path.join(foldername, filename)
                    # Add the file to the ZIP archive with its relative path
                    zipf.write(file_path, os.path.relpath(file_path, source_dir))
        
        print(f'Files compressed to "{zip_filename}" successfully!')

        # Move the ZIP archive to the "exports" folder
        print(f'moving zip')
        shutil.move(zip_filename, os.path.join(script_dir, "exports", "web", zip_filename))

        # check if the there is a .zip in the root folder

        

    except Exception as e:
        print(f'Error: {e}')

def cleanup():
    export_web_dir = os.path.join(script_dir, "exports", "web")
    all_files = os.listdir(export_web_dir)

    # Remove all files except the ZIP file
    for file in all_files:
        if file != zip_filename:
            file_path = os.path.join(export_web_dir, file)
            if os.path.isfile(file_path):
                os.remove(file_path)

    print(f"Cleanup completed")




# Run the export process and create the ZIP archive
run_export()
print("Export completed. Creating ZIP archive... (This may take a moment)")
compress_files_to_zip()
cleanup()

# if there is a zip in the root folder, print success
if os.path.isfile(zip_filename):
    print(f'Game export completed successfully!')

# Wait for the user to press Enter before closing the window
input("Press Enter to exit...")
