def Therapyify(userMessage: str):    
    import os
    from openai import OpenAI
    from dotenv import load_dotenv

    load_dotenv() # will search for .env file in local folder and load variables 

    client = OpenAI(api_key=os.getenv('API_KEY'))

    with open('messageHistory.txt', 'r') as file:
        content = file.read()
        chatHistory = str(content) if content else ""  # Handle empty file
    file.close()

    def request_API(prompt, tokens: bool = True):

        response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=prompt)
    
        if tokens:  # Display amount of tokens used
            print(f'\nYou used {response.usage.prompt_tokens} prompt tokens + {response.usage.completion_tokens} completion tokens = {response.usage.total_tokens} tokens\n')
        
        return response.choices[0].message.content.strip()
    
    therapistResponse = request_API([{"role": "system", "content": f"You are a therapy chatbot on a mental health website. Respond to the following inquiry appropriately: {userMessage}. Use the following message history to respond in context: {chatHistory}"}], False)

    # print(therapistResponse)
    chatHistory.append(therapistResponse)
    
    with open('messageHistory.txt', 'w') as file:
        file.write(chatHistory)
    file.close()
    return therapistResponse

print(Therapyify("I'm feeling bored, do you have any way tips to cheer up?"))