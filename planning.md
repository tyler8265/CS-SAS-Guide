# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

<!-- What domain did you choose? Why is this knowledge valuable and hard to find through official channels? -->

The domain I chose is Rutgers University course difficulty and survival strategies, covering CS core courses, CS electives, Calc 2, and SAS Core requirements. This knowledge is valuable because it reflects real student experiences — what professors are actually like, how hard exams are, and which courses are worth taking. It is hard to find through official channels because the Rutgers website only provides syllabi, prerequisites, and scheduling information. It does not tell you that Francisco's CS214 projects can take 100+ hours, that Centeno's CS111 videos are more useful than lecture, or which gen ed is the easiest A.


---

## Documents

<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions.
     Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->

| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
| 1 | reddit_cs111_beginner_difficulty.txt | Reddit thread on whether CS111 is beginner friendly | https://www.reddit.com/r/rutgers/comments/14ndsgd/how_geared_towards_beginners_is_cs111/ |
| 2 | reddit_cs111_exam_recovery.txt | Reddit thread on how to recover and pass CS111 before an exam | https://www.reddit.com/r/rutgers/comments/1o6x57h/am_i_cooked_cs111/ |
| 3 | rmp_centeno_cs111.txt | Rate My Professors reviews for Professor Centeno (CS111) | https://www.ratemyprofessors.com/professor/2547756 |
| 4 | reddit_cs_course_difficulty_guide.txt | Reddit post rating difficulty of CS111 through ECE424 with professor names | https://www.reddit.com/r/rutgers/comments/kpualv/review_of_rutgers_cs_part_2_classes_ratings/ |
| 5 | reddit_rutgers_cs_survival_guide.txt | Comprehensive CS major survival guide covering courses, internships, and study tips | https://www.reddit.com/r/rutgers/comments/kpuwo9/review_of_rutgers_cs_part_1_my_journey_and/ |
| 6 | reddit_calc2_how_to_pass.txt | Reddit thread on strategies for passing Calc 2 at Rutgers | https://www.reddit.com/r/rutgers/comments/1rq7xay/is_calc_2_possible_to_pass/ |
| 7 | rmp_ullman_calc152.txt | Rate My Professors reviews for Professor Ullman (Calc 152) | https://www.ratemyprofessors.com/professor/2079421 |
| 8 | reddit_easy_sas_core_classes.txt | Reddit thread recommending easy SAS core courses for freshmen | https://www.reddit.com/r/rutgers/comments/1d453s6/easy_and_fun_sas_core_classes/ |
| 9 | reddit_easy_writing_requirement_courses.txt | Reddit thread recommending easy WCr and WCd writing requirement courses | https://www.reddit.com/r/rutgers/comments/1hk4aay/can_anyone_recommend_me_an_easy_a_wcrwcd_course/ |
| 10 | reddit_cs112_how_to_get_an_a.txt | Reddit thread on how to get an A in CS112 Data Structures | https://www.reddit.com/r/rutgers/comments/eeount/how_can_i_get_an_a_in_cs112/ |
| 11 | rmp_sesh_cs112.txt | Rate My Professors reviews for Professor Sesh Venugopal (CS112) | https://www.ratemyprofessors.com/professor/182646 |
| 12 | rmp_francisco_cs214.txt | Rate My Professors reviews for Professor Francisco (CS214) | https://www.ratemyprofessors.com/professor/1833903 |

---

## Chunking Strategy

<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->

