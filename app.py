from dataclasses import dataclass

from litestar import Litestar, get, post
from litestar.exceptions import NotFoundException


@dataclass
class TodoItem:
    """Class for keeping track of an Todo item."""

    title: str
    done: bool


# Create a basic todo list
TODO_LIST: list[TodoItem] = [
    TodoItem(title="Start writing TOOD list", done=True),
    TodoItem(title="???", done=False),
    TodoItem(title="Profit", done=False),
]


def get_todo_by_title(title) -> TodoItem:
    """Get a todo from the list by its title"""
    # search the todo list for a todo with a matching title
    for todo in TODO_LIST:
        # return the
        if todo.title == title:
            return todo
    # Raise a not found exception if a todo wasn't returned
    raise NotFoundException(detail="Todo titled '{title}' not found")


@get("/")
async def hello_world() -> str:
    return "hello, world!"


@get("/list")
async def get_list(done: bool | None = None) -> list[TodoItem]:
    """Returns a list of Todo's"""

    # If no query parameter is provided, return all items
    if done is None:
        return TODO_LIST

    # If done query parameter is provided, return any items
    return [item for item in TODO_LIST if item.done == done]


@post("/{title:str}")
async def update_todo(title: str, data: TodoItem) -> list[TodoItem]:
    todo = get_todo_by_title(title=title)
    todo.title = data.title
    todo.done = data.done
    return TODO_LIST


@post("/add")
async def add_todo(data: TodoItem) -> list[TodoItem]:
    TODO_LIST.append(data)
    return TODO_LIST


# A Litestar() class is the entrypoint for everything
app = Litestar([hello_world, get_list, add_todo, update_todo])
