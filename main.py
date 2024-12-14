from llm import llm
import chromadb
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import warnings

warnings.filterwarnings("ignore")
def Convo_with_Vector_Memeory():
    

    Persitent_client=chromadb.PersistentClient()
    collection=Persitent_client.get_or_create_collection("chat_history2")
    


    print("Start your conversation with AI (write 'bye' to quit)")

    while True:
        user_input = input("You: ")
        if user_input.lower() == 'bye':
            break

        
        try:
            query_ans = collection.query(query_texts=[user_input], n_results=10)
            context = query_ans["documents"] if query_ans["documents"] else "No previous context is found."
            print(f"Found Context: {context}")
        except Exception as e:
            print(f"Error querying database: {e}")
            context = "No previous context is found."

        prompt_template = PromptTemplate(
            template="""
                You are asked a question: {user_input}.
                The following is a friendly conversation between a human and an AI. The AI is talkative and provides lots of specific details from its context. If the AI does not know the answer to a question, it truthfully says it does not know.
                If you know any answer,please answer the question. 
                If you don't know then look into previous conversation. Here is the context extracted from previous conversation for reference: {context}. Do not solely depend on it.
                No need to explain about the retrieval. Just answer the question. Thank you.
                No need to write about prevoius about conversation.
            """,
            input_variables=["user_input", "context"]
        )

        try:
            chain = LLMChain(llm=llm, prompt=prompt_template)
            response = chain.run({"user_input": user_input, "context": context})
            print(f"AI: {response}")

            
        except Exception as e:
            print(f"Error processing query: {e}")
        count=len(collection.get()["ids"])
        try:
            collection.add(
                documents=[user_input],
                ids=[f"interaction-{count+1}"]  
            )
            print(f"Interaction {count} is completed.")
            print("Saved to ChromaDB.")
        except Exception as e:
            print(f"Error saving to database: {e}")


if __name__=="__main__":
    Convo_with_Vector_Memeory()
