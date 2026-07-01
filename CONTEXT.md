# TestSense AI — Complete Project Context & Day-by-Day Plan
> *This file carries everything. Read it fully before starting any conversation.*

---

## 🤖 INSTRUCTIONS FOR CLAUDE — READ THIS ENTIRE SECTION FIRST

This is a context briefing file. The person who gave you this file has been working with another Claude instance to design a career-defining project. You are picking up exactly where that conversation left off.

### Who you are in this conversation:
- A **senior automation engineer with 15 years of experience**
- Also a **supportive mentor** who genuinely wants them to succeed
- Also an **interviewer from November 2026** who knows exactly what impresses
- You are **not a chatbot giving generic advice** — you know this specific project inside out

### How to behave:
- Keep conversations **slow, clear, one concept at a time**
- When they share code, **review it thoroughly** — what's good, what needs improvement
- When they're stuck, **don't just give the answer** — ask guiding questions first
- **Track their weekly milestones** — celebrate them when hit, they matter psychologically
- Occasionally **zoom out and say how to explain this in an interview**
- If motivation dips, **remind them of the November vision**
- Be **genuinely excited** — because this project is genuinely good
- Use **plain, direct language** — no jargon without explanation

### Current status when this file was created:
- Full plan designed and agreed upon
- Tech stack locked — no changes needed
- Day-by-day plan ready
- **They have NOT started building yet. Week 1 Day 1 is next.**

### Start every new session by asking:
> "Which week and day are you on? What did you finish last session? Show me any code you wrote."

### What NOT to do:
- Do not suggest changing the tech stack — it is decided
- Do not suggest Ollama or local models — user explicitly chose cloud APIs only
- Do not rush — they learn best with slow, clear explanations
- Do not add features outside the plan — scope creep kills projects
- Do not say "looks good" without actually reviewing — teach properly

---

## 👤 ABOUT THIS PERSON

| Field | Detail |
|-------|--------|
| Current company | Cognizant |
| Current role | QEA (Quality Engineering Associate) |
| Experience | 6 months at time of planning |
| Target | Crack a job interview by November 2026 (10 months experience) |
| Java skills | Selenium, TestNG, Cucumber — solid from training |
| Python skills | Basics — comfortable enough to learn fast |
| Currently learning | Agentic AI |
| Laptop RAM | 16GB+ |
| API budget | ₹0 — zero — free tiers only, absolutely no paid APIs |
| Personality | Eager, honest, asks excellent questions, thinks deeply |
| Learning style | Slow and clear, needs concepts explained before code |

### Their commitment level:
This person wants to crack an interview with under 1 year of experience. They know a genuinely useful project is their best asset. They are serious, committed, and consistent. Treat them like a motivated junior engineer who is fully invested.

### Energy note:
They came into this planning session with fire. They pushed back when things weren't clear. They asked hard questions about the LLM API, the Gemini key format, the free tier situation. They are not passive — they engage. Match that energy.

---

## 🎯 PROJECT OVERVIEW

### Project Name: **TestSense AI**
### Tagline: *Intelligent Test Failure Analysis Agent*

### What it does — one paragraph:
TestSense AI is an AI-powered agent that automatically analyzes Selenium test failures. When a test fails, the agent wakes up, collects all available evidence (stack trace, logs, screenshots), reasons through the failure using a LangChain ReAct agent, sends everything to Google Gemini for intelligent analysis, and produces a structured verdict: is this a real bug or a test maintenance issue? What exactly caused it? What should the engineer do next? The result is delivered as a clean HTML report — saving QA engineers 2-4 hours per day of manual failure investigation.

### The interview pitch — memorize this:
> "I built TestSense AI — an intelligent failure analysis agent for test automation teams. When a Selenium test fails, the agent automatically collects the stack trace, logs, and screenshot. It uses a LangChain ReAct agent to reason about the failure — deciding whether it needs more context before sending everything to Gemini for analysis. The agent classifies failures as real bugs versus test maintenance issues, gives a root cause, suggests a fix, and generates a professional HTML report. This saves QA teams 2-4 hours of daily manual investigation."

---

## 🔥 WHY THIS PROJECT EXISTS — THE 3 REAL PAINS

These are real pains in real QA teams, validated from 15 years of industry experience. Knowing and articulating these in interviews is critical.

### Pain 1 — Flaky Tests
A suite runs at 9am — 47 pass. Same suite at 11am — 43 pass, 4 fail. Same suite at 11:05am — all 47 pass. Nothing changed. Engineers waste 2+ hours investigating. Find nothing. Mark it "environment issue." Move on. This happens every single day in real teams and nobody has cleanly solved it.

### Pain 2 — Manual Failure Analysis is Brutal
CI/CD runs 300 tests overnight. Morning: 37 failures. Someone spends 3-4 hours opening each failure one by one — reading stack traces, looking at screenshots, figuring out: is this a real product bug or did our test break? That person is not fixing bugs. They are reading reports. That is completely wasted time.

### Pain 3 — Nobody Knows What to Test After a Change
Developer pushes a change to the payment module. Run all 300 tests (2 hours)? Run only payment tests (risk missing side effects)? Teams either over-test (slow feedback) or guess wrong (risky deployment).

### Which pains this project solves:
- **Layer 1 (what we build):** Solves Pain 2 completely. Reduces Pain 1.
- **Layer 2 (future):** Solves Pain 1 — Flaky Test Detector
- **Layer 3 (future):** Solves Pain 3 — Smart Test Selector

---

## 🏗️ FULL ARCHITECTURE

```
╔══════════════════════════════════════════════════════════════╗
║              TESTSENSE AI — LAYER 1 ARCHITECTURE            ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  JAVA SIDE                         PYTHON SIDE              ║
║  ─────────────────                 ──────────────────────── ║
║                                                              ║
║  Selenium Test                     failure_watcher.py        ║
║  TestNG Runner     ──reports──►    watches /reports/json/    ║
║  FailureListener   ──JSON────►     evidence_collector.py     ║
║  Log4j Logger      ──logs────►     reads JSON + logs         ║
║  Screenshot        ──PNG─────►     + screenshots             ║
║  Capture                           analyzer_agent.py         ║
║                                    LangChain ReAct Agent     ║
║                                    llm_config.py             ║
║                                    Gemini Flash API          ║
║                                    report_generator.py       ║
║                                    Jinja2 HTML Report        ║
╚══════════════════════════════════════════════════════════════╝

COMPLETE FLOW — STEP BY STEP:
═══════════════════════════════

1. Selenium test runs and FAILS
         │
         ▼
2. TestNG FailureListener fires automatically
         ├── Captures screenshot → /reports/screenshots/test_20260701.png
         ├── Writes detailed log → /reports/logs/test_20260701.log
         └── Writes failure_report.json → /reports/json/
         │
         ▼
3. Python failure_watcher.py detects new .json file
   (watchdog library watching /reports/json/ in real time)
         │
         ▼
4. evidence_collector.py reads and packages all evidence:
         ├── Stack trace from JSON
         ├── Error message and type from JSON
         ├── Log file contents
         └── Screenshot path (for agent to read)
         │
         ▼
5. analyzer_agent.py — LangChain ReAct Agent starts reasoning:
         │
         ├── Thought: "I have a NoSuchElementException.
         │            Let me read the logs for more context."
         ├── Action: read_log_file("/reports/logs/test.log")
         ├── Observation: "Log shows element #login-btn not found"
         │
         ├── Thought: "Button may have changed. Read screenshot."
         ├── Action: read_screenshot("/reports/screenshots/test.png")
         ├── Observation: "Page shows Sign In button, not Login"
         │
         └── Thought: "This is a TEST_ISSUE — locator changed."
         │
         ▼
6. Gemini Flash API processes the full evidence + reasoning
         │
         ▼
7. Structured JSON verdict returned:
         {
           "failure_type": "TEST_ISSUE",
           "root_cause": "CSS selector #login-btn no longer exists",
           "is_real_bug": false,
           "confidence": 91,
           "suggested_fix": "Update to .sign-in-button in LoginPage.java",
           "severity": "LOW"
         }
         │
         ▼
8. report_generator.py creates HTML report via Jinja2
         │
         ▼
9. /reports/html/LoginTest_20260701_103045.html ✅
   Professional report ready. Engineer never had to investigate.
```

---

## 🛠️ TECH STACK — FINAL. DO NOT CHANGE.

| Layer | Technology | Purpose | Cost |
|-------|-----------|---------|------|
| Test Framework | Java 11+ + Selenium 4 + TestNG 7 | Write and run tests | Free |
| Build Tool | Maven | Java dependency management | Free |
| Logging | Log4j 2 | Structured, readable Java logs | Free |
| JSON writing | Gson | Write failure data as JSON from Java | Free |
| Agent Framework | Python + LangChain | ReAct agent — the AI brain | Free |
| LLM API | Google Gemini 2.5 Flash | Intelligence and reasoning | Free tier |
| Gemini Python SDK | **google-genai** (NEW SDK) | Python to Gemini connection | Free |
| LangChain+Gemini | langchain-google-genai | LangChain wrapper for Gemini | Free |
| File Watching | Python watchdog | Detect new failure JSON files | Free |
| Image handling | Pillow | Read and encode screenshots | Free |
| Report Engine | Jinja2 | Generate HTML reports from templates | Free |
| Config | PyYAML + config.yaml | Clean configuration management | Free |
| Env variables | python-dotenv | Manage API keys safely | Free |
| Version Control | Git + GitHub | Portfolio and history | Free |

---

## ⚠️ CRITICAL NOTES — READ BEFORE TOUCHING GEMINI

### The API key situation (important context):
The user previously tried to use Gemini and got confused because the API key format changed. Here is the full truth:

- **Old key format:** `AIza...` — This is the old "Standard key" format. **Being deprecated. Will stop working in September 2026.**
- **New key format:** `AQ.Ab...` — This is the new "Auth key" format. **This is correct. This is what you get when you create a key today.**
- The user's previous attempt failed because they used the **old `google-generativeai` package** (now deprecated) with the new key format. That mismatch caused the error.

### The correct setup:
```
1. Get key from: https://aistudio.google.com/apikey
   → Your key will start with AQ.Ab... — this is RIGHT
   → No credit card needed
   → Free tier: 1500 requests/day, 60 req/min

2. Install: pip install google-genai
   → NOT google-generativeai (that's deprecated)
   → The package name is google-genai

3. Use in code:
   from google import genai
   client = genai.Client(api_key="AQ.Ab...your_key")
```

### What NOT to install:
```
pip install google-generativeai  ← DEPRECATED. DO NOT USE.
```

---

## 📁 COMPLETE PROJECT FOLDER STRUCTURE

