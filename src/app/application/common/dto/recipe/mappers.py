from src.app.application.common.dto.recipe.recipe import RecipeDto, RecipeResponse, RecipeUpdateDto
from src.app.application.models.recipe import Recipe


def to_recipe(request: RecipeDto) -> Recipe:
    return Recipe(
        title=request.title,
        ingredients=request.ingredients,
        instructions=request.instructions,
        cooking_time=request.cooking_time,
        difficulty=request.difficulty,
        cuisine=request.cuisine
    )

def update_from_request(source: RecipeUpdateDto, target: Recipe) -> None:
    update_data = source.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(target, field, value)

def to_response_dto(recipe: Recipe) -> RecipeResponse:
    return RecipeResponse(
        title=recipe.title,
        ingredients=recipe.ingredients,
        instructions=recipe.instructions,
        cooking_time=recipe.cooking_time,
        difficulty=recipe.difficulty,
        cuisine=recipe.cuisine
    )