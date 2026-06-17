import streamlit as st
from google import genai
from prompt import zero_shot_prompt, few_shot_prompt, cot_prompt, judge_prompt
from dotenv import load_dotenv
import os
from pydantic import BaseModel


load_dotenv()
api_key = os.getenv("Gem_Api_Key")
client = genai.Client(api_key=api_key)

st.title("Prompt Score Studio")

class JudgeResult(BaseModel):
    zero_shot_score: int
    few_shot_score: int
    cot_score: int
    best_technique: str
    reasoning: str

task = st.text_input("Ask anything...:")
if st.button("Run comparison"):
    with st.spinner("🤖 Generating responses..."):
        resp1 = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=zero_shot_prompt(task)
        )
        resp2 = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=few_shot_prompt(task)
        )
        resp3 = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=cot_prompt(task)
        )
    with st.spinner("⚖️ Judging responses..."):
        judge_response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=judge_prompt(task, resp1.text, resp2.text, resp3.text),
        config={
            "response_mime_type": "application/json",
            "response_schema": JudgeResult,
        },
        )
    if judge_response.parsed is None:
       st.error("UNEXPECTED ERROR OCCURED JUDGMENT COUDN'T BE PASSED")
       st.write(judge_response.text)
       st.stop()

    result = judge_response.parsed
 
    col1, col2, col3 = st.columns([1,1,1.1])
    
    with col1:
        st.subheader("Zero-shot")
        with st.container(height=300):
            st.write(resp1.text)
        st.metric("Score", f"{result.zero_shot_score}/100")
        st.progress(result.zero_shot_score / 100)
    
    with col2:
        st.subheader("Few-shot")
        with st.container(height=300):
            st.write(resp2.text)
        st.metric("Score", f"{result.few_shot_score}/100")
        st.progress(result.few_shot_score / 100)

    with col3:
        st.subheader("Chain-of-Thought")
        with st.container(height=300):
            st.write(resp3.text)
        st.metric("Score", f"{result.cot_score}/100")
        st.progress(result.cot_score / 100)
    

    st.divider()
    st.success(f"🏆 Best technique: {result.best_technique} — REASON BEHIND THE CHOICE: {result.reasoning}")
