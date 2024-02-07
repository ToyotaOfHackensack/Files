import base64
import requests
import time
from PIL import ImageGrab
from io import BytesIO
import pyperclip
import sys
import logging

# Configure logging
logging.basicConfig(filename='captcha_solver.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Your Anti-Captcha API key
API_KEY = "f0daa814d689e1468782e0a0e035ace0"

def get_base64_image_from_clipboard():
    """Converts the clipboard image to a base64-encoded string."""
    image = ImageGrab.grabclipboard()
    if image:
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        logging.info("Image captured and converted to base64.")
        return img_str
    else:
        logging.warning("No image in clipboard!")
        return None

def submit_image_captcha(base64_image):
    """Submits the base64-encoded image to the CAPTCHA solving service."""
    task_payload = {
        "clientKey": API_KEY,
        "task": {
            "type": "ImageToTextTask",
            "body": base64_image,
            "case": True,
            "numeric": 2,
            "minLength": 4,
            "maxLength": 4,
        }
    }
    
    create_task_url = "https://api.anti-captcha.com/createTask"
    response = requests.post(create_task_url, json=task_payload)
    response_data = response.json()
    
    if response_data.get("errorId") == 0:
        logging.info(f"Task successfully created. Task ID: {response_data.get('taskId')}")
        return response_data.get('taskId'), None
    else:
        logging.error(f"Failed to create task: {response_data.get('errorDescription')}")
        return None, response_data.get('errorDescription')

def get_task_result(task_id):
    """Polls the CAPTCHA solving service for the task result with error handling, for up to 2 minutes."""
    result_payload = {
        "clientKey": API_KEY,
        "taskId": task_id
    }
    
    get_result_url = "https://api.anti-captcha.com/getTaskResult"
    start_time = time.time()
    while time.time() - start_time < 120:
        response = requests.post(get_result_url, json=result_payload)
        result_data = response.json()
        
        if result_data.get("errorId") != 0:
            logging.error(f"Polling error: {result_data.get('errorDescription')}")
            return None
        
        if result_data.get("status") == "ready":
            logging.info("CAPTCHA solved successfully.")
            return result_data["solution"]["text"]
        
        time.sleep(5)
    logging.warning("Timeout reached while waiting for CAPTCHA solution.")
    return None

if __name__ == "__main__":
    base64_image = get_base64_image_from_clipboard()
    
    if base64_image:
        task_id, error = submit_image_captcha(base64_image)
        if task_id:
            captcha_solution = get_task_result(task_id)
            if captcha_solution:
                logging.info(f"Captcha Solved: {captcha_solution}")
                # Copy to clipboard
                pyperclip.copy(captcha_solution)
            else:
                logging.error("Failed to get a valid solution.")
        else:
            logging.error(f"Failed to create task: {error}")
    else:
        logging.error("No image found in clipboard or failed to convert image.")

    sys.exit()
