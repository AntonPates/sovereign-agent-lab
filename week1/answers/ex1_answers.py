"""
Exercise 1 — Answers
====================
Fill this in after running exercise1_context.py.
Run `python grade.py ex1` to check for obvious issues before submitting.
"""

# ── Part A ─────────────────────────────────────────────────────────────────

# The exact answer the model gave for each condition.
# Copy-paste from your terminal output (the → "..." part).

PART_A_PLAIN_ANSWER    = "The Haymarket Vaults"
PART_A_XML_ANSWER      = "The Albanach"
PART_A_SANDWICH_ANSWER = "The Albanach"

# Was each answer correct? True or False.
# Correct = contains "Haymarket" or "Albanach" (both satisfy all constraints).

PART_A_PLAIN_CORRECT    = True   # True or False
PART_A_XML_CORRECT      = True
PART_A_SANDWICH_CORRECT = True

# Explain what you observed. Minimum 30 words.

PART_A_EXPLANATION = """
All three conditions produced correct answers, but the model chose different valid venues depending on
formatting. PLAIN returned "The Haymarket Vaults" while XML and SANDWICH both returned "The Albanach."
This suggests that context structure influences which matching item the model latches onto first, even
when the signal-to-noise ratio is high enough for all formats to succeed.
"""

# ── Part B ─────────────────────────────────────────────────────────────────

PART_B_PLAIN_ANSWER    = "The Haymarket Vaults"
PART_B_XML_ANSWER      = "The Albanach"
PART_B_SANDWICH_ANSWER = "The Albanach"

PART_B_PLAIN_CORRECT    = True
PART_B_XML_CORRECT      = True
PART_B_SANDWICH_CORRECT = True

# Did adding near-miss distractors change any results? True or False.
PART_B_CHANGED_RESULTS = False

# Which distractor was more likely to cause a wrong answer, and why?
# Minimum 20 words.
PART_B_HARDEST_DISTRACTOR = """
The Holyrood Arms (capacity=160, vegan=yes, status=full) is the harder distractor because it satisfies
two out of three constraints — capacity and vegan — and only fails on availability. A model skimming
for keyword matches could easily select it without checking the status field. The New Town Vault fails
on vegan=no, which is more obviously disqualifying.
"""

# ── Part C ─────────────────────────────────────────────────────────────────

# Did the exercise run Part C (small model)?
# Check outputs/ex1_results.json → "part_c_was_run"
PART_C_WAS_RUN = True   # True or False

PART_C_PLAIN_ANSWER    = "Haymarket Vaults"
PART_C_XML_ANSWER      = "The Haymarket Vaults"
PART_C_SANDWICH_ANSWER = "The Haymarket Vaults"

# Explain what Part C showed, or why it wasn't needed. Minimum 30 words.
PART_C_EXPLANATION = """
Part C ran Gemma 2 2B on the distractor dataset to stress-test a weaker model. Surprisingly, all three
conditions still produced correct answers — the 2B model returned "Haymarket Vaults" across all formats.
Unlike the 70B model, the small model did not vary its pick by format, always choosing Haymarket. This
shows that even with distractors, the constraint set was explicit enough for a small model to filter
correctly, though the uniformity of answers suggests less sensitivity to structural formatting cues.
"""

# ── Core lesson ────────────────────────────────────────────────────────────

# Complete this sentence. Minimum 40 words.
# "Context formatting matters most when..."

CORE_LESSON = """
Context formatting matters most when the signal-to-noise ratio drops — longer contexts, more
distractors, weaker models, or constraints that require cross-referencing multiple fields per item.
In my experiment the 70B model handled all formats correctly, but its venue choice shifted between
PLAIN and XML/SANDWICH, proving that structure still steers attention even when accuracy is unaffected.
In production agent systems where contexts are far longer, tool outputs are noisy, and the model must
filter across dozens of candidates, structural formatting like XML tags and sandwich prompting becomes
the difference between a reliable system and one that silently picks the wrong option.
"""
