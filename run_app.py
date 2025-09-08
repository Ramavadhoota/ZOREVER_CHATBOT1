#!/usr/bin/env python3
"""
ZOREVER Real Estate Chatbot - Application Runner
A convenience script to start the Streamlit application with proper setup.
"""

import os
import sys
import subprocess
from pathlib import Path
from dotenv import load_dotenv

def check_requirements():
    """Check if all required packages are installed."""
    required_packages = ['streamlit', 'pandas', 'groq', 'python-dotenv']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f" Missing packages: {', '.join(missing_packages)}")
        print(" Please install requirements: pip install -r requirements.txt")
        return False
    
    print("All required packages are installed!")
    return True

def check_env_file():
    """Check if .env file exists and has required variables."""
    env_path = Path('.env')
    
    if not env_path.exists():
        print(" .env file not found!")
        print("Please create .env file with: GROQ_API_KEY=your_api_key_here")
        return False
    
    load_dotenv()
    groq_key = os.getenv('GROQ_API_KEY')
    
    if not groq_key:
        print(" GROQ_API_KEY not found in .env file!")
        print(" Please add: GROQ_API_KEY=your_api_key_here to .env file")
        return False
    
    print("Environment variables loaded successfully!")
    return True

def check_data_files():
    """Check if required data files exist."""
    required_files = ['data/properties.csv']
    missing_files = []
    
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        print(f" Missing data files: {', '.join(missing_files)}")
        print("Please ensure all data files are in place")
        return False
    
    print("All data files found!")
    return True

def create_directories():
    """Create necessary directories if they don't exist."""
    directories = ['data', 'src']
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
    
    # Create visits.csv if it doesn't exist
    visits_file = Path('data/visits.csv')
    if not visits_file.exists():
        with open(visits_file, 'w') as f:
            f.write('timestamp,listing_id,property_name,name,email,phone,user_query,bot_response\n')
        print("Created data/visits.csv for interaction logging")

def run_streamlit_app(debug_mode=False):
    """Run the Streamlit application."""
    app_file = 'src/app_debug.py' if debug_mode else 'src/app.py'
    
    if not Path(app_file).exists():
        print(f"Application file {app_file} not found!")
        return False
    
    print(f"Starting ZOREVER Real Estate Chatbot...")
    print(f"Application will open in your browser at: http://localhost:8501")
    print(f"Running: streamlit run {app_file}")
    
    try:
        subprocess.run(['streamlit', 'run', app_file], check=True)
    except subprocess.CalledProcessError:
        print("Failed to start Streamlit application")
        return False
    except KeyboardInterrupt:
        print("\n Application stopped by user")
        return True
    
    return True

def main():
    """Main function to run the application with all checks."""
    print("ZOREVER Real Estate Chatbot - Starting Up...")
    print("=" * 50)
    
    # Check if debug mode is requested
    debug_mode = '--debug' in sys.argv
    if debug_mode:
        print(" Debug mode enabled")
    
    # Perform all checks
    print(" Performing system checks...")
    
    create_directories()
    
    if not check_requirements():
        sys.exit(1)
    
    if not check_env_file():
        sys.exit(1)
    
    if not check_data_files():
        print(" Some data files are missing, but continuing...")
    
    print("=" * 50)
    
    # Run the application
    success = run_streamlit_app(debug_mode)
    
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()

