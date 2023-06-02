"""Main script for the k8scli-gpt package."""
import os
import sys
from snowgpt.config import load_config, set_api_key
from snowgpt.snowflake_agent import execute,verify_prompt
import streamlit.web.bootstrap

if __name__ == '__main__':
    config_file_path = 'config.ini'
    if 'OPENAI_API_KEY' not in os.environ and not config_file_path:
        raise ValueError(
            'Environment variable OPENAI_API_KEY not found, you can set it in Project Settings')

    if not config_file_path:
        set_api_key()
    else:
        load_config(config_file_path)

    if sys.argv[1] == 'upload':
        streamlit.web.bootstrap.run("snowgpt/upload.py", sys.argv[0], [], [])
    else:
        execute(sys.argv[1])