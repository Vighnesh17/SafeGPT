import requests

api_key = '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'
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}
data = {
    "model": "llama-3.1-sonar-small-128k-chat",
    "messages": [{"role": "user", "content": "Hello, how are you?"}]
}
response = requests.post(
    "https://api.perplexity.ai/chat/completions",
    headers=headers,
    json=data
)
print(response.status_code)
print(response.json())
