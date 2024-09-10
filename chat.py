import requests

CHAT_APP_SERVER_URL = 'http://localhost:5000/chat'

def chat_with_model_server(messages):
    url = CHAT_APP_SERVER_URL  # Replace with your app server URL
    response = requests.post(url, json={"messages": messages})  # Send the entire history
    
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Failed to communicate with the model server"}

def parse_model_response(response):
    print("The response is:")
    print(response)
    print("="*10)
    """Parse the model's response for better readability."""
    if 'response' in response:
        parsed_response = response['response'].split("\nUser said: ")
        formatted_response = "Model Response:\n" + parsed_response[0].strip() + "\n"

        for i in range(1, len(parsed_response)):
            formatted_response += f"User: {parsed_response[i].strip()}\n"

        return formatted_response
    return "No valid response from model."

if __name__ == "__main__":
    conversation_history = []
    
    while True:
        user_input = input("You: ")
        if user_input.lower() in ['exit', 'quit']:
            break
        
        # print("user input lol:")
        # print(user_input)
        # print('='*10)
        conversation_history.append({"role": "user", "content": user_input})
        print("user input lol:")
        print(conversation_history)
        print('='*10)
        response = chat_with_model_server(conversation_history)
        conversation_history.append({"role": "model", "content": response})
        
        # Parse and print the model's response
        parsed_response = parse_model_response(response)
        print(parsed_response)
