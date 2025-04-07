from search import search
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def ask_demon(user_input):
    # Step 1: Search relevant chunks
    context = search(user_input)

    # Step 2: Send context + user input to GPT
    prompt = f"""Use the following information to answer the user's question:\n\n{context}\n\nUser: {user_input}\nAnswer:"""

    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are AskDemon, a helpful chatbot for DePaul students."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content.strip()

#Ai