# 🔑 OpenRouter Setup Guide

**OpenRouter** is an excellent proxy service that gives you access to multiple AI models (Claude, GPT-4, Llama, Mistral, etc.) through a single API. This is perfect for TestGenie AI!

## Why Use OpenRouter?

✅ **Multiple Models**: Access Claude, GPT-4, Llama, Mistral, and more from one API key  
✅ **Cost Effective**: Often cheaper than official APIs  
✅ **Easy Switching**: Change models without changing code  
✅ **Simple Setup**: Just one API key needed  
✅ **Reliable**: Good uptime and support  

---

## Step-by-Step Setup

### 1. Create OpenRouter Account

1. Go to https://openrouter.io/
2. Click **"Sign Up"** (top right)
3. Sign up with email or GitHub
4. Verify your email

### 2. Get Your API Key

1. Go to https://openrouter.io/keys
2. Click **"Create Key"**
3. Name your key (e.g., "TestGenie AI")
4. Copy the key (starts with `sk-or-`)
5. **Keep it safe** - don't share it!

### 3. Add Credit (Optional but Recommended)

1. Go to https://openrouter.io/credits
2. Add a payment method
3. Add credit ($5-$50 to start)
4. You only pay for what you use!

### 4. Configure TestGenie AI

**Option A: Via .env file**
```bash
# Edit .env file
nano .env

# Add this line:
OPENROUTER_API_KEY=sk-or-your_key_here
```

**Option B: Via Sidebar**
1. Open TestGenie AI
2. In the sidebar, select **"OpenRouter"** from provider dropdown
3. Paste your API key in the input field
4. Select your model (Claude, GPT-4, Llama, etc.)

### 5. Start Using!

1. Select **OpenRouter** as your AI provider
2. Choose a model from the dropdown
3. Paste your requirement/API/user story
4. Click **⚡ Generate Test Cases**
5. Done! 🎉

---

## Available Models on OpenRouter

| Model | Best For | Speed | Cost |
|-------|----------|-------|------|
| **Claude 3.5 Sonnet** | Complex analysis, comprehensive tests | Fast | Medium |
| **GPT-4 Turbo** | Quick generation, good quality | Very Fast | Higher |
| **Claude 3 Opus** | Most capable, detailed tests | Medium | Higher |
| **Llama 2 70B** | Budget-friendly, decent quality | Medium | Low |
| **Mistral Large** | Fast and efficient, cost-effective | Very Fast | Low |

---

## Pricing Estimate

### Example Costs (Approximate)

**Generating 15 test cases from a complex requirement:**

- **Claude 3.5 Sonnet**: ~$0.05-0.10
- **GPT-4 Turbo**: ~$0.10-0.20
- **Llama 2 70B**: ~$0.02-0.05
- **Mistral Large**: ~$0.03-0.08

**Monthly Budget Examples:**
- Light usage (2-3 generations/day): $3-5/month
- Medium usage (5-10 generations/day): $10-20/month
- Heavy usage (20+ generations/day): $30-50/month

---

## Troubleshooting

### "Invalid OpenRouter API Key"
- ✅ Check key starts with `sk-or-`
- ✅ Copy from https://openrouter.io/keys (not a different page)
- ✅ Make sure there are no extra spaces
- ✅ Verify account has credits: https://openrouter.io/credits

### "Rate limit reached"
- ✅ Wait a few seconds and try again
- ✅ Check your credit balance
- ✅ Try a different model that might be less busy

### "Model not found"
- ✅ Make sure you're selecting from the TestGenie dropdown
- ✅ Available models are: claude-3.5-sonnet, gpt-4-turbo, claude-3-opus, llama-2-70b, mistral-large

### Slow Response
- ✅ Try switching to a faster model (Mistral Large, GPT-4 Turbo)
- ✅ Input requirements might be very long - consider breaking them up
- ✅ Check your internet connection

---

## Pro Tips 💡

### Tip 1: Budget Optimization
Start with **Mistral Large** or **Llama 2 70B** for cost-effective test generation. Only use Claude 3.5 Sonnet or GPT-4 when you need maximum quality.

### Tip 2: Quick Testing
Use **GPT-4 Turbo** for quick turnaround on small requirements. It's very fast!

### Tip 3: Monitor Costs
Keep an eye on your OpenRouter dashboard to track spending and adjust as needed.

### Tip 4: Bulk Generation
Generate multiple test suites in one session to batch requests and optimize costs.

---

## Comparison: OpenRouter vs Direct APIs

| Feature | OpenRouter | OpenAI Direct | Anthropic Direct | Gemini Direct |
|---------|-----------|---------------|------------------|---------------|
| **Setup Time** | 5 min ⚡ | 10 min | 10 min | 10 min |
| **Multiple Models** | ✅ Yes | ❌ No | ❌ No | ❌ No |
| **Cost Control** | ✅ Easy | ⚠️ Medium | ⚠️ Medium | ✅ Easy |
| **Price/Token** | 💰 Competitive | 💰 Base rate | 💰 Base rate | 💰 Best for volume |
| **Support** | ⭐ Good | ⭐⭐ Excellent | ⭐⭐ Excellent | ⭐ Good |

---

## Getting Help

- **OpenRouter Docs**: https://openrouter.io/docs
- **OpenRouter Discord**: Community support
- **TestGenie Issues**: Report bugs at repository
- **Email Support**: Available for paid tier

---

## Quick Reference

```bash
# Test your OpenRouter API key with curl:
curl https://openrouter.io/api/v1/chat/completions \
  -H "Authorization: Bearer sk-or-your_key_here" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "anthropic/claude-3.5-sonnet",
    "messages": [{"role": "user", "content": "Hello!"}]
  }'
```

---

**Happy testing! 🚀** If you have questions, check the TestGenie AI README or OpenRouter documentation.
