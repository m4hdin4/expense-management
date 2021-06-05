Get_Item_Schema = {
    "type": "object",
    "properties": {
        "spend_id": {"type": "string"},
    },
    "required": [
                   "spend_id",
                ]
}

Insert_Item_Schema = {
    "type": "object",
    "properties": {
        "product_name": {"type": "string"},
        "product_price": {"type": "number"},
        "category": {"type": "string"},
    },
    "required": [
                   "product_name",
                   "product_price",
                   "category",
                ]
}

Update_Item_Schema = {
    "type": "object",
    "properties": {
        "spend_id": {"type": "string"},
        "product_name": {"type": "string"},
        "product_price": {"type": "number"},
        "category": {"type": "string"},
    },
    "required": [
                   "spend_id",
                   "product_name",
                   "product_price",
                   "category",
                ]
}

Delete_Item_Schema = {
    "type": "object",
    "properties": {
        "spend_id": {"type": "string"},
    },
    "required": [
                   "spend_id",
                ]
}