```
testsense-ai/                          ← Root folder (create this first)
│
├── java-tests/                        ← Maven Java project
│   ├── pom.xml                        ← Maven dependencies
│   └── src/
│       ├── main/
│       │   ├── java/
│       │   │   └── utils/
│       │   │       ├── FailureListener.java    ← TestNG listener (main)
│       │   │       ├── ScreenshotUtil.java      ← Screenshot capture
│       │   │       ├── FailureReportWriter.java ← Writes JSON reports
│       │   │       └── DriverManager.java       ← WebDriver management
│       │   └── resources/
│       │       └── log4j2.xml                  ← Logging configuration
│       └── test/
│           └── java/
│               ├── tests/
│               │   ├── LoginTest.java           ← Sample test (fails intentionally)
│               │   └── SearchTest.java          ← Another sample test
│               └── pages/
│                   ├── LoginPage.java           ← Page Object Model
│                   └── SearchPage.java          ← Page Object Model
│
├── agent/                             ← Python AI agent (the brain)
│   ├── main.py                        ← Entry point — run this to start
│   ├── failure_watcher.py             ← Watches /reports/json/ for new files
│   ├── evidence_collector.py          ← Reads JSON + logs + screenshots
│   ├── analyzer_agent.py              ← LangChain ReAct agent core
│   ├── llm_config.py                  ← Gemini API connection + config
│   ├── report_generator.py            ← Jinja2 HTML report creator
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── log_reader.py              ← Tool: reads log files
│   │   ├── screenshot_reader.py       ← Tool: reads/encodes screenshots
│   │   └── failure_analyzer.py        ← Tool: sends to Gemini
│   └── templates/
│       └── report_template.html       ← HTML report template
│
├── reports/                           ← Auto-generated output (in .gitignore)
│   ├── json/                          ← Failure JSONs from Java
│   ├── screenshots/                   ← PNGs from Java tests
│   ├── logs/                          ← Log files from Java
│   └── html/                          ← Final HTML reports for engineers
│
├── config.yaml                        ← All configuration in one place
├── requirements.txt                   ← Python dependencies
├── .env                               ← API keys (NEVER commit this)
├── .gitignore                         ← Must ignore .env and reports/
└── README.md                          ← Your portfolio showpiece
```

---

## 🗺️ 8-WEEK OVERVIEW

| Week | Phase | Theme | End Milestone |
|------|-------|-------|---------------|
| 1 | Learn | Python setup + Gemini API | Gemini analyzes a test failure |
| 2 | Learn | LangChain fundamentals | LangChain calls custom tools |
| 3 | Build | ReAct agent — the brain | Agent reasons through failures on its own |
| 4 | Build | Java test side setup | Java test auto-generates JSON + screenshot |
| 5 | Build | Connect Java → Python | Java fails → Python agent wakes automatically |
| 6 | Integrate | Full pipeline + classification | Complete pipeline works reliably |
| 7 | Polish | HTML report generation | Beautiful HTML reports auto-generated |
| 8 | Polish | GitHub + demo prep | Project live, interview-ready |
| 9 | Buffer | Edge cases + deep prep | Every component explained confidently |

---

---

# 📅 DETAILED DAY-BY-DAY PLAN

> **The golden rule:** Learn only what you are about to build with immediately. Never learn ahead.

---

## ═══════════════════════════════════════
## PHASE 1: LEARN THE TOOLS (Week 1–2)
## ═══════════════════════════════════════

---

## WEEK 1: Python Setup + Gemini API

**Week goal:** Make a Python script that sends a real test failure to Gemini and gets back an intelligent structured analysis.

**Time required:** 2–3 hours per day.

---

### Day 1 — Python environment + project structure

**Why this day matters:** Everything you build sits inside a proper Python environment. Get this right once and never think about it again.

**Concepts to understand:**
- What is a virtual environment and why you cannot skip it (different projects need different package versions — venv keeps them separate)
- pip and requirements.txt — installing and tracking dependencies
- How to create the project folder structure

**Step-by-step tasks:**
```
1. Install Python 3.10 or higher if not already installed
   → Verify: python --version or python3 --version

2. Create the project:
   mkdir testsense-ai
   cd testsense-ai

3. Create virtual environment:
   python -m venv venv

4. Activate it:
   Mac/Linux: source venv/bin/activate
   Windows:   venv\Scripts\activate
   → Your terminal prompt will show (venv) — that means it is active

5. Create the full folder structure:
   mkdir -p agent/tools agent/templates
   mkdir -p java-tests/src/main/java/utils
   mkdir -p java-tests/src/test/java/tests
   mkdir -p java-tests/src/test/java/pages
   mkdir -p java-tests/src/main/resources
   mkdir -p reports/json reports/screenshots reports/logs reports/html

6. Create requirements.txt with these contents:
   google-genai
   python-dotenv

7. Install dependencies:
   pip install -r requirements.txt

8. Verify:
   pip list
   → You should see google-genai and python-dotenv in the list
```

**Exercises to reinforce:**
1. Deactivate the venv with `deactivate`. Then reactivate it. Notice the terminal prompt change. Understand what just happened.
2. Run `pip list` before and after activating venv. See the difference.
3. Answer this question in your own words (write it down): "Why do we need a virtual environment? What goes wrong without it?"
4. Create a file called `notes.md` in the project root and write your answer there.

**End of day checklist:**
- [ ] Project folder exists: `testsense-ai/`
- [ ] All subfolders created
- [ ] venv created and activates without errors
- [ ] requirements.txt exists with 2 packages
- [ ] `pip install` ran without errors
- [ ] `pip list` shows the installed packages

**Common problems and fixes:**
- `python not found` → try `python3` instead
- Permission error on Windows → run terminal as administrator
- Pip not found → `python -m pip install` instead of `pip install`

---

### Day 2 — Gemini API key + environment variables

**Why this day matters:** You need the API key. And you need to learn to never hardcode it in your code — because hardcoded secrets in GitHub is a career-ending mistake in real companies.

**Concepts to understand:**
- Google AI Studio and how to get a key
- The new AQ. key format (explained in the Critical Notes section above)
- Environment variables — what they are: named values stored outside your code
- python-dotenv — reads a .env file and loads variables into Python's environment
- .gitignore — files Git must never track

**Step-by-step tasks:**
```
1. Go to: https://aistudio.google.com/apikey
   → Sign in with your Google account
   → Click "Create API key"
   → Your key will start with AQ.Ab... — this is CORRECT, not an error

2. Create .env file in testsense-ai/ root:
   GEMINI_API_KEY=AQ.Ab...paste_your_full_key_here

3. Create .gitignore in testsense-ai/ root:
   .env
   venv/
   __pycache__/
   *.pyc
   reports/
   .idea/
   *.class
   target/

4. Create agent/llm_config.py:
```
```python
# agent/llm_config.py
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()  # This reads .env and loads all variables

def get_gemini_client() -> genai.Client:
    """Creates and returns a configured Gemini client."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found. Did you create .env?")
    return genai.Client(api_key=api_key)

if __name__ == "__main__":
    client = get_gemini_client()
    print("Gemini client created successfully.")
    print(f"Client type: {type(client)}")
```
```
5. Run it: python agent/llm_config.py
   → Should print: "Gemini client created successfully."
```

**Exercises to reinforce:**
1. What happens if you delete the GEMINI_API_KEY line from .env and run the file? Try it. Read the error. Put it back.
2. What happens if you accidentally push .env to GitHub? (Answer: your API key is now public. Anyone can use it and Google will likely revoke it.)
3. Add a second fake variable to .env called `APP_ENV=development`. Read it in Python with `os.getenv("APP_ENV")`. Print it. This proves you understand how env variables work.

**End of day checklist:**
- [ ] API key obtained from AI Studio (AQ. format)
- [ ] .env created with key
- [ ] .gitignore created and includes .env
- [ ] llm_config.py runs without errors
- [ ] You understand WHY .env is in .gitignore

---

### Day 3 — First real Gemini API call

**Why this day matters:** This is the first moment the AI actually does something for you. It is motivating and educational.

**Concepts to understand:**
- `client.models.generate_content()` — the main call
- `model="gemini-2.5-flash"` — why Flash (free tier, fast, good enough)
- `response.text` — getting the text out of the response
- What tokens are (briefly — units of text, you pay/limit by them)

**Step-by-step tasks:**

Create `agent/test_gemini.py`:
```python
# agent/test_gemini.py
from llm_config import get_gemini_client

client = get_gemini_client()

# Step 1 — Basic sanity check
print("Step 1: Basic sanity check")
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Say hello and confirm you are ready to analyze test failures."
)
print(response.text)
print("-" * 50)

# Step 2 — Send a real fake test failure
print("Step 2: Fake test failure analysis")
fake_failure = """
Test Name: LoginTest.testValidLogin
Error Type: org.openqa.selenium.NoSuchElementException
Error Message: no such element: Unable to locate element: {"method":"css selector","selector":"#login-btn"}
Stack Trace:
    at LoginPage.clickLoginButton(LoginPage.java:47)
    at LoginTest.testValidLogin(LoginTest.java:23)
    at sun.reflect.NativeMethodAccessorImpl.invoke0(Native Method)
Browser: Chrome 124
Environment: staging
"""

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=f"You are a test failure expert. Analyze this failure:\n\n{fake_failure}"
)
print(response.text)
```

Run it: `python agent/test_gemini.py`

**Exercises to reinforce:**
1. Change the error type to `TimeoutException`. What does Gemini say now? Is the analysis different?
2. Change the error to `AssertionError: Expected 'Payment Successful' but got 'Payment Failed'`. What does Gemini classify this as? Should it be a real bug or test issue?
3. Try a 500 Internal Server Error in the payload. What does Gemini think?
4. What is the difference between `response.text` and `response`? Print both.

**End of day checklist:**
- [ ] Basic Gemini call works (Step 1 runs)
- [ ] Fake failure analyzed (Step 2 runs)
- [ ] You have seen at least 3 different failure types analyzed
- [ ] You understand what `response.text` contains

---

### Day 4 — Prompt engineering for consistent JSON output

**Why this day matters:** Right now Gemini answers in free text. We need it to answer in a specific JSON format every single time. This is prompt engineering — one of the most important skills for building AI applications.

**Concepts to understand:**
- System instruction — a fixed instruction that shapes ALL responses from Gemini
- Why JSON output matters: Python can parse JSON but not free text
- `json.loads()` — converting a JSON string into a Python dictionary
- `try/except` for JSON parsing — what if Gemini doesn't return valid JSON?

**Step-by-step tasks:**

Update `agent/test_gemini.py`:
```python
# agent/test_gemini.py — Day 4 version
import json
from llm_config import get_gemini_client

client = get_gemini_client()

# System instruction — this shapes EVERY response
SYSTEM_INSTRUCTION = """
You are an expert test failure analyzer with 15 years of QA experience.
When given a test failure, analyze it and respond ONLY in this exact JSON format:
{
  "failure_type": "TEST_ISSUE or REAL_BUG or ENVIRONMENT_ISSUE",
  "root_cause": "one clear sentence explaining the root cause",
  "is_real_bug": true or false,
  "confidence": integer from 0 to 100,
  "suggested_fix": "one clear actionable sentence on how to fix this",
  "severity": "LOW or MEDIUM or HIGH"
}

Rules:
- TEST_ISSUE: the test code itself is wrong (bad locator, wrong expected value, timing)
- REAL_BUG: the application has a bug (wrong behavior, API error, missing feature)
- ENVIRONMENT_ISSUE: infrastructure failure (DB down, network, 3rd party service)
- confidence: how sure you are (0=guessing, 100=certain)
- Respond ONLY with the JSON. No text before or after. No markdown backticks.
"""

failure = """
Test Name: LoginTest.testValidLogin
Error: NoSuchElementException
Message: Unable to locate element: #login-btn
Stack: at LoginPage.clickLoginButton(LoginPage.java:47)
"""

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=failure,
    config={"system_instruction": SYSTEM_INSTRUCTION}
)

print("Raw response:")
print(response.text)
print()

# Parse it
try:
    result = json.loads(response.text)
    print("Parsed successfully:")
    print(f"  Type:       {result['failure_type']}")
    print(f"  Cause:      {result['root_cause']}")
    print(f"  Is bug:     {result['is_real_bug']}")
    print(f"  Confidence: {result['confidence']}%")
    print(f"  Fix:        {result['suggested_fix']}")
    print(f"  Severity:   {result['severity']}")
except json.JSONDecodeError as e:
    print(f"JSON parsing failed: {e}")
    print("Gemini did not return valid JSON — refine the prompt")
```

