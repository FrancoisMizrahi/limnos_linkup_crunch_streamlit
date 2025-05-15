import requests
import time
import json
import sys
import streamlit as st
import pandas as pd



def query_linkup(question, api_token, interval):
    """
    Send a question to the Linkup API and poll until we get a final response.

    Args:
        question (str): The question to send to the API
        api_token (str): Your Linkup API token

    Returns:
        The final answer from the API
    """
    # Create headers with authorization
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }

    # Step 1: Send initial POST request
    post_url = "https://api.linkup.so/v1/beta/crunch"
    payload = {
        "q": question
    }

    print(f"Sending question: {question}")
    response = requests.post(post_url, json=payload, headers=headers)

    if response.status_code != 201:
        print(f"Error: POST request failed with status code {response.status_code}")
        print(f"Response: {response.text}")
        sys.exit(1)

    # Extract the ID from the response
    response_data = response.json()
    request_id = response_data.get("id")

    if not request_id:
        print("Error: No ID returned in the response")
        print(f"Response: {response_data}")
        sys.exit(1)

    print(f"Request ID: {request_id}")
    print("Waiting for response...")

    # Step 2: Poll the GET endpoint every 10 seconds
    get_url = f"https://api.linkup.so/v1/beta/crunch/{request_id}"
    with st.spinner("Wait for it...", show_time=True):
        while True:
            time.sleep(interval)

            get_response = requests.get(get_url, headers=headers)

            if get_response.status_code != 200:
                print(f"Error: GET request failed with status code {get_response.status_code}")
                print(f"Response: {get_response.text}")
                sys.exit(1)

            get_data = get_response.json()
            status = get_data.get("status")

            print(f"Current status: {status}")

            # Check if processing is complete
            if status in ["success", "error"]:
                break

    if status == "success" and get_data.get("response") and get_data["response"].get("answer"):
        st.success("Done!")
        print("\nAnswer:")
        print(get_data["response"]["answer"])
        st.markdown(get_data["response"]["answer"])
    else:
        print("\nError: No answer available or request failed")
        print(f"Final response: {json.dumps(get_data, indent=2)}")