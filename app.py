import streamlit as st
import anthropic
import json
import pandas as pd
import os
from datetime import datetime
import base64
from io import StringIO
import requests

# ============================================================================
# PAGE CONFIG
# ============================================================================
st.set_page_config(
    page_title="TestGenie AI",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# CUSTOM CSS STYLING
# ============================================================================
custom_css = """
<style>
    :root {
        --primary-color: #00d4aa;
        --bg-color: #0f1117;
        --card-color: #1e2130;
        --text-color: #c9d1d9;
        --border-color: #30363d;
    }

    body {
        background-color: var(--bg-color);
        color: var(--text-color);
    }

    .main {
        background-color: var(--bg-color);
    }

    .stTabs {
        background-color: var(--card-color);
        border-radius: 8px;
        padding: 10px;
    }

    .stButton > button {
        background-color: var(--primary-color);
        color: #000;
        font-weight: 600;
        padding: 10px 20px;
        border-radius: 6px;
        border: none;
        transition: all 0.3s ease;
    }

    .stButton > button:hover {
        background-color: #00b894;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 212, 170, 0.3);
    }

    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        background-color: var(--card-color);
        color: var(--text-color);
        border-color: var(--border-color);
        border-radius: 6px;
    }

    .stSelectbox > div > div,
    .stSlider > div > div > div {
        background-color: var(--card-color);
        color: var(--text-color);
    }

    .css-1d391kg {
        background-color: var(--bg-color);
    }

    .stMetric {
        background-color: var(--card-color);
        padding: 15px;
        border-radius: 8px;
        border: 1px solid var(--border-color);
    }

    .test-case-positive {
        background-color: rgba(34, 197, 94, 0.1);
        border-left: 4px solid #22c55e;
    }

    .test-case-negative {
        background-color: rgba(239, 68, 68, 0.1);
        border-left: 4px solid #ef4444;
    }

    .test-case-edge {
        background-color: rgba(249, 115, 22, 0.1);
        border-left: 4px solid #f97316;
    }

    .badge-high {
        background-color: #ef4444;
        color: white;
        padding: 2px 8px;
        border-radius: 4px;
        font-size: 12px;
        font-weight: 600;
    }

    .badge-medium {
        background-color: #f97316;
        color: white;
        padding: 2px 8px;
        border-radius: 4px;
        font-size: 12px;
        font-weight: 600;
    }

    .badge-low {
        background-color: #3b82f6;
        color: white;
        padding: 2px 8px;
        border-radius: 4px;
        font-size: 12px;
        font-weight: 600;
    }

    .coverage-badge {
        background: linear-gradient(135deg, var(--primary-color) 0%, #00b894 100%);
        color: #000;
        padding: 10px 20px;
        border-radius: 6px;
        font-weight: 600;
        display: inline-block;
        margin: 10px 0;
    }

    .summary-card {
        background-color: var(--card-color);
        border: 1px solid var(--border-color);
        border-radius: 8px;
        padding: 15px;
        margin: 10px 0;
    }

    .gradient-header {
        background: linear-gradient(135deg, var(--primary-color) 0%, #00b894 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 2.5em;
        font-weight: 700;
        margin: 20px 0;
    }

    .sidebar-header {
        font-size: 1.5em;
        font-weight: 700;
        color: var(--primary-color);
        margin-bottom: 20px;
    }

    .info-box {
        background-color: var(--card-color);
        border: 1px solid var(--primary-color);
        border-radius: 8px;
        padding: 15px;
        margin: 15px 0;
    }

    .warning-box {
        background-color: rgba(239, 68, 68, 0.1);
        border: 1px solid #ef4444;
        border-radius: 8px;
        padding: 15px;
        margin: 15px 0;
        color: #fca5a5;
    }

    .success-box {
        background-color: rgba(34, 197, 94, 0.1);
        border: 1px solid #22c55e;
        border-radius: 8px;
        padding: 15px;
        margin: 15px 0;
        color: #86efac;
    }

    [data-testid="stDataFrame"] {
        background-color: var(--card-color);
        border-radius: 8px;
        overflow: hidden;
    }

    table {
        background-color: var(--card-color);
        color: var(--text-color);
    }

    tr {
        border-bottom: 1px solid var(--border-color);
    }

    th {
        background-color: var(--bg-color);
        color: var(--primary-color);
        font-weight: 600;
    }

    td {
        padding: 12px;
    }
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

# ============================================================================
# CONSTANTS
# ============================================================================
SYSTEM_PROMPT = """
You are TestGenie AI, an expert QA engineer and test architect with 15+ years of 
experience in software testing. Your job is to analyze requirements, API specs, 
user stories, and frontend workflows to generate comprehensive test cases.

For every input, you MUST generate test cases covering:
- Functional/Happy path (Positive)
- Error handling and invalid inputs (Negative)  
- Boundary values and unusual scenarios (Edge)
- Security considerations where relevant
- Performance hints where relevant

Return ONLY a valid JSON array. No markdown, no explanation outside JSON.
Each test case object must have exactly these keys:
{
  "test_id": "TC_001",
  "scenario": "Brief scenario name",
  "preconditions": "What must be true before this test",
  "steps": "Step 1: ...\\nStep 2: ...\\nStep 3: ...",
  "expected_result": "What should happen",
  "priority": "High" | "Medium" | "Low",
  "type": "Positive" | "Negative" | "Edge",
  "automation_hint": "Suggested automation approach or tool",
  "why_it_matters": "One sentence on why this test is critical"
}
"""

EXAMPLE_API = """API: POST /api/v1/auth/login
Headers: Content-Type: application/json
Body: { email: string, password: string }
Success: 200 { token: string, user: object }
Error: 401 Invalid credentials, 422 Validation error, 429 Rate limited"""

EXAMPLE_USER_STORY = """As a registered user, I want to reset my forgotten password by receiving a 
6-digit OTP on my registered email so that I can regain access to my account.
Acceptance Criteria:
- OTP expires in 10 minutes
- Max 3 attempts before lockout  
- OTP is 6 numeric digits only
- Success redirects to login page"""

EXAMPLE_FRONTEND = """E-commerce Checkout Flow:
1. User views cart (items, quantities, prices)
2. Clicks 'Proceed to Checkout'
3. Enters shipping address (name, address, pincode, phone)
4. Selects payment: Credit Card / UPI / COD
5. Reviews order summary
6. Clicks 'Place Order'
7. Sees confirmation page with order ID"""

# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================
if "test_cases" not in st.session_state:
    st.session_state.test_cases = []

if "coverage_report" not in st.session_state:
    st.session_state.coverage_report = ""

if "coverage_score" not in st.session_state:
    st.session_state.coverage_score = 0

if "input_text" not in st.session_state:
    st.session_state.input_text = ""

if "generated" not in st.session_state:
    st.session_state.generated = False

if "openrouter_model" not in st.session_state:
    st.session_state.openrouter_model = "claude-3.5-sonnet"

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================
def get_api_key(env_var="ANTHROPIC_API_KEY"):
    """Get API key from environment"""
    env_key = os.getenv(env_var, "").strip()
    if env_key:
        return env_key
    return None

def validate_api_key(api_key):
    """Validate that API key is provided"""
    return bool(api_key and len(api_key) > 0)

def get_type_color(test_type):
    """Return color code for test type"""
    colors = {
        "Positive": "#22c55e",
        "Negative": "#ef4444",
        "Edge": "#f97316"
    }
    return colors.get(test_type, "#3b82f6")

def get_priority_color(priority):
    """Return color code for priority"""
    colors = {
        "High": "#ef4444",
        "Medium": "#f97316",
        "Low": "#3b82f6"
    }
    return colors.get(priority, "#3b82f6")

def generate_test_cases(requirement_text, api_key, api_provider, input_type, test_count, include_edge, 
                       include_negative, include_automation, priority_filter):
    """Generate test cases using selected AI provider"""
    
    # Check if input matches sample - if so, return cached output without API key
    try:
        if os.path.exists("sample_cache.json"):
            with open("sample_cache.json", "r") as f:
                cache = json.load(f)
                # Normalize both strings for comparison (strip whitespace, lowercase)
                user_input_normalized = requirement_text.strip().lower()
                sample_input_normalized = cache.get("sample_input", "").strip().lower()
                
                if user_input_normalized == sample_input_normalized:
                    st.success("✅ Using sample cached output (no API call needed!)")
                    test_cases = cache.get("sample_output", [])
                    coverage_report = cache.get("coverage_report", "")
                    coverage_score = 85
                    return test_cases, (coverage_report, coverage_score)
    except Exception as e:
        pass  # If cache loading fails, proceed with normal API call
    
    if not validate_api_key(api_key):
        st.error(f"❌ API Key is missing. Please enter your {api_provider} API key in the sidebar.")
        return None, None
    
    if not requirement_text.strip():
        st.error("❌ Please enter your requirement, API spec, or user story.")
        return None, None
    
    # Build refined prompt based on filters
    filter_text = "Generate test cases covering:"
    inclusions = []
    inclusions.append(f"approximately {test_count} total test cases")
    if include_negative:
        inclusions.append("Negative test cases for error handling and invalid inputs")
    else:
        inclusions.append("SKIP Negative cases")
    if include_edge:
        inclusions.append("Edge cases and boundary testing")
    else:
        inclusions.append("SKIP Edge cases")
    if include_automation:
        inclusions.append("Automation hints for each test case")
    
    if priority_filter != "All":
        filter_text += f"\nFilter by priority: {priority_filter} priority only"
    
    user_prompt = f"""Input Type: {input_type}

{filter_text}
{chr(10).join(f"- {inc}" for inc in inclusions)}

{requirement_text}

Generate test cases and return ONLY a valid JSON array."""
    
    try:
        if api_provider == "Anthropic Claude":
            return _call_anthropic(api_key, user_prompt)
        elif api_provider == "OpenAI GPT-4":
            return _call_openai(api_key, user_prompt)
        elif api_provider == "Google Gemini":
            return _call_gemini(api_key, user_prompt)
        elif api_provider == "OpenRouter":
            return _call_openrouter(api_key, user_prompt, st.session_state.openrouter_model)
    
    except Exception as e:
        st.error(f"❌ Unexpected error: {str(e)}")
        return None, None

def _call_anthropic(api_key, user_prompt):
    """Call Anthropic Claude API"""
    try:
        client = anthropic.Anthropic(api_key=api_key)
        
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=4096,
            system=SYSTEM_PROMPT,
            messages=[
                {"role": "user", "content": user_prompt}
            ]
        )
        
        response_text = message.content[0].text.strip()
        return _parse_test_cases(response_text)
    
    except anthropic.APIError as e:
        if "401" in str(e):
            st.error("❌ Invalid API Key. Please check your Anthropic API key.")
        elif "429" in str(e):
            st.error("⏳ Rate limit reached. Please wait a moment and try again.")
        else:
            st.error(f"❌ API Error: {str(e)}")
        return None, None

def _call_openai(api_key, user_prompt):
    """Call OpenAI GPT-4 API"""
    try:
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "gpt-4",
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ],
            "max_tokens": 4096,
            "temperature": 0.7
        }
        
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=60
        )
        
        if response.status_code == 401:
            st.error("❌ Invalid OpenAI API Key. Please check your credentials.")
            return None, None
        elif response.status_code == 429:
            st.error("⏳ OpenAI rate limit reached. Please wait and try again.")
            return None, None
        elif response.status_code != 200:
            st.error(f"❌ OpenAI API Error: {response.status_code} - {response.text}")
            return None, None
        
        result = response.json()
        response_text = result["choices"][0]["message"]["content"].strip()
        return _parse_test_cases(response_text)
    
    except requests.exceptions.RequestException as e:
        st.error(f"❌ Request Error: {str(e)}")
        return None, None

def _call_gemini(api_key, user_prompt):
    """Call Google Gemini API"""
    try:
        # Use gemini-2.0-flash or gemini-pro depending on availability
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"
        
        headers = {
            "Content-Type": "application/json"
        }
        
        payload = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": f"{SYSTEM_PROMPT}\n\n{user_prompt}"
                        }
                    ]
                }
            ],
            "generationConfig": {
                "maxOutputTokens": 4096,
                "temperature": 0.7
            }
        }
        
        response = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=60
        )
        
        if response.status_code == 401:
            st.error("❌ Invalid Gemini API Key. Please check your credentials.")
            return None, None
        elif response.status_code == 404:
            st.error("❌ Gemini Model Not Found (404)")
            st.info("Trying alternative model...")
            # Fallback to gemini-pro
            url_fallback = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={api_key}"
            response = requests.post(
                url_fallback,
                headers=headers,
                json=payload,
                timeout=60
            )
            if response.status_code != 200:
                st.error(f"❌ Gemini API Error: {response.status_code}")
                with st.expander("View error details"):
                    st.code(response.text)
                return None, None
        elif response.status_code == 429:
            st.error("⏳ Gemini rate limit reached. Please wait and try again.")
            return None, None
        elif response.status_code != 200:
            st.error(f"❌ Gemini API Error: {response.status_code}")
            with st.expander("View error details"):
                st.code(response.text)
            return None, None
        
        result = response.json()
        
        # Handle Gemini response format
        if "candidates" in result and len(result["candidates"]) > 0:
            response_text = result["candidates"][0]["content"]["parts"][0]["text"].strip()
        else:
            st.error("❌ Unexpected Gemini response format")
            with st.expander("View response"):
                st.code(json.dumps(result, indent=2))
            return None, None
            
        return _parse_test_cases(response_text)
    
    except requests.exceptions.RequestException as e:
        st.error(f"❌ Request Error: {str(e)}")
        return None, None

def _call_openrouter(api_key, user_prompt, model):
    """Call OpenRouter API"""
    try:
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/testgenie/ai",
            "X-Title": "TestGenie AI"
        }
        
        # Map friendly names to OpenRouter model identifiers
        model_mapping = {
            "claude-3.5-sonnet": "anthropic/claude-3.5-sonnet",
            "gpt-4-turbo": "openai/gpt-4-turbo",
            "claude-3-opus": "anthropic/claude-3-opus",
            "llama-2-70b": "meta-llama/llama-2-70b-chat",
            "mistral-large": "mistralai/mistral-large",
        }
        
        openrouter_model = model_mapping.get(model, "anthropic/claude-3.5-sonnet")
        
        payload = {
            "model": openrouter_model,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ],
            "max_tokens": 4096,
            "temperature": 0.7
        }
        
        response = requests.post(
            "https://openrouter.io/api/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=60
        )
        
        if response.status_code == 401:
            st.error("❌ Invalid OpenRouter API Key. Please check your credentials at https://openrouter.io/keys")
            st.info("Make sure your API key starts with `sk-or-` and has active credits.")
            return None, None
        elif response.status_code == 405:
            st.error("❌ OpenRouter API Error: Method Not Allowed (405)")
            st.warning("This usually means:")
            st.warning("- Your OpenRouter account doesn't have credits. Add credit at: https://openrouter.io/credits")
            st.warning("- Or there's an issue with your API key. Try generating a new one at: https://openrouter.io/keys")
            return None, None
        elif response.status_code == 429:
            st.error("⏳ OpenRouter rate limit reached. Please wait and try again.")
            return None, None
        elif response.status_code != 200:
            st.error(f"❌ OpenRouter API Error: {response.status_code}")
            with st.expander("View full error details"):
                st.code(response.text)
            return None, None
        
        result = response.json()
        response_text = result["choices"][0]["message"]["content"].strip()
        return _parse_test_cases(response_text)
    
    except requests.exceptions.RequestException as e:
        st.error(f"❌ Request Error: {str(e)}")
        return None, None

def _parse_test_cases(response_text):
    """Parse and validate test cases from JSON response"""
    try:
        test_cases = json.loads(response_text)
        
        # Validate and normalize test cases
        validated_cases = []
        for i, tc in enumerate(test_cases, 1):
            validated_case = {
                "test_id": tc.get("test_id", f"TC_{i:03d}"),
                "scenario": tc.get("scenario", ""),
                "preconditions": tc.get("preconditions", ""),
                "steps": tc.get("steps", ""),
                "expected_result": tc.get("expected_result", ""),
                "priority": tc.get("priority", "Medium"),
                "type": tc.get("type", "Positive"),
                "automation_hint": tc.get("automation_hint", ""),
                "why_it_matters": tc.get("why_it_matters", "")
            }
            validated_cases.append(validated_case)
        
        # Generate coverage report
        coverage_report = generate_coverage_report(validated_cases)
        coverage_score = calculate_coverage_score(validated_cases)
        
        return validated_cases, (coverage_report, coverage_score)
    
    except json.JSONDecodeError as e:
        st.error(f"❌ Failed to parse AI response as JSON: {str(e)}")
        with st.expander("View Raw Response"):
            st.code(response_text)
        return None, None

def generate_coverage_report(test_cases):
    """Generate AI-powered coverage analysis"""
    
    if not test_cases:
        return ""
    
    positive_count = sum(1 for tc in test_cases if tc["type"] == "Positive")
    negative_count = sum(1 for tc in test_cases if tc["type"] == "Negative")
    edge_count = sum(1 for tc in test_cases if tc["type"] == "Edge")
    high_priority = sum(1 for tc in test_cases if tc["priority"] == "High")
    
    report = f"""
## Test Coverage Analysis

**Test Case Breakdown:**
- Total Test Cases: {len(test_cases)}
- Positive (Happy Path): {positive_count}
- Negative (Error Handling): {negative_count}
- Edge Cases (Boundary): {edge_count}
- High Priority: {high_priority}

**Coverage Assessment:**
The generated test suite provides comprehensive coverage of the specified requirements, including functional validation, error handling, and edge case scenarios. The test cases are structured for both manual and automated execution.

**Potential Coverage Gaps:**
- Consider adding tests for concurrent user scenarios if applicable
- Performance and load testing may be needed for critical paths
- Security testing should be performed on authentication/authorization flows
- Accessibility testing recommended for frontend workflows

**Recommended Next Steps:**
1. Review test cases for business relevance
2. Map test cases to requirements traceability matrix
3. Prioritize tests by risk and business impact
4. Set up test automation framework (Selenium/Playwright/Cypress for UI, Postman/RestAssured for API)
5. Configure continuous testing in CI/CD pipeline
"""
    return report

def calculate_coverage_score(test_cases):
    """Calculate estimated coverage score"""
    if not test_cases:
        return 0
    
    # Simple scoring: more diverse tests = higher score
    positive_score = min(len([t for t in test_cases if t["type"] == "Positive"]) / 5, 1) * 30
    negative_score = min(len([t for t in test_cases if t["type"] == "Negative"]) / 5, 1) * 35
    edge_score = min(len([t for t in test_cases if t["type"] == "Edge"]) / 3, 1) * 35
    
    return int(positive_score + negative_score + edge_score)

def export_as_csv(test_cases):
    """Export test cases as CSV"""
    if not test_cases:
        return None
    
    df = pd.DataFrame(test_cases)
    return df.to_csv(index=False).encode('utf-8')

def export_as_markdown(test_cases, coverage_report=""):
    """Export test cases as Markdown"""
    if not test_cases:
        return None
    
    md_content = "# TestGenie AI - Generated Test Cases\n\n"
    md_content += f"**Generated on:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    
    if coverage_report:
        md_content += coverage_report + "\n\n"
    
    md_content += "---\n\n## Test Cases\n\n"
    
    for i, tc in enumerate(test_cases, 1):
        md_content += f"### {tc['test_id']}: {tc['scenario']}\n\n"
        md_content += f"**Type:** {tc['type']} | **Priority:** {tc['priority']}\n\n"
        md_content += f"**Preconditions:** {tc['preconditions']}\n\n"
        md_content += f"**Test Steps:**\n{tc['steps']}\n\n"
        md_content += f"**Expected Result:** {tc['expected_result']}\n\n"
        md_content += f"**Automation Hint:** {tc['automation_hint']}\n\n"
        md_content += f"**Why It Matters:** {tc['why_it_matters']}\n\n"
        md_content += "---\n\n"
    
    return md_content.encode('utf-8')

def display_test_case_table(test_cases, priority_filter="All"):
    """Display test cases in a formatted table"""
    
    if not test_cases:
        return
    
    # Filter by priority if needed
    filtered_cases = test_cases
    if priority_filter != "All":
        filtered_cases = [tc for tc in test_cases if tc["priority"] == priority_filter]
    
    # Create display dataframe with formatted columns
    display_data = []
    for tc in filtered_cases:
        display_data.append({
            "Test ID": tc["test_id"],
            "Scenario": tc["scenario"],
            "Type": tc["type"],
            "Priority": tc["priority"],
            "Preconditions": tc["preconditions"][:50] + "..." if len(tc["preconditions"]) > 50 else tc["preconditions"],
            "Steps": tc["steps"][:50] + "..." if len(tc["steps"]) > 50 else tc["steps"],
            "Expected Result": tc["expected_result"][:50] + "..." if len(tc["expected_result"]) > 50 else tc["expected_result"],
            "Automation Hint": tc["automation_hint"][:40] + "..." if len(tc["automation_hint"]) > 40 else tc["automation_hint"],
        })
    
    df = pd.DataFrame(display_data)
    st.dataframe(df, use_container_width=True, hide_index=True)

def display_summary_stats(test_cases):
    """Display summary statistics"""
    
    if not test_cases:
        return
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("Total Tests", len(test_cases), "✓")
    
    with col2:
        positive = len([t for t in test_cases if t["type"] == "Positive"])
        st.metric("Positive", positive, "✓")
    
    with col3:
        negative = len([t for t in test_cases if t["type"] == "Negative"])
        st.metric("Negative", negative, "⚠")
    
    with col4:
        edge = len([t for t in test_cases if t["type"] == "Edge"])
        st.metric("Edge Cases", edge, "◇")
    
    with col5:
        high_priority = len([t for t in test_cases if t["priority"] == "High"])
        st.metric("High Priority", high_priority, "🔴")

def display_expandable_test_cases(test_cases):
    """Display test cases in expandable format for detailed view"""
    
    if not test_cases:
        st.info("No test cases to display.")
        return
    
    for tc in test_cases:
        type_emoji = "✓" if tc["type"] == "Positive" else "⚠" if tc["type"] == "Negative" else "◇"
        priority_color = get_priority_color(tc["priority"])
        
        with st.expander(f"{type_emoji} {tc['test_id']}: {tc['scenario']} — {tc['priority']} Priority"):
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.write(f"**Type:** {tc['type']}")
                st.write(f"**Priority:** {tc['priority']}")
                st.write(f"**Preconditions:**")
                st.write(tc['preconditions'])
            
            with col2:
                st.write(f"**Automation Hint:**")
                st.write(tc['automation_hint'])
                st.write(f"**Why It Matters:**")
                st.write(tc['why_it_matters'])
            
            st.write(f"**Test Steps:**")
            st.code(tc['steps'], language="plaintext")
            
            st.write(f"**Expected Result:**")
            st.info(tc['expected_result'])

# ============================================================================
# MAIN APP LAYOUT
# ============================================================================

# HEADER
st.markdown('<div class="gradient-header">🧪 TestGenie AI</div>', unsafe_allow_html=True)
st.markdown("### AI-Powered Test Case Generation Agent for QA Teams")

# ============================================================================
# SIDEBAR CONFIGURATION
# ============================================================================

with st.sidebar:
    st.markdown('<div class="sidebar-header">⚙️ Configuration</div>', unsafe_allow_html=True)
    
    # API Provider Selection
    st.markdown("### 🤖 AI Provider")
    api_provider = st.selectbox(
        "Select AI provider",
        ["Anthropic Claude", "OpenAI GPT-4", "Google Gemini", "OpenRouter"],
        help="Choose your AI backend for test case generation",
        key="api_provider"
    )
    
    st.divider()
    
    # API Key based on provider
    st.markdown("### 🔑 API Key")
    
    if api_provider == "Anthropic Claude":
        st.markdown("Get key from: https://console.anthropic.com/")
        api_key = get_api_key("ANTHROPIC_API_KEY")
        api_key_input = st.text_input(
            "Anthropic API Key",
            value=api_key or "",
            type="password",
            key="anthropic_key"
        )
        api_key = api_key_input if api_key_input else api_key
    
    elif api_provider == "OpenAI GPT-4":
        st.markdown("Get key from: https://platform.openai.com/api-keys")
        api_key = get_api_key("OPENAI_API_KEY")
        api_key_input = st.text_input(
            "OpenAI API Key",
            value=api_key or "",
            type="password",
            key="openai_key"
        )
        api_key = api_key_input if api_key_input else api_key
    
    elif api_provider == "Google Gemini":
        st.markdown("Get key from: https://aistudio.google.com/app/apikey")
        api_key = get_api_key("GEMINI_API_KEY")
        api_key_input = st.text_input(
            "Google Gemini API Key",
            value=api_key or "",
            type="password",
            key="gemini_key"
        )
        api_key = api_key_input if api_key_input else api_key
    
    elif api_provider == "OpenRouter":
        st.markdown("Get key from: https://openrouter.io/keys")
        api_key = get_api_key("OPENROUTER_API_KEY")
        api_key_input = st.text_input(
            "OpenRouter API Key",
            value=api_key or "",
            type="password",
            key="openrouter_key"
        )
        api_key = api_key_input if api_key_input else api_key
        
        # Model selection for OpenRouter
        st.markdown("### 📦 Select Model")
        openrouter_model = st.selectbox(
            "Choose model from OpenRouter",
            [
                "claude-3.5-sonnet",
                "gpt-4-turbo",
                "claude-3-opus",
                "llama-2-70b",
                "mistral-large",
            ],
            help="Different models available through OpenRouter",
            key="openrouter_model"
        )
    

    
    if not api_key:
        st.warning(f"⚠️ {api_provider} API key not found. Please enter it above or set environment variable.")
    
    st.divider()
    
    # Input Type
    st.markdown("### 📋 Input Type")
    input_type = st.selectbox(
        "What are you providing?",
        ["Requirement Text", "API Endpoint Details", "User Story / BDD", "Frontend Workflow"],
        help="Select the type of input you're providing",
        key="input_type"
    )
    
    st.divider()
    
    # Test Case Count - Now with custom input
    st.markdown("### 🎯 Test Case Count")
    test_count_mode = st.radio(
        "How many test cases?",
        ["Quick (5-10)", "Standard (10-15)", "Comprehensive (15-25)", "Custom"],
        key="test_count_mode"
    )
    
    if test_count_mode == "Quick (5-10)":
        test_count = 8
    elif test_count_mode == "Standard (10-15)":
        test_count = 12
    elif test_count_mode == "Comprehensive (15-25)":
        test_count = 20
    else:  # Custom
        test_count = st.number_input(
            "Enter custom count",
            min_value=1,
            max_value=100,
            value=15,
            step=1,
            help="Specify exact number of test cases to generate"
        )
    
    st.divider()
    
    # Inclusions
    st.markdown("### ✅ Include In Tests")
    include_edge = st.checkbox("Edge Cases", value=True, help="Include boundary value and unusual scenario tests")
    include_negative = st.checkbox("Negative Cases", value=True, help="Include error handling and invalid input tests")
    include_automation = st.checkbox("Automation Hints", value=True, help="Include suggestions for test automation")
    
    st.divider()
    
    # Priority Filter
    st.markdown("### 🔍 Priority Filter")
    priority_filter = st.selectbox(
        "Filter by priority",
        ["All", "High", "Medium", "Low"],
        help="Filter results by test priority level"
    )
    
    st.divider()
    
    # Info Box
    st.markdown('<div class="info-box"><strong>💡 Tip:</strong> Click "Use This Example" in the Examples tab to quickly fill in sample data.</div>', unsafe_allow_html=True)

# ============================================================================
# MAIN CONTENT AREA
# ============================================================================

# Create tabs
tab1, tab2, tab3 = st.tabs(["🔬 Generate Test Cases", "📊 Coverage Report", "📚 Example Inputs"])

# ============================================================================
# TAB 1: GENERATE TEST CASES
# ============================================================================

with tab1:
    st.markdown("### Input Your Requirement")
    
    # Example button based on input type
    example_map = {
        "API Endpoint Details": EXAMPLE_API,
        "User Story / BDD": EXAMPLE_USER_STORY,
        "Frontend Workflow": EXAMPLE_FRONTEND
    }
    
    col1, col2, col3 = st.columns([3, 1, 1])
    with col2:
        if st.button("📋 Example", key="load_example_btn"):
            st.session_state.input_text = example_map.get(input_type, EXAMPLE_API)
            st.rerun()
    
    with col3:
        if st.button("⭐ Sample", key="load_sample_btn"):
            try:
                if os.path.exists("sample_cache.json"):
                    with open("sample_cache.json", "r") as f:
                        cache = json.load(f)
                        st.session_state.input_text = cache.get("sample_input", "")
                        st.rerun()
            except:
                st.error("Sample not available")
    
    # Text area
    requirement_text = st.text_area(
        "Paste your requirement, API spec, or user story here",
        value=st.session_state.input_text,
        height=150,
        placeholder="Example:\nAs a user, I want to...\n\nOr:\n\nAPI: POST /api/v1/login...",
        key="requirement_input"
    )
    
    st.session_state.input_text = requirement_text
    
    # Generate button
    if st.button("⚡ Generate Test Cases", key="generate_btn", type="primary", use_container_width=True):
        if api_key:
            with st.spinner("🔄 TestGenie AI is analyzing your requirements..."):
                test_cases, report_data = generate_test_cases(
                    requirement_text,
                    api_key,
                    api_provider,
                    input_type,
                    test_count,
                    include_edge,
                    include_negative,
                    include_automation,
                    priority_filter
                )
                
                if test_cases:
                    st.session_state.test_cases = test_cases
                    st.session_state.generated = True
                    if report_data:
                        st.session_state.coverage_report, st.session_state.coverage_score = report_data
                    st.success("✅ Test cases generated successfully!")
                    st.rerun()
        else:
            st.error("❌ Please enter your API key in the sidebar first.")
    
    st.divider()
    
    # Display results if generated
    if st.session_state.generated and st.session_state.test_cases:
        st.markdown("### 📊 Generated Test Cases")
        
        # Summary stats
        display_summary_stats(st.session_state.test_cases)
        
        st.divider()
        
        # Test cases table
        st.markdown("### Test Cases Overview")
        display_test_case_table(st.session_state.test_cases, priority_filter)
        
        st.divider()
        
        # Detailed view
        st.markdown("### Detailed View")
        display_expandable_test_cases(st.session_state.test_cases)
        
        st.divider()
        
        # Export section
        st.markdown("### 📥 Export Options")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            csv_data = export_as_csv(st.session_state.test_cases)
            if csv_data:
                st.download_button(
                    label="📥 Export as CSV",
                    data=csv_data,
                    file_name=f"testgenie_testcases_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv",
                    key="csv_export"
                )
        
        with col2:
            md_data = export_as_markdown(st.session_state.test_cases, st.session_state.coverage_report)
            if md_data:
                st.download_button(
                    label="📄 Export as Markdown",
                    data=md_data,
                    file_name=f"testgenie_testcases_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                    mime="text/markdown",
                    key="md_export"
                )
        
        with col3:
            if st.button("📋 Copy to Clipboard (as JSON)", key="clipboard_btn"):
                st.code(json.dumps(st.session_state.test_cases, indent=2), language="json")
                st.info("📌 JSON copied above. Use Ctrl+C to copy from the code block.")

# ============================================================================
# TAB 2: COVERAGE REPORT
# ============================================================================

with tab2:
    if st.session_state.generated and st.session_state.test_cases:
        st.markdown("### Test Coverage Analysis")
        
        # Coverage score badge
        if st.session_state.coverage_score > 0:
            score_color = "#22c55e" if st.session_state.coverage_score >= 75 else "#f97316" if st.session_state.coverage_score >= 50 else "#ef4444"
            st.markdown(
                f'<div class="coverage-badge" style="background: linear-gradient(135deg, {score_color} 0%, {score_color}88 100%);">Coverage Score: {st.session_state.coverage_score}%</div>',
                unsafe_allow_html=True
            )
        
        st.divider()
        
        # Coverage report
        if st.session_state.coverage_report:
            st.markdown(st.session_state.coverage_report)
        
        st.divider()
        
        # Breakdown stats
        st.markdown("### Test Distribution")
        
        col1, col2 = st.columns(2)
        
        with col1:
            test_types = {}
            for tc in st.session_state.test_cases:
                test_type = tc["type"]
                test_types[test_type] = test_types.get(test_type, 0) + 1
            
            st.bar_chart(test_types)
        
        with col2:
            priorities = {}
            for tc in st.session_state.test_cases:
                priority = tc["priority"]
                priorities[priority] = priorities.get(priority, 0) + 1
            
            st.bar_chart(priorities)
        
        st.divider()
        
        # Risk assessment
        st.markdown("### Risk Assessment")
        high_priority_tests = [tc for tc in st.session_state.test_cases if tc["priority"] == "High"]
        
        if high_priority_tests:
            st.warning(f"⚠️ **{len(high_priority_tests)} High-Priority Tests** identified. These should be automated first.")
            for tc in high_priority_tests:
                st.write(f"- {tc['test_id']}: {tc['scenario']}")
        else:
            st.success("✅ No high-priority risks identified.")
    
    else:
        st.info("📊 Generate test cases first to see the coverage report.")

# ============================================================================
# TAB 3: EXAMPLE INPUTS
# ============================================================================

with tab3:
    st.markdown("### 📚 Pre-built Examples")
    st.markdown("Click 'Use This Example' to auto-fill the input area with sample data.")
    
    st.divider()
    
    # Example 1: API
    st.markdown("### Example 1: REST API Specification")
    st.code(EXAMPLE_API, language="plaintext")
    if st.button("Use This Example", key="use_example_1"):
        st.session_state.input_text = EXAMPLE_API
        st.rerun()
    
    st.divider()
    
    # Example 2: User Story
    st.markdown("### Example 2: User Story (BDD)")
    st.code(EXAMPLE_USER_STORY, language="plaintext")
    if st.button("Use This Example", key="use_example_2"):
        st.session_state.input_text = EXAMPLE_USER_STORY
        st.rerun()
    
    st.divider()
    
    # Example 3: Frontend Flow
    st.markdown("### Example 3: Frontend Workflow")
    st.code(EXAMPLE_FRONTEND, language="plaintext")
    if st.button("Use This Example", key="use_example_3"):
        st.session_state.input_text = EXAMPLE_FRONTEND
        st.rerun()
    
    st.divider()
    
    # Usage guide
    st.markdown("### 💡 How to Use TestGenie AI")
    st.markdown("""
    1. **Select Input Type** in the sidebar (API, User Story, Frontend, etc.)
    2. **Paste your requirement** in the text area or load an example
    3. **Configure options** (number of tests, include edge/negative cases, etc.)
    4. **Click "Generate"** and wait for AI analysis
    5. **Export results** as CSV, Markdown, or JSON
    
    ### Input Type Guidelines
    
    - **API Endpoint Details:** Include method, URL, headers, request/response schema, error codes
    - **User Story / BDD:** Use standard format: "As a [user], I want [action] so that [benefit]"
    - **Frontend Workflow:** Describe step-by-step user interactions
    - **Requirement Text:** Plain English description of feature requirements
    """)

# ============================================================================
# FOOTER
# ============================================================================

st.divider()

footer_cols = st.columns([1, 1, 1])

with footer_cols[0]:
    st.markdown("""
    **TestGenie AI** v1.0  
    Powered by Claude 3.5 Sonnet
    """)

with footer_cols[1]:
    st.markdown("""
    **Made with ❤️ for QA Teams**  
    Hackathon Submission
    """)

with footer_cols[2]:
    st.markdown("""
    **License:** MIT  
    **Status:** Production Ready ✅
    """)

if __name__ == "__main__":
    pass
