from agents import build_reader_agent,build_search_agent,writer_chain,critic_chain
from rich import print
from langchain_core.messages import ToolMessage

def extract_search_results(search_result):
    for msg in search_result["messages"]:
        if isinstance(msg, ToolMessage):
            return msg.content
        
    return "No search results found."

def run_research_pipeline(topic : str)->dict:
    state = {}

    #search agent working 
    print("\n"+ " ="*50)
    print("step 1 - search agent is working ")
    print("\n"+ " ="*50)

    search_agent = build_search_agent()
    search_result = search_agent.invoke({
        "messages":[
            ("user",f"Find recent, reliable and detailed information about : {topic}")
        ]
    })

    state["search_results"]=extract_search_results(search_result)
    
    print("\n"+ " ="*50)
    print("\n search result ",state['search_results'])
    print("\n"+ " ="*50)

    #reader agent working 
    print("\n"+ " ="*50)
    print("step 2 - reader agent is scraping.... ")
    print("\n"+ " ="*50)

    reader_agent = build_reader_agent()

    reader_results = reader_agent.invoke({
        "messages": [("user",
            f"Based on the following search results about '{topic}', "
            f"pick the most relevant URL and scrape it for deeper content.\n\n"
            f"Search Results:\n{state['search_results']}"
        )]
    })

    state["reader_results"]=reader_results["messages"][-1]

    print("\n"+ " ="*50)
    print("\n reader result ",state['reader_results'])
    print("\n"+ " ="*50)

    #step 3 writer chain 
    print("\n"+ " ="*50)
    print("step 3 - writer agent is drafting.... ")
    print("\n"+ " ="*50)

    research_combined = (
        f"SEARCH RESULT : \n {state['search_results']} \n\n"
        f"DETAILED SCRAPED CONTENT : \n {state['reader_results']}" 
    )

    state["report"]=writer_chain.invoke({
        "topic" : topic,
        "research":research_combined
    })

    print("\n"+ " ="*50)
    print("Final Report \n",state["report"])
    print("\n"+ " ="*50)


    #step 4 critic chain 
    print("\n"+ " ="*50)
    print("step 3 - critic agent is working.... ")
    print("\n"+ " ="*50)

    state["critic"]=critic_chain.invoke({
        "report":state["report"]
    })

    print("\n"+ " ="*50)
    print("Critic Report \n",state["critic"])
    print("\n"+ " ="*50)


    return state


if __name__ == "__main__":
    topic = input("\n Enter research Topic : ")
    run_research_pipeline(topic=topic)