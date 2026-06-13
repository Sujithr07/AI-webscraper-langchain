from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import OllamaLLM

def parse_content(content, query="Summarize the main points from the content"):
    llm = OllamaLLM(model="mistral")
    
    prompt = ChatPromptTemplate.from_template(
        "You are an AI assistant analyzing web content.\n\n"
        "Content:\n{content}\n\n"
        "Task: {query}\n\n"
        "Provide a clear and concise response:"
    )
    
    chain = prompt | llm
    
    result = chain.invoke({"content": content, "query": query})
    
    return result
