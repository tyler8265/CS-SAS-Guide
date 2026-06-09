# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section *after* you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

---

## Domain

<!-- What topic or category of knowledge does your system cover?
     Why is this knowledge valuable, and why is it hard to find through official channels?
     Example: "Student reviews of CS professors at [university] — useful because official
     course descriptions don't reflect teaching style, exam difficulty, or workload." -->

This system covers Rutgers University course difficulty and survival strategies — what students actually say about workload, professors, exams, and how to pass specific courses. This knowledge is valuable because it reflects real student experience rather than official course descriptions, which rarely mention how hard a professor grades, whether projects are unreasonably long, or which gen ed courses are easy A's. It is hard to find through official channels because the Rutgers website only provides syllabi, prerequisites, and scheduling information, but what it fails to tell you are the experiences that only students can relay like that Francisco's CS214 projects can take 100+ hours, or that Centeno's CS111 videos are more useful than lecture, or which gen ed is the easiest A.

## Document Sources

<!-- List every source you collected documents from.
     Be specific: include URLs, subreddit names, forum thread titles, or file names.
     Aim for variety — sources that together cover different subtopics or perspectives. -->

| # | Source | Type | URL or file path |
|---|--------|------|-----------------|
| 1 | reddit_cs111_beginner_difficulty.txt | Reddit thread | https://www.reddit.com/r/rutgers/comments/14ndsgd/how_geared_towards_beginners_is_cs111/ |
| 2 | reddit_cs111_exam_recovery.txt | Reddit thread | https://www.reddit.com/r/rutgers/comments/1o6x57h/am_i_cooked_cs111/ |
| 3 | rmp_centeno_cs111.txt | Rate My Professors | https://www.ratemyprofessors.com/professor/2547756 |
| 4 | reddit_cs_course_difficulty_guide.txt | Reddit thread | https://www.reddit.com/r/rutgers/comments/kpualv/review_of_rutgers_cs_part_2_classes_ratings/ |
| 5 | reddit_rutgers_cs_survival_guide.txt | Reddit thread | https://www.reddit.com/r/rutgers/comments/kpuwo9/review_of_rutgers_cs_part_1_my_journey_and/ |
| 6 | reddit_calc2_how_to_pass.txt | Reddit thread | https://www.reddit.com/r/rutgers/comments/1rq7xay/is_calc_2_possible_to_pass/ |
| 7 | rmp_ullman_calc152.txt | Rate My Professors | https://www.ratemyprofessors.com/professor/2079421 |
| 8 | reddit_easy_sas_core_classes.txt | Reddit thread | https://www.reddit.com/r/rutgers/comments/1d453s6/easy_and_fun_sas_core_classes/ |
| 9 | reddit_easy_writing_requirement_courses.txt | Reddit thread | https://www.reddit.com/r/rutgers/comments/1hk4aay/can_anyone_recommend_me_an_easy_a_wcrwcd_course/ |
| 10 | reddit_cs112_how_to_get_an_a.txt | Reddit thread | https://www.reddit.com/r/rutgers/comments/eeount/how_can_i_get_an_a_in_cs112/ |
| 11 | rmp_sesh_cs112.txt | Rate My Professors | https://www.ratemyprofessors.com/professor/182646 |
| 12 | rmp_francisco_cs214.txt | Rate My Professors | https://www.ratemyprofessors.com/professor/1833903 |

---

## Chunking Strategy

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->

**Chunk size:** 800 Characters

**Overlap:** 100 characters

**Why these choices fit your documents:** My documents are a mix of short Rate My Professors reviews and longer Reddit 
guide paragraphs. I split primarily on `---` dividers, which separate individual 
reviews and comments in my cleaned source files. This keeps each review or comment 
as its own self-contained chunk. For paragraphs that exceed 800 characters — common 
in the CS survival guide and course difficulty guide — I fall back to a hard cut at 
800 characters with 100 characters of overlap. The overlap ensures that key 
information sitting at a chunk boundary isn't lost. Before chunking, I manually 
cleaned all documents to remove ads, navigation text, upvote counts, GPTZero labels, 
and any content unrelated to the actual reviews or advice.

**Final chunk count:** 121 chunks across 12 documents.

---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:** all-MiniLM-L6-v2 via sentence-transformers