**Exercises to reinforce:**
1. Test with 3 different failures. Does the JSON come back consistently every time?
2. What happens if you remove "No markdown backticks" from the system instruction? Try it. Does Gemini add ```json ``` around the response?
3. Write a function `safe_parse_json(text: str) -> dict or None` that handles JSON parsing failures gracefully.
4. What is the difference between confidence 45 and confidence 90 in your results? Does it make intuitive sense?

**End of day checklist:**
- [ ] System instruction defined and working
- [ ] Gemini returns consistent JSON structure
- [ ] `json.loads()` parses it successfully
- [ ] try/except handles JSON errors
- [ ] You understand what each field in the JSON means

---

### Day 5 — Build llm_config.py properly + WEEK 1 MILESTONE

**Why this day matters:** Turn everything from this week into clean, production-quality code. Functions, not scripts. This is the foundation everything else builds on.

**Concepts to understand:**
- Organizing code into functions (not just top-level scripts)
- Type hints in Python: `def analyze_failure(text: str) -> dict:`
- `if __name__ == "__main__":` — why this exists
- Clean code principles: one function, one job

**Step-by-step tasks:**

Rewrite `agent/llm_config.py` completely:
```python
# agent/llm_config.py — Final Week 1 version
import os
import json
import logging
from typing import Optional
from dotenv import load_dotenv
from google import genai

load_dotenv()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

MODEL = "gemini-2.5-flash"

SYSTEM_INSTRUCTION = """
You are an expert test automation failure analyst with 15 years of QA experience.
Your job is to analyze test failures and classify them with high accuracy.

Respond ONLY in this exact JSON format — no other text, no markdown:
{
  "failure_type": "TEST_ISSUE | REAL_BUG | ENVIRONMENT_ISSUE",
  "root_cause": "one clear sentence",
  "is_real_bug": true or false,
  "confidence": 0-100,
  "suggested_fix": "one clear actionable sentence",
  "severity": "LOW | MEDIUM | HIGH"
}

Classification rules:
- TEST_ISSUE: locator changed, wrong selector, bad test data, timing issue
- REAL_BUG: application logic wrong, API error, feature broken
- ENVIRONMENT_ISSUE: DB down, network failure, infrastructure problem
"""


def get_gemini_client() -> genai.Client:
    """Creates and returns a Gemini client using the API key from .env."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not set. Check your .env file.")
    return genai.Client(api_key=api_key)


def analyze_failure(failure_text: str) -> Optional[dict]:
    """
    Sends a test failure description to Gemini and returns structured analysis.
    
    Args:
        failure_text: Description of the test failure including error, stack trace, etc.
        
    Returns:
        Dictionary with failure_type, root_cause, is_real_bug, confidence,
        suggested_fix, severity — or None if analysis failed.
    """
    try:
        client = get_gemini_client()
        response = client.models.generate_content(
            model=MODEL,
            contents=failure_text,
            config={"system_instruction": SYSTEM_INSTRUCTION}
        )
        
        # Clean response — remove markdown if Gemini adds it
        text = response.text.strip()
        if text.startswith("```"):
            text = text[text.find("{"):text.rfind("}")+1]
        
        result = json.loads(text)
        logger.info(f"Analysis complete: {result['failure_type']} (confidence: {result['confidence']}%)")
        return result
        
    except json.JSONDecodeError as e:
        logger.error(f"JSON parsing failed: {e}. Raw: {response.text[:200]}")
        return None
    except Exception as e:
        logger.error(f"Gemini analysis failed: {e}")
        return None


if __name__ == "__main__":
    # Quick self-test
    test_input = """
    Test: LoginTest.testValidLogin
    Error: NoSuchElementException on selector #login-btn
    Stack: at LoginPage.java:47
    Environment: staging, Chrome 124
    """
    
    print("Running self-test...")
    result = analyze_failure(test_input)
    
    if result:
        print("\n✅ WEEK 1 MILESTONE ACHIEVED")
        print(f"   Type:       {result['failure_type']}")
        print(f"   Cause:      {result['root_cause']}")
        print(f"   Is bug:     {result['is_real_bug']}")
        print(f"   Confidence: {result['confidence']}%")
        print(f"   Fix:        {result['suggested_fix']}")
    else:
        print("\n❌ Analysis failed — check logs above")
```

Run: `python agent/llm_config.py`

**Exercises to reinforce:**
1. Call `analyze_failure()` 5 times with 5 different failures in a loop. Print all results.
2. What does `Optional[dict]` mean in the return type? Why `Optional` instead of just `dict`?
3. What does `if __name__ == "__main__":` do? Why not just write the test code at the top level?
4. Add a `validate_result(result: dict) -> bool` function that checks if all required keys are present.

**🏆 WEEK 1 MILESTONE:**
- [ ] `python agent/llm_config.py` runs and shows analysis results
- [ ] JSON is parsed and all fields are populated
- [ ] Code is in functions, not just top-level scripts
- [ ] Logger messages are clear and informative
- [ ] You can explain what each function does in one sentence

**Celebrate this milestone.** The AI brain is connected. Week 1 complete.

---

## WEEK 2: LangChain Fundamentals

**Week goal:** Build two custom LangChain tools that a future ReAct agent can call automatically to gather evidence about a test failure.

**Why LangChain when you already have Gemini?**
Direct Gemini calls are one-shot — you ask, you get an answer. An agent needs to reason in a loop: decide what it needs, call a function to get it, see the result, decide what to do next. LangChain gives you this loop. It is the difference between a chatbot and an agent.

---

### Day 1 — Install LangChain + basic ChatModel

**Concepts to understand:**
- LangChain is a framework that sits on top of any LLM (including Gemini)
- `ChatGoogleGenerativeAI` — LangChain's wrapper for Gemini
- Why use the wrapper: LangChain makes Gemini compatible with the agent system
- `.invoke()` — how you call a chat model in LangChain

**Step-by-step tasks:**

Add to requirements.txt:
```
langchain
langchain-google-genai
langchain-core
```
Run: `pip install -r requirements.txt`

Create `agent/langchain_test.py`:
```python
# agent/langchain_test.py
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0.1
)

response = llm.invoke("What is a NoSuchElementException in Selenium? One paragraph.")
print(response.content)
print()
print(f"Response type: {type(response)}")
```

Run: `python agent/langchain_test.py`

**Exercises to reinforce:**
1. What is the difference between `response.text` (from raw Gemini SDK) and `response.content` (from LangChain)? Why different attribute names?
2. What does `temperature=0.1` mean? Change it to `temperature=0.9`. Does the response feel different? More creative? More random?
3. What would break if you set temperature to 0? To 2.0? (2.0 is too high — Gemini may refuse)

**End of day checklist:**
- [ ] LangChain and langchain-google-genai installed
- [ ] ChatGoogleGenerativeAI works and returns a response
- [ ] You understand the difference between direct Gemini SDK and LangChain wrapper

---

### Day 2 — Prompt Templates

**Concepts to understand:**
- `ChatPromptTemplate` — reusable, parameterized prompt with system + user messages
- Variables in templates: `{test_name}`, `{error_type}`, etc.
- LCEL pipe operator `|` — chains components together
- `.invoke()` with variables filling in the template

**Step-by-step tasks:**

Create `agent/prompt_test.py`:
```python
# agent/prompt_test.py
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0.1
)

# Create a reusable template
analysis_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are an expert test failure analyzer.
    Analyze the given failure. Respond in 2-3 clear sentences:
    1. What type of issue is this (TEST_ISSUE, REAL_BUG, or ENVIRONMENT_ISSUE)?
    2. What is the likely cause?
    3. What should the engineer do?"""),
    ("human", """Analyze this failure:
    Test: {test_name}
    Error: {error_type}
    Message: {error_message}
    Stack: {stack_trace}
    """)
])

# Create a chain using | operator
chain = analysis_prompt | llm

# Invoke with variables
result = chain.invoke({
    "test_name": "LoginTest.testValidLogin",
    "error_type": "NoSuchElementException",
    "error_message": "Unable to locate element: #login-btn",
    "stack_trace": "at LoginPage.clickLoginButton(LoginPage.java:47)"
})

print(result.content)
```

**Exercises to reinforce:**
1. What does the `|` operator do between `analysis_prompt` and `llm`? This is called LCEL (LangChain Expression Language). Look it up briefly.
2. Add variables for `{browser}` and `{environment}` to the template. Fill them in when invoking.
3. Create a completely different template for a different use case: "Explain this log line to a junior engineer." Test it.
4. What happens if you invoke the chain without providing a required variable? Try it deliberately and read the error.

**End of day checklist:**
- [ ] ChatPromptTemplate created and working
- [ ] Variables fill in correctly in the template
- [ ] Chain with `|` operator works
- [ ] You understand what each part of `chain = template | llm` does

---

### Day 3 — Tools concept — functions the agent can call

**Why this matters:** Tools are the hands of the agent. The ReAct agent (next week) reads tool docstrings to decide when to call which tool. This is not metaphorical — the LLM literally reads your docstring text to make that decision. Write them well.

**Concepts to understand:**
- `@tool` decorator — wraps a Python function as a LangChain tool
- Why docstrings are mandatory and critical (the agent reads them)
- `.invoke()` on a tool — how to call it manually for testing
- Type hints are required in tool functions

**Step-by-step tasks:**

Create `agent/tools/log_reader.py`:
```python
# agent/tools/log_reader.py
from langchain_core.tools import tool

@tool
def read_log_file(file_path: str) -> str:
    """
    Reads a test execution log file and returns its full contents as text.
    
    Use this tool when you need to understand what happened during test execution —
    for example, to see what page was loaded, what elements were found, or what
    errors occurred in the application logs during the test run.
    
    Args:
        file_path: The absolute or relative path to the .log file
        
    Returns:
        The complete log file contents as a string, or an error message if not found
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if not content.strip():
            return "Log file exists but is empty."
            
        return content
        
    except FileNotFoundError:
        return f"Log file not found at: {file_path}"
    except PermissionError:
        return f"Permission denied reading: {file_path}"
    except Exception as e:
        return f"Error reading log file: {str(e)}"


if __name__ == "__main__":
    # Manual test
    result = read_log_file.invoke({"file_path": "nonexistent.log"})
    print(f"Result: {result}")
    
    # Create a temporary log and test it
    with open("/tmp/test.log", "w") as f:
        f.write("INFO - 2026-07-01 10:30:00 - Test started\n")
        f.write("INFO - 2026-07-01 10:30:01 - Browser opened: Chrome\n")
        f.write("ERROR - 2026-07-01 10:30:05 - Element #login-btn not found after 10s\n")
    
    result = read_log_file.invoke({"file_path": "/tmp/test.log"})
    print(f"Log contents:\n{result}")
```

**Critical note about docstrings:**
Notice how the docstring explains WHEN to use the tool, not just what it does. The agent reads: "Use this tool when you need to understand what happened during test execution." That sentence tells the agent exactly when to call this tool. This is how the agent makes decisions.

**Exercises to reinforce:**
1. Create a tool with a bad docstring ("reads a file") and a good docstring (as shown above). Ask yourself: if you were an AI agent, which would you know how to use?
2. What happens if a tool raises an exception? Test it. Does it crash or return an error string?
3. Create a third tool: `get_current_timestamp() -> str` that returns the current date and time. When would an agent use this?

**End of day checklist:**
- [ ] `@tool` decorator understood and used
- [ ] `read_log_file` tool created in `agent/tools/log_reader.py`
- [ ] Docstring is clear, specific, and tells the agent WHEN to use this tool
- [ ] Tool tested manually with `.invoke()`

---

### Day 4 — Screenshot reader tool

**Concepts to understand:**
- Reading binary files in Python (`open(path, 'rb')`)
- Base64 encoding — why we convert images to text strings for APIs
- Pillow library — image manipulation in Python
- File validation — check the file exists and is the right type before reading

**Step-by-step tasks:**

Add to requirements.txt: `Pillow`
Run: `pip install -r requirements.txt`

Create `agent/tools/screenshot_reader.py`:
```python
# agent/tools/screenshot_reader.py
import base64
import os
from pathlib import Path
from langchain_core.tools import tool

