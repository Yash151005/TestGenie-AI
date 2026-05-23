# 🧪 TestGenie AI: AI-Powered Test Case Generation Agent for QA Teams

**Hackathon Submission | Production-Ready | MIT License**

## 📋 Project Overview

TestGenie AI is a professional-grade Streamlit application that leverages multiple AI providers (Anthropic Claude, OpenAI GPT-4, Google Gemini, OpenRouter, NVIDIA) to automatically generate comprehensive test cases from requirements, API specifications, user stories, and frontend workflows. Designed specifically for QA teams and software testers, it eliminates manual test case creation overhead and ensures coverage across positive, negative, and edge case scenarios.

### Problem Statement

Manual test case creation is:
- **Time-consuming** – QA teams spend hours translating requirements into structured test cases
- **Error-prone** – Manual processes lead to coverage gaps and missed edge cases
- **Hard to scale** – Adding new features or modules requires repetitive work
- **Lacks consistency** – Different team members create tests in different formats

**TestGenie AI solves this** by using advanced AI to analyze requirements once and generate comprehensive, structured, ready-to-automate test cases in seconds.

---

## ✨ Features

### 🎯 Core Capabilities

- **🤖 Multi-AI Support**: Supports Anthropic Claude, OpenAI GPT-4, Google Gemini, OpenRouter, and NVIDIA for test generation
- **🔄 Multiple Input Types**: Supports API specs, user stories, frontend workflows, and plain requirements
- **📊 Comprehensive Coverage**: Generates positive, negative, and edge case tests automatically
- **🎨 Professional UI**: Dark theme with customizable styling, intuitive controls, and responsive layout
- **📥 Export Options**: Download as CSV, Markdown, or copy as JSON
- **📈 Coverage Analysis**: AI-generated coverage report with score and risk assessment
- **⚡ Real-time Processing**: Live updates with Streamlit's reactive framework

### 🛠️ Advanced Options

- ✅ **AI Provider Selection**: Choose between Anthropic Claude, OpenAI GPT-4, Google Gemini, OpenRouter, or NVIDIA
- ✅ **Flexible Test Count**: Quick (5-10), Standard (10-15), Comprehensive (15-25), or Custom (1-100)
- ✅ **Edge Case Testing**: Enable/disable boundary and unusual scenario tests
- ✅ **Negative Test Cases**: Configure error handling and invalid input coverage
- ✅ **Automation Hints**: Get suggestions for test automation tools and approaches
- 🔍 **Priority Filtering**: Filter results by High/Medium/Low priority
- 📋 **Example Templates**: Pre-built examples for quick start

### 📊 Output Features

- **Structured Test Cases**: Each case includes:
  - Test ID and Scenario name
  - Preconditions and step-by-step instructions
  - Expected results and automation hints
  - Priority level and test type classification
  - Contextual explanation of importance

- **Summary Statistics**: 
  - Total test count
  - Distribution by type (Positive/Negative/Edge)
  - High-priority test count
  - Coverage score percentage

- **Coverage Report**:
  - Analysis of what was tested
  - Coverage gaps identified
  - Recommended additional testing areas
  - Risk assessment for high-priority tests

---

## 🛠️ Tech Stack

| Layer | Technology | Version |
|-------|-----------|---------|
| **Frontend** | Streamlit | 1.40.2 |
| **AI Backends** | Anthropic Claude API, OpenAI GPT-4, Google Gemini, OpenRouter, NVIDIA | Latest |
| **HTTP Client** | requests | 2.32.3 |
| **Python SDK** | anthropic | 0.104.1 |
| **Data Processing** | pandas | 2.2.3 |
| **Configuration** | python-dotenv | 1.0.1 |
| **Runtime** | Python | 3.8+ |

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- At least one AI provider API key:
  - **Anthropic**: https://console.anthropic.com/
  - **OpenAI**: https://platform.openai.com/api-keys
  - **Google Gemini**: https://aistudio.google.com/app/apikey
  - **OpenRouter**: https://openrouter.io/keys (supports multiple models)
  - **NVIDIA**: https://build.nvidia.com/ (enterprise-grade)
- pip package manager

### Installation

1. **Clone or download this repository**:
```bash
cd TestGenie\ AI
```

2. **Create a virtual environment** (recommended):
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Set up your API key(s)**:

**Option A: Environment variables** (recommended for production)
```bash
# Create .env file from template
cp .env.example .env

# Edit .env and add your API keys
ANTHROPIC_API_KEY=sk_ant_xxxxxxxxxxxxx
OPENAI_API_KEY=sk_xxxxxxxxxxxxx
GEMINI_API_KEY=your_gemini_key_here
OPENROUTER_API_KEY=sk-or-xxxxxxxxxxxxx
NVIDIA_API_KEY=nvapi-xxxxxxxxxxxxx
```

