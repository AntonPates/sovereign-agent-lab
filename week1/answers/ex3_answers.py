"""
Exercise 3 — Answers
====================
Fill this in after completing the three Rasa conversations.

CALM vs Old Rasa — what changed
---------------------------------
The old open-source Rasa approach used:
  - nlu.yml: intent training examples
  - rules.yml: explicit dialogue rules
  - FormValidationAction: Python class to parse slot values

Rasa Pro CALM uses:
  - flows.yml: natural language descriptions of what each flow does
  - from_llm slots: the LLM extracts values from conversation
  - ONE custom action: ActionValidateBooking for the business rules

The conversation is the same from the manager's perspective.
The machinery underneath is completely different.

CONVERSATION SCRIPTS
---------------------
Conversation 1 (happy path):
  You:    calling to confirm a booking
  Agent:  [asks guest count]
  You:    160 guests
  Agent:  [asks vegan count]
  You:    about 50 need vegan
  Agent:  [asks deposit]
  You:    £200 deposit
  Agent:  [confirms or escalates?]

Conversation 2 (deposit too high):
  Same as above but use a deposit above £300 (e.g. "£500 deposit").

Conversation 3 (out of scope):
  Start normally, then when asked for vegan count say something like
  "can you arrange parking for the speakers?" and observe what happens.
  Does CALM handle this differently than the old rules approach?
"""

# ── Conversation 1: Happy path ─────────────────────────────────────────────

CONVERSATION_1_TRACE = """
  Your input ->  calling to confirm a booking                                                                                                                                   
How many guests are you confirming for tonight's event?
Your input ->  160 guests                                                                                                                                                     
And how many of those guests will need vegan meals?
Your input ->  about 50 need vegan                                                                                                                                            
I’m sorry I am unable to understand you, could you please rephrase?
And how many of those guests will need vegan meals?
Your input ->  about 50 guests need vegan meals                                                                                                                               
What deposit amount in GBP are you proposing to secure the booking?
Your input ->  £200 deposit                                                                                                                                                   
Thank you — booking confirmed. 160 guests, 50 requiring vegan meals, £200 deposit accepted. I'll send written confirmation to the organiser shortly.
Is there anything else I can help you with?
Your input ->  No, thank you                                                                                                                                                  
Okay, I'll be around in case you need further help.
? How would you rate your experience today? 1: 👍 Satisfied (/SetSlots(csat_score=satisfied))                                                                                 
Thank you for your feedback! I'm glad I could help.
"""

CONVERSATION_1_OUTCOME = "confirmed"   # "confirmed" or "escalated"

# ── Conversation 2: Deposit too high ───────────────────────────────────────

