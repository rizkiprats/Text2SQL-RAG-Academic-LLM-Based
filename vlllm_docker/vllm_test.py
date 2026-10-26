from openai import OpenAI

# Initialize the OpenAI client pointing to the local vLLM Docker container.
client = OpenAI(
    base_url="http://localhost:8000/v1",
    api_key="token-not-needed-for-vllm" # vLLM doesn't require a real key by default
)

def get_active_model():
    """Fetches the active model name directly from the running vLLM container."""
    try:
        models_list = client.models.list()
        # Get the first active model ID from the data list
        active_model = models_list.data[0].id
        print(f"[vLLM] Auto-detected active model: '{active_model}'\n")
        return active_model
    except Exception as e:
        print(f"[Warning] Could not auto-detect model: {e}. Defaulting to '/model'.\n")
        return "/model"

# Automatically set the model name from Docker
model_name = get_active_model()

def test_chat_completion():
    print("Sending request to vLLM Docker container...\n")
    
    try:
        # Send a chat completion request using the auto-detected model name
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Hello! Introduce yourself briefly."}
            ],
            temperature=0.7,
            max_tokens=100
        )
        
        print("--- Response Received ---")
        print(response.choices[0].message.content)
        print("-------------------------")
        print("\nTest Status: SUCCESS")
        
    except Exception as e:
        print(f"\nTest Status: FAILED")
        print(f"Error details: {e}")

if __name__ == "__main__":
    test_chat_completion()