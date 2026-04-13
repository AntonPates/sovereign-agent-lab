"""
Exercise 4 — Answers
====================
Fill this in after running exercise4_mcp_client.py.
"""

# ── Basic results ──────────────────────────────────────────────────────────

# Tool names as shown in "Discovered N tools" output.
TOOLS_DISCOVERED = ["search_venues", "get_venue_details"]

QUERY_1_VENUE_NAME    = "The Haymarket Vaults"
QUERY_1_VENUE_ADDRESS = "1 Dalry Road, Edinburgh"
QUERY_2_FINAL_ANSWER  = "The best match for 160 guests with vegan options is **The Haymarket Vaults**, located at **1 Dalry Road, Edinburgh**. This venue exactly meets the capacity requirement (160 guests) and offers vegan menu options, with current availability confirmed."

# ── The experiment ─────────────────────────────────────────────────────────
# Required: modify venue_server.py, rerun, revert.

EX4_EXPERIMENT_DONE = True   # True or False

# What changed, and which files did or didn't need updating? Min 30 words.
EX4_EXPERIMENT_RESULT = """
After changing The Albanach's status to 'full' in mcp_venue_server.py, the agent's Query 1 results
changed: it no longer recommended The Albanach, since search_venues filtered it out as unavailable.
The Haymarket Vaults became the only match for 160+ guests with vegan options. Crucially, no client
code needed updating — exercise4_mcp_client.py was not touched. The agent discovered the same tools
dynamically and simply received different data from the server. This demonstrates the MCP separation:
venue data lives in one place, and every client sees the change immediately.
"""

# ── MCP vs hardcoded ───────────────────────────────────────────────────────

LINES_OF_TOOL_CODE_EX2 = 8   # count in exercise2_langgraph.py
LINES_OF_TOOL_CODE_EX4 = 50   # count in exercise4_mcp_client.py

# What does MCP buy you beyond "the tools are in a separate file"? Min 30 words.
MCP_VALUE_PROPOSITION = """
MCP provides dynamic tool discovery and a protocol-level contract, not just file separation. In
Exercise 2, the LangGraph agent imported tool functions directly — if a tool signature changed, the
agent code broke. With MCP, the client connects, calls list_tools(), and builds its tool bindings at
runtime. This means a second client (e.g. the Rasa CALM agent) can connect to the exact same server
without duplicating any tool logic. Adding a new tool to the server makes it instantly available to
every connected client with zero code changes on the client side.
"""

# ── PyNanoClaw architecture — SPECULATION QUESTION ─────────────────────────
#
# (The variable below is still called WEEK_5_ARCHITECTURE because the
# grader reads that exact name. Don't rename it — but read the updated
# prompt: the question is now about PyNanoClaw, the hybrid system the
# final assignment will have you build.)
#
# This is a forward-looking, speculative question. You have NOT yet seen
# the material that covers the planner/executor split, memory, or the
# handoff bridge in detail — that is what the final assignment (releases
# 2026-04-18) is for. The point of asking it here is to check that you
# have read PROGRESS.md and can imagine how the Week 1 pieces grow into
# PyNanoClaw.
#
# Read PROGRESS.md in the repo root. Then write at least 5 bullet points
# describing PyNanoClaw as you imagine it at final-assignment scale.
#
# Each bullet should:
#   - Name a component (e.g. "Planner", "Memory store", "Handoff bridge",
#     "Rasa MCP gateway")
#   - Say in one clause what that component does and which half of
#     PyNanoClaw it lives in (the autonomous loop, the structured agent,
#     or the shared layer between them)
#
# You are not being graded on getting the "right" architecture — there
# isn't one right answer. You are being graded on whether your description
# is coherent and whether you have thought about which Week 1 file becomes
# which PyNanoClaw component.
#
# Example of the level of detail we want:
#   - The Planner is a strong-reasoning model (e.g. Nemotron-3-Super or
#     Qwen3-Next-Thinking) that takes the raw task and produces an ordered
#     list of subgoals. It lives upstream of the ReAct loop in the
#     autonomous-loop half of PyNanoClaw, so the Executor never sees an
#     ambiguous task.

WEEK_5_ARCHITECTURE = """
- The Planner is a strong-reasoning model (e.g. Qwen/Qwen3-Next-80B-A3B-Thinking) that decomposes raw request into ordered subgoals (find venue, check weather, calculate cost, hand off to confirmation). It lives upstream of the autonomous-loop half, so the executor never receives an ambiguous task.
- The Executor is the Week 1 research_agent.py ReAct loop, extended with web search and file tools. It lives inside the autonomous-loop half, executing each subgoal the planner produces by reasoning across tool calls.
- The Shared MCP Tool Server is the Week 1 mcp_venue_server.py, grown to include web search, calendar, email, and booking tools. It sits in the shared layer between both halves — both the LangGraph loop and the Rasa agent discover tools from it dynamically.
- The Structured Agent is the Week 1 Rasa Pro CALM confirmation agent, wired to the shared MCP server and extended with a RAG knowledge base. It lives in the structured-agent half and handles the pub-manager phone call with deterministic flows and auditable business rules.
- The Handoff Bridge routes control between the two halves: when the autonomous loop identifies that a human conversation is needed (e.g. confirming the deposit), it delegates to the structured agent; when the structured agent needs research (e.g. looking up an alternative venue mid-call), it delegates back. It lives in the shared layer, acting as the glue that makes PyNanoClaw one system rather than two.
"""

# ── The guiding question ───────────────────────────────────────────────────
# Which agent for the research? Which for the call? Why does swapping feel wrong?
# Must reference specific things you observed in your runs. Min 60 words.

GUIDING_QUESTION_ANSWER = """
LangGraph is the right agent for research: in Exercise 2 Task A it autonomously decided to check two
venues, compared their capacity buffers, checked the weather, calculated catering, and generated a
flyer — all without being told the order. That open-ended reasoning across tools cannot be scripted
in advance. Rasa CALM is the right agent for the confirmation call: in Exercise 3 it collected slots
in a fixed order, enforced the £300 deposit limit deterministically, and escalated when the rule was
violated — no improvisation, fully auditable. Swapping them would be disastrous: a Rasa flow cannot
reason about which of two venues is better (it has no loop, no tool-selection logic), and a LangGraph
agent cannot guarantee it will always enforce the deposit limit before confirming (it might skip the
check or hallucinate an exception). The research problem needs flexibility; the confirmation problem
needs guardrails. Using one agent for both sacrifices exactly the property that matters.
"""