**Production tradeoff reflection:**
I chose all-MiniLM-L6-v2 because it runs locally with no API key or rate limits 
and is fast enough for a corpus of 121 chunks. For a production deployment serving 
real Rutgers students, I would prioritize two tradeoffs above all others.

First, accuracy on domain-specific informal text. My retrieval distances are 
consistently high (0.42-0.95), which suggests all-MiniLM-L6-v2 struggles with 
the informal language in Reddit threads and Rate My Professors reviews. A model 
like OpenAI's text-embedding-3-large, trained on a much larger and more diverse 
dataset, would likely produce lower distances and more precise retrieval.

Second, multilingual support. Rutgers is a diverse university and not all students 
are native English speakers. all-MiniLM-L6-v2 is English-only. A production system 
would benefit from a multilingual model like multilingual-e5-large, which supports 
100+ languages without sacrificing much accuracy on English text.

The tradeoff is cost and latency — API-hosted models like text-embedding-3-large 
cost money per token and introduce network latency, whereas all-MiniLM-L6-v2 is 
free and runs locally in milliseconds.

---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:**
Grounding is enforced through the system prompt passed to Groq's 
llama-3.3-70b-versatile model. The exact instruction is:

"Answer the question using only the information in the provided documents. 
If the documents don't contain enough information to answer, say 'I don't 
have enough information on that.'"

The retrieved chunks are passed to the model in the user message, formatted 
as a context block before the question:

"Context:
Source: [filename]
Content: [chunk text]

Question: [user query]"

This structure ensures the model sees the source documents before the question, 
making it more likely to draw from the provided context rather than general 
training knowledge.


**How source attribution is surfaced in the response:**
Source filenames are extracted from the ChromaDB metadata for each retrieved 
chunk and returned alongside the LLM response as a separate output. The Gradio 
UI displays them in a dedicated "Retrieved from" field so the user can see 
exactly which documents the answer drew from.

---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

## Evaluation Report

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | What do students say about CS111's difficulty and how should a complete beginner prepare? | CS111 is beginner friendly but harder without prior experience. Watch Centeno's videos, do recitation slides, complete all homework. | Mixed opinions reported — tough for some, manageable for others. Recommends Java book over summer and locking in before exams. Cites specific users. | Partially relevant — 3 of 5 chunks on topic, 2 CS112 chunks retrieved incorrectly | Partially accurate |
| 2 | What are the most common complaints about Professor Francisco in CS214 and is it worth taking with him? | Vague projects, extremely slow grading, poor communication. One project took 110 hours. Avoid if possible, take one fewer class if you must. | Correctly identified disorganization, slow grading, ego, and unclear guidelines. Contradictorily said "I don't have enough information" before listing complaints. | Relevant — 4 of 5 chunks about Francisco | Partially accurate |
| 3 | What do students recommend for doing well in CS112 Data Structures? | Start projects early, do all problem sets, watch Sesh's YouTube videos, study past exams on GitHub, focus on Big O notation. | Correctly recommended starting projects early, doing problem sets, consulting TAs, modularizing code, and becoming a TA/LA. | Relevant — chunks from dedicated CS112 sources | Accurate |
| 4 | What study strategies do Rutgers students recommend for passing Calc 2? | Memorize formula sheet, do practice problems, use Vera problem bank, attend recitation, watch Ullman's YouTube videos. | Correctly recommended attending lectures, memorizing formula sheet, doing book problems, and watching professor's YouTube videos. Cites specific users. | Relevant — 4 of 5 chunks from Calc 2 sources | Accurate |
| 5 | What are the easiest SAS core courses to fulfill writing and humanities requirements at Rutgers? | Structure of Information with Fausto Pinto, Creative Writing with Pelsue, Gods Myths and Religions with Fruchtman, Research in Disciplines with Schroepfer. | Only mentioned Gods Myths and Religions and History of Work and Labor. Retrieved off-topic chunks from CS difficulty guide and CS112 sources. | Off-target — 2 of 5 chunks unrelated to SAS core | Inaccurate |

**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

