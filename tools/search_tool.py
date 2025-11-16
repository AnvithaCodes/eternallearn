"""Google Search Tool"""

class SearchTool:
    """Wrapper for Google Search"""
    
    def __init__(self):
        self.name = "google_search"
    
    async def search(self, query: str, num_results: int = 3):
        """Search Google (simulated for demo)"""
        print(f"Searching: {query}")
        
        # simulated results for demo purpose
        return [
            {
                "title": f"Understanding {query}",
                "snippet": f"Comprehensive guide to {query}...",
                "url": f"https://example.com/{query.replace(' ', '-')}"
            }
        ]
    
    def format_results_for_context(self, results) -> str:
        """Format search results"""
        if not results:
            return "No results found."
        
        formatted = "Search Results:\n\n"
        for i, result in enumerate(results, 1):
            formatted += f"{i}. {result['title']}\n"
            formatted += f"   {result['snippet']}\n\n"
        return formatted

search_tool = SearchTool()