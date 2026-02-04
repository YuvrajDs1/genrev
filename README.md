# AI Developer Assessment - Agent-Based Educational Content Generator

A LangChain-based system with two AI agents (Generator and Reviewer) that creates and evaluates educational content with a Streamlit UI.

## 🏗️ Architecture

This project implements a **multi-agent system** using LangChain with the following components:

### 1. Generator Agent
- **Responsibility**: Generate age-appropriate educational content
- **Input**: Grade level and topic
- **Output**: Structured JSON with explanation and MCQs
- **Implementation**: Uses LangChain's `ChatAnthropic`, `ChatPromptTemplate`, and `JsonOutputParser`

### 2. Reviewer Agent
- **Responsibility**: Evaluate content quality
- **Input**: Generated content + metadata
- **Output**: Pass/fail status with specific feedback
- **Implementation**: Uses LangChain chains with structured output parsing

### 3. Agent Pipeline
- **Orchestration**: Manages the complete workflow
- **Refinement Logic**: Automatically refines content if review fails (max 1 iteration)
- **Results Tracking**: Maintains complete audit trail

## 📋 Requirements

- Python 3.8+
- Anthropic API Key

## 🚀 Installation

### 1. Clone or Download the Project

```bash
# If you have the files, navigate to the directory
cd ai-assessment
```

### 2. Create Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## 🔑 API Key Setup

You need an Anthropic API key to use this application:

1. Visit [console.anthropic.com](https://console.anthropic.com)
2. Sign up or log in
3. Navigate to "API Keys"
4. Create a new API key
5. Copy the key (you'll enter it in the UI)

## 💻 Usage

### Option 1: Run with Streamlit UI (Recommended)

```bash
streamlit run app.py
```

This will:
1. Start a local web server
2. Open your browser automatically
3. Display the interactive UI

**In the UI:**
1. Enter your Anthropic API key in the sidebar
2. Configure grade level and topic
3. Click "Generate Content"
4. View the agent pipeline flow in real-time
5. Download results as JSON

### Option 2: Run Programmatically

```python
from agent_system import AgentPipeline

# Initialize the pipeline
pipeline = AgentPipeline(api_key="your-api-key-here")

# Run the pipeline
results = pipeline.run(
    grade=4,
    topic="Types of angles"
)

# Access results
print(results["final_output"])
```

## 📊 Agent Flow

```
Input (Grade + Topic)
        ↓
┌───────────────────┐
│ Generator Agent   │ → Creates initial content
└────────┬──────────┘
         ↓
┌───────────────────┐
│ Reviewer Agent    │ → Evaluates quality
└────────┬──────────┘
         ↓
    Pass or Fail?
         ↓
    ┌────┴────┐
    │         │
   Pass      Fail
    │         │
    │    ┌────────────────┐
    │    │ Refinement     │ → Regenerate with feedback
    │    └────────────────┘
    │         │
    └────┬────┘
         ↓
   Final Output
```

## 🔍 Code Structure

```
.
├── agent_system.py      # Core agent implementation
│   ├── GeneratorAgent   # Content creation agent
│   ├── ReviewerAgent    # Quality evaluation agent
│   └── AgentPipeline    # Orchestration logic
├── app.py               # Streamlit UI
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## 🎯 Key Features

### LangChain Implementation
- ✅ **ChatAnthropic**: Uses Claude Sonnet 4 for both agents
- ✅ **ChatPromptTemplate**: Structured prompts with variables
- ✅ **JsonOutputParser**: Ensures structured, predictable outputs
- ✅ **Pydantic Models**: Type-safe data validation
- ✅ **Chains**: LCEL (LangChain Expression Language) for composability

### Agent Capabilities
- ✅ **Structured Input/Output**: JSON-based communication
- ✅ **Clear Responsibilities**: Separation of concerns
- ✅ **Feedback Loop**: Automatic refinement based on review
- ✅ **Deterministic Structure**: Consistent output format

### UI Features
- ✅ **Visual Pipeline**: See each agent's work
- ✅ **Real-time Progress**: Track generation steps
- ✅ **Detailed Results**: View all outputs and feedback
- ✅ **Export Options**: Download JSON results
- ✅ **Error Handling**: Graceful error display

## 📝 Example Output

**Input:**
```json
{
  "grade": 4,
  "topic": "Types of angles"
}
```

**Generator Output:**
```json
{
  "explanation": "An angle is formed when two lines meet at a point...",
  "mcqs": [
    {
      "question": "What is an angle that measures exactly 90 degrees called?",
      "options": ["Acute angle", "Right angle", "Obtuse angle", "Straight angle"],
      "answer": "Right angle"
    }
  ]
}
```

**Reviewer Output:**
```json
{
  "status": "pass",
  "feedback": []
}
```

## 🛠️ Customization

### Change AI Model

In `agent_system.py`, modify the model parameter:

```python
self.llm = ChatAnthropic(
    model="claude-sonnet-4-20250514",  # Change this
    api_key=api_key,
    temperature=0.7
)
```

### Adjust Temperature

- **Generator**: Higher temperature (0.7) for creativity
- **Reviewer**: Lower temperature (0.3) for consistency

### Add More Agents

You can extend the system by creating additional agent classes following the same pattern:

```python
class NewAgent:
    def __init__(self, api_key):
        self.llm = ChatAnthropic(model="...", api_key=api_key)
        self.parser = JsonOutputParser(pydantic_object=YourModel)
        self.prompt = ChatPromptTemplate.from_messages([...])
        self.chain = self.prompt | self.llm | self.parser
    
    def process(self, input_data):
        return self.chain.invoke(input_data)
```

## 🐛 Troubleshooting

### "Module not found" Error
```bash
pip install -r requirements.txt
```

### API Key Issues
- Ensure your API key is valid
- Check your Anthropic account has credits
- Verify the key is entered correctly in the UI

### Streamlit Not Opening
```bash
# Try specifying port
streamlit run app.py --server.port 8501
```

### Import Errors
Make sure you're in the correct directory and virtual environment is activated.

## 📚 LangChain Concepts Used

1. **LLMs**: `ChatAnthropic` for Claude integration
2. **Prompts**: `ChatPromptTemplate` for structured prompts
3. **Output Parsers**: `JsonOutputParser` with Pydantic
4. **Chains**: LCEL syntax (`|` operator) for composition
5. **Structured Output**: Type-safe responses with Pydantic models

## 🎓 Educational Topics You Can Try

- Mathematics: "Fractions", "Multiplication", "Geometry basics"
- Science: "Photosynthesis", "Water cycle", "Simple machines"
- Language: "Parts of speech", "Sentence structure"
- Social Studies: "Map reading", "Community helpers"

## 📄 License

This is an assessment project. Modify and use as needed.

## 🤝 Contributing

This is a standalone assessment project. Feel free to fork and enhance!

## ⚡ Performance Notes

- First run may be slower (model initialization)
- Typical generation time: 5-15 seconds
- Refinement adds 5-10 seconds if needed
- Results are not cached between runs

## 🔐 Security Notes

- **Never commit API keys** to version control
- Use environment variables for production
- The UI accepts API keys securely (password field)
- Keys are stored only in memory during session

## 📞 Support

For LangChain documentation: [docs.langchain.com](https://docs.langchain.com)
For Anthropic API docs: [docs.anthropic.com](https://docs.anthropic.com)

---

Built with ❤️ using LangChain and Streamlit