@tool
def read_screenshot(screenshot_path: str) -> str:
    """
    Reads a test failure screenshot and returns information about what was visible.
    
    Use this tool when you need visual context about what was on screen when the
    test failed — for example, to see if the correct page loaded, what UI elements
    were visible, or if there was an error message on screen.
    
    Args:
        screenshot_path: Path to the .png screenshot file
        
    Returns:
        A description of the screenshot file including its size and confirmation
        it was loaded, or an error message if the file cannot be read
    """
    try:
        path = Path(screenshot_path)
        
        if not path.exists():
            return f"Screenshot not found at: {screenshot_path}"
        
        if path.suffix.lower() not in ['.png', '.jpg', '.jpeg']:
            return f"Expected image file (.png/.jpg), got: {path.suffix}"
        
        file_size = path.stat().st_size
        
        if file_size > 10 * 1024 * 1024:  # 10MB limit
            return f"Screenshot too large ({file_size} bytes). Max 10MB."
        
        with open(screenshot_path, 'rb') as f:
            image_bytes = f.read()
        
        encoded = base64.b64encode(image_bytes).decode('utf-8')
        
        return (
            f"Screenshot loaded successfully. "
            f"File: {path.name}, "
            f"Size: {file_size} bytes, "
            f"Base64 length: {len(encoded)} chars. "
            f"Screenshot is ready for visual analysis."
        )
        
    except Exception as e:
        return f"Error reading screenshot: {str(e)}"


if __name__ == "__main__":
    # Test with a non-existent file
    result = read_screenshot.invoke({"screenshot_path": "/nonexistent/path.png"})
    print(f"Missing file result: {result}")
```

**Why Base64?**
APIs communicate through text (JSON). You cannot send raw binary image data in JSON directly. Base64 converts binary bytes into a string of printable ASCII characters. That string can be sent through any text-based API. On the receiving end, you decode it back to binary.

**Exercises to reinforce:**
1. What is base64? Encode the word "TestSense" to base64 manually using Python: `import base64; base64.b64encode(b"TestSense").decode()`. Decode it back.
2. What happens if `screenshot_path` points to a text file instead of a PNG? Does the tool handle it?
3. Add file size validation: if file is larger than 5MB, return a warning instead of loading.
4. Why is the file size check at 10MB? What happens on mobile devices where screenshots might be very large?

**End of day checklist:**
- [ ] Pillow installed
- [ ] `read_screenshot` tool created and works
- [ ] Base64 encoding understood (not just used — understood)
- [ ] File validation catches missing and wrong-type files

---

### Day 5 — Bind tools to LLM + WEEK 2 MILESTONE

**Why this day matters:** Binding tools to the LLM teaches it what tools are available. When you then send a message, the LLM can respond with a tool call instead of a text answer — it says "I need to call read_log_file before I can answer." That is the foundation of an agent.

**Concepts to understand:**
- `llm.bind_tools([tool1, tool2])` — tells the LLM what tools exist
- `response.tool_calls` — when the LLM wants to call a tool, this field is populated
- Tools do not run automatically — the agent framework (Week 3) handles that
- This day is about proving the LLM KNOWS about your tools and WANTS to use them

**Step-by-step tasks:**

Create `agent/tools/__init__.py`:
```python
# agent/tools/__init__.py
from agent.tools.log_reader import read_log_file
from agent.tools.screenshot_reader import read_screenshot

ALL_TOOLS = [read_log_file, read_screenshot]
```

Create `agent/tools_test.py`:
```python
# agent/tools_test.py
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

load_dotenv()

from tools.log_reader import read_log_file
from tools.screenshot_reader import read_screenshot

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0.1
)

# Bind tools to the LLM
llm_with_tools = llm.bind_tools([read_log_file, read_screenshot])

# Test 1 — Ask something that needs a tool
print("Test 1 — Message that requires a tool:")
response = llm_with_tools.invoke(
    "A Selenium test failed. The log file is at /reports/logs/login.log. Read it and tell me what happened."
)
print(f"Content: {response.content}")
print(f"Tool calls: {response.tool_calls}")
print()

# Test 2 — Ask something that does NOT need a tool
print("Test 2 — Message that does not need a tool:")
response = llm_with_tools.invoke(
    "What does NoSuchElementException mean in Selenium?"
)
print(f"Content: {response.content}")
print(f"Tool calls: {response.tool_calls}")
```

**Exercises to reinforce:**
1. Print `response.tool_calls` fully. What is inside it? What arguments did the LLM decide to pass to the tool?
2. Try 3 different messages. Predict before running: will the LLM call a tool or not? Were you right?
3. Bind only `read_log_file` (not screenshot). Now ask about a screenshot. What happens? Does it still try to call a tool?

**🏆 WEEK 2 MILESTONE:**
- [ ] Two tools created: `read_log_file` and `read_screenshot`
- [ ] Tools bound to LLM successfully
- [ ] LLM correctly decides when to call tools (Test 1 shows tool_calls, Test 2 does not)
- [ ] `agent/tools/__init__.py` exists with ALL_TOOLS list

**Celebrate this milestone.** The agent now has hands. Next week you give it a brain that decides when to use them.

---

---

## ═══════════════════════════════════════
## PHASE 2: BUILD THE CORE (Week 3–5)
## ═══════════════════════════════════════

---

## WEEK 3: ReAct Agent — The Brain

**Week goal:** Build a working ReAct agent that autonomously reasons through a test failure, decides what tools to call, calls them, and produces a structured verdict.

**The big concept — ReAct (Reason + Act):**
A single LLM call gives you one answer. A ReAct agent gives you a loop:
```
Thought → Action (tool call) → Observation (tool result) → Thought → Action → ... → Final Answer
```
The agent keeps going until it has enough information to be confident. That is why it is smarter than a single call.

---

### Day 1 — Understand ReAct deeply (conceptual day — no coding)

**Why a full day on concepts?** The ReAct loop is the core of this entire project. If you build it without understanding it, you will not be able to explain it in interviews and you will not be able to debug it when it breaks.

**Do this today:**

Read this complete ReAct trace carefully. Every line:
```
INPUT: LoginTest failed with NoSuchElementException on #login-btn.
       Log at /reports/logs/login.log. Screenshot at /reports/screenshots/login.png

THOUGHT: I have a NoSuchElementException on a CSS selector. 
         This could be a changed locator (TEST_ISSUE) or a page that didn't load 
         (ENVIRONMENT_ISSUE). I need more information. Let me read the log file first.

ACTION: read_log_file
ACTION INPUT: /reports/logs/login.log

OBSERVATION: "2026-07-01 10:30 INFO - Chrome started. Page loaded: /login. 
              2026-07-01 10:30 INFO - Waiting for element #login-btn. 
              2026-07-01 10:30 ERROR - Element not found after 10s timeout."

THOUGHT: The page loaded correctly (not an environment issue). The element simply
         wasn't found. The selector #login-btn might have changed in the UI.
         Let me look at the screenshot to confirm what's on the page.

ACTION: read_screenshot
ACTION INPUT: /reports/screenshots/login.png

OBSERVATION: Screenshot loaded. Shows login page with a button labeled 'Sign In'
             (not 'Login'). The button appears to have a different CSS class.

THOUGHT: Now I understand. The login button changed from id='login-btn' to a 
         different selector. The page loaded fine, the test simply has a stale 
         locator. This is definitively a TEST_ISSUE, not a real bug.
         Confidence: 92%. I have enough to give a final answer.

FINAL ANSWER: {
  "failure_type": "TEST_ISSUE",
  "root_cause": "Login button selector #login-btn changed to a new CSS class",
  "is_real_bug": false,
  "confidence": 92,
  "suggested_fix": "Update the login button locator in LoginPage.java",
  "severity": "LOW"
}
```

**Exercises (on paper, not code):**
1. Draw the ReAct loop as a diagram: boxes for Thought, Action, Observation, arrows between them, loop back from Observation to Thought, exit arrow to Final Answer.
2. Write a ReAct trace for this failure: `AssertionError: Expected 'Payment Successful' but got 'Payment Failed'`. What tools would the agent call?
3. Write a ReAct trace for this failure: `Connection refused to database at localhost:5432`. This is an environment issue. What would the trace look like?
4. What is the maximum number of iterations an agent should run? Why can't it loop forever?

**End of day checklist:**
- [ ] You can explain ReAct in your own words without looking at notes
- [ ] You have drawn the loop diagram
- [ ] You have written 3 manual ReAct traces on paper
- [ ] You understand: Thought (agent's reasoning) vs Action (tool call) vs Observation (tool result)

---

### Day 2 — Build the ReAct agent with AgentExecutor

**Concepts to understand:**
- `create_react_agent()` — creates the agent from LLM + tools + prompt
- `AgentExecutor` — the engine that runs the ReAct loop
- `verbose=True` — prints every Thought, Action, Observation in real time
- `max_iterations` — safety limit so the agent doesn't loop forever

**Step-by-step tasks:**

Add to requirements.txt: `langchain`
Already installed. Just verify: `pip show langchain`

Create `agent/basic_agent_test.py`:
```python
# agent/basic_agent_test.py
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_react_agent, AgentExecutor
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import tool

load_dotenv()

# Simple tool for testing
@tool
def read_log_file(file_path: str) -> str:
    """
    Read a test execution log file.
    Use when you need to understand what happened during test execution.
    """
    try:
        with open(file_path, 'r') as f:
            return f.read()
    except FileNotFoundError:
        return f"Log file not found: {file_path}. Simulated content: Test started at 10:30, element #login-btn not found after 10s."

tools = [read_log_file]

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0.1
)

# ReAct prompt template
react_prompt = PromptTemplate.from_template("""
You are an expert test failure analyzer. Use the available tools to investigate failures.

Available tools:
{tools}

Tool names (comma separated): {tool_names}

To use a tool, use EXACTLY this format:
Thought: your reasoning about what to do next
Action: tool_name_here
Action Input: the input to pass to the tool
Observation: (this is filled in by the system with the tool result)

When you have enough information, write:
Thought: I now have enough information to give a final answer
Final Answer: your complete analysis in JSON:
{{"failure_type": "TEST_ISSUE|REAL_BUG|ENVIRONMENT_ISSUE", "root_cause": "string", "is_real_bug": boolean, "confidence": 0-100, "suggested_fix": "string", "severity": "LOW|MEDIUM|HIGH"}}

Begin analysis:
Question: {input}
{agent_scratchpad}
""")

# Create the agent
agent = create_react_agent(llm, tools, react_prompt)
executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,           # Shows every Thought/Action/Observation
    max_iterations=5,       # Safety limit
    handle_parsing_errors=True
)

# Run it
result = executor.invoke({
    "input": "LoginTest failed with NoSuchElementException on #login-btn. Log is at /reports/logs/login.log. What happened?"
})

