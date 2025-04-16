<div align="center">
  <img src="https://github.com/kalekarnn/smart-summarizer-agentic-chrome-plugin/blob/main/extension/icons/icon128.png" alt="Alt text" title="Smart Summarizer Agent" />
</div>

# Smart Summarizer Agent

A powerful text summarization tool that uses Google's Gemini AI to create concise summaries of web page content. The project includes both a Python backend service and a Chrome extension for seamless web integration.

## Features

- 🤖 Powered by Google's Gemini AI model
- 📝 Intelligent text summarization
- 💾 Automatic note saving with timestamps
- 🌐 Chrome extension for easy web page summarization
- 🔄 Multi-step processing with agent-based architecture

## Prerequisites

- Python 3.13+
- Google API Key for Gemini AI
- Chrome browser (for extension)

## Installation

1. Clone the repository
2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up your Google API Key:
   - Get an API key from Google AI Studio
   - Set it in the environment variable:
     ```python
     export GOOGLE_API_KEY="your-api-key"
     ```

## Chrome Extension Setup

1. Open Chrome and navigate to `chrome://extensions/`
2. Enable "Developer mode"
3. Click "Load unpacked" and select the `extension` folder

## Usage

1. Start the Python server:
   ```bash
   python server.py
   ```

2. Use the Chrome extension:
   - Click the extension icon on any webpage
   - The page content will be automatically summarized
   - Summaries are saved in your Downloads folder with timestamps

## Project Structure

```
├── smart_summarizer_agent.py  # Core summarization logic
├── server.py                  # Flask server for extension
├── extension/                 # Chrome extension files
│   ├── icons/
│   │   └── icon128.png
│   ├   └── icon48.png
│   ├   └── icon16.png
│   ├── manifest.json
│   ├── popup.html
│   ├── popup.js
│   ├── content.js
│   └── background.js
└── requirements.txt          # Python dependencies
```

## How It Works

1. The agent processes web page content in multiple steps
2. Uses function calls to trigger actions (summarize, save_note)
3. Implements error handling and fallback mechanisms
4. Provides detailed logging for debugging

## Error Handling

- Falls back to text truncation if summary generation fails
- Validates function calls and input data
- Provides clear error messages and logging

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.