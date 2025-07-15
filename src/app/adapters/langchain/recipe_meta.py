from typing import List

from langchain.chains.query_constructor.schema import AttributeInfo


def get_metadata_field_info() -> List[AttributeInfo]:
     return [
        AttributeInfo(
            name="title",
            description="The name of the recipe",
            type="string",
        ),
        AttributeInfo(
            name="ingredients",
            description="List of ingredients required for the recipe",
            type="list[string]",
        ),
        AttributeInfo(
            name="instructions",
            description="Step-by-step cooking instructions for the recipe",
            type="string",
        ),
        AttributeInfo(
            name="cooking_time",
            description="Total cooking time in minutes",
            type="integer",
        ),
        AttributeInfo(
            name="difficulty",
            description="The difficulty level of the recipe. One of ['easy', 'medium', 'hard']",
            type="string",
        ),
        AttributeInfo(
            name="cuisine",
            description="The cuisine type of the recipe. One of ['italian', 'french']",
            type="string",
        ),
    ]

def get_document_content_description() -> str:
    return "A complete recipe including title, ingredients, cooking instructions, cooking time, difficulty, and cuisine type"