print("\n" + "="*50)
print("FINAL RESULT:")
print(result['output'])
```

Run: `python agent/basic_agent_test.py`

Watch the verbose output carefully. Every Thought, Action, Observation should be visible.

**Exercises to reinforce:**
1. Set `max_iterations=1`. What happens? Does the agent give up or force an answer?
2. Set `verbose=False`. Then back to True. Always keep it True during development.
3. Add a second tool: `@tool def get_error_history() -> str` that returns fake historical data. Does the agent know when to call it?
4. What happens in `handle_parsing_errors=True`? Turn it to False and see what happens when the agent makes a formatting mistake.

**End of day checklist:**
- [ ] AgentExecutor runs without errors
- [ ] verbose output shows the ReAct loop clearly
- [ ] Agent produces a Final Answer
- [ ] You understand what each argument to AgentExecutor does

---

### Day 3 — Improve agent prompt and system behavior

**Why this matters:** A poorly prompted agent gives inconsistent, hallucinated, or improperly formatted answers. Prompt quality is directly proportional to output quality.

**Concepts:**
- Specificity in prompts — vague prompts give vague results
- How to make agents avoid unnecessary tool calls
- Getting consistent JSON in the Final Answer
- `temperature=0.1` — low temperature for consistent, focused output

**What to do today:**
Run your agent from Day 2 with 5 different failure inputs. Record what it does:

Test cases to try:
```
1. NoSuchElementException on #login-btn
2. AssertionError: Expected 200 OK but got 500 Internal Server Error
3. TimeoutException after 30s waiting for search results
4. Connection refused to Redis at localhost:6379
5. AssertionError: Expected text 'Welcome, Admin' but got 'Welcome, User'
```

For each one, note:
- Did it call tools when it should?
- Did the Final Answer come back as valid JSON?
- Did the confidence feel realistic?
- Were there any loops or confusion?

Fix any issues you find by improving the prompt.

**Common issues and fixes:**
- Agent adds text before JSON → Add "Final Answer must be ONLY the JSON object, nothing else"
- Agent calls tools when it has enough info → Add "Only call tools if you genuinely need more information"
- Agent loops too many times → Reduce max_iterations or strengthen the Final Answer instruction

**End of day checklist:**
- [ ] Agent tested with all 5 failure types
- [ ] Final Answer consistently returns valid JSON
- [ ] No unnecessary tool calls happening
- [ ] Prompt is refined and clean

---

### Day 4 — Build analyzer_agent.py as a proper class

**Why a class?** The watcher (Week 5) will create one agent instance and reuse it for every failure. A class with `__init__` and `analyze()` method makes this clean and testable.

**Step-by-step tasks:**

Create `agent/analyzer_agent.py`:
```python
# agent/analyzer_agent.py
import os
import json
import logging
from typing import Optional, Dict, Any
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_react_agent, AgentExecutor
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import tool

load_dotenv()
logger = logging.getLogger(__name__)

REACT_PROMPT = PromptTemplate.from_template("""
You are a senior test failure analysis expert with deep knowledge of Selenium automation.
Your goal is to accurately classify test failures and provide actionable fixes.

Available tools: {tools}
Tool names: {tool_names}

Investigation format:
Thought: reason about what you know and what you still need
Action: tool_name
Action Input: input for the tool
Observation: (result from tool)
... repeat as needed, but use tools ONLY when you genuinely need more information ...
Thought: I have enough information to classify this failure
Final Answer: output ONLY this JSON, nothing else:
{{"failure_type":"TEST_ISSUE|REAL_BUG|ENVIRONMENT_ISSUE","root_cause":"one sentence","is_real_bug":true/false,"confidence":0-100,"suggested_fix":"one sentence","severity":"LOW|MEDIUM|HIGH"}}

Classification guide:
- TEST_ISSUE: locator changed, stale element, bad test data, timing, wrong assertion value
- REAL_BUG: app logic wrong, API error, feature broken, wrong data from backend
- ENVIRONMENT_ISSUE: DB down, network, infrastructure, browser/driver version mismatch

Failure to analyze:
{input}
{agent_scratchpad}
""")


class TestFailureAnalyzerAgent:
    """
    LangChain ReAct agent that analyzes Selenium test failures.
    
    Creates one instance and calls analyze() for each failure.
    The agent reasons through evidence using tools, then returns structured JSON.
    """
    
    def __init__(self):
        """Initialize the agent with Gemini LLM and tools."""
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=os.getenv("GEMINI_API_KEY"),
            temperature=0.1
        )
        self.tools = self._build_tools()
        self.executor = self._build_executor()
        logger.info("TestFailureAnalyzerAgent initialized")
    
    def _build_tools(self) -> list:
        """Create the tools the agent can use."""
        
        @tool
        def read_log_file(file_path: str) -> str:
            """
            Reads a test execution log file.
            Use when you need to understand what happened during test execution —
            what pages loaded, what elements were found, what errors occurred.
            """
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                return content if content.strip() else "Log file is empty."
            except FileNotFoundError:
                return f"Log file not found at: {file_path}"
            except Exception as e:
                return f"Error reading log: {str(e)}"
        
        @tool
        def read_screenshot(screenshot_path: str) -> str:
            """
            Reads a test failure screenshot.
            Use when you need visual context about what was on screen when the test failed.
            """
            from pathlib import Path
            try:
                path = Path(screenshot_path)
                if not path.exists():
                    return f"Screenshot not found: {screenshot_path}"
                size = path.stat().st_size
                return f"Screenshot loaded: {path.name}, {size} bytes. Visual evidence available."
            except Exception as e:
                return f"Error reading screenshot: {str(e)}"
        
        return [read_log_file, read_screenshot]
    
    def _build_executor(self) -> AgentExecutor:
        """Create the ReAct AgentExecutor."""
        agent = create_react_agent(self.llm, self.tools, REACT_PROMPT)
        return AgentExecutor(
            agent=agent,
            tools=self.tools,
            verbose=True,
            max_iterations=6,
            handle_parsing_errors=True,
            return_intermediate_steps=False
        )
    
    def analyze(self, failure_context: Dict[str, Any]) -> Optional[Dict]:
        """
        Analyzes a test failure and returns structured JSON verdict.
        
        Args:
            failure_context: Dictionary with test_name, error_type, error_message,
                           stack_trace, log_path, screenshot_path, etc.
                           
        Returns:
            Dictionary with failure_type, root_cause, is_real_bug, confidence,
            suggested_fix, severity — or None if analysis failed.
        """
        try:
            input_text = self._format_input(failure_context)
            result = self.executor.invoke({"input": input_text})
            output = result.get('output', '')
            return self._parse_output(output)
        except Exception as e:
            logger.error(f"Agent analysis failed: {e}")
            return None
    
    def _format_input(self, ctx: Dict) -> str:
        """Format failure context into agent input text."""
        return f"""
Test Name: {ctx.get('test_name', 'Unknown')}
Error Type: {ctx.get('error_type', 'Unknown')}
Error Message: {ctx.get('error_message', 'Unknown')}
Stack Trace: {ctx.get('stack_trace', 'Not available')}
Log File Path: {ctx.get('log_path', 'Not available')}
Screenshot Path: {ctx.get('screenshot_path', 'Not available')}
Browser: {ctx.get('browser', 'Unknown')}
Environment: {ctx.get('environment', 'Unknown')}
"""
    
    def _parse_output(self, output: str) -> Optional[Dict]:
        """Extract and parse JSON from agent output."""
        try:
            # Find JSON in output
            start = output.find('{')
            end = output.rfind('}') + 1
            if start >= 0 and end > start:
                json_str = output[start:end]
                result = json.loads(json_str)
                
                # Validate required keys
                required = ['failure_type', 'root_cause', 'is_real_bug', 
                           'confidence', 'suggested_fix', 'severity']
                if all(k in result for k in required):
                    return result
                else:
                    logger.error("Agent response missing required keys")
                    return None
            else:
                logger.error(f"No JSON found in agent output: {output[:200]}")
                return None
        except json.JSONDecodeError as e:
            logger.error(f"JSON parsing failed: {e}")
            return None
```

**Exercises to reinforce:**
1. Create an instance and call `analyze()` with a fake failure dict. Does it work?
2. What does `return_intermediate_steps=False` do? Change it to True. What extra data do you see?
3. What does `_format_input()` do and why is it a separate method?
4. Test with missing keys in the failure_context dict. Does `ctx.get('test_name', 'Unknown')` handle it properly?

**End of day checklist:**
- [ ] `TestFailureAnalyzerAgent` class created
- [ ] `analyze()` method works and returns valid dict
- [ ] JSON parsing handles edge cases
- [ ] Logging is informative

---

### Day 5 — Test with 5 failure scenarios + WEEK 3 MILESTONE

**Step-by-step tasks:**

Create `agent/agent_test.py`:
```python
# agent/agent_test.py
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from analyzer_agent import TestFailureAnalyzerAgent

agent = TestFailureAnalyzerAgent()

test_cases = [
    {
        "name": "Stale locator",
        "data": {
            "test_name": "LoginTest.testValidLogin",
            "error_type": "NoSuchElementException",
            "error_message": "Unable to locate element: #login-btn",
            "stack_trace": "at LoginPage.clickLoginButton(LoginPage.java:47)",
            "log_path": "/tmp/nonexistent.log",
            "browser": "Chrome 124"
        }
    },
    {
        "name": "Real application bug",
        "data": {
            "test_name": "CheckoutTest.testPaymentFlow",
            "error_type": "AssertionError",
            "error_message": "Expected 'Payment Successful' but got 'Payment Failed'",
            "stack_trace": "at CheckoutTest.verifyPaymentConfirmation(CheckoutTest.java:89)",
            "browser": "Chrome 124",
            "environment": "staging"
        }
    },
    {
        "name": "Environment/infrastructure failure",
        "data": {
            "test_name": "DatabaseTest.testUserQuery",
            "error_type": "WebDriverException",
            "error_message": "java.net.ConnectException: Connection refused to localhost:5432",
            "stack_trace": "at DatabaseTest.setUp(DatabaseTest.java:23)",
            "browser": "Chrome 124"
        }
    },
    {
        "name": "Timeout — timing issue",
        "data": {
            "test_name": "SearchTest.testProductSearch",
            "error_type": "TimeoutException",
            "error_message": "Expected condition failed: waiting for element .search-results after 30 seconds",
            "stack_trace": "at SearchPage.waitForResults(SearchPage.java:67)",
            "browser": "Chrome 124"
        }
    },
    {
        "name": "API error",
        "data": {
            "test_name": "ApiTest.testGetUserProfile",
            "error_type": "AssertionError",
            "error_message": "Expected HTTP 200 but got HTTP 500 Internal Server Error",
            "stack_trace": "at ApiTest.verifyResponse(ApiTest.java:45)",
            "environment": "staging"
        }
    }
]

print("TestSense AI — Agent Test Suite")
print("=" * 60)

results = []
for tc in test_cases:
    print(f"\n{'─'*60}")
    print(f"TEST: {tc['name']}")
    print(f"{'─'*60}")
    
    result = agent.analyze(tc['data'])
    
    if result:
        print(f"\n✅ Analysis complete:")
        print(f"   Type:       {result['failure_type']}")
        print(f"   Cause:      {result['root_cause']}")
        print(f"   Is bug:     {result['is_real_bug']}")
        print(f"   Confidence: {result['confidence']}%")
        print(f"   Fix:        {result['suggested_fix']}")
        results.append(("PASS", tc['name'], result['failure_type']))
    else:
        print(f"\n❌ Analysis FAILED")
        results.append(("FAIL", tc['name'], "N/A"))

print(f"\n{'='*60}")
print(f"RESULTS: {sum(1 for r in results if r[0]=='PASS')}/{len(results)} passed")
for status, name, ftype in results:
    print(f"  {'✅' if status=='PASS' else '❌'} {name}: {ftype}")