CONVERSATION_2_TRACE = """
Your input ->  calling to confirm a booking                                                                                                                                   
How many guests are you confirming for tonight's event?
Your input ->  160 guests                                                                                                                                                     
And how many of those guests will need vegan meals?
Your input ->  about 50 need vegan                                                                                                                                            
I’m sorry I am unable to understand you, could you please rephrase?
And how many of those guests will need vegan meals?
Your input ->  about 50 guests need vegan meals                                                                                                                               
I’m sorry I am unable to understand you, could you please rephrase?
And how many of those guests will need vegan meals?
Your input ->  about 50 guests will need vegan meals                                                                                                                          
I’m sorry I am unable to understand you, could you please rephrase?
And how many of those guests will need vegan meals?
Your input ->  around 50 guests will need vegan meals                                                                                                                         
What deposit amount in GBP are you proposing to secure the booking?
Your input ->  £500 deposit                                                                                                                                                   
I need to check one thing with the organiser before I can confirm. The issue is: a deposit of £500 exceeds the organiser's authorised limit of £300. Can I call you back within 15 minutes?
Is there anything else I can help you with?
Your input ->  yes, you can call me back. Waiting for confirmation                                                                                                            
2026-04-13 16:48:57 ERROR    rasa.shared.providers.llm._base_litellm_client  - [error    ] openaillmclient.llm.timeout    error='APITimeoutError - Request timed out. Error_str: Request timed out. - timeout value=30.000000, time taken=30.000000 seconds'
2026-04-13 16:48:57 ERROR    rasa.dialogue_understanding.generator.llm_based_command_generator  - [error    ] llm_based_command_generator.llm.error error=ProviderClientAPIException('
Original error: APITimeoutError - Request timed out. Error_str: Request timed out. - timeout value=30.000000, time taken=30.000000 seconds)')
2026-04-13 16:48:57 WARNING  rasa.utils.log_utils  - [warning  ] ProviderClientAPIException occurred while predicting commands. commands=[ErrorCommand(error_type='rasa_internal_error_default', info={})] event_key=llm_command_generator.predict_commands.api_exception
Sorry, I am having trouble with that. Please try again in a few minutes.
Is there anything else I can help you with?
Your input ->  no, just waiting for confirmation                                                                                                                              
I’m sorry I am unable to understand you, could you please rephrase?
Is there anything else I can help you with?
Your input ->  no, thank you                                                                                                                                                  
I can only help with confirming tonight's venue booking. For anything else, please contact the event organiser directly.
Is there anything else I can help you with?
Your input ->  no, thank you                                                                                                                                                  
Okay, I'll be around in case you need further help.
? How would you rate your experience today? 1: 👍 Satisfied (/SetSlots(csat_score=satisfied))                                                                                 
Thank you for your feedback! I'm glad I could help.
"""

CONVERSATION_2_OUTCOME = "escalated"   # "confirmed" or "escalated"
CONVERSATION_2_REASON  = "a deposit of £500 exceeds the organiser's authorised limit of £300"   # the reason the agent gave for escalating

# ── Conversation 3: Out of scope ───────────────────────────────────────────

CONVERSATION_3_TRACE = """
Your input ->  calling to confirm a booking                                                                                                                                   
How many guests are you confirming for tonight's event?
Your input ->  160 guests                                                                                                                                                     
And how many of those guests will need vegan meals?
Your input ->  can you arrange parking for the speakers?                                                                                                                      
I can only help with confirming tonight's venue booking. For anything else, please contact the event organiser directly.
Would you like to continue with confirm booking?
"""

# Describe what CALM did after the out-of-scope message. Min 20 words.
CONVERSATION_3_WHAT_HAPPENED = """
After the out-of-scope message, CALM informed the user that it could only assist with confirming tonight's venue booking and suggested contacting the event organiser for other requests.
"""

# Compare Rasa CALM's handling of the out-of-scope request to what
# LangGraph did in Exercise 2 Scenario 3. Min 40 words.
OUT_OF_SCOPE_COMPARISON = """
In Exercise 2 Scenario 3, LangGraph also recognized the out-of-scope request and did not attempt to hallucinate an answer. However, it explicitly stated its limitations and suggested an alternative source for the information, similar to CALM's behaviour. The key difference is that CALM offered to resume the booking flow ("Would you like to continue with confirm booking?"), keeping the user on the defined path, whereas LangGraph had no built-in mechanism to return to a structured conversation flow.
"""

# ── Task B: Cutoff guard ───────────────────────────────────────────────────

TASK_B_DONE = True   # True or False

# List every file you changed.
TASK_B_FILES_CHANGED = ["exercise3_rasa/actions/actions.py"]