**Option B: Manual input** (recommended for testing)
- Run the app and enter your API key in the sidebar when prompted
- Select your preferred AI provider from the dropdown

5. **Run the application**:
```bash
streamlit run app.py
```

6. **Open in browser**:
```
Your app is running at: http://localhost:8501
```

---

## 📖 How to Use

### Step 1: Select AI Provider

1. In the sidebar, choose your preferred AI provider:
   - **Anthropic Claude**: Best for comprehensive analysis (Recommended)
   - **OpenAI GPT-4**: Fast and powerful
   - **Google Gemini**: Cost-effective option

2. Enter the corresponding API key for your chosen provider

### Step 2: Provide Your Input

1. Select the **Input Type** from the sidebar:
   - **Requirement Text**: Plain English feature description
   - **API Endpoint Details**: REST API specification with methods, endpoints, schemas
   - **User Story / BDD**: Standard format user stories with acceptance criteria
   - **Frontend Workflow**: Step-by-step user interaction flow

2. **Paste your content** into the text area, or click **Load Example** to use a template

### Step 3: Configure Options

In the sidebar, customize:
- **AI Provider**: Which AI model to use
- **Test Case Count**: 
  - Quick: 5-10 tests (fast)
  - Standard: 10-15 tests (balanced)
  - Comprehensive: 15-25 tests (thorough)
  - Custom: 1-100 tests (exact control)
- **Include Edge Cases**: Test boundary values and unusual scenarios
- **Include Negative Cases**: Test error handling and invalid inputs
- **Include Automation Hints**: Get suggestions for test automation
- **Priority Filter**: Show all tests or filter by High/Medium/Low

### Step 4: Generate

Click **⚡ Generate Test Cases** and wait for AI analysis (typically 10-30 seconds depending on provider and input size)

### Step 5: Review Results

The app displays:
- **📊 Summary Statistics**: Total, positive, negative, edge, high-priority counts
- **📋 Test Cases Table**: Quick overview of all generated tests
- **🔍 Detailed View**: Expandable cards with full test details

### Step 6: Export

Download your test cases:
- **📥 CSV**: Open in Excel/Sheets for bulk editing
- **📄 Markdown**: Paste into Confluence/Notion/Wiki
- **📋 JSON**: Import into test management tools

### Step 7: Coverage Analysis

Check the **📊 Coverage Report** tab for:
- AI-generated coverage analysis
- Coverage score (estimated %)
- Test distribution charts
- Risk assessment and recommendations

---

## 🏗️ Architecture

### System Diagram

```
┌─────────────────────────────────────────────────────────┐
│                   USER INTERFACE                        │
│  (Streamlit - Dark Theme Professional UI)               │
│                                                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │   Sidebar    │  │  Main Area   │  │  Tabs        │  │
│  │ - API Key    │  │ - Input Area │  │ - Generate   │  │
│  │ - Settings   │  │ - Load Btn   │  │ - Coverage   │  │
│  │ - Filters    │  │ - Gen Button │  │ - Examples   │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
└────────────────────────┬────────────────────────────────┘
                         │
                ┌────────▼────────┐
                │  Session State  │
                │  (st.cache)     │
                └────────┬────────┘
                         │
         ┌───────────────┼───────────────┐
         │               │               │
    ┌────▼────┐   ┌─────▼──────┐  ┌────▼────────┐
    │ Validation│  │ AI Engine   │  │ Export      │
    │ & Parse   │  │ (Claude API)│  │ Module      │
    └──────────┘  └─────┬──────┘  └────────────┘
                        │
              ┌─────────▼──────────┐
              │  Anthropic Claude  │
              │  API (Sonnet 4)    │
              │                    │
              │ System Prompt:     │
              │ - QA Expertise     │
              │ - Test Strategy    │
              │ - JSON Output      │
              └────────────────────┘
```

### Data Flow

```
User Input
    ↓
Validation
    ↓
Build Prompt + System Guidance
    ↓
Call Anthropic API
    ↓
Parse JSON Response
    ↓
Store in Session State
    ↓
Display Results (Tables, Charts, Expandable Cards)
    ↓
Export (CSV/Markdown/JSON)
```

### Key Components

1. **Input Handler**
   - Accepts 4 input types
   - Validates input length and format
   - Loads examples on demand

2. **AI Engine**
   - Builds context-aware prompts
   - Calls Claude Sonnet 4 via Anthropic SDK
   - Parses JSON response with error handling

3. **Output Formatter**
   - Structures test cases with consistent schema
   - Generates coverage reports
   - Calculates coverage scores

