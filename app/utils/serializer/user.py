Identification_Schema = {
    "type": "object",
    "properties": {
        "username": {"type": "string"},
        "password": {"type": "string"},
    },
    "required": [
                   "username",
                   "password",
                ]
}

Password_Change_Schema = {
    "type": "object",
    "properties": {
        "old_password": {"type": "string"},
        "new_password": {"type": "string"},
    },
    "required": [
                   "old_password",
                   "new_password",
                ]
}

Check_Password_Schema = {
    "type": "object",
    "properties": {
        "password": {"type": "string"},
    },
    "required": [
                   "password",
                ]
}

Get_items = {
    "type": "object",
    "properties": {
        "page_size": {"type": "number"},
        "page_num": {"type": "number"},
    },
}