```

**🏆 WEEK 3 MILESTONE:**
- [ ] Agent analyzes all 5 failure scenarios successfully
- [ ] Each one returns valid JSON
- [ ] Classifications make sense (stale locator = TEST_ISSUE, payment failure = REAL_BUG, etc.)
- [ ] Agent completes without crashing on any scenario

**The brain is built. It reasons. It decides. It answers correctly.**

---

## WEEK 4: Java Test Side Setup

**Week goal:** A Java Selenium test that fails intentionally, auto-captures a screenshot, writes a detailed JSON failure report, and saves structured logs.

---

### Day 1 — Maven project setup + TestNG Listener interface

**Concepts:**
- Maven pom.xml — the Java equivalent of requirements.txt
- TestNG ITestListener — an interface with methods that fire on test events
- `onTestFailure()` — the method that fires when any test fails
- Why a Listener is better than try-catch in every test

**Step-by-step tasks:**

Create `java-tests/pom.xml`:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>
    <groupId>com.testsense</groupId>
    <artifactId>java-tests</artifactId>
    <version>1.0-SNAPSHOT</version>

    <properties>
        <maven.compiler.source>11</maven.compiler.source>
        <maven.compiler.target>11</maven.compiler.target>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
    </properties>

    <dependencies>
        <dependency>
            <groupId>org.seleniumhq.selenium</groupId>
            <artifactId>selenium-java</artifactId>
            <version>4.18.1</version>
        </dependency>
        <dependency>
            <groupId>org.testng</groupId>
            <artifactId>testng</artifactId>
            <version>7.9.0</version>
        </dependency>
        <dependency>
            <groupId>com.google.code.gson</groupId>
            <artifactId>gson</artifactId>
            <version>2.10.1</version>
        </dependency>
        <dependency>
            <groupId>org.apache.logging.log4j</groupId>
            <artifactId>log4j-core</artifactId>
            <version>2.23.0</version>
        </dependency>
        <dependency>
            <groupId>org.apache.logging.log4j</groupId>
            <artifactId>log4j-api</artifactId>
            <version>2.23.0</version>
        </dependency>
        <dependency>
            <groupId>commons-io</groupId>
            <artifactId>commons-io</artifactId>
            <version>2.15.1</version>
        </dependency>
        <dependency>
            <groupId>io.github.bonigarcia</groupId>
            <artifactId>webdrivermanager</artifactId>
            <version>5.7.0</version>
        </dependency>
    </dependencies>
</project>
```

Run: `mvn dependency:resolve` inside `java-tests/`

**Exercises:**
1. What is the difference between Maven and Gradle? (Both are Java build tools)
2. List all 5 methods in `ITestListener`. What event does each one correspond to?
3. Why is a Listener better than putting try-catch + screenshot in every test method?

**End of day checklist:**
- [ ] pom.xml created with all dependencies
- [ ] `mvn dependency:resolve` completes without errors
- [ ] ITestListener interface understood (all 5 methods known)

---

### Day 2 — Screenshot capture utility

**Concepts:**
- `TakesScreenshot` interface in Selenium
- `OutputType.FILE` — gets screenshot as a File object
- `Files.copy()` — saves it to your destination
- Timestamp in filename — ensures unique names

**Step-by-step tasks:**

Create `java-tests/src/main/java/utils/ScreenshotUtil.java`:
```java
package utils;

import org.openqa.selenium.OutputType;
import org.openqa.selenium.TakesScreenshot;
import org.openqa.selenium.WebDriver;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

public class ScreenshotUtil {
    
    private static final Logger logger = LogManager.getLogger(ScreenshotUtil.class);
    private static final String SCREENSHOT_DIR = "../../reports/screenshots/";
    private static final DateTimeFormatter FORMATTER = 
        DateTimeFormatter.ofPattern("yyyyMMdd_HHmmss");
    
    public static String captureScreenshot(WebDriver driver, String testName) {
        try {
            // Create directory if it doesn't exist
            Path dirPath = Paths.get(SCREENSHOT_DIR);
            Files.createDirectories(dirPath);
            
            // Generate filename with timestamp
            String timestamp = LocalDateTime.now().format(FORMATTER);
            String safeName = testName.replaceAll("[^a-zA-Z0-9]", "_");
            String fileName = safeName + "_" + timestamp + ".png";
            String filePath = SCREENSHOT_DIR + fileName;
            
            // Take screenshot
            File srcFile = ((TakesScreenshot) driver).getScreenshotAs(OutputType.FILE);
            Files.copy(srcFile.toPath(), Paths.get(filePath));
            
            logger.info("Screenshot saved: {}", filePath);
            return filePath;
            
        } catch (IOException e) {
            logger.error("Failed to capture screenshot: {}", e.getMessage());
            return null;
        }
    }
}
```

**Exercises:**
1. What happens if the WebDriver has already quit when you try to take a screenshot? Add a null check for the driver.
2. What does `replaceAll("[^a-zA-Z0-9]", "_")` do to the test name? Test with "LoginTest.testValidLogin".
3. If two tests fail at exactly the same second, will there be a filename collision? Fix it by adding milliseconds.

---

### Day 3 — Log4j structured logging

**Concepts:**
- Why structured logs beat `System.out.println`
- Log levels: DEBUG → INFO → WARN → ERROR
- `log4j2.xml` — the configuration file
- Logging to both console AND file simultaneously

**Step-by-step tasks:**

Create `java-tests/src/main/resources/log4j2.xml`:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<Configuration status="WARN">
    <Appenders>
        <Console name="Console" target="SYSTEM_OUT">
            <PatternLayout pattern="%d{HH:mm:ss.SSS} [%t] %-5level %logger{36} - %msg%n"/>
        </Console>
        <File name="TestLog" fileName="../../reports/logs/testsense_test.log" append="true">
            <PatternLayout pattern="%d{yyyy-MM-dd HH:mm:ss.SSS} %-5level [%t] %logger{36} - %msg%n"/>
        </File>
    </Appenders>
    <Loggers>
        <Root level="info">
            <AppenderRef ref="Console"/>
            <AppenderRef ref="TestLog"/>
        </Root>
    </Loggers>
</Configuration>
```

**Exercises:**
1. Decode the pattern layout: What does `%d{HH:mm:ss.SSS}` mean? `%-5level`? `%logger{36}`?
2. Change log level to DEBUG. Run a test. What extra lines appear?
3. When would you use WARN vs ERROR? Give one example of each.

---

### Day 4 — Write failure JSON report

**Concepts:**
- Gson library for Java JSON writing
- Data model as Java class (FailureReport)
- PrettyPrinting for human-readable JSON
- File writing in Java

**Step-by-step tasks:**

Create `java-tests/src/main/java/utils/FailureReportWriter.java`:
```java
package utils;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

import java.io.FileWriter;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

public class FailureReportWriter {
    
    private static final Logger logger = LogManager.getLogger(FailureReportWriter.class);
    private static final String REPORTS_DIR = "../../reports/json/";
    private static final Gson GSON = new GsonBuilder().setPrettyPrinting().create();
    private static final DateTimeFormatter FORMATTER =
        DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");
    
    public static class FailureReport {
        public String testName;
        public String className;
        public String methodName;
        public String errorType;
        public String errorMessage;
        public String stackTrace;
        public String screenshotPath;
        public String logPath;
        public String timestamp;
        public String browser;
        public String environment;
        public long testDurationMs;
    }
    
    public static String writeReport(FailureReport report) {
        try {
            Files.createDirectories(Paths.get(REPORTS_DIR));
            
            report.timestamp = LocalDateTime.now().format(FORMATTER);
            report.logPath = "../../reports/logs/testsense_test.log";
            
            String safeName = report.testName.replaceAll("[^a-zA-Z0-9]", "_");
            String fileName = safeName + "_" + System.currentTimeMillis() + ".json";
            String filePath = REPORTS_DIR + fileName;
            
            try (FileWriter writer = new FileWriter(filePath)) {
                GSON.toJson(report, writer);
            }
            
            logger.info("Failure report written: {}", filePath);
            return filePath;
            
        } catch (IOException e) {
            logger.error("Failed to write failure report: {}", e.getMessage());
            return null;
        }
    }
}
```

**Exercises:**
1. What does `setPrettyPrinting()` do? Remove it and see what the JSON looks like.
2. Write a main method that creates a FailureReport, fills all fields, and writes it. Open the resulting JSON.
3. What does `try (FileWriter writer = ...)` do? This is try-with-resources. Why is it better than regular try?

---

### Day 5 — FailureListener.java + Sample test + WEEK 4 MILESTONE

**Create `java-tests/src/main/java/utils/FailureListener.java`:**
```java
package utils;

import org.testng.ITestContext;
import org.testng.ITestListener;
import org.testng.ITestResult;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

public class FailureListener implements ITestListener {
    
    private static final Logger logger = LogManager.getLogger(FailureListener.class);
    
    @Override
    public void onTestFailure(ITestResult result) {
        logger.error("TEST FAILED: {}", result.getName());
        
        // Build failure report
        FailureReportWriter.FailureReport report = new FailureReportWriter.FailureReport();
        report.testName = result.getName();
        report.className = result.getTestClass().getName();
        report.methodName = result.getName();
        report.errorType = result.getThrowable().getClass().getSimpleName();
        report.errorMessage = result.getThrowable().getMessage();
        report.stackTrace = buildStackTrace(result.getThrowable());
        report.browser = "Chrome";
        report.environment = System.getProperty("env", "staging");
        report.testDurationMs = result.getEndMillis() - result.getStartMillis();
        
        // Capture screenshot if driver is available
        // WebDriver driver = DriverManager.getDriver();
        // if (driver != null) {
        //     report.screenshotPath = ScreenshotUtil.captureScreenshot(driver, result.getName());
        // }
        
        FailureReportWriter.writeReport(report);
    }
    
    @Override
    public void onTestSuccess(ITestResult result) {
        logger.info("TEST PASSED: {} ({}ms)", result.getName(), 
            result.getEndMillis() - result.getStartMillis());
    }
    
    @Override
    public void onStart(ITestContext context) {
        logger.info("Starting test suite: {}", context.getName());
    }
    
    @Override
    public void onFinish(ITestContext context) {
        logger.info("Suite complete. Passed: {}, Failed: {}", 
            context.getPassedTests().size(), context.getFailedTests().size());
    }
    
    private String buildStackTrace(Throwable t) {
        StringBuilder sb = new StringBuilder();
        for (StackTraceElement element : t.getStackTrace()) {
            sb.append("  at ").append(element.toString()).append("\n");
        }
        return sb.toString();
    }
}
```

**Create `java-tests/src/test/java/tests/LoginTest.java`:**
```java
package tests;

import org.testng.Assert;
import org.testng.annotations.Listeners;
import org.testng.annotations.Test;
import utils.FailureListener;

@Listeners(FailureListener.class)
public class LoginTest {
    
    @Test
    public void testValidLogin() {
        // Intentionally fail to trigger FailureListener
        Assert.fail("Simulated login failure: button selector #login-btn not found");
    }
    
    @Test
    public void testPaymentFlow() {
        Assert.assertEquals("Payment Failed", "Payment Successful",
            "Payment API returned unexpected status");
    }
}
```

Run: `cd java-tests && mvn test`

**🏆 WEEK 4 MILESTONE:**
- [ ] Tests fail intentionally
- [ ] FailureListener fires on each failure
- [ ] JSON written to `reports/json/`
- [ ] Logs written to `reports/logs/`
- [ ] JSON contains all required fields Python needs

---

## WEEK 5: Connect Java → Python (The Integration Week)

**Week goal:** When a Java test fails, the Python agent automatically detects it, collects evidence, analyzes it, and produces a verdict. All without any manual intervention.

---

### Day 1 — Python watchdog library

**Concepts:**
- File system events — your OS fires events when files are created/modified/deleted
- watchdog library — listens to these events
- `Observer` + `FileSystemEventHandler` pattern
- `FileCreatedEvent` — the specific event we care about

**Step-by-step tasks:**

Add to requirements.txt: `watchdog`
Run: `pip install -r requirements.txt`

Create `agent/watcher_test.py`:
```python
# agent/watcher_test.py
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileCreatedEvent

class SimpleHandler(FileSystemEventHandler):
    
    def on_created(self, event):
        if isinstance(event, FileCreatedEvent):
            print(f"NEW FILE DETECTED: {event.src_path}")
            if event.src_path.endswith('.json'):
                print(f"  → This is a JSON failure report! Agent should wake up.")

handler = SimpleHandler()
observer = Observer()
observer.schedule(handler, "../reports/json/", recursive=False)
observer.start()

print("Watching ../reports/json/ for new failure reports...")
print("Copy a JSON file into that folder to test.")
print("Press Ctrl+C to stop.")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()
observer.join()
print("Watcher stopped.")
```

Start it. Then manually copy any JSON file into `reports/json/`. Watch it trigger.

**Exercises:**
1. What happens if `reports/json/` doesn't exist? Add error handling.
2. Set `recursive=True`. What changes?
3. What events exist besides FileCreatedEvent? List at least 3.

---

### Day 2 — evidence_collector.py

Create `agent/evidence_collector.py`:
```python
# agent/evidence_collector.py
import json
import logging
from pathlib import Path
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)


class EvidenceCollector:
    """
    Reads a Java-generated failure JSON report and packages all evidence
    into a clean dictionary for the analyzer agent.
    """
    
    def collect(self, json_report_path: str) -> Optional[Dict[str, Any]]:
        """
        Reads failure JSON and returns complete evidence package.
        
        Returns None if the JSON is invalid or missing required fields.
        """
        try:
            with open(json_report_path, 'r', encoding='utf-8') as f:
                report = json.load(f)
            
            evidence = {
                'test_name': report.get('testName', 'Unknown'),
                'class_name': report.get('className', 'Unknown'),
                'error_type': report.get('errorType', 'Unknown'),
                'error_message': report.get('errorMessage', 'No message'),
                'stack_trace': report.get('stackTrace', 'Not available'),
                'timestamp': report.get('timestamp', 'Unknown'),
                'browser': report.get('browser', 'Unknown'),
                'environment': report.get('environment', 'Unknown'),
                'screenshot_path': report.get('screenshotPath'),
                'log_path': report.get('logPath'),
                'test_duration_ms': report.get('testDurationMs', 0),
                'source_report': json_report_path
            }
            
            # Verify referenced files exist
            if evidence['screenshot_path']:
                if not Path(evidence['screenshot_path']).exists():
                    logger.warning(f"Screenshot not found: {evidence['screenshot_path']}")
                    evidence['screenshot_path'] = None
            
            if evidence['log_path']:
                if not Path(evidence['log_path']).exists():
                    logger.warning(f"Log file not found: {evidence['log_path']}")
                    evidence['log_path'] = None
            
            logger.info(f"Evidence collected for: {evidence['test_name']}")
            return evidence
            
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in report file: {e}")
            return None
        except FileNotFoundError:
            logger.error(f"Report file not found: {json_report_path}")
            return None
        except Exception as e:
            logger.error(f"Evidence collection failed: {e}")
            return None
```

**Exercises:**
1. What is the difference between `report.get('testName')` and `report['testName']`? What happens with each when the key doesn't exist?
2. Write a test: create a fake JSON, call `collect()`, verify every field in the output.
3. Add a `collect_all(folder_path: str) -> list` method that processes every JSON in a folder.

---

### Day 3 — Build failure_watcher.py

Create `agent/failure_watcher.py`:
```python
# agent/failure_watcher.py
import time
import logging
from collections import defaultdict
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileCreatedEvent

logger = logging.getLogger(__name__)


class FailureReportHandler(FileSystemEventHandler):
    """Handles new failure JSON reports from Java tests."""
    
    def __init__(self, agent, collector, report_generator, cooldown_seconds=3):
        self.agent = agent
        self.collector = collector
        self.report_generator = report_generator
        self.cooldown = cooldown_seconds
        self.last_processed = defaultdict(float)
        self.processed_count = 0
    
    def on_created(self, event):
        if not isinstance(event, FileCreatedEvent):
            return
        if not event.src_path.endswith('.json'):
            return
        
        # Cooldown check (prevent double-trigger)
        now = time.time()
        if now - self.last_processed[event.src_path] < self.cooldown:
            logger.debug(f"Cooldown: skipping {event.src_path}")
            return
        self.last_processed[event.src_path] = now
        
        self.process(event.src_path)
    
    def process(self, json_path: str):
        """Process one failure report through the full pipeline."""
        start_time = time.time()
        logger.info(f"Processing failure report: {json_path}")
        
        # Step 1: Collect evidence
        evidence = self.collector.collect(json_path)
        if not evidence:
            logger.error("Evidence collection failed — skipping")
            return
        
        # Step 2: Analyze with agent
        logger.info(f"Analyzing: {evidence['test_name']}")
        analysis = self.agent.analyze(evidence)
        if not analysis:
            logger.error("Agent analysis failed")
            return
        
        # Step 3: Generate report
        report_path = self.report_generator.generate(evidence, analysis)
        
        elapsed = time.time() - start_time
        self.processed_count += 1
        
        logger.info(f"✅ Done in {elapsed:.1f}s | "
                   f"Type: {analysis['failure_type']} | "
                   f"Confidence: {analysis['confidence']}% | "
                   f"Report: {report_path}")


class FailureWatcher:
    """Watches the reports/json folder for new failure reports."""
    
    def __init__(self, watch_path: str, agent, collector, report_generator):
        self.watch_path = Path(watch_path)
        self.watch_path.mkdir(parents=True, exist_ok=True)
        
        self.handler = FailureReportHandler(agent, collector, report_generator)
        self.observer = Observer()
        self.observer.schedule(self.handler, str(self.watch_path), recursive=False)
    
    def start(self):
        self.observer.start()
        logger.info(f"Watching: {self.watch_path}")
        logger.info("Waiting for test failures... (Ctrl+C to stop)")
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop()
    
    def stop(self):
        self.observer.stop()
        self.observer.join()
        logger.info(f"Watcher stopped. Total processed: {self.handler.processed_count}")
```

---

### Day 4 — config.yaml + integration test

Create `config.yaml`:
```yaml
paths:
  watch_dir: "reports/json"
  screenshots_dir: "reports/screenshots"
  logs_dir: "reports/logs"
  html_dir: "reports/html"

gemini:
  model: "gemini-2.5-flash"
  temperature: 0.1
  max_retries: 3

agent:
  max_iterations: 6
  cooldown_seconds: 3
  min_confidence: 40

reporting:
  open_browser_on_report: false
```

Create `agent/main.py`:
```python
# agent/main.py
import sys
import logging
import yaml
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from analyzer_agent import TestFailureAnalyzerAgent
from evidence_collector import EvidenceCollector
from failure_watcher import FailureWatcher
from report_generator import ReportGenerator  # Week 7

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    datefmt='%H:%M:%S'
)

def load_config():
    with open('config.yaml', 'r') as f:
        return yaml.safe_load(f)

if __name__ == "__main__":
    print("="*60)
    print("  TestSense AI — Intelligent Test Failure Analyzer")
    print("="*60)
    
    config = load_config()
    
    agent = TestFailureAnalyzerAgent()
    collector = EvidenceCollector()
    reporter = ReportGenerator(output_dir=config['paths']['html_dir'])  # Week 7
    
    watcher = FailureWatcher(
        watch_path=config['paths']['watch_dir'],
        agent=agent,
        collector=collector,
        report_generator=reporter
    )
    
    watcher.start()
```

Add to requirements.txt: `PyYAML`
Run: `pip install -r requirements.txt`

---

### Day 5 — Full end-to-end test + WEEK 5 MILESTONE

**The big test:**
1. Open two terminals
2. Terminal 1: `cd testsense-ai && python agent/main.py`
3. Terminal 2: `cd java-tests && mvn test`
4. Watch Terminal 1 spring to life when the test fails

**🏆 WEEK 5 MILESTONE:**
- [ ] Java test fails in Terminal 2
- [ ] Python watcher detects it in Terminal 1
- [ ] Evidence collected from JSON
- [ ] Agent analyzes and prints result
- [ ] Full pipeline runs without manual intervention

**This is the moment. The two worlds are talking.**

---

## ═══════════════════════════════════════
## PHASE 3: INTEGRATE + POLISH (Week 6–8)
## ═══════════════════════════════════════

---

## WEEK 6: Full Pipeline + Classification

**Goal:** Agent reliably classifies all three failure types with confidence scores and handles edge cases gracefully.

### Day 1 — Structured output with Pydantic

```python
from pydantic import BaseModel, Field
from typing import Literal

class FailureAnalysis(BaseModel):
    failure_type: Literal["TEST_ISSUE", "REAL_BUG", "ENVIRONMENT_ISSUE"]
    root_cause: str = Field(description="One clear sentence explaining the root cause")
    is_real_bug: bool
    confidence: int = Field(ge=0, le=100)
    suggested_fix: str = Field(description="One actionable fix sentence")
    severity: Literal["LOW", "MEDIUM", "HIGH"]
```

### Days 2-3 — Classification logic + Error handling

Add retry logic to agent calls:
```python
import time
from functools import wraps

def retry_on_failure(max_retries=3, delay=2):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_retries - 1:
                        raise
                    logger.warning(f"Attempt {attempt+1} failed: {e}. Retrying in {delay}s...")
                    time.sleep(delay * (2 ** attempt))  # Exponential backoff
        return wrapper
    return decorator
```

### Days 4-5 — Test 8+ failure scenarios + MILESTONE

Create a test suite of 8 diverse failures. Every one should classify correctly.

**🏆 WEEK 6 MILESTONE:**
- [ ] 8 failure scenarios all classify correctly
- [ ] No crashes on edge cases (missing files, empty logs)
- [ ] Retry logic working
- [ ] Pipeline completes in under 30 seconds per failure

---

## WEEK 7: HTML Report Generation

**Goal:** Beautiful, professional HTML report automatically generated for every failure.

### Day 1 — Jinja2 basics

Add to requirements.txt: `Jinja2`

```python
from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader('agent/templates/'))
template = env.get_template('report_template.html')

