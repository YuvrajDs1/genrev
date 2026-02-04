# AI Developer Assessment - Agent-Based Educational Content Generator

An Agentic system with two AI agents (Generator and Reviewer) that creates and evaluates educational content with a Streamlit UI.

## Deployed

[Genrev App](https://yuvrajds1-genrev-app-svl66e.streamlit.app/)

## Architecture

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

## Installation

## API Key Setup

You need an Anthropic API key to use this application:

1. Visit [console.groq.com](https://console.groq.com/keys)
2. Sign up or log in
3. Navigate to "API Keys"
4. Create a new API key
5. Copy the key (you'll enter it in the UI)

## Educational Topics You Can Try

- Mathematics: "Fractions", "Multiplication", "Geometry basics"
- Science: "Photosynthesis", "Water cycle", "Simple machines"
- Language: "Parts of speech", "Sentence structure"
- Social Studies: "Map reading", "Community helpers"