**Chunk size:**
The chunk size that I've decided to go with is 800 characters.
**Overlap:**
My overlap size is 100 characters.
**Reasoning:**
My documents are a mix of short RMP reviews and long Reddit guide paragraphs. 
Most paragraphs and reviews fall under 800 characters, so splitting by paragraph 
first keeps natural topic boundaries intact — one review or one topic per chunk. 
For paragraphs that exceed 800 characters (common in the survival guide and 
difficulty guide), I fall back to a hard cut at 800 characters with 100 characters 
of overlap. The overlap protects against key information sitting at a chunk 
boundary — for example, a CS214 paragraph that mentions Francisco's grading 
issues across two sentences won't lose context if it gets cut. Chunks that are 
too small risk cutting reviews in half with no standalone meaning, while chunks 
that are too large blend multiple topics together and hurt retrieval precision.
---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:**
I chose all-MiniLM-L6-v2 because it runs locally with no API key or rate limits, 
which is practical for a project of this size. It also handles the kind of 
informal, opinion-based text in my documents well enough for semantic similarity 
search to work effectively.
**Top-k:**
I settled on k=5 after considering the tradeoffs. Too few chunks risks returning 
a skewed picture — if someone asks how hard CS112 is and the top 3 chunks happen 
to be the minority opinion that it's easy, the LLM gets misleading context. Too 
many chunks dilutes the context with loosely related material, hurting response 
quality. 5 gives the LLM a representative sample without overwhelming it.
**Production tradeoff reflection:**
For a real deployment serving thousands of Rutgers students, I would prioritize 
accuracy and multilingual support when choosing an embedding model. Accuracy 
matters because wrong retrievals lead directly to wrong answers — a student 
making course decisions based on bad information is a real harm. Multilingual 
support matters because Rutgers is a diverse university and not all students are 
native English speakers. all-MiniLM-L6-v2 handles neither of these as well as 
a production-grade model like OpenAI's text-embedding-3-large would.---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | What do students say about CS111's difficulty and how should a complete beginner prepare? | CS111 is beginner friendly but more challenging without prior coding experience. Students recommend watching Centeno's videos on the CS111 website, doing the recitation practice slides, attending lectures, and completing all homework assignments. With Centeno, difficulty is rated 1/5 with experience and 2/5 without. |
| 2 | What are the most common complaints about Professor Francisco in CS214 and is it worth taking with him? | The most common complaints are unreasonably long and vague project descriptions, extremely slow grading, and poor communication. One student spent 110 hours on a single project. Students recommend avoiding Francisco if possible but say to take one fewer class that semester if he is your only option. |
| 3 | What do students recommend for doing well in CS112 Data Structures? | Start projects early, do all problem sets thoroughly since Sesh bases exam questions directly on them, watch Sesh's YouTube videos, study past exams available on GitHub, and focus heavily on Big O notation and runtime analysis. Attend lectures since Sesh creates all graded assignments. |
| 4 | What study strategies do Rutgers students recommend for passing Calc 2? | Memorize the formula sheet by writing it out repeatedly, do as many practice problems as possible, use the Vera problem bank on the Rutgers Calc 2 page, attend recitation, and watch Professor Ullman's YouTube videos. Pattern recognition from grinding problems matters more than brute force memorization. |
| 5 | What are the easiest SAS core courses to fulfill writing and humanities requirements at Rutgers? | For writing requirements: Structure of Information with Fausto Pinto (students report ending with a 100), Research in Disciplines with Schroepfer, and History of Work and Labor with John Lavin. For humanities: Creative Writing with Professor Pelsue (free A, asynchronous), Gods Myths and Religions with Fruchtman, and Art Appreciation online. |

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1. Conflicting opinions on professors and courses
Because my sources are real student reviews spanning multiple years and 
different professors, the system may retrieve chunks that directly contradict 
each other. For example, CS214 reviews range from "Francisco is the worst 
professor at Rutgers" to "my favorite professor as a rising junior." If the 
system retrieves both, the LLM may struggle to generate a grounded, consistent 
answer and could produce a misleading or wishy-washy response that doesn't 
actually help the student make a decision.

2. Possibility of Outdated Information
My sources range from 2018 to 2026. A student asking about a specific professor 
may receive an answer based on reviews from 5+ years ago when that professor 
taught differently, or may get information about a professor who no longer 
teaches that course at all. The system has no way to flag that retrieved chunks 
are old, which could lead to confidently stated but outdated answers — for 
example, recommending a gen ed course that is no longer offered or has changed 
its format significantly.

---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->

Document Ingestion (.txt files) → Chunking (recursive, 800 chars, 100 overlap) 
→ Embedding + Vector Store (all-MiniLM-L6-v2 + ChromaDB) 
→ Retrieval (semantic search, top-5) 
→ Generation (Groq llama-3.3-70b, grounded prompt) 
→ Gradio UI (answer + sources)

---

## AI Tool Plan

<!-- For each part of the pipeline below, describe:
     - Which AI tool you plan to use (Claude, Copilot, ChatGPT, etc.)
     - What you'll give it as input (which sections of this planning.md, which requirements)
     - What you expect it to produce
     - How you'll verify the output matches your spec

     "I'll use AI to help me code" is not a plan.
     "I'll give Claude my Chunking Strategy section and ask it to implement chunk_text()
     with my specified chunk size and overlap" is a plan. -->

**Milestone 3 — Ingestion and chunking:**
I will use Claude. I will give it my Documents section and ask 
it to implement a load_documents() function that reads all .txt files from my 
data/ folder and returns their content with filenames as metadata. I will verify 
the output by printing each loaded document and confirming the filename and 
content are correct.


I will use Claude. I will give it my Chunking Strategy section 
and ask it to implement a chunk_documents() function using recursive character 
splitting with an 800 character max and 100 character overlap, splitting on 
paragraphs first. I will verify by printing 5 random chunks and checking they 
are self-contained and under 800 characters.

**Milestone 4 — Embedding and retrieval:**
 I will use Claude. I will give it my Retrieval 
Approach section and my pipeline diagram and ask it to implement an embed_and_store() 
function using all-MiniLM-L6-v2 and ChromaDB, storing source filename as metadata. 
I will verify by querying ChromaDB and confirming chunks and metadata are stored correctly.

I will use Claude. I will give it my Retrieval Approach section 
and ask it to implement a retrieve() function that takes a query string and returns 
the top 5 most relevant chunks with source metadata. I will verify by running 3 
test queries and checking that returned chunks are relevant.

**Milestone 5 — Generation and interface:**

I will use Claude. I will give it my evaluation plan 
and grounding requirement and ask it to implement a generate() function with a 
prompt that instructs the LLM to answer only from retrieved context, plus a 
Gradio UI displaying the answer and source attribution. I will verify by testing 
an out-of-scope question and confirming the system declines to answer.