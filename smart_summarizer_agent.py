import os
import google.generativeai as genai

os.environ["GOOGLE_API_KEY"] = ""
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

AGENT_PROMPT = """You are a summarizer agent that processes web page content in multiple steps.

Your job is to:
1. Use function calls to trigger next actions.
2. Finish with a final answer only when the task is fully completed.

Always respond in EXACTLY ONE of the following formats:

1. FUNCTION_CALL: function_name|input_data
2. FINAL_ANSWER: final_text

Examples:
- FUNCTION_CALL: summarize|<web page text>
- FUNCTION_CALL: save_note|<summary>
- FINAL_ANSWER: Note saved successfully.

Rules:
- Do not perform any actions internally. Only suggest actions via FUNCTION_CALL.
- Do not suggest any actions that are not explicitly mentioned in the rules.
- End only with FINAL_ANSWER when all steps are completed.

You are reliable, precise, and follow the rules strictly.
"""

def summarize(text):
    print("📝 Starting text summarization...")
    model = genai.GenerativeModel(model_name="gemini-2.0-flash")
    print("🤖 Created Gemini model instance for summarization")
    
    prompt = f"Please provide a concise summary of the following text, maintaining key information while reducing length:\n\n{text}"
    print("🔄 Sending text to Gemini for summarization...")
    
    try:
        response = model.generate_content(prompt)
        summary = response.text.strip()
        print("✨ Successfully generated summary")
        
        if not summary:
            print("⚠️ Empty summary received, falling back to text truncation")
            return text.strip()[:300] + "..." if len(text.strip()) > 300 else text.strip()
        
        print(f"📊 Summary length: {len(summary)} characters")
        return summary
    except Exception as e:
        print(f"❌ Error generating summary: {e}")
        return text.strip()[:300] + "..." if len(text.strip()) > 300 else text.strip()

def save_note(summary):
    print("💾 Saving note to file...")
    from datetime import datetime
    import os
    
    # Get downloads folder path
    downloads_path = os.path.expanduser("~/Downloads")
    
    # Create timestamp-based filename with website name
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"note_{timestamp}.txt"
    
    # Create full file path in downloads folder
    file_path = os.path.join(downloads_path, filename)
    
    # Structure content with summary only
    content = f"Summary:\n{summary}"
    
    with open(file_path, "w") as f:
        f.write(content)
    print(f"✅ Note saved successfully to {file_path}")
    return {"message": "Note saved successfully.", "file_path": file_path}

def run_agent(page_text):
    print("\n=== Agent Execution Started ===")
    print("\n🚀 Initializing summarizer agent...")
    model = genai.GenerativeModel(model_name="gemini-2.0-flash")
    chat = model.start_chat(history=[])
    print("🤖 Created Gemini chat instance\n")
    
    print("📋 Setting up agent with prompt...")
    chat.send_message(AGENT_PROMPT)
    print("✅ Agent initialized successfully\n")

    # Send the page text to the agent
    print("📤 Sending page text to agent...")
    response = chat.send_message(f"Page Text:\n{page_text}")
    print("📥 Received initial response from agent\n")
    
    iteration = 1
    while True:
        print(f"\n--- Step: {iteration} ---")
        reply = response.text.strip()
        print("\n🧠 Agent Response:", reply)
        print("")

        if reply.startswith("FUNCTION_CALL:"):
            print("⚙️ Processing function call...")
            _, payload = reply.split(":", 1)
            func_name, arg = payload.strip().split("|", 1)
            print(f"📌 Function requested: {func_name}\n")

            if func_name == "summarize":
                print("🔄 Executing summarize function...")
                result = summarize(page_text)
                print("✅ Summarization complete\n")
            elif func_name == "save_note":
                print("🔄 Executing save_note function...")
                result = save_note(arg)
                print("✅ Note saving complete\n")
            else:
                print(f"❌ Unknown function: {func_name}\n")
                raise ValueError(f"Unknown function: {func_name}")

            status_message = f"Previous step {iteration}: I executed the {func_name} function with result: {result}. What should I do next?"
            print("📤 Sending status and requesting next action from agent...")
            response = chat.send_message(status_message)
            iteration += 1

        elif reply.startswith("FINAL_ANSWER:"):
            final_answer = reply[len("FINAL_ANSWER:"):].strip()
            print("\n=== Agent Execution Complete ===")
            print("✨ Task completed!")
            print("✅ Final result:", final_answer)
            break
        else:
            print(f"❌ Unexpected agent output: {reply}\n")
            raise ValueError(f"Unexpected agent output: {reply}")
