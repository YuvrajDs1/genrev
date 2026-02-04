import streamlit as st
import json
from agent_system import AgentPipeline
import os

st.set_page_config(
    page_title="AI Educational Content Generator",
    page_icon="🎓",
    layout="wide"
)

st.markdown("""
<style>
    .stAlert {
        padding: 1rem;
        border-radius: 0.5rem;
    }
    .agent-box {
        border: 2px solid #e0e0e0;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
        background-color: #f8f9fa;
    }
    .pass-status {
        color: #28a745;
        font-weight: bold;
        font-size: 1.2em;
    }
    .fail-status {
        color: #dc3545;
        font-weight: bold;
        font-size: 1.2em;
    }
    .mcq-box {
        background-color: #ffffff;
        border-left: 4px solid #007bff;
        padding: 15px;
        margin: 10px 0;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

st.title("🎓 AI Educational Content Generator")
st.markdown("""
This system uses **two AI agents** to create and review educational content:
- **Generator Agent**: Creates age-appropriate explanations and quiz questions
- **Reviewer Agent**: Evaluates content quality and provides feedback
""")

st.sidebar.header("📝 Content Configuration")

api_key = st.sidebar.text_input(
    "Groq API Key",
    type="password",
    help="Enter your Groq API key to start chat"
)

if api_key:
    os.environ['GROQ_API_KEY'] = api_key

grade = st.sidebar.number_input(
    "Grade Level",
    min_value=1,
    max_value=12,
    value=4,
    help="Select the grade level for the content"
)

topic = st.sidebar.text_input(
    "Topic",
    value="Types of angles",
    help="Enter the educational topic"
)

generate_button = st.sidebar.button("🚀 Generate Content", type="primary", use_container_width=True)

st.sidebar.markdown("---")
st.sidebar.markdown("### 💡 Example Topics")
st.sidebar.markdown("""
- The water cycle (Grade 3)
- Types of angles (Grade 4)
- Simple machines (Grade 4)
- Photosynthesis (Grade 5)
- Fractions and decimals (Grade 6)
""")

if not api_key:
    st.info("👈 Please enter your Groq API key in the sidebar to get started.")
    st.markdown("""
    ### How to get an API key:
    1. Visit [console.groq.com](https://console.groq.com/keys)
    2. Sign up or log in
    3. Navigate to API Keys
    4. Create a new key and paste it in the sidebar
    """)
else:
    if generate_button:
        if not topic.strip():
            st.error("Please enter a topic!")
        else:
            with st.spinner("Initializing AI agents..."):
                pipeline = AgentPipeline()
            
            st.markdown("## 🔄 Agent Pipeline Flow")
            
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            try:
                status_text.text("🤖 Generator Agent working...")
                progress_bar.progress(33)
                
                results = pipeline.run(grade=grade, topic=topic)
                
                status_text.text("🔍 Reviewer Agent evaluating...")
                progress_bar.progress(66)
                
                status_text.text("✅ Pipeline complete!")
                progress_bar.progress(100)
                
                st.markdown("---")
                
                st.markdown("### 1️⃣ Generator Agent Output")
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown("#### 📖 Explanation")
                    st.info(results["initial_generation"]["explanation"])
                
                with col2:
                    st.markdown("#### 📊 Content Stats")
                    st.metric("Grade Level", grade)
                    st.metric("MCQs Generated", len(results["initial_generation"]["mcqs"]))
                
                st.markdown("#### ❓ Multiple Choice Questions")
                for idx, mcq in enumerate(results["initial_generation"]["mcqs"], 1):
                    with st.expander(f"Question {idx}: {mcq['question']}", expanded=True):
                        for option in mcq['options']:
                            if option == mcq['answer']:
                                st.success(f"✓ {option} (Correct Answer)")
                            else:
                                st.write(f"○ {option}")
                
                st.markdown("---")
                
                st.markdown("### 2️⃣ Reviewer Agent Evaluation")
                
                review_status = results["initial_review"]["status"]
                if review_status == "pass":
                    st.success("✅ **Status: PASS** - Content meets quality standards!")
                else:
                    st.warning("⚠️ **Status: FAIL** - Content needs improvement")
                
                if results["initial_review"]["feedback"]:
                    st.markdown("#### 💬 Reviewer Feedback")
                    for feedback_item in results["initial_review"]["feedback"]:
                        st.markdown(f"- {feedback_item}")
                else:
                    st.info("No feedback - content is excellent!")
                
                st.markdown("---")
                
                if results["refinement"]:
                    st.markdown("### 3️⃣ Refinement Process")
                    st.info("The Generator Agent has refined the content based on reviewer feedback.")
                    
                    st.markdown("#### 📝 Feedback Addressed:")
                    for item in results["refinement"]["feedback_addressed"]:
                        st.markdown(f"- {item}")
                    
                    st.markdown("#### 📖 Refined Explanation")
                    st.success(results["refinement"]["content"]["explanation"])
                    
                    st.markdown("#### ❓ Refined Questions")
                    for idx, mcq in enumerate(results["refinement"]["content"]["mcqs"], 1):
                        with st.expander(f"Question {idx}: {mcq['question']}", expanded=False):
                            for option in mcq['options']:
                                if option == mcq['answer']:
                                    st.success(f"✓ {option} (Correct Answer)")
                                else:
                                    st.write(f"○ {option}")
                    
                    st.markdown("---")
                
                st.markdown("### 🎯 Final Approved Content")
                
                final = results["final_output"]
                
                st.markdown("#### 📖 Explanation")
                st.success(final["explanation"])
                
                st.markdown("#### ❓ Quiz Questions")
                for idx, mcq in enumerate(final["mcqs"], 1):
                    with st.expander(f"**Question {idx}**: {mcq['question']}", expanded=True):
                        cols = st.columns(2)
                        for i, option in enumerate(mcq['options']):
                            col = cols[i % 2]
                            if option == mcq['answer']:
                                col.success(f"✓ **{option}** ← Correct")
                            else:
                                col.write(f"○ {option}")
                
                st.markdown("---")
                st.markdown("### 💾 Export Results")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    final_json = json.dumps(results["final_output"], indent=2)
                    st.download_button(
                        label="📥 Download Final Content (JSON)",
                        data=final_json,
                        file_name=f"content_grade{grade}_{topic.replace(' ', '_')}.json",
                        mime="application/json"
                    )
                
                with col2:
                    complete_json = json.dumps(results, indent=2)
                    st.download_button(
                        label="📥 Download Complete Pipeline Results",
                        data=complete_json,
                        file_name=f"pipeline_results_grade{grade}_{topic.replace(' ', '_')}.json",
                        mime="application/json"
                    )
                
            except Exception as e:
                st.error(f"❌ An error occurred: {str(e)}")
                st.exception(e)
    
    else:
        st.info("👈 Configure your settings in the sidebar and click **Generate Content** to start!")
        
        st.markdown("### 🔄 How It Works")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            #### 1️⃣ Generator Agent
            - Creates educational content
            - Generates explanations
            - Produces MCQs
            - Adapts to grade level
            """)
        
        with col2:
            st.markdown("""
            #### 2️⃣ Reviewer Agent
            - Evaluates content quality
            - Checks age-appropriateness
            - Verifies correctness
            - Provides specific feedback
            """)
        
        with col3:
            st.markdown("""
            #### 3️⃣ Refinement
            - Addresses feedback
            - Improves content
            - Re-evaluates quality
            - Produces final output
            """)