4. **Export Module**
   - CSV export via pandas
   - Markdown formatting with metadata
   - JSON copy-to-clipboard

5. **UI Components**
   - Custom CSS for professional dark theme
   - Responsive layout with columns and tabs
   - Color-coded badges and status indicators

## 🎯 Supported AI Providers

TestGenie AI supports multiple AI providers, allowing you to choose the best option for your needs:

### Anthropic Claude 3.5 Sonnet (Recommended)
- **Strengths**: Excellent at understanding complex requirements, contextual awareness
- **Model**: claude-3-5-sonnet-20241022
- **Best For**: Comprehensive test coverage, complex scenarios
- **Pricing**: Check https://www.anthropic.com/pricing

### OpenAI GPT-4
- **Strengths**: Fast processing, great for quick test generation
- **Model**: gpt-4
- **Best For**: Quick turnaround, API testing
- **Pricing**: Check https://openai.com/pricing

### Google Gemini 1.5 Pro
- **Strengths**: Cost-effective, handles large inputs well
- **Model**: gemini-1.5-pro
- **Best For**: Large requirements, budget-conscious teams
- **Pricing**: Check https://ai.google.dev/pricing

### OpenRouter
- **Strengths**: Multiple models in one API, cost-effective, easy to switch models
- **Supported Models**: Claude 3.5 Sonnet, GPT-4 Turbo, Claude 3 Opus, Llama 2 70B, Mistral Large
- **Best For**: Teams wanting flexibility across multiple models, budget optimization
- **Pricing**: Check https://openrouter.io/pricing
- **Get Started**: https://openrouter.io/keys

### NVIDIA
- **Strengths**: High-performance LLM inference, enterprise-grade reliability, optimized for production
- **Model**: NVIDIA Nemotron (running on NVIDIA infrastructure)
- **Best For**: Enterprise teams, high-throughput test generation, production deployments
- **Pricing**: Check https://build.nvidia.com/
- **Get Started**: https://build.nvidia.com/
- **API**: NVIDIA Cloud Functions (NVCF)

---

Each generated test case includes:

```json
{
  "test_id": "TC_001",
  "scenario": "Valid user login with correct credentials",
  "preconditions": "User account exists in system, user is not logged in",
  "steps": "Step 1: Navigate to login page\nStep 2: Enter valid email\nStep 3: Enter correct password\nStep 4: Click login",
  "expected_result": "User successfully logged in, redirected to dashboard, auth token received",
  "priority": "High",
  "type": "Positive",
  "automation_hint": "Selenium: Use Page Object Model, assert on dashboard URL and welcome message",
  "why_it_matters": "Core authentication is critical; without passing this, no user can access the system"
}
```

---

## 🔐 Security & Privacy

- **API Keys**: Only stored in environment variables or user input (never in code)
- **No Data Storage**: All processing is temporary; test cases are not saved to servers
- **User Input**: Only sent to Anthropic API; no third-party tracking
- **Rate Limiting**: Handles API rate limits gracefully with user-friendly messages
- **Error Handling**: Validates all API responses; displays helpful errors

---

## 📚 Example Inputs

### Example 1: REST API

```
API: POST /api/v1/auth/login
Headers: Content-Type: application/json
Body: { email: string, password: string }
Success: 200 { token: string, user: object }
Error: 401 Invalid credentials, 422 Validation error, 429 Rate limited
```

### Example 2: User Story (BDD)

```
As a registered user, I want to reset my forgotten password by receiving a 
6-digit OTP on my registered email so that I can regain access to my account.

Acceptance Criteria:
- OTP expires in 10 minutes
- Max 3 attempts before lockout  
- OTP is 6 numeric digits only
- Success redirects to login page
```

### Example 3: Frontend Workflow

```
E-commerce Checkout Flow:
1. User views cart (items, quantities, prices)
2. Clicks 'Proceed to Checkout'
3. Enters shipping address (name, address, pincode, phone)
4. Selects payment: Credit Card / UPI / COD
5. Reviews order summary
6. Clicks 'Place Order'
7. Sees confirmation page with order ID
```

---

## 🛠️ Configuration

### Streamlit Config (Optional)

Create `.streamlit/config.toml`:

```toml
[theme]
primaryColor = "#00d4aa"
backgroundColor = "#0f1117"
secondaryBackgroundColor = "#1e2130"
textColor = "#c9d1d9"

[client]
showErrorDetails = true
showWarningOnDirectExecution = false
```

### Environment Variables

```bash
# Required
ANTHROPIC_API_KEY=sk_ant_xxxxxxxxxxxxx

# Optional
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_HEADLESS=true
```

