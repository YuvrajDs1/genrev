from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field
from typing import List, Literal
import json
import os

class MCQ(BaseModel):
    """Multiple Choice Question model"""
    question: str = Field(description="The question text")
    options: List[str] = Field(description="Four answer options")
    answer: str = Field(description="The correct answer")


class GeneratorOutput(BaseModel):
    """Generator Agent output structure"""
    explanation: str = Field(description="Educational explanation of the topic")
    mcqs: List[MCQ] = Field(description="List of multiple choice questions")


class ReviewerOutput(BaseModel):
    """Reviewer Agent output structure"""
    status: Literal["pass", "fail"] = Field(description="Pass or fail status")
    feedback: List[str] = Field(description="List of specific feedback items")


class GeneratorAgent:
    """
    Generator Agent: Creates educational content for a given grade and topic
    """
    
    def __init__(self):
        """Initialize the Generator Agent with LangChain components"""
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY environment variable is not set")
            
        self.llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0.7
        )
        
        self.parser = JsonOutputParser(pydantic_object=GeneratorOutput)
        
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert educational content creator. 
Generate age-appropriate educational content including an explanation and multiple choice questions.

{format_instructions}

IMPORTANT: Your output must be valid JSON matching the exact structure specified."""),
            ("user", """Create educational content for:
Grade: {grade}
Topic: {topic}

{feedback_section}

Requirements:
- Language must be appropriate for grade {grade} students
- Explanation should be clear, engaging, and accurate
- Create exactly 4 multiple choice questions
- Each MCQ must have 4 options
- Ensure concepts are introduced before being tested

Return ONLY valid JSON, no markdown formatting or code blocks.""")
        ])
        
        self.chain = self.prompt | self.llm | self.parser
    
    def generate(self, grade: int, topic: str, feedback: List[str] = None) -> dict:
        """
        Generate educational content
        
        Args:
            grade: Grade level (e.g., 4)
            topic: Educational topic (e.g., "Types of angles")
            feedback: Optional feedback from reviewer for refinement
            
        Returns:
            Structured output with explanation and MCQs
        """
        feedback_section = ""
        if feedback:
            feedback_section = f"""
FEEDBACK FROM REVIEWER (Address these issues):
{chr(10).join(f"- {item}" for item in feedback)}
"""
        
        result = self.chain.invoke({
            "grade": grade,
            "topic": topic,
            "feedback_section": feedback_section,
            "format_instructions": self.parser.get_format_instructions()
        })
        
        return result


class ReviewerAgent:
    """
    Reviewer Agent: Evaluates educational content quality
    """
    
    def __init__(self):
        """Initialize the Reviewer Agent with LangChain components"""
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY environment variable is not set")
            
        self.llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0.3 
        )
        
        self.parser = JsonOutputParser(pydantic_object=ReviewerOutput)
        
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert educational content reviewer.
Evaluate educational content for age-appropriateness, conceptual correctness, and clarity.

{format_instructions}

IMPORTANT: Your output must be valid JSON matching the exact structure specified."""),
            ("user", """Review this educational content:

Grade Level: {grade}
Topic: {topic}

Content to Review:
{content}

Evaluation Criteria:
1. Age Appropriateness: Is the language suitable for grade {grade}?
2. Conceptual Correctness: Are all concepts accurate?
3. Clarity: Is the explanation clear and well-structured?
4. Question Quality: Do MCQs test introduced concepts appropriately?

Provide specific, actionable feedback. Set status to "fail" if there are issues that need fixing.

Return ONLY valid JSON, no markdown formatting or code blocks.""")
        ])
        
        self.chain = self.prompt | self.llm | self.parser
    
    def review(self, grade: int, topic: str, content: dict) -> dict:
        """
        Review educational content
        
        Args:
            grade: Grade level
            topic: Educational topic
            content: Generated content to review
            
        Returns:
            Structured review with status and feedback
        """
        result = self.chain.invoke({
            "grade": grade,
            "topic": topic,
            "content": json.dumps(content, indent=2),
            "format_instructions": self.parser.get_format_instructions()
        })
        
        return result


class AgentPipeline:
    """
    Orchestrates the Generator and Reviewer agents with refinement logic
    """
    
    def __init__(self):
        """Initialize the pipeline with both agents"""
        self.generator = GeneratorAgent()
        self.reviewer = ReviewerAgent()
    
    def run(self, grade: int, topic: str) -> dict:
        """
        Run the complete agent pipeline
        
        Args:
            grade: Grade level
            topic: Educational topic
            
        Returns:
            Complete results including all agent outputs
        """
        results = {
            "input": {"grade": grade, "topic": topic},
            "initial_generation": None,
            "initial_review": None,
            "refinement": None,
            "final_output": None
        }
        
        print(f"🤖 Generator Agent: Creating content for Grade {grade} - {topic}")
        initial_content = self.generator.generate(grade, topic)
        results["initial_generation"] = initial_content
        
        print("🔍 Reviewer Agent: Evaluating content...")
        review = self.reviewer.review(grade, topic, initial_content)
        results["initial_review"] = review
        

        if review["status"] == "fail":
            print("⚠️  Review failed. Refining content...")
            refined_content = self.generator.generate(
                grade, 
                topic, 
                feedback=review["feedback"]
            )
            results["refinement"] = {
                "content": refined_content,
                "feedback_addressed": review["feedback"]
            }
            results["final_output"] = refined_content
        else:
            print("✅ Review passed!")
            results["final_output"] = initial_content
        
        return results


if __name__ == "__main__":
    pipeline = AgentPipeline()
    
    result = pipeline.run(
        grade=4,
        topic="Types of angles"
    )
    
    print("\n" + "="*60)
    print("FINAL RESULTS")
    print("="*60)
    print(json.dumps(result, indent=2))
