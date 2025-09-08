#!/usr/bin/env python3

print("Testing imports...")

try:
    import streamlit as st
    print("streamlit imported successfully")
except ImportError as e:
    print(f"❌ streamlit import failed: {e}")

try:
    import pandas as pd
    print("pandas imported successfully")
except ImportError as e:
    print(f"❌ pandas import failed: {e}")

try:
    import groq
    print("groq imported successfully")
except ImportError as e:
    print(f"❌ groq import failed: {e}")

try:
    import dotenv
    print("dotenv imported successfully")
except ImportError as e:
    print(f"dotenv import failed: {e}")

try:
    import sys
    sys.path.append('src')
    from helpers import PropertyHelper, FAQHelper, detect_intent
    print("helpers module imported successfully")
except ImportError as e:
    print(f"helpers import failed: {e}")

print("Import test completed!")
