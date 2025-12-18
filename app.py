import streamlit as st
import pandas as pd
import openai
import plotly.express as px

# 1. SETUP: High-end UI Config
st.set_page_config(page_title="Lumina AI Analytics", layout="wide")
st.title("✨ Lumina: Next-Gen AI Dashboards")

# 2. AUTH: Enter your OpenAI API Key
api_key = st.sidebar.text_input("Enter OpenAI API Key", type="password")

# 3. DATA IMPORT
uploaded_file = st.file_uploader("Upload your data (CSV or Excel)", type=["csv", "xlsx"])

if uploaded_file and api_key:
    df = pd.read_csv(uploaded_file)
    st.write("### Data Preview", df.head(3))
    
    # 4. THE AI INTERFACE
    user_query = st.text_input("Ask Lumina anything (e.g., 'Show me a bar chart of sales by region')")

    if user_query:
        openai.api_key = api_key
        
        # AI Prompting Logic
        prompt = f"""
        You are a data expert. Based on these columns: {df.columns.tolist()}, 
        tell me which Plotly Express function (bar, line, scatter, pie) and 
        which x and y columns I should use to answer: '{user_query}'.
        Return ONLY in this format: function|x_column|y_column
        """
        
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "system", "content": prompt}]
        )
        
        # 5. GENERATIVE VISUALIZATION
        try:
            ai_decision = response.choices[0].message.content.split("|")
            func, x_col, y_col = ai_decision[0].strip(), ai_decision[1].strip(), ai_decision[2].strip()
            
            st.write(f"🪄 Lumina suggests a **{func}** chart...")
            
            if func == "bar": fig = px.bar(df, x=x_col, y=y_col, template="plotly_dark")
            elif func == "line": fig = px.line(df, x=x_col, y=y_col, template="plotly_dark")
            elif func == "pie": fig = px.pie(df, names=x_col, values=y_col, template="plotly_dark")
            else: fig = px.scatter(df, x=x_col, y=y_col, template="plotly_dark")
            
            # Add flashy effects via Plotly Layout
            fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig, use_container_width=True)
            
        except Exception as e:
            st.error("AI is still learning this data. Try rephrasing your request!")