# How did you test that it works? Min 20 words.
TASK_B_HOW_YOU_TESTED = """
1. Uncomment the block 
 ```now = datetime.datetime.now()
        if now.hour > 16 or (now.hour == 16 and now.minute >= 45):
            return escalate(
                "it is past 16:45 — insufficient time to process the confirmation"
                " before the 5 PM deadline"
            )
  ```          
  2. Save exercise3_rasa/actions/actions.py
  3. Retrain
  4. Restart the action server
  5. Test after 16:45:
  6. Run a conversation, verify it escalates, then revert.

Conversation:
Your input ->  calling to confirm a booking                                                        
How many guests are you confirming for tonight's event?
Your input ->  160 guests                                                                          
And how many of those guests will need vegan meals?
Your input ->  about 50 need vegan                                                                 
What deposit amount in GBP are you proposing to secure the booking?
Your input ->  £200 deposit                                                                        
I need to check one thing with the organiser before I can confirm. The issue is: it is past 16:45 — insufficient time to process the confirmation before the 5 PM deadline. Can I call you back within 15 minutes?
Is there anything else I can help you with?
Your input ->  That would be all thank you                                                                 
I'm sorry, I'm not trained to help with that.
Okay, I'll be around in case you need further help.
? How would you rate your experience today? 1: 👍 Satisfied (/SetSlots(csat_score=satisfied))              
Thank you for your feedback! I'm glad I could help. 
"""

# ── CALM vs Old Rasa ───────────────────────────────────────────────────────

# In the old open-source Rasa (3.6.x), you needed:
#   ValidateBookingConfirmationForm with regex to parse "about 160" → 160.0
#   nlu.yml intent examples to classify "I'm calling to confirm"
#   rules.yml to define every dialogue path
#
# In Rasa Pro CALM, you need:
#   flow descriptions so the LLM knows when to trigger confirm_booking
#   from_llm slot mappings so the LLM extracts values from natural speech
#   ONE action class (ActionValidateBooking) for the business rules
#
# What does this simplification cost? What does it gain?
# Min 30 words.

CALM_VS_OLD_RASA = """
The LLM now handles intent classification and slot extraction — tasks that previously required
hand-written NLU training examples and regex validators in Python (e.g. parsing "about 160" into
160.0). This eliminates nlu.yml, rules.yml, and the FormValidationAction class entirely.

Python still handles the business rules: deposit limits, guest capacity, vegan ratio checks, and
the time cutoff guard. These are deterministic constraints with real operational consequences, so
they belong in auditable, testable code rather than in probabilistic LLM output.

The old approach was more predictable — regex either matches or it doesn't, and rules.yml defines
every dialogue path explicitly. With CALM, slot extraction depends on the LLM, which can
occasionally fail (as seen in Conversation 2 where "about 50 need vegan" required multiple
rephrases). The gain is dramatically less boilerplate and easier maintenance: adding a new slot
means writing a flow description, not curating dozens of NLU examples and writing a new validator.
"""

# ── The setup cost ─────────────────────────────────────────────────────────

# CALM still required: config.yml, domain.yml, flows.yml, endpoints.yml,
# rasa train, two terminals, and a Rasa Pro licence.
# The old Rasa ALSO needed nlu.yml, rules.yml, and a FormValidationAction.
#
# CALM is simpler. But it's still significantly more setup than LangGraph.
# That setup bought you something specific.
# Min 40 words.

SETUP_COST_VALUE = """
The CALM agent cannot improvise beyond what is defined in flows.yml — it cannot call a tool that
was not pre-declared, generate a freeform response to an unexpected question, or deviate from the
scripted flow steps. When the user asked about parking for speakers, CALM refused and redirected
back to the booking flow. LangGraph, by contrast, could have routed that request to an additional
tool or generated a helpful ad-hoc response because it has no fixed flow structure.

For the confirmation use case, this rigidity is a feature, not a limitation. A venue booking
agent should not improvise — it should collect exactly the required slots, enforce the business
rules, and either confirm or escalate. The setup cost (config.yml, domain.yml, flows.yml,
endpoints.yml, training, two terminals, a licence) buys you guardrails: the agent literally
cannot go off-script, which is exactly what you want when the conversation has operational and
potentially legal consequences. The trade-off is that extending the agent to handle new use cases
requires defining new flows and retraining, rather than just adding a tool function.
"""
