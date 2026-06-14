from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import OllamaLLM
import logging

logger = logging.getLogger(__name__)

def parse_content(content, query="Summarize the main points from the content"):
    """Parse content using Ollama LLM with error handling."""
    try:
        if not content or not content.strip():
            return "Error: No content provided to analyze."
        
        llm = OllamaLLM(model="mistral", timeout=60)
        
        prompt = ChatPromptTemplate.from_template(
            "You are an AI assistant analyzing web content.\n\n"
            "Content:\n{content}\n\n"
            "Task: {query}\n\n"
            "Provide a clear and concise response:"
        )
        
        chain = prompt | llm
        result = chain.invoke({"content": content, "query": query})
        
        return result
    except ConnectionError as e:
        logger.error(f"Connection error: {e}")
        return "Error: Cannot connect to Ollama. Make sure Ollama is running."
    except TimeoutError as e:
        logger.error(f"Timeout error: {e}")
        return "Error: Analysis timed out. Try with shorter content."
    except Exception as e:
        logger.error(f"Unexpected error in parse_content: {e}")
        return f"Error during analysis: {str(e)}"
