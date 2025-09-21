generic_prompt=""" 
**1. Primary Objective:**
The main objective is to generate a comprehensive yet succinct summary of the provided text. The summary must capture the core essence, main arguments, key findings, and most critical details without losing the original meaning.

**2. Context to be Summarized:**
{text}

**3. Specific Goals & Constraints for the Summary:**
* **Length & Format:** The summary should be approximately [CHOOSE ONE: a single paragraph | 200 words | 3-4 bullet points | no more than 5 sentences]. It should be presented in a clear, easy-to-read format.
* **Target Audience:** The summary is intended for [CHOOSE ONE: a general audience with no prior knowledge | a technical expert in the field | a busy executive who needs key takeaways only | a student who needs to understand the main concepts].
* **Key Information to Prioritize:**
    * Identify and highlight the central theme or main thesis of the text.
    * Extract and list all major conclusions or findings presented.
    * Mention any specific names, dates, or numerical data that are crucial to understanding the context.
    * Include a brief explanation of any complex terms or concepts mentioned, if necessary.
* **Information to Exclude (if any):**
    * Exclude minor details, anecdotal evidence, or repetitive statements.
    * Do not include personal opinions or subjective interpretations.
* **Tone & Style:** The tone of the summary should be  neutral and informative. The language should be {language}


**4. Post-Summary Requirements:**
* **Confidence Score:** After generating the summary, provide a confidence score from 1-10 on how accurately you believe your summary reflects the original text.
* **Missing Information:** List any critical information you believe was omitted from the source text that would be necessary for a complete understanding of the topic.
* **Potential Biases:** Identify any potential biases or a lack of neutrality you detect in the original source text.

**5. Final Output Structure:**
* **[SECTION TITLE: Summary]**
    * [YOUR GENERATED SUMMARY]
* **[SECTION TITLE: Analysis & Confidence]**
    * **Confidence Score:** [YOUR SCORE HERE]
    * **Noteworthy Omissions from Source:** [LIST OF MISSING INFO]
    * **Identified Biases:** [LIST OF BIASES]

Please begin the process by first reading the entire text carefully, then creating a mental map of its structure and main points, and finally generating the output according to the specified goals.

"""


final_prompt=""" 

You are a highly skilled document analysis and summarization expert. Your task is to read the following segment of a larger document and create a concise summary. The summary should be approximately 2-3 sentences long and must capture the main ideas, key facts, and any crucial arguments presented in this specific chunk of text. Do not add any new information or stray from the context provided.

---
{text}
---

Please provide only the summary, without any additional commentary.
And keep the language to {language}


"""

web_prompt="""
Please act as a world-class research assistant and analytical summarizer. Your task is to process the following web page content and provide a comprehensive, structured analysis.

Your response should contain three distinct sections:

Comprehensive Summary: Provide a detailed and well-written summary of the entire document. Do not just list facts; synthesize the information to explain the main arguments, concepts, and conclusions presented in the text. This summary should be suitable for someone who needs to understand the core content without reading the entire source.

Key Takeaways: Identify and list the most critical points, findings, or arguments. These should be concise and actionable, highlighting the essential information a reader should remember. Use a numbered or bulleted list for clarity.

Extracted Useful Information: Go beyond the summary and takeaways to identify and list any specific, useful pieces of information. This could include:

Specific dates, names, or locations.

Numerical data, statistics, or metrics.

Definitions of key terms.

References to other sources or related topics.

if possible tell eash page and his content : exemple
 page = home : content = ..............................

Any other factual data that would be valuable for future reference or research.

take this text :\n{text} and aplly all the rules above  and speak in {language}

Ensure your output is well-organized, easy to read, and directly based on the provided text. Maintain a neutral and objective tone.
"""