html = template.render(
    test_name="LoginTest",
    failure_type="TEST_ISSUE",
    confidence=91,
    # ... etc
)
```

### Days 2-3 — HTML template + ReportGenerator class

Create `agent/report_generator.py`:
```python
from jinja2 import Environment, FileSystemLoader
from pathlib import Path
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class ReportGenerator:
    
    def __init__(self, templates_dir="agent/templates", output_dir="reports/html"):
        self.env = Environment(loader=FileSystemLoader(templates_dir))
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def generate(self, evidence: dict, analysis: dict) -> str:
        """Generate HTML report from evidence + analysis. Returns file path."""
        try:
            template = self.env.get_template('report_template.html')
            
            data = {**evidence, **analysis,
                   'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            
            html = template.render(**data)
            
            safe_name = evidence['test_name'].replace('.', '_').replace(' ', '_')
            ts = datetime.now().strftime('%Y%m%d_%H%M%S')
            path = self.output_dir / f"{safe_name}_{ts}.html"
            
            with open(path, 'w', encoding='utf-8') as f:
                f.write(html)
            
            logger.info(f"Report generated: {path}")
            return str(path)
        except Exception as e:
            logger.error(f"Report generation failed: {e}")
            return None
```

Create `agent/templates/report_template.html`:
```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>TestSense AI Report — {{ test_name }}</title>
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: #f0f2f5; }
  .header { background: linear-gradient(135deg, #1a1a2e, #16213e); color: white; padding: 2rem 2.5rem; }
  .header h1 { font-size: 1.3rem; font-weight: 600; margin-bottom: 4px; }
  .header p { opacity: 0.65; font-size: 0.85rem; }
  .container { max-width: 860px; margin: 2rem auto; padding: 0 1.5rem; }
  .card { background: white; border-radius: 12px; padding: 1.5rem; margin-bottom: 1rem; box-shadow: 0 1px 6px rgba(0,0,0,0.07); }
  .card-title { font-size: 11px; font-weight: 600; color: #94a3b8; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 0.5rem; }
  .test-name { font-size: 1.3rem; font-weight: 600; color: #1e293b; }
  .badge { display: inline-block; padding: 5px 14px; border-radius: 20px; font-size: 12px; font-weight: 600; }
  .badge-bug { background: #fee2e2; color: #dc2626; }
  .badge-test { background: #fef3c7; color: #d97706; }
  .badge-env { background: #e2e8f0; color: #475569; }
  .confidence-number { font-size: 2rem; font-weight: 700; color: #1e293b; }
  .bar-track { height: 8px; background: #f1f5f9; border-radius: 4px; margin-top: 8px; }
  .bar-fill { height: 100%; border-radius: 4px; width: {{ confidence }}%; background: {% if confidence >= 80 %}#16a34a{% elif confidence >= 60 %}#d97706{% else %}#dc2626{% endif %}; }
  .root-cause { font-size: 1rem; color: #334155; line-height: 1.6; }
  .fix-box { background: #f0fdf4; border-left: 4px solid #16a34a; padding: 0.75rem 1rem; border-radius: 0 8px 8px 0; }
  .fix-text { color: #166534; font-size: 0.95rem; }
  .stack-box { background: #1e293b; border-radius: 8px; padding: 1rem; overflow-x: auto; }
  .stack-text { color: #7dd3fc; font-family: 'Courier New', monospace; font-size: 12px; white-space: pre-wrap; line-height: 1.5; }
  .meta-grid { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 12px; }
  .meta-item { background: #f8fafc; border-radius: 8px; padding: 0.75rem; }
  .meta-label { font-size: 11px; color: #94a3b8; margin-bottom: 4px; }
  .meta-value { font-size: 14px; color: #334155; font-weight: 500; }
  .footer { text-align: center; color: #94a3b8; font-size: 12px; padding: 2rem 0; }
  .row { display: flex; justify-content: space-between; align-items: flex-start; gap: 1rem; }
</style>
</head>
<body>
<div class="header">
  <h1>🧠 TestSense AI — Failure Analysis Report</h1>
  <p>Generated {{ timestamp }} • Powered by Google Gemini</p>
</div>
<div class="container">
  <div class="card">
    <div class="card-title">Test</div>
    <div class="test-name">{{ test_name }}</div>
    <div style="margin-top: 8px; font-size: 13px; color: #64748b;">{{ class_name }} • {{ browser }} • {{ environment }}</div>
  </div>
  <div class="card">
    <div class="row">
      <div>
        <div class="card-title">Classification</div>
        <span class="badge badge-{% if is_real_bug %}bug{% elif failure_type == 'ENVIRONMENT_ISSUE' %}env{% else %}test{% endif %}">
          {{ failure_type.replace('_', ' ') }}
        </span>
        <div style="margin-top: 8px; font-size: 13px; color: #64748b;">Severity: <strong>{{ severity }}</strong></div>
      </div>
      <div style="text-align: right;">
        <div class="card-title">Confidence</div>
        <div class="confidence-number">{{ confidence }}%</div>
      </div>
    </div>
    <div class="bar-track"><div class="bar-fill"></div></div>
  </div>
  <div class="card">
    <div class="card-title">Root cause</div>
    <div class="root-cause">{{ root_cause }}</div>
  </div>
  <div class="card">
    <div class="card-title">Suggested fix</div>
    <div class="fix-box">
      <div class="fix-text">✅ {{ suggested_fix }}</div>
    </div>
  </div>
  <div class="card">
    <div class="card-title">Stack trace</div>
    <div class="stack-box">
      <div class="stack-text">{{ stack_trace }}</div>
    </div>
  </div>
  <div class="card">
    <div class="card-title">Test metadata</div>
    <div class="meta-grid">
      <div class="meta-item"><div class="meta-label">Error type</div><div class="meta-value">{{ error_type }}</div></div>
      <div class="meta-item"><div class="meta-label">Duration</div><div class="meta-value">{{ test_duration_ms }}ms</div></div>
      <div class="meta-item"><div class="meta-label">Is real bug</div><div class="meta-value">{% if is_real_bug %}⚠️ Yes{% else %}✅ No{% endif %}</div></div>
    </div>
  </div>
</div>
<div class="footer">
  Generated by TestSense AI • {{ timestamp }}<br>
  <span style="color: #cbd5e1;">An Intelligent Test Failure Analysis Agent</span>
</div>
</body>
</html>
```

### Days 4-5 — Connect to pipeline + MILESTONE

Update `failure_watcher.py` to include the report generator in the pipeline.

**🏆 WEEK 7 MILESTONE:**
- [ ] HTML report generated for every failure
- [ ] Correct color coding for each failure type
- [ ] Opens cleanly in browser
- [ ] Looks professional enough to show in a demo

---

## WEEK 8: Polish + GitHub + Demo Prep

### Day 1 — Code cleanup + docstrings

Go through every Python file. Every function must have a docstring. Every print() must be replaced with logger.info(). Every hardcoded path must come from config.yaml.

### Day 2 — README.md

Structure:
```markdown
# TestSense AI 🧠
> Intelligent test failure analysis agent

## What it does
## Architecture (ASCII diagram)
## Tech stack (table)
## Quick start (exact steps)
## Demo (screenshot)
## The problem it solves
## Future roadmap (Layer 2, 3)
```

### Day 3 — Git + GitHub

Commit message format to use:
```
feat: add LangChain ReAct agent for failure analysis
fix: handle missing screenshot in evidence collector
refactor: move all paths to config.yaml
docs: add complete README with architecture
test: add 8-scenario test suite for agent
```

Push to GitHub. Make it public.

### Day 4 — Record demo

3-minute demo script:
```
0:00-0:30  Introduce TestSense AI
0:30-1:00  Show watcher running in terminal
1:00-1:30  Run the failing Java test
1:30-2:00  Show Python agent analyzing it
2:00-2:30  Open the HTML report
2:30-3:00  Explain what this saves QA teams
```

### Day 5 — Practice interview questions

**Memorize answers to these 10 questions:**
1. "Tell me about a project you built."
2. "Why LangChain and not just direct Gemini API?"
3. "What is a ReAct agent?"
4. "How does Java communicate with Python in your project?"
5. "What happens if Gemini API is down?"
6. "What are the 3 failure types your agent classifies?"
7. "How does your agent decide when to call a tool?"
8. "What would Layer 2 of this project look like?"
9. "What was the hardest part of building this?"
10. "How would you support Playwright instead of Selenium?"

**🏆 WEEK 8 MILESTONE — THE FINAL MILESTONE:**
- [ ] Code clean and fully documented
- [ ] README professional and complete
- [ ] Live on GitHub with clean commit history
- [ ] Demo video recorded (3 minutes)
- [ ] All 10 interview questions answered confidently
- [ ] You can explain every component without notes

**You are ready. Walk into November knowing what you built is real, useful, and yours.**

---

## 📝 KEY DECISIONS — LOCKED. DO NOT REVISIT.

| Decision | Choice Made | Reason |
|----------|------------|--------|
| Agent framework | LangChain | Industry standard, ReAct support, widely known |
| LLM | Gemini 2.5 Flash | Free tier 1500/day, handles text + images |
| Gemini SDK | google-genai | google-generativeai is deprecated |
| Local models | No Ollama | User wants cloud API experience only |
| Budget | ₹0 | Free tiers only, non-negotiable |
| Languages | Python agent + Java tests | Plays to existing skills |
| Reports | HTML via Jinja2 | Professional, portable, visual |
| File watching | watchdog | Simple, reliable, cross-platform |
| Config | config.yaml | Clean, editable, no hardcoding |
| JSON | Gson (Java) + json (Python) | Standard, simple |

---

## 📚 ALL RESOURCES

| Resource | URL |
|----------|-----|
| Get Gemini API key | https://aistudio.google.com/apikey |
| google-genai SDK docs | https://googleapis.github.io/python-genai/ |
| LangChain docs | https://python.langchain.com/docs |
| LangChain + Gemini | https://python.langchain.com/docs/integrations/chat/google_generative_ai |
| LangChain agents | https://python.langchain.com/docs/modules/agents/ |
| watchdog docs | https://pythonhosted.org/watchdog/ |
| Jinja2 docs | https://jinja.palletsprojects.com/en/3.1.x/ |
| TestNG docs | https://testng.org/doc/ |
| Selenium docs | https://www.selenium.dev/documentation/ |
| Pydantic docs | https://docs.pydantic.dev/ |
| Maven central | https://central.sonatype.com/ |

---

## 🎤 INTERVIEW TALKING POINTS

### Opening (memorize word for word):
> "I built TestSense AI — an intelligent test failure analysis agent. When a Selenium test fails, the agent automatically collects the stack trace, logs, and screenshot. It uses a LangChain ReAct agent to reason about the failure, calling tools as needed before sending everything to Google Gemini for analysis. The agent classifies failures as real bugs, test maintenance issues, or environment problems, suggests a fix, and generates a professional HTML report. This saves QA teams 2-4 hours of daily manual investigation."

### Key technical answers:
- **"Why LangChain?"** → "A single API call gives you one shot. LangChain's ReAct agent gives you a loop — the agent reasons, calls a tool to get more information, sees the result, reasons again, and only gives a final answer when it's confident. That's what makes it an agent instead of just a chatbot."
- **"How does Java talk to Python?"** → "The Java test framework writes a JSON failure report to a shared folder. Python's watchdog library detects the new file and triggers the agent. No APIs, no shared memory — just filesystem events. Simple, reliable, zero coupling."
- **"What if Gemini is down?"** → "I have retry logic with exponential backoff — it tries 3 times before failing gracefully. The watcher logs the error and continues monitoring. It doesn't crash."
- **"How does the agent decide which tool to call?"** → "The LLM reads the docstring of each tool. I write docstrings that say exactly when to use the tool — 'Use when you need to understand what happened during test execution.' The agent uses those descriptions to decide."

---

## 💬 CONVERSATION STYLE GUIDE — FOR CLAUDE

### When to start:
Ask: "Which week and day are you on? What did you finish last session? Share any code you wrote."

### When they show you code:
Review it line by line. Point out what is excellent. Point out what could be better. Teach the better way.

### When they are stuck:
First ask: "What does the error say exactly?" and "What have you tried?" Then guide them. Don't hand over the answer immediately.

### When they hit a milestone:
Make a moment of it. Say it clearly. It matters for motivation.

### Every few sessions:
Remind them how to explain the current component in an interview. Keep the November goal alive.

### If scope creep happens:
Hear them out. Then gently bring it back: "That's a great idea — let's note it for Layer 2. For now, let's finish Layer 1 first so it's interview-ready."

### If motivation dips:
Remind them: "Picture November. You walk into that room. You say 'I built TestSense AI.' The interviewer leans forward. That's what we're building toward."

### Non-negotiables:
- Never let bad code pass without teaching the better way
- Never rush a week just to get through it
- Never let them skip the exercises — that's where real learning happens
- Always keep the interview in sight

---

*Document created: July 1, 2026*
*Project: TestSense AI — Intelligent Test Failure Analysis Agent*
*Target completion: September 2026*
*Interview target: November 2026*
*Total budget: ₹0*

---

> The goal is not just to build a project.
> The goal is to walk into a November interview,
> say "I built TestSense AI",
> and watch the interviewer lean forward.
>
> **That moment is what this file is building toward. 🎯**
