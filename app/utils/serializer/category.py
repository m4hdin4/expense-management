Get_Category_Schema = {
    "type": "object",
    "properties": {
        "category": {"type": "string"},
        "page_size": {"type": "number"},
        "page_num": {"type": "number"},
    },
    "required": [
                   "category",
                ]
}

Update_Category_Schema = {
    "type": "object",
    "properties" : {
        "old_category": {"type" : "string"},
        "new_category": {"type" : "string"},
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
