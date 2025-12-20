from string import Template

##### RAG prompts #####

# System message template
system_prompt = Template(
    """
أنت مساعد ذكي مفيد.
استخدم قطع السياق التالية للإجابة على سؤال المستخدم.
إذا كنت لا تعرف الإجابة، فقط قل إنك لا تعرف، ولا تحاول اختلاق إجابة.
"""
)

# Document prompt template for formatting individual documents
document_prompt = Template(
    """
    المستند $doc_number:
        المحتوي: $doc_content
        """
)

# Footer prompt template
footer_prompt = Template(
    """
    بناء على السياق التالي، يرجى الإجابة على السؤال. إذا لم يمكن العثور على الإجابة في السياق، فقل ذلك.
    السؤال: {question}
$query
    الإجابة:"""
)
