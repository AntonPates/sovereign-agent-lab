"""
Exercise 2 — Answers
====================
Fill this in after running exercise2_langgraph.py.
Run `python grade.py ex2` to check for obvious issues.
"""

# ── Task A ─────────────────────────────────────────────────────────────────

# List of tool names called during Task A, in order of first appearance.
# Look at [TOOL_CALL] lines in your terminal output.
# Example: ["check_pub_availability", "get_edinburgh_weather"]

TASK_A_TOOLS_CALLED = ["check_pub_availability", "check_pub_availability","calculate_catering_cost", "get_edinburgh_weather", "generate_event_flyer"]

# Which venue did the agent confirm? Must be one of:
# "The Albanach", "The Haymarket Vaults", or "none"
TASK_A_CONFIRMED_VENUE = "The Albanach"

# Total catering cost the agent calculated. Float, e.g. 5600.0
# Write 0.0 if the agent didn't calculate it.
TASK_A_CATERING_COST_GBP = 5_600.0

# Did the weather tool return outdoor_ok = True or False?
TASK_A_OUTDOOR_OK = True

# Optional — anything unexpected.
# If you used a non-default model via RESEARCH_MODEL env var, note it here.
# Example: "Used nvidia/nemotron-3-super-120b-a12b for the agent loop."
TASK_A_NOTES = "Used Qwen/Qwen3-Next-80B-A3B-Thinking for the agent loop."

# ── Task B ─────────────────────────────────────────────────────────────────
#
# The scaffold ships with a working generate_event_flyer that has two paths:
#
#   - Live mode: if FLYER_IMAGE_MODEL is set in .env, the tool calls that
#     model and returns a real image URL.
#   - Placeholder mode: otherwise (the default) the tool returns a
#     deterministic placehold.co URL with mode="placeholder".
#
# Both paths return success=True. Both count as "implemented" for grading.
# This is not the original Task B — the original asked you to write a direct
# FLUX image call, but Nebius removed FLUX on 2026-04-13. See CHANGELOG.md
# §Changed for why we pivoted the task.

# Did your run of the flyer tool produce a success=True result?
# (This will be True for both live and placeholder mode — both are valid.)
TASK_B_IMPLEMENTED = True   # True or False

# Which path did your run take? "live" or "placeholder"
# Look for the "mode" field in the TOOL_RESULT output of Task B.
# If you didn't set FLYER_IMAGE_MODEL in .env, you will get "placeholder".
TASK_B_MODE = "placeholder"

# The image URL returned by the tool. Copy exactly from your terminal output.
# In placeholder mode this will be a placehold.co URL.
# In live mode it will be a provider CDN URL.
TASK_B_IMAGE_URL = "https://placehold.co/1200x628/1a1a2e/eaeaea?text=The+Haymarket+Vaults+%7C+160+guests&id=2ef939fbbaf6"

# The prompt sent to the image model. Copy from terminal output.
TASK_B_PROMPT_USED = "Professional event flyer for Edinburgh AI Meetup, tech professionals, modern venue at The Haymarket Vaults, Edinburgh. 160 guests tonight. Warm lighting, Scottish architecture background, clean modern typography."

# Why did the agent's behaviour NOT change when Nebius removed FLUX?
# One sentence. This is the point of the lesson.
TASK_B_WHY_AGENT_SURVIVED = """
The agent's behaviour survived because the generate_event_flyer tool encapsulates the provider dependency
behind a graceful fallback — it returns success=True with a placeholder URL when no live image model is
configured, so the agent's ReAct loop never sees a failure and continues its plan unchanged.
"""

# ── Task C ─────────────────────────────────────────────────────────────────

# Scenario 1: first choice unavailable
# Quote the specific message where the agent changed course. Min 20 words.
SCENARIO_1_PIVOT_MOMENT = """
The Bow Bar does not meet the requirements (capacity 80 < 160 needed). The Albanach meets all requirements: capacity 180 (sufficient for 160 guests), vegan options available, and currently available.
"""

