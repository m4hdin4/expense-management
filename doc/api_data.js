define({ "api": [
  {
    "type": "DELETE",
    "url": "/category",
    "title": "delete category",
    "name": "delete_category",
    "group": "category",
    "header": {
      "fields": {
        "Header": [
          {
            "group": "Header",
            "type": "String",
            "optional": false,
            "field": "token",
            "description": "<ul> <li>a unique session id that is valid for each login for 3 hours</li> </ul>"
          }
        ]
      }
    },
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "category",
            "description": ""
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "returns",
            "description": "<p>json contains a message</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Success-Response:",
          "content": "HTTP/1.1 200 OK\n    {\n        \"message\": \"DELETED\"\n    }",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "app/controllers/Category/category.py",
    "groupTitle": "category"
  },
  {
    "type": "GET",
    "url": "/user",
    "title": "get category",
    "name": "get_category",
    "group": "category",
    "header": {
      "fields": {
        "Header": [
          {
            "group": "Header",
            "type": "String",
            "optional": false,
            "field": "token",
            "description": "<ul> <li>a unique session id that is valid for each login for 3 hours</li> </ul>"
          }
        ]
      }
    },
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "category",
            "description": ""
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "page_size",
            "description": "<p>string of numbers to show how much item should be per page</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "page_num",
            "description": "<p>string of numbers to show which page you want</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "returns",
            "description": "<p>query objects if exists</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Success-Response:",
          "content": "HTTP/1.1 200 OK\n{\n    \"list\":\n    [\n        {\n            \"id\": \"60b4c7a37ba96ba33ab0d977\",\n            \"username\": \"m4hdin4\",\n            \"product_name\": \"test1\",\n            \"category\": \"test_category\",\n            \"product_price\": 10000,\n            \"date\": \"2021-05-31 15:54:45.024000\"\n        },\n        {\n            \"id\": \"60b4c7da7ba96ba33ab0d978\",\n            \"username\": \"m4hdin4\",\n            \"product_name\": \"test1\",\n            \"category\": \"test_category\",\n            \"product_price\": 10000,\n            \"date\": \"2021-05-31 15:54:45.024000\"\n        }\n    ],\n    \"sum\": 20000\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "app/controllers/Category/category.py",
    "groupTitle": "category"
  },
  {
    "type": "POST",
    "url": "/category",
    "title": "insert category",
    "name": "insert_category",
    "group": "category",
    "header": {
      "fields": {
        "Header": [
          {
            "group": "Header",
            "type": "String",
            "optional": false,
            "field": "token",
            "description": "<ul> <li>a unique session id that is valid for each login for 3 hours</li> </ul>"
          }
        ]
      }
    },
    "body": [
      {
        "group": "Body",
        "type": "String",
        "optional": false,
        "field": "category",
        "description": ""
      }
    ],
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "returns",
            "description": "<p>json contains category name</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Success-Response:",
          "content": "HTTP/1.1 201 CREATED\n    {\n        \"category\": \"test_category1\",\n        \"message\": \"category added\"\n    }",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "app/controllers/Category/category.py",
    "groupTitle": "category"
  },
  {
    "type": "PUT",
    "url": "/category",
    "title": "update category",
    "name": "update_category",
    "group": "category",
    "header": {
      "fields": {
        "Header": [
          {
            "group": "Header",
            "type": "String",
            "optional": false,
            "field": "token",
            "description": "<ul> <li>a unique session id that is valid for each login for 3 hours</li> </ul>"
          }
        ]
      }
    },
    "body": [
      {
        "group": "Body",
        "type": "String",
        "optional": false,
        "field": "new_category",
        "description": ""
      },
      {
        "group": "Body",
        "type": "String",
        "optional": false,
        "field": "old_category",
        "description": ""
      }
    ],
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "returns",
            "description": "<p>json contains updated category name</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Success-Response:",
          "content": "HTTP/1.1 200 OK\n    {\n        \"category_name\": \"updated_category\"\n    }",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "app/controllers/Category/category.py",
    "groupTitle": "category"
  },
  {
    "type": "DELETE",
    "url": "/item",
    "title": "delete item",
    "name": "delete",
    "group": "item",
    "header": {
      "fields": {
        "Header": [
          {
            "group": "Header",
            "type": "String",
            "optional": false,
            "field": "token",
            "description": "<ul> <li>a unique session id that is valid for each login for 3 hours</li> </ul>"
          }
        ]
      }
    },
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "spend_id",
            "description": ""
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "returns",
            "description": "<p>json contains a message</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Success-Response:",
          "content": "HTTP/1.1 200 OK\n    {\n        \"message\": \"DELETED\"\n    }",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "app/controllers/Item/item.py",
    "groupTitle": "item"
  },
  {
    "type": "GET",
    "url": "/item",
    "title": "get item",
    "name": "get_one",
    "group": "item",
    "header": {
      "fields": {
        "Header": [
          {
            "group": "Header",
            "type": "String",
            "optional": false,
            "field": "token",
            "description": "<ul> <li>a unique session id that is valid for each login for 3 hours</li> </ul>"
          }
        ]
      }
    },
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "spend_id",
            "description": ""
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "returns",
            "description": "<p>the query object if exists</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Success-Response:",
          "content": "HTTP/1.1 200 OK\n{\n    \"list\":\n    [\n        {\n            \"id\": \"60b4c7a37ba96ba33ab0d977\",\n            \"username\": \"m4hdin4\",\n            \"product_name\": \"test1\",\n            \"category\": \"test_category\",\n            \"product_price\": 10000,\n            \"date\": \"2021-05-31 15:54:45.024000\"\n        }\n    ],\n    \"sum\": 10000\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "app/controllers/Item/item.py",
    "groupTitle": "item"
  },
  {
    "type": "POST",
    "url": "/item",
    "title": "insert item",
    "name": "insert",
    "group": "item",
    "header": {
      "fields": {
        "Header": [
          {
            "group": "Header",
            "type": "String",
            "optional": false,
            "field": "token",
            "description": "<ul> <li>a unique session id that is valid for each login for 3 hours</li> </ul>"
          }
        ]
      }
    },
    "body": [
      {
        "group": "Body",
        "type": "String",
        "optional": false,
        "field": "product_name",
        "description": ""
      },
      {
        "group": "Body",
        "type": "Number",
        "optional": false,
        "field": "product_price",
        "description": ""
      },
      {
        "group": "Body",
        "type": "String",
        "optional": false,
        "field": "category",
        "description": ""
      }
    ],
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "returns",
            "description": "<p>json contains inserted object id</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Success-Response:",
          "content": "HTTP/1.1 201 CREATED\n    {\n        \"spend_id\": \"60b4c7da7ba96ba33ab0d978\",\n        \"message\": \"item added\"\n    }",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "app/controllers/Item/item.py",
    "groupTitle": "item"
  },
  {
    "type": "PUT",
    "url": "/item",
    "title": "update item",
    "name": "update",
    "group": "item",
    "header": {
      "fields": {
        "Header": [
          {
            "group": "Header",
            "type": "String",
            "optional": false,
            "field": "token",
            "description": "<ul> <li>a unique session id that is valid for each login for 3 hours</li> </ul>"
          }
        ]
      }
    },
    "body": [
      {
        "group": "Body",
        "type": "String",
        "optional": false,
        "field": "product_name",
        "description": ""
      },
      {
        "group": "Body",
        "type": "Number",
        "optional": false,
        "field": "product_price",
        "description": ""
      },
      {
        "group": "Body",
        "type": "String",
        "optional": false,
        "field": "category",
        "description": ""
      },
      {
        "group": "Body",
        "type": "String",
        "optional": false,
        "field": "spend_id",
        "description": ""
      }
    ],
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "returns",
            "description": "<p>json contains updated object id</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Success-Response:",
          "content": "HTTP/1.1 200 OK\n    {\n        \"spend_id\": \"60b4c7da7ba96ba33ab0d978\",\n        \"message\": \"item updated\"\n    }",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "app/controllers/Item/item.py",
    "groupTitle": "item"
  },
  {
    "type": "DELETE",
    "url": "/user",
    "title": "delete account",
    "name": "delete_account",
    "group": "user",
    "header": {
      "fields": {
        "Header": [
          {
            "group": "Header",
            "type": "String",
            "optional": false,
            "field": "token",
            "description": "<ul> <li>a unique session id that is valid for each login for 3 hours</li> </ul>"
          }
        ]
      }
    },
    "body": [
      {
        "group": "Body",
        "type": "String",
        "optional": false,
        "field": "password",
        "description": ""
      }
    ],
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "returns",
            "description": "<p>json contains a message</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Success-Response:",
          "content": "HTTP/1.1 200 OK\n    {\n        \"message\": \"DELETED\"\n    }",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "app/controllers/User/user.py",
    "groupTitle": "user"
  },
  {
    "type": "GET",
    "url": "/user/user_items",
    "title": "get user list",
    "name": "get_list",
    "group": "user",
    "header": {
      "fields": {
        "Header": [
          {
            "group": "Header",
            "type": "String",
            "optional": false,
            "field": "token",
            "description": "<ul> <li>a unique session id that is valid for each login for 3 hours</li> </ul>"
          }
        ]
      }
    },
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "page_size",
            "description": "<p>string of numbers to show how much item should be per page</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "page_num",
            "description": "<p>string of numbers to show which page you want</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "returns",
            "description": "<p>query objects if exists</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Success-Response:",
          "content": "HTTP/1.1 200 OK\n{\n    \"list\":\n    [\n        {\n            \"id\": \"60b4c7a37ba96ba33ab0d977\",\n            \"username\": \"m4hdin4\",\n            \"product_name\": \"test1\",\n            \"category\": \"test_category\",\n            \"product_price\": 10000,\n            \"date\": \"2021-05-31 15:54:45.024000\"\n        },\n        {\n            \"id\": \"60b4c7da7ba96ba33ab0d978\",\n            \"username\": \"m4hdin4\",\n            \"product_name\": \"test1\",\n            \"category\": \"test_category\",\n            \"product_price\": 10000,\n            \"date\": \"2021-05-31 15:54:45.024000\"\n        }\n    ],\n    \"sum\": 20000\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "app/controllers/User/user.py",
    "groupTitle": "user"
  },
  {
    "type": "UNLOCK",
    "url": "/user/login",
    "title": "login",
    "name": "login",
    "group": "user",
    "body": [
      {
        "group": "Body",
        "type": "String",
        "optional": false,
        "field": "username",
        "description": ""
      },
      {
        "group": "Body",
        "type": "String",
        "optional": false,
        "field": "password",
        "description": ""
      }
    ],
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "returns",
            "description": "<p>json contains a token - a unique session id that is valid for each login for 3 hours</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Success-Response:",
          "content": "HTTP/1.1 200 OK\n{\n    \"token\": \"9d2db59d-5d16-4773-adb1-f39e71321e4f\",\n    \"message\": \"login successful\"\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "app/controllers/User/user.py",
    "groupTitle": "user"
  },
  {
    "type": "POST",
    "url": "/user/signup",
    "title": "signup",
    "name": "signup",
    "group": "user",
    "body": [
      {
        "group": "Body",
        "type": "String",
        "optional": false,
        "field": "username",
        "description": ""
      },
      {
        "group": "Body",
        "type": "String",
        "optional": false,
        "field": "password",
        "description": ""
      }
    ],
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "returns",
            "description": "<p>json contains username</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Success-Response:",
          "content": "HTTP/1.1 201 CREATED\n    {\n        \"username\": m4hdin4,\n        \"message\": \"user added\"\n    }",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "app/controllers/User/user.py",
    "groupTitle": "user"
  },
  {
    "type": "PUT",
    "url": "/user",
    "title": "update user password",
    "name": "update_password",
    "group": "user",
    "header": {
      "fields": {
        "Header": [
          {
            "group": "Header",
            "type": "String",
            "optional": false,
            "field": "token",
            "description": "<ul> <li>a unique session id that is valid for each login for 3 hours</li> </ul>"
          }
        ]
      }
    },
    "body": [
      {
        "group": "Body",
        "type": "String",
        "optional": false,
        "field": "new_password",
        "description": ""
      },
      {
        "group": "Body",
        "type": "String",
        "optional": false,
        "field": "old_password",
        "description": ""
      }
    ],
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "returns",
            "description": "<p>json contains username</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Success-Response:",
          "content": "HTTP/1.1 200 OK\n    {\n        \"username\": \"m4hdin4\",\n        \"message\": \"password changed\"\n    }",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "app/controllers/User/user.py",
    "groupTitle": "user"
  }
] });
