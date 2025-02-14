import subprocess
import os

python_version = 'python3.11'

def run_python_file(file_path):
  try:
    print(f"Running {file_path}...")
    result = subprocess.run([python_version, file_path], check=True, capture_output=True, text=True)
    print(f"Successfully completed {file_path}")
    return True
  except subprocess.CalledProcessError as e:
    print(f"Error running {file_path}")
    print(f"Error message: {e.stderr}")
    return False

def main():
  # List of Python files to run in order
  files_to_run = [
    'fetch_complete_wordpress_data.py',
    'check_data_integrity.py',
    os.path.join('db', 'transform_wordpress_data.py'),
    os.path.join('db', 'insert_schema.py'),
    os.path.join('db', 'insert_sql.py')
  ]

  # Run each file in sequence
  for file_path in files_to_run:
    if not run_python_file(file_path):
      print(f"Stopping execution due to error in {file_path}")
      break

if __name__ == "__main__":
  main()