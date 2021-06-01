define({ "api": [
  {
    "type": "DELETE",
    "url": "/category",
    "title": "delete an available category",
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
            "type": "String",
            "optional": false,
            "field": "returns",
            "description": "<p>text &quot;DELETED&quot;</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Success-Response:",
          "content": "HTTP/1.1 200 OK\nDELETED",
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
    "title": "get category expenses",
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
    "type": "PUT",
    "url": "/category",
    "title": "update an available category name",
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
            "type": "String",
            "optional": false,
            "field": "returns",
            "description": "<p>updated category name</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Success-Response:",
          "content": "HTTP/1.1 200 OK\nupdated_category",
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
    "title": "delete an available expense",
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
            "type": "String",
            "optional": false,
            "field": "returns",
            "description": "<p>text &quot;DELETED&quot;</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Success-Response:",
          "content": "HTTP/1.1 200 OK\nDELETED",
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
    "title": "get one item",
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
    "title": "insert a new expense",
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
            "type": "String",
            "optional": false,
            "field": "returns",
            "description": "<p>inserted object id</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Success-Response:",
          "content": "HTTP/1.1 200 OK\n60b4c7da7ba96ba33ab0d978",
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
    "title": "update an available item",
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
            "type": "String",
            "optional": false,
            "field": "returns",
            "description": "<p>updated object id</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Success-Response:",
          "content": "HTTP/1.1 200 OK\n60b4c7da7ba96ba33ab0d978",
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
    "title": "delete an account",
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
            "type": "String",
            "optional": false,
            "field": "returns",
            "description": "<p>text &quot;DELETED&quot;</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Success-Response:",
          "content": "HTTP/1.1 200 OK\nDELETED",
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
    "url": "/user",
    "title": "get user expenses",
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
    "url": "/login",
    "title": "log in users account",
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
            "type": "String",
            "optional": false,
            "field": "returns",
            "description": "<p>a token - a unique session id that is valid for each login for 3 hours</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Success-Response:",
          "content": "HTTP/1.1 200 OK\n9d2db59d-5d16-4773-adb1-f39e71321e4f",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "app/controllers/User/login.py",
    "groupTitle": "user"
  },
  {
    "type": "POST",
    "url": "/signup",
    "title": "insert a new user",
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
            "type": "String",
            "optional": false,
            "field": "returns",
            "description": "<p>inserted user id(username)</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Success-Response:",
          "content": "HTTP/1.1 200 OK\nm4hdin4",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "app/controllers/User/signup.py",
    "groupTitle": "user"
  },
  {
    "type": "PUT",
    "url": "/user",
    "title": "update the user password",
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
            "type": "String",
            "optional": false,
            "field": "returns",
            "description": "<p>username</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Success-Response:",
          "content": "HTTP/1.1 200 OK\nm4hdin4",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "app/controllers/User/user.py",
    "groupTitle": "user"
  }
] });