---

## 📈 Performance & Scaling

| Metric | Value | Notes |
|--------|-------|-------|
| **Response Time** | 10-30s | Depends on input length and API latency |
| **Max Input Size** | ~50,000 chars | Streamlit text area limit |
| **Test Cases Generated** | 5-20 | User-configurable |
| **Concurrent Users** | Single-threaded | Run multiple instances for scaling |
| **API Rate Limit** | Per Anthropic tier | Handles gracefully with error messages |

---

## 🧪 Testing

The app is tested for:
- ✅ Valid JSON parsing from AI
- ✅ Graceful error handling (invalid API keys, rate limits, malformed input)
- ✅ Session state persistence across reruns
- ✅ Export functionality (CSV, Markdown)
- ✅ UI responsiveness across screen sizes
- ✅ Input validation (empty fields, missing API key)

---

## 🐛 Troubleshooting

### Problem: "API Key is missing"
**Solution**: 
- Set `ANTHROPIC_API_KEY` environment variable, or
- Enter API key manually in the sidebar

### Problem: "Invalid API Key"
**Solution**:
- Verify key at https://console.anthropic.com/
- Ensure no extra spaces in the key
- Check key hasn't been revoked

### Problem: "Rate limit reached"
**Solution**:
- Wait a moment and try again
- Check your Anthropic account usage
- Upgrade your API tier if needed

### Problem: "JSON parsing error"
**Solution**:
- Check that input is valid and descriptive
- Try with a shorter input first
- Click "View Raw Response" to see actual output
- Report the issue with the raw response

### Problem: App won't start
**Solution**:
```bash
# Clear cache
streamlit cache clear

# Check dependencies
pip install -r requirements.txt --upgrade

# Run with debug info
streamlit run app.py --logger.level=debug
```

---

## 🚀 Future Scope & Roadmap

### Phase 2 Features
- 🎤 **Voice Input**: Speak requirements, get test cases
- 🔗 **GitHub Integration**: Auto-generate tests from README/docs
- 📋 **Jira Sync**: Export directly to Jira tickets
- 🔄 **CI/CD Pipeline**: GitHub Actions integration
- 📊 **Advanced Analytics**: Track test metrics over time
- 🤖 **Multi-Model Support**: GPT-4, Llama, PaLM
- 🌐 **Web Deployment**: Cloud hosting (Streamlit Cloud, AWS)
- 🔀 **Test Merging**: Deduplicate and consolidate related tests

### Community Features
- 📚 **Test Case Library**: Reusable templates by industry
- 🏆 **Community Tests**: Share generated test cases
- 🎓 **QA Academy**: Best practices and tutorials
- 🐛 **Bug Bounty**: Report issues and get rewards

---

## 📝 License

This project is licensed under the **MIT License** – see LICENSE file for details.

Free to use, modify, and distribute for commercial and personal projects.

---

## 👥 Contributing

We welcome contributions! To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit changes (`git commit -am 'Add feature'`)
4. Push to branch (`git push origin feature/your-feature`)
5. Open a Pull Request

### Guidelines
- Follow PEP 8 style guide
- Add docstrings to functions
- Test changes locally before submitting
- Include example inputs/outputs

---

## 📧 Support & Contact

- **Issues**: Report bugs on GitHub Issues
- **Discussions**: Start a discussion for feature requests
- **Email**: support@testgenie.ai (placeholder)
- **Discord**: Join our community server (coming soon)

---

## 🎓 Credits

**Built with**:
- Streamlit – Interactive web app framework
- Anthropic Claude – AI backbone
- pandas – Data manipulation
- python-dotenv – Configuration management

**Inspired by**: Leading QA teams and test automation experts

---

## 📊 Statistics

- **Lines of Code**: ~1200 (app.py)
- **Functions**: 15+
- **Supported Input Types**: 4
- **Test Case Fields**: 9
- **Export Formats**: 3 (CSV, Markdown, JSON)
- **Development Time**: Hackathon submission
- **Status**: Production Ready ✅

---

## 🎯 Vision

TestGenie AI aims to democratize test case generation and make professional QA accessible to all development teams, from startups to enterprises. We believe that AI should augment human expertise, not replace it – and that great testing is a team sport.

**Let's make testing faster, smarter, and more collaborative. 🚀**

---

## 📎 Quick Links

- [Anthropic Console](https://console.anthropic.com/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Claude API Docs](https://docs.anthropic.com/)
- [QA Best Practices](https://www.qa-wiki.com/)
- [Test Case Templates](https://www.testcase.com/)

---

**TestGenie AI v1.0** | Made with ❤️ for QA Teams | Hackathon Submission | MIT License
