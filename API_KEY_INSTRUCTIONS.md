
# 🔑 QUICK START - ADD YOUR API KEY HERE

## Step 1: Open this file
You're already here! Just edit the line below.

## Step 2: Paste your API key

### For OpenAI (Recommended):
OPENAI_API_KEY = "PASTE-YOUR-KEY-HERE"

Get your key from: https://platform.openai.com/api-keys

### For Anthropic Claude (Alternative):
If using Claude instead, also change:
- ANTHROPIC_API_KEY = "PASTE-YOUR-KEY-HERE"
- AI_PROVIDER = "anthropic"

Get your key from: https://console.anthropic.com/

## Step 3: Save this file

## Step 4: Run the app
```bash
source venv/bin/activate
streamlit run streamlit_ui_enhanced.py
```

## That's it! 🎉

The AI features will now work automatically.

---

## ⚠️ IMPORTANT NOTES:

1. **Keep your key secret!** Don't commit it to GitHub
2. **Cost:** Using gpt-4o-mini costs ~$0.0003 per recommendation (less than a penny!)
3. **Fallback:** If the key doesn't work, the system still runs in template mode

---

## 🧪 Test It Works:

After adding your key:
1. Run the app
2. Look for "🤖 AI-Powered by OPENAI" badge in the UI
3. Get recommendations - they should be personalized narratives
4. Try asking a follow-up question in the Q&A section

If you see "✅ Enhanced Mode: OPENAI" in the sidebar, it's working!

