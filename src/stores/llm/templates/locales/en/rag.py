from string import Template

##### RAG prompts #####

# System message template
system_prompt = Template(
    """
You are a helpful AI assistant.
Use the following pieces of context to answer the user's question.
If you don't know the answer, just say that you don't know, don't try to make up an answer.
"""
)

# Document prompt template for formatting individual documents
document_prompt = Template(
    """
    Document $doc_number:
    Content: $doc_content
    """
)

# Footer prompt template
footer_prompt = Template(
    """
    Based on the following context, please answer the question. If the answer cannot be found in the context, say so.
Question: {question}

Answer:"""
)
