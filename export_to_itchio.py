import subprocess
import os

def get_current_branch():
    # Function to get the current Git branch
    try:
        result = subprocess.check_output(["git", "symbolic-ref", "--short", "HEAD"], universal_newlines=True).strip()
        return result
    except subprocess.CalledProcessError:
        return None

def get_game_name():
    # Function to get the game name from project.godot
    with open("project.godot", "r") as f:
        for line in f:
            if line.strip().startswith("config/name"):
                return line.split("=")[1].strip(' "\n')

def export_to_itchio():
    # Main export function
    target_branch = "production"
    itchio_user = "mittomrum"

    current_branch = get_current_branch()

    if current_branch != target_branch:
        print(f"Not on the '{target_branch}' branch. Skipping build.")
        print(f"Current branch: '{current_branch}'")
        input("Press Enter to exit...")
        exit(1)
    else:
        print(f"Current branch: '{current_branch}'")

    game_name = get_game_name()

    if game_name is None:
        print("Failed to get the game name from project.godot.")
        input("Press Enter to exit...")
        exit(1)

    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Construct the project path based on the script directory
    itchio_credentials = f"{itchio_user}/{game_name}:html5"

    print("Exporting project to itch.io...")

    try:
        output_bytes = subprocess.check_output(["butler", "push", os.path.join(script_dir, "exports"), itchio_credentials])
        output_text = output_bytes.decode('utf-8')
        print(output_text)
        print("Export successful.")
    except subprocess.CalledProcessError as e:
        print(f"Export failed with error: {e}")
        print(f"Command output:\n{e.output.decode('utf-8')}")
        input("Press Enter to exit...")
        exit(1)

    input("Press Enter to exit...")

if __name__ == "__main__":
    export_to_itchio()
