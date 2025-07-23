"""RAG search tool using OpenAI Vector Store."""

from pathlib import Path

from langchain_core.tools import StructuredTool
from openai import OpenAI
from pydantic import BaseModel, Field


class OfficialDocsInput(BaseModel):
    """Input schema for RAG search tool."""

    query: str = Field(description="The search query to find relevant documentation")
    country: str | None = Field(
        default="es", description="Country filter for the search (for now only 'es' for Spain)"
    )
    subject: str | None = Field(
        default="verifactu",
        description="""Subject filter for the search
('regulation' for general regulations or 'verifactu' for VeriFactu-specific docs)""",
    )


class OfficialDocsTool:
    """RAG search tool using OpenAI Vector Store."""

    def __init__(self, vector_store_id: str, max_results: int = 10):
        """Initialize the RAG search tool."""
        self.client = OpenAI()
        self.vector_store_id = vector_store_id
        self.max_results = max_results

        prompts_dir = Path(__file__).parent / "prompts"

        with open(prompts_dir / "official_docs_description.md") as f:
            self.official_docs_description = f.read().strip()

    def search(self, query: str, country: str = "es", subject: str = "verifactu") -> str:
        """
        Search the vector store for relevant documents with filters.
        Args:
            query: The search query
            country: Country filter (default: "es")
            subject: Subject filter (default: "verifactu")
        Returns:
            Formatted string with search results
        """
        try:
            # Build filters based on parameters
            filters = {"type": "and", "filters": []}

            # Add country filter
            if country:
                filters["filters"].append({"type": "eq", "key": "country", "value": country})

            # Add subject filter
            if subject:
                filters["filters"].append({"type": "eq", "key": "subject", "value": subject})

            # Use OpenAI client with built-in filter support
            results = self.client.vector_stores.search(
                vector_store_id=self.vector_store_id,
                query=query,
                filters=filters if filters["filters"] else None,
            )

            # Convert to dict for easier handling
            results_dict = results.model_dump()

            if not results_dict.get("data"):
                return f"""No relevant documents found for 
your query with filters (country: {country}, subject: {subject})."""

            # Format the results
            formatted_results = []
            for i, result in enumerate(results_dict["data"][: self.max_results], 1):
                content_texts = []
                if result.get("content"):
                    for content in result["content"]:
                        if content.get("text"):
                            content_texts.append(content["text"])

                # Get attributes for context
                attributes = result.get("attributes", {})
                attr_info = []
                if attributes.get("subject"):
                    attr_info.append(f"Subject: {attributes['subject']}")
                if attributes.get("type"):
                    attr_info.append(f"Type: {attributes['type']}")
                if attributes.get("country"):
                    attr_info.append(f"Country: {attributes['country']}")
                if attributes.get("format"):
                    attr_info.append(f"Format: {attributes['format']}")
                if attributes.get("url"):
                    attr_info.append(f"Source: {attributes['url']}")

                attr_str = f" ({', '.join(attr_info)})" if attr_info else ""

                result_text = "\n".join(content_texts) if content_texts else "No content available"
                formatted_results.append(f"## Result {i}{attr_str}\n\n{result_text}")

            # Add filter info to the response
            filter_info = f"**Filtered by:** Country='{country}', Subject='{subject}'\n\n"

            return filter_info + "\n\n---\n\n".join(formatted_results)

        except Exception as e:
            return f"Error performing search: {str(e)}"

    def get_tool(self) -> StructuredTool:
        """Get the LangChain tool for this RAG search."""
        return StructuredTool.from_function(
            func=self.search,
            name="search_official",
            description=self.official_docs_description,
            args_schema=OfficialDocsInput,
        )
