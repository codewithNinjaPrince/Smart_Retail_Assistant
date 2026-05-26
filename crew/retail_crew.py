import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process, LLM

load_dotenv(override=True)

# Kill wrong Azure values
for key in [
    "AZURE_API_BASE",
    "AZURE_OPENAI_ENDPOINT",
    "AZURE_ENDPOINT",
]:
    os.environ.pop(key, None)

# FORCE correct values
os.environ["AZURE_API_KEY"] = os.getenv("CREW_AZURE_OPENAI_KEY")
os.environ["AZURE_API_BASE"] = "https://smart-retail-openai-prince2201.openai.azure.com"
os.environ["AZURE_API_VERSION"] = "2025-01-01-preview"

print("FORCED:", os.environ["AZURE_API_BASE"])

llm = LLM(
    model="azure/gpt-4.1-retail"
)

retail_analyst = Agent(
    role="Retail Business Intelligence Analyst",

    goal="""
    Generate short, actionable retail insights
    for dashboards and executives.
    """,

    backstory="""
    You are a senior retail AI analyst.
    You create concise business summaries,
    identify trends, risks, and give
    executive recommendations.
    Never generate long reports.
    """,

    llm=llm,
    verbose=True
)



async def run_retail_crew(
    total_sales,
    monthly_growth,
    top_category
):

    analysis_task = Task(
        description=f"""
    You are an AI Retail Decision Assistant.

    Retail Data:
    - Total Sales: {total_sales}
    - Monthly Growth: {monthly_growth}%
    - Top Category: {top_category}
    
    Generate output ONLY in this exact structure:

    📊 Retail Summary
    - Sales Status:
    - Growth Status:
    - Top Category:

    📈 Key Insights
    - Insight 1
    - Insight 2
    - Insight 3

    ⚠ Risks
    - Risk 1
    - Risk 2

    🚀 Recommendations
    - Recommendation 1
    - Recommendation 2
    - Recommendation 3

    Rules:
    Use ONLY provided input
    Do NOT invent seasons, campaigns, customer behavior, or external factors
    keep under 150 words
    Short bullet points only
    Dashboard-style output
    """,
    expected_output="Concise retail business insights",
    agent=retail_analyst
   )

    crew = Crew(
        agents=[retail_analyst],
        tasks=[analysis_task],
        process=Process.sequential,
        verbose=True
    )

    result = await crew.kickoff_async()

    return str(result)