# FastAPI Pagination

A simple example of implementing **pagination in FastAPI** using `page` and `limit` query parameters.

## 📌 How It Works

Pagination uses two parameters:

* `page` → specifies which page to retrieve
* `limit` → specifies how many items to return per page

Example:

```text
/news?page=2&limit=5
```

## 🔢 Pagination Logic

```python
start = (page - 1) * limit
end = start + limit

data = titles[start:end]
```

### Example

If:

```text
page = 2
limit = 5
```

Then:

```text
start = (2 - 1) * 5
      = 5

end = 5 + 5
    = 10
```

So items from index `5` to `9` are returned.

## 🚀 FastAPI Example

```python
from fastapi import FastAPI

app = FastAPI()

items = [
    "Item 1",
    "Item 2",
    "Item 3",
    "Item 4",
    "Item 5",
    "Item 6",
    "Item 7",
    "Item 8",
    "Item 9",
    "Item 10"
]


@app.get("/items")
def get_items(page: int = 1, limit: int = 5):

    start = (page - 1) * limit
    end = start + limit

    return {
        "page": page,
        "limit": limit,
        "total": len(items),
        "data": items[start:end]
    }
```

## 🔗 API Examples

### First Page

```text
/items?page=1&limit=5
```

### Second Page

```text
/items?page=2&limit=5
```

### Third Page

```text
/items?page=3&limit=5
```

## 📖 Key Concept

```python
start = (page - 1) * limit
end = start + limit
```

This calculates which portion of the list should be returned for the requested page.
