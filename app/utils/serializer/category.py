Get_Category_Schema = {
    "type": "object",
    "properties": {
        "category": {"type": "string"},
        "page_size": {"type": "string", "pattern": "^[0-9]*$"},
        "page_num": {"type": "string", "pattern": "^[0-9]*$"},
    },
    "required": [
                   "category",
                ]
}

Update_Category_Schema = {
    "type": "object",
    "properties": {
        "old_category": {"type": "string"},
        "new_category": {"type": "string"},
    },
    "required": [
                   "old_category",
                   "new_category",
                ]
}

Delete_Category_Schema = {
    "type": "object",
    "properties": {
        "category": {"type": "string"},
    },
    "required": [
                   "category",
                ]
}

Insert_Category_Schema = {
    "type": "object",
    "properties": {
        "category": {"type": "string"},
    },
    "required": [
                   "category",
                ]
}