SCENARIO_1_FALLBACK_VENUE = "The Albanach"

# Scenario 2: impossible constraint (300 guests)
# Did the agent recommend a pub name not in the known venues list?
SCENARIO_2_HALLUCINATED = False   # True or False

# Paste the final [AI] message.
SCENARIO_2_FINAL_ANSWER = """
None of the known Edinburgh venues meet both the capacity requirement of 300 people and vegan dietary options:

- **The Albanach**: Capacity 180 (too small), vegan available  
- **The Haymarket Vaults**: Capacity 160 (too small), vegan available  
- **The Guilford Arms**: Capacity 200 (too small), **no vegan options**  
- **The Bow Bar**: Capacity 80 (too small), vegan available but currently **full**  

No venue in our list can accommodate 300 guests with vegan catering. Would you like to adjust the guest count or explore alternative options?
"""

# Scenario 3: out of scope (train times)
# Did the agent try to call a tool?
SCENARIO_3_TRIED_A_TOOL = False   # True or False

SCENARIO_3_RESPONSE = "\n\nI don't have access to train schedule information or transportation-related tools. My capabilities are limited to checking pub availability, weather in Edinburgh, catering cost calculations, and generating event flyers. For train schedules, I recommend checking National Rail Enquiries or a similar service."

# Would this behaviour be acceptable in a real booking assistant? Min 30 words.
SCENARIO_3_ACCEPTABLE = """
Yes, this is acceptable and arguably ideal for a real booking assistant. The agent correctly recognised
that train schedules are outside its tool set, refused to hallucinate an answer, and pointed the user
to National Rail Enquiries instead. A booking assistant that invents train times would be dangerous —
clear scope boundaries and honest deflection are exactly what you want in production.
"""

# ── Task D ─────────────────────────────────────────────────────────────────

# Paste the Mermaid output from `python exercise2_langgraph.py task_d` here.
TASK_D_MERMAID_OUTPUT = """
---
config:
  flowchart:
    curve: linear
---
graph TD;
        __start__([<p>__start__</p>]):::first
        agent(agent)
        tools(tools)
        __end__([<p>__end__</p>]):::last
        __start__ --> agent;
        agent -.-> __end__;
        agent -.-> tools;
        tools --> agent;
        classDef default fill:#f2f0ff,line-height:1.2
        classDef first fill-opacity:0
        classDef last fill:#bfb6fc
"""

# Compare the LangGraph graph to exercise3_rasa/data/flows.yml. Min 30 words.
TASK_D_COMPARISON = """
The LangGraph graph is a single agent→tools loop — the model decides what to do at every step, and all
routing is implicit. The Rasa flows.yml is the opposite: every possible path (confirm_booking,
handle_out_of_scope) is written out explicitly with deterministic steps. The LLM only decides which
flow to trigger; after that, Rasa executes collect→collect→collect→action in fixed order. LangGraph
gives flexibility for open-ended research; Rasa CALM gives auditability for high-stakes conversations
where you need to guarantee which steps run and in what order.
"""

# ── Reflection ─────────────────────────────────────────────────────────────

# The most unexpected thing the agent did. Min 40 words.
# Must reference a specific behaviour from your run.

MOST_SURPRISING = """
The most surprising behaviour was in Task A: the agent chose The Albanach over The Haymarket Vaults
even though both passed all constraints, and it explicitly reasoned about the capacity buffer — noting
that The Albanach's 180-seat capacity gives a 20-person buffer over the 160 requirement, while
Haymarket Vaults has "exactly 160 seats (no buffer)." It also flagged that the quiet corner for the
webinar wasn't explicitly verifiable through the tool, but inferred from the spare capacity that a
separate area could be designated. This kind of unprompted comparative reasoning and honest disclosure
of what the tool could not verify was unexpected from a ReAct loop.
"""