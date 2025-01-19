def Therapyify(userMessage: str):    
    import os
    from openai import OpenAI
    from dotenv import load_dotenv
    import json

    load_dotenv() # will search for .env file in local folder and load variables 

    client = OpenAI(api_key=os.getenv('API_KEY'))

    file = open('messageHistory.json', 'r')
    chatHistory = json.load(file)
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
    chatHistory.append([{"role": "user", "content": userMessage}])
    chatHistory.append([{"role": "system", "content":therapistResponse}])
    
    with open('messageHistory.json', 'w') as file:
        json.dump(chatHistory, file)
    file.close()
    return therapistResponse