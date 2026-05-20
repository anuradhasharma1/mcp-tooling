from pydantic import Field
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("DocumentMCP", log_level="ERROR")


docs = {
    "deposition.md": "This deposition covers the testimony of Angela Smith, P.E.",
    "report.pdf": "The report details the state of a 20m condenser tower.",
    "financials.docx": "These financials outline the project's budget and expenditures.",
    "outlook.pdf": "This document presents the projected future performance of the system.",
    "plan.md": "The plan outlines the steps for the project's implementation.",
    "spec.txt": "These specifications define the technical requirements for the equipment.",
}


@mcp.tool(
    name = "read_doc_contents",
    description="read the content of documents and return it as a string ."
)
def read_document (
    doc_id: str = Field(description = "Id of a document to read")
):
    if doc_id not in docs:
        raise ValueError(f"Doc with {doc_id} not found")
    
    return docs[doc_id]

@mcp.tool(
    name = "edit_a_document",
    description="Edit a document by replacing a string in document with a new string"
)
def edit_document(
    doc_id: str = Field(description = "Id of a document to edit"),
    old_str:str=Field(description= "The text to replace . Must Watch exactly ,including Whitespace "),
    new_str:str=Field(description="The new text to be insert in place of the old text ")
):
    if doc_id not in docs:
        raise ValueError(f"Doc with {doc_id} not found")
    
    docs[doc_id] = docs[doc_id].replace(old_str, new_str)
# TODO: Write a resource to return all doc id's
# TODO: Write a resource to return the contents of a particular doc
# TODO: Write a prompt to rewrite a doc in markdown format
# TODO: Write a prompt to summarize a doc


if __name__ == "__main__":
    mcp.run(transport="stdio")
