# Slide 1 - Welcome

Hamza (≈45s)
“Hi everyone, I’m Hamza El Ghoujdami, Senior Cloud & AI Tech Advisor at Microsoft. I partner with customers like G42/Core42 and MBZUAI on AI/HPC workloads and hands-on PoCs—from RAG systems to agentic workflows on Azure. Before Microsoft, I worked with AI startups at Google, mentoring teams in accelerator programs and helping founders go from MVP to first production launches. My focus today is the practical side: using Azure AI Foundry, AI Search, Agent Service, and Content Safety to ship a safe, measurable v1 agent.”

Hosam (≈30–40s)
“I’m Hosam Kamel, I lead Data & AI + Apps within Microsoft’s Customer Success Unit here in the UAE. My team helps organizations adopt GenAI responsibly—modernizing apps, measuring outcomes, and scaling what works. I’ll connect today’s patterns to what we see across customers and highlight the adoption path.”

Transition (≈10s)
“Quick housekeeping: we’ll keep the flow crisp, run a short demo, and leave time for Q&A. Let’s start with why agents now—and why this is founder-friendly.”

# Slide 2 - Agenda 
“Here’s our flow. We’ll set the ‘why’, confirm readiness in plain English, then run a compact demo showing both paths—answer and safe action—with Azure tracing. We’ll wrap with the Azure stack you can use today and a simple three-step plan to start this week, then Q&A.”

# Slide 3 - Why AI agents now

“Traditional chat gives answers; agents deliver results. An agent plans the task, pulls facts from your docs using Azure AI Search, and then safely calls tools—like creating a ticket or checking status—so work actually gets done. This is feasible now because small, cost-efficient models handle most flows, and Azure adds the pieces you need in production: Content Safety to enforce policy and AI Foundry observability to see each step in the run. The payoff is simple: quicker responses, lower handling costs, and more consistent operations. We’ll keep it narrow, prove value fast, and iterate.”

# Slide 4 - Agentic AI Readiness

“Before building, check readiness. First, do we have repeatable demand—a handful of intents that appear again and again? Second, do we have usable knowledge—even a small set like 20–30 FAQs and one onboarding PDF is enough to power Azure AI Search. Third, do we have a safe action path—at least one API the agent can call, like creating a ticket, ideally with a clear owner. If any box is missing, keep it simple: ship read-only RAG while you draft a starter FAQ or identify one action API. On Azure, the mapping is straightforward: AI Search for retrieval, Agent Service or Functions for actions, Content Safety for guardrails, and AI Foundry for tracing every step.”



Slide 5 - Demo: MVP → RAG & RAG → Agent 

“We’ll show two flows. First, a straight RAG answer: the question hits Azure AI Search using hybrid vector+keyword, and we return a grounded response with quick citations. 

Second, when confidence is low, the agent safely acts—it calls create_ticket() and returns a ticket_id, and we can follow up with get_status(id). Before and after the model call we run Content Safety so you’ll see how we block or sanitize risky input. Then we open Foundry’s trace to walk the steps—user message, retrieval results, model reasoning, and the tool I/O—so it’s explainable. Finally, we flash a tiny success panel: latency, token use, and one KPI like deflection %—the number we’ll improve week by week.”



# Pres Flow 
- Welcome/context (3) → Why now (6) → Readiness (6) → Demo (18) → Stack (10) → Start Building (10) → Q&A (7).
