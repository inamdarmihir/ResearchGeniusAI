import asyncio
import streamlit as st
from typing import Dict, Any
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import from our own modules
from utils.research_tools import deep_research_tool
from models.agents import create_research_agent, create_elaboration_agent
from utils.config import set_api_keys, get_openai_key, get_firecrawl_key

# Set page configuration with personalized branding
st.set_page_config(
    page_title="ResearchGenius AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #4F8BF9;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #6c757d;
        margin-bottom: 2rem;
    }
    .result-header {
        font-size: 1.8rem;
        color: #4F8BF9;
        margin: 1.5rem 0;
    }
    .footer {
        margin-top: 3rem;
        padding-top: 1rem;
        border-top: 1px solid #f0f0f0;
        color: #6c757d;
        font-size: 0.9rem;
    }
    .sidebar-header {
        font-size: 1.5rem;
        margin-bottom: 1.5rem;
    }
    .stButton>button {
        background-color: #4F8BF9;
        color: white;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for API keys
if "openai_api_key" not in st.session_state:
    st.session_state.openai_api_key = ""
if "firecrawl_api_key" not in st.session_state:
    st.session_state.firecrawl_api_key = ""
if "history" not in st.session_state:
    st.session_state.history = []

# Create sidebar for configuration
with st.sidebar:
    st.markdown("<div class='sidebar-header'>🔑 API Configuration</div>", unsafe_allow_html=True)
    
    openai_api_key = st.text_input(
        "OpenAI API Key", 
        value=st.session_state.openai_api_key,
        type="password",
        help="Your OpenAI API key for accessing GPT models"
    )
    
    firecrawl_api_key = st.text_input(
        "Firecrawl API Key", 
        value=st.session_state.firecrawl_api_key,
        type="password",
        help="Your Firecrawl API key for web research capabilities"
    )
    
    if openai_api_key:
        st.session_state.openai_api_key = openai_api_key
    if firecrawl_api_key:
        st.session_state.firecrawl_api_key = firecrawl_api_key
    
    set_api_keys(openai_api_key, firecrawl_api_key)
    
    st.markdown("---")
    st.markdown("<div class='sidebar-header'>⚙️ Research Settings</div>", unsafe_allow_html=True)
    
    max_depth = st.slider(
        "Research Depth", 
        min_value=1, 
        max_value=5, 
        value=3,
        help="Higher values enable deeper research but take longer"
    )
    
    time_limit = st.slider(
        "Time Limit (seconds)", 
        min_value=60, 
        max_value=300, 
        value=180,
        help="Maximum time to spend on research"
    )
    
    max_urls = st.slider(
        "Maximum Sources", 
        min_value=5, 
        max_value=20, 
        value=10,
        help="Maximum number of web sources to analyze"
    )
    
    st.markdown("---")
    
    if st.session_state.history:
        st.markdown("<div class='sidebar-header'>📚 Research History</div>", unsafe_allow_html=True)
        for idx, item in enumerate(st.session_state.history):
            if st.button(f"{item[:30]}...", key=f"history_{idx}"):
                st.session_state.selected_history = item

# Main content area
st.markdown("<h1 class='main-header'>🧠 ResearchGenius AI</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-header'>Your AI-powered research assistant for comprehensive, in-depth analysis</p>", unsafe_allow_html=True)

# Create tabs for different functions
tab1, tab2 = st.tabs(["Research", "About"])

with tab1:
    # Research topic input
    research_topic = st.text_input(
        "What would you like to research today?", 
        placeholder="e.g., Latest advancements in quantum computing",
        help="Enter any topic, question, or research area"
    )
    
    # Advanced options expander
    with st.expander("Advanced Options"):
        research_focus = st.selectbox(
            "Research Focus",
            options=["Comprehensive", "Technical", "Business Impact", "Future Trends", "Academic"],
            index=0,
            help="Select the primary focus of your research"
        )
        
        include_visuals = st.checkbox(
            "Suggest Visualizations", 
            value=True,
            help="Include suggestions for charts and visual elements"
        )
        
        citation_style = st.selectbox(
            "Citation Style",
            options=["APA", "MLA", "Chicago", "Harvard", "IEEE"],
            index=0,
            help="Select preferred citation style for references"
        )
    
    # Create a container for the research button
    button_col1, button_col2, button_col3 = st.columns([1, 2, 1])
    with button_col2:
        start_research = st.button(
            "🔍 Start Deep Research",
            use_container_width=True,
            disabled=not (get_openai_key() and get_firecrawl_key() and research_topic)
        )
    
    # Main research process
    if start_research:
        if not get_openai_key() or not get_firecrawl_key():
            st.warning("⚠️ Please enter both API keys in the sidebar.")
        elif not research_topic:
            st.warning("⚠️ Please enter a research topic.")
        else:
            try:
                # Save to history
                if research_topic not in st.session_state.history:
                    st.session_state.history.append(research_topic)
                
                # Create research agents
                research_agent = create_research_agent(deep_research_tool)
                elaboration_agent = create_elaboration_agent(focus=research_focus, visuals=include_visuals)
                
                # Progress indicators
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                # Phase 1: Initial Research
                status_text.text("📡 Phase 1/2: Gathering information from the web...")
                
                async def run_phase1():
                    result = await research_agent.run(
                        f"Research topic: {research_topic}. Parameters: max_depth={max_depth}, time_limit={time_limit}, max_urls={max_urls}"
                    )
                    return result.final_output
                
                initial_report = asyncio.run(run_phase1())
                progress_bar.progress(50)
                
                # Display initial report in an expander
                with st.expander("View Initial Research Report"):
                    st.markdown(initial_report)
                
                # Phase 2: Enhance and elaborate
                status_text.text("🧠 Phase 2/2: Enhancing research with deeper insights...")
                
                async def run_phase2():
                    elaboration_input = f"""
                    RESEARCH TOPIC: {research_topic}
                    RESEARCH FOCUS: {research_focus}
                    INCLUDE VISUALIZATIONS: {'Yes' if include_visuals else 'No'}
                    CITATION STYLE: {citation_style}
                    
                    INITIAL RESEARCH REPORT:
                    {initial_report}
                    
                    Please enhance this research report with additional information, examples, case studies, 
                    and deeper insights while maintaining academic rigor and factual accuracy.
                    """
                    
                    result = await elaboration_agent.run(elaboration_input)
                    return result.final_output
                
                enhanced_report = asyncio.run(run_phase2())
                progress_bar.progress(100)
                status_text.empty()
                
                # Display final enhanced report
                st.markdown("<h2 class='result-header'>📊 Enhanced Research Report</h2>", unsafe_allow_html=True)
                st.markdown(enhanced_report)
                
                # Download options
                col1, col2 = st.columns(2)
                with col1:
                    st.download_button(
                        "📥 Download as Markdown",
                        enhanced_report,
                        file_name=f"{research_topic.replace(' ', '_')}_report.md",
                        mime="text/markdown"
                    )
                with col2:
                    st.download_button(
                        "📄 Download as Text",
                        enhanced_report,
                        file_name=f"{research_topic.replace(' ', '_')}_report.txt",
                        mime="text/plain"
                    )
                
            except Exception as e:
                st.error(f"❌ An error occurred: {str(e)}")
                st.error("Please check your API keys and try again.")

with tab2:
    st.markdown("""
    ## About ResearchGenius AI
    
    ResearchGenius AI is a powerful research assistant that leverages the latest advancements in artificial intelligence 
    to provide comprehensive, in-depth research on any topic. This tool combines multiple specialized AI agents to deliver 
    research results that would normally take hours or even days to compile manually.
    
    ### How It Works
    
    1. **Research Agent**: Searches the web using Firecrawl's deep research capabilities, gathering information from 
       multiple sources and synthesizing the findings into an initial report.
       
    2. **Elaboration Agent**: Takes the initial report and enhances it with additional context, examples, case studies, 
       and practical implications, creating a comprehensive final report.
       
    3. **Multi-Agent Coordination**: The research process seamlessly coordinates between these specialized agents to 
       produce better results than a single agent could achieve alone.
    
    ### Features
    
    - **Deep Web Research**: Automatically searches multiple web sources and extracts relevant content
    - **Enhanced Analysis**: Provides detailed explanations, examples, and case studies
    - **Customizable Focus**: Tailor your research to technical, business, academic, or future-oriented perspectives
    - **Citation Support**: Includes proper citations in your preferred style
    - **Visualization Suggestions**: Recommends charts and visual elements to enhance understanding
    - **Downloadable Reports**: Export your research findings in multiple formats
    
    ### Privacy & Ethics
    
    This tool uses your own API keys and runs on your infrastructure. No research data is stored on our servers.
    All research is conducted ethically, with proper attribution to original sources.
    
    ### About the Creator
    
    ResearchGenius AI was created to democratize access to high-quality research capabilities. In a world where 
    premium research services can cost hundreds of dollars per month, this tool provides similar capabilities using 
    your own API keys at a fraction of the cost.
    """)

# Footer
st.markdown("<div class='footer'>© 2025 ResearchGenius AI. Built with OpenAI Agents SDK and Firecrawl.</div>", unsafe_allow_html=True) 