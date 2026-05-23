# 🚀 NVIDIA Setup Guide for TestGenie AI

**NVIDIA Cloud Functions (NVCF)** provides enterprise-grade, high-performance LLM inference. Perfect for production test generation!

## Why Use NVIDIA?

✅ **Enterprise-Grade**: Built for production workloads  
✅ **High Performance**: Optimized inference on NVIDIA GPUs  
✅ **Reliable**: Enterprise SLA and support  
✅ **Scalable**: Auto-scaling for high-throughput scenarios  
✅ **Secure**: Enterprise security features  

---

## Step-by-Step Setup

### 1. Create NVIDIA Account

1. Go to: https://build.nvidia.com/
2. Click **"Sign Up"** or **"Sign In"**
3. Use your work/personal email
4. Verify email

### 2. Get Your API Key

1. Go to: https://build.nvidia.com/
2. Navigate to **"API Keys"** or **"Account Settings"**
3. Click **"Create API Key"**
4. Copy your API key (starts with `nvapi-`)
5. **Keep it safe** - don't share it!

### 3. Explore Available Models

NVIDIA provides various models through NVCF:
- **NVIDIA Nemotron**: Recommended for test generation
- **LLaMA 2**: Open-source alternative
- **Other models**: Check https://build.nvidia.com/explore

### 4. Configure TestGenie AI

**Option A: Via .env file**
```bash
# Edit .env file
nano .env

# Add this line:
NVIDIA_API_KEY=nvapi-your_key_here
```

**Option B: Via Sidebar**
1. Open TestGenie AI
2. In the sidebar, select **"NVIDIA"** from provider dropdown
3. Paste your API key in the input field
4. Click Generate!

### 5. Start Using!

1. Select **NVIDIA** as your AI provider
2. Paste your requirement/API/user story
3. Click **⚡ Generate Test Cases**
4. Done! 🎉

---

## NVIDIA vs Other Providers

| Feature | NVIDIA | OpenRouter | Gemini | OpenAI |
|---------|--------|-----------|--------|--------|
| **Performance** | ⭐⭐⭐⭐⭐ Enterprise | ⭐⭐⭐⭐ Good | ⭐⭐⭐ Decent | ⭐⭐⭐⭐⭐ Very Fast |
| **Reliability** | ⭐⭐⭐⭐⭐ SLA | ⭐⭐⭐⭐ Good | ⭐⭐⭐⭐ Good | ⭐⭐⭐⭐⭐ Excellent |
| **Cost** | 💰 Medium | 💰💰 Cheap | 💰 Free/Cheap | 💰💰💰 Higher |
| **Scale** | ✅ Auto-scaling | ❌ Limited | ❌ Limited | ✅ Enterprise |
| **Use Case** | Enterprise | Cost-sensitive | Hobbyist | Production |

---

## Pricing

NVIDIA NVCF uses a **pay-as-you-go** model:

**Estimated Costs per 1000 tokens:**
- **Input**: $0.0001-0.0002 (varies by model)
- **Output**: $0.0004-0.0008 (varies by model)

**Monthly Budget Examples:**
- Light usage (2-3 generations/day): $1-3/month
- Medium usage (5-10 generations/day): $5-15/month
- Heavy usage (20+ generations/day): $20-50/month

Check https://build.nvidia.com/pricing for current rates.

---

## Troubleshooting

### "Invalid NVIDIA API Key"
- ✅ Check key starts with `nvapi-`
- ✅ Copy from https://build.nvidia.com/account/api-keys
- ✅ Make sure there are no extra spaces
- ✅ Verify account is active

### "Rate limit reached"
- ✅ Wait 1-2 minutes and retry
- ✅ Check your usage at https://build.nvidia.com/
- ✅ Upgrade your plan if needed

### "Model not found"
- ✅ Ensure you have API access to the model
- ✅ Check available models at https://build.nvidia.com/explore
- ✅ Try a different model if needed

### Slow Response
- ✅ NVIDIA inference is typically very fast
- ✅ Check your internet connection
- ✅ Try a shorter requirement first

---

## Advanced Usage

### Using Custom Models

1. Navigate to https://build.nvidia.com/explore
2. Choose a model
3. Copy the function ID
4. Update `_call_nvidia()` in app.py with your function ID

### Batch Processing

For high-volume test generation:
```bash
# Create multiple requirements in a file
# Run TestGenie multiple times
# Export all results to CSV
```

### Integration with CI/CD

```yaml
# Example GitHub Actions workflow
- name: Generate Test Cases with TestGenie
  env:
    NVIDIA_API_KEY: ${{ secrets.NVIDIA_API_KEY }}
  run: |
    streamlit run app.py --headless
```

---

## Pro Tips 💡

### Tip 1: Use for Production
NVIDIA is ideal for production environments with SLA requirements and high throughput.

### Tip 2: Monitor Costs
Check your usage dashboard at https://build.nvidia.com/ regularly to track spending.

### Tip 3: Batch Requests
Group multiple test generations into one session to optimize cost.

### Tip 4: Documentation
Check NVIDIA's documentation: https://docs.nvidia.com/nvcf/

---

## Getting Help

- **NVIDIA Documentation**: https://docs.nvidia.com/nvcf/
- **NVIDIA Support**: https://build.nvidia.com/support
- **TestGenie Issues**: Report bugs at repository
- **Community Discord**: Check NVIDIA developer community

---

## Quick Reference

```bash
# Test your NVIDIA API key with curl:
curl -X POST "https://api.nvcf.com/v2/nvcf/pexec/functions/{FUNCTION_ID}" \
  -H "Authorization: Bearer nvapi-your_key_here" \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [{"role": "user", "content": "Hello!"}],
    "max_tokens": 100
  }'
```

---

**Enterprise-grade test generation! 🚀** If you have questions, check NVIDIA documentation or contact enterprise support.
