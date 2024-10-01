import requests

url = "http://localhost:8000/api/process_prompt"
test_prompts = [
    "My name is John Doe and my email is john@example.com",
    "The server IP is 192.168.1.100 and the password is 'secret123'",
    "Please debug the code in C:\\Users\\JohnDoe\\Projects\\SafeGPT"
]

for prompt in test_prompts:
    response = requests.post(url, json={"prompt": prompt})
    print(f"Prompt: {prompt}")
    print(f"Response: {response.json()['response']}")
    print("---")
