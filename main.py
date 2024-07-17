import os
import subprocess
import sys

def compile_latex(directory):
    # Get the directory of the script
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Check if logger.sty exists in the script directory
    package_path = os.path.join(script_dir, 'logger.sty')
    if not os.path.isfile(package_path):
        print(f"Error: 'logger.sty' not found in {script_dir}")
        print("Make sure the package file is in the same directory as this script.")
        return

    # TODO: Replace with a more robust check for the main file 
    main_file_path = os.path.join(directory, 'main.tex')
    if not os.path.isfile(main_file_path):
        print(f"Error: File 'main.tex' does not exist in {directory}.")
        return

    print(f"Compiling main.tex in directory: {directory}")
    
    # Prepare the environment for subprocess
    env = os.environ.copy()
    env['TEXINPUTS'] = f"{script_dir}:{env.get('TEXINPUTS', '')}"
    
    # Prepare the pdflatex command
    pdflatex_cmd = [
        'pdflatex',
        '-interaction=nonstopmode',
        '\\RequirePackage{logger}\\input{main}'
    ]
    
    # Run pdflatex twice to resolve references
    for i in range(2):
        print(f"Pass {i+1}...")
        result = subprocess.run(pdflatex_cmd, capture_output=True, text=True, env=env, cwd=directory)
        
        # Check if compilation was successful
        if result.returncode != 0:
            print(f"Error compiling main.tex in {directory}. Error message:")
            print(result.stderr)
            return
    
    print(f"Successfully processed {directory}")
    print(f"Output: {os.path.join(directory, 'output.txt')}")

def process_directories(base_dir):
    for root, dirs, files in os.walk(base_dir):
        if 'main.pdf' in files:
            compile_latex(root)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py <directory>")
        sys.exit(1)

    base_directory = sys.argv[1]
    if not os.path.isdir(base_directory):
        print(f"Error: {base_directory} is not a valid directory.")
        sys.exit(1)

    process_directories(base_directory)