<!-- Identify at least one question where retrieval or generation did not work as expected.
     Write a specific explanation of *why* it failed, tied to a part of the pipeline.

     "The answer was wrong" is not an explanation.

     "The relevant information was split across a chunk boundary, so retrieval returned
     only half the context — the model didn't have enough to answer correctly" is an explanation.

     "The embedding model treated the professor's nickname as out-of-vocabulary and returned
     results from an unrelated review" is an explanation. -->

**Question that failed:**
"What are the easiest SAS core courses to fulfill writing and humanities 
requirements at Rutgers?"

**What the system returned:**
The system only mentioned Gods Myths and Religions and History of Work and 
Labor as potential options, missing specific recommendations like Structure 
of Information with Fausto Pinto (which students report ending with a 100), 
Creative Writing with Professor Pelsue, and Research in Disciplines with 
Schroepfer. Two of the five retrieved chunks came from completely unrelated 
sources — the CS course difficulty guide and a CS112 thread.

**Root cause (tied to a specific pipeline stage):**
This is a retrieval failure caused by a vocabulary mismatch between the query 
and the source documents. The query uses formal academic language — "SAS core," 
"writing requirements," "humanities requirements" — while the source documents 
use informal student language like "easy gen ed," "easy A," "fun classes," and 
"WCr/WCd." The all-MiniLM-L6-v2 embedding model produced vectors that were not 
close enough to surface the most relevant chunks, instead pulling in CS-related 
chunks that shared more general "Rutgers course" semantic similarity with the query.

**What you would change to fix it:**
I would implement query expansion — automatically rewriting the user's query to 
include informal synonyms before embedding it. For example, "SAS core writing 
requirements" would be expanded to also search "easy gen ed writing Rutgers easy 
A WCr WCd." Alternatively, adding metadata tags to each source file (e.g., 
topic: SAS core, gen ed) and implementing metadata filtering would allow the 
system to pre-filter chunks by topic before semantic search, bypassing the 
vocabulary mismatch entirely.

---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:**  
Planning.md helped me during my implementation in numerous ways, but the way that it helped me the most would probably be with the evaluation plan. With the evaluation plan, the directions allowed me to give a proper specificity for my evaluation which I feel helped out in the long run as I tested with more vague answers and the results that I got weren't as good as the results that I got with the more specific questions.

**One way your implementation diverged from the spec, and why:**
One way my implmentation diverged from the spec was the AI tool plan. I diverged from allowing the AI to implement the functions for me fully into helping me if I had any questions, but letting me do the heavy loading for that.

---

## AI Usage

<!-- Describe at least 2 specific instances where you used an AI tool during this project.
     For each: what did you give the AI as input, what did it produce, and what did you
     change, override, or direct differently?

     "I used Claude to help me code" is not sufficient.
     "I gave Claude my Chunking Strategy section from planning.md and asked it to implement
     chunk_text(). It returned a function using a fixed character split. I overrode the
     chunk size from 500 to 200 because my documents are short reviews, not long guides." -->

**Instance 1**

- *What I gave the AI:* I gave Claude my generate() function, that lives in generate.py.
- *What it produced:*
Simplify it like this — build a context string and sources list, then pass both to the LLM:
pythoncontext = ""
sources = []
for i in range(5):
 context += f"Source: {top_five_chunks['metadatas'][0][i]['source']}\n"
 context += f"Content: {top_five_chunks['documents'][0][i]}\n\n"
 sources.append(top_five_chunks['metadatas'][0][i]['source'])
Then pass context in the user message:
python{"role": "user", "content": f"Context:\n{context}\n\nQuestion: {query}"}
And return both the answer and sources:
pythonreturn res.choices[0].message.content, sources
Rewrite the function with these fixes.
- *What I changed or overrode:* I implemented those changes into the function.

**Instance 2**

- *What I gave the AI:*
I asked if I could just import the chromadb client, and the rutgers_guide collection.
- *What it produced:*
You could import the client and collection from `embed.py`, but that's not a good idea — importing from `embed.py` would run all the embedding code every time you import it, which is slow and unnecessary.

Better to just reinitialize the client and collection in `retrieve.py` — it's only two lines and it just connects to the existing database without re-embedding anything.

So start your `retrieve.py` with the imports and initialization. What do you need to import?
- *What I changed or overrode:* 

from embed import embedding_model
import chromadb

client = chromadb.PersistentClient(path="db")
collection = client.get_or_create_collection(name="rutgers_guide")

