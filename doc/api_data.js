define({ "api": [
  {
    "type": "DELETE",
    "url": "/category",
    "title": "delete an available category",
    "name": "delete_category",
    "group": "category",
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
    "filename": "./main.py",
    "groupTitle": "category"
  },
  {
    "type": "GET",
    "url": "/user",
    "title": "get category expenses",
    "name": "get_category",
    "group": "category",
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
    "filename": "./main.py",
    "groupTitle": "category"
  },
  {
    "type": "PUT",
    "url": "/category",
    "title": "update an available category name",
    "name": "update_category",
    "group": "category",
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
    "filename": "./main.py",
    "groupTitle": "category"
  },
  {
    "type": "DELETE",
    "url": "/item",
    "title": "delete an available expense",
    "name": "delete",
    "group": "item",
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
    "filename": "./main.py",
    "groupTitle": "item"
  },
  {
    "type": "GET",
    "url": "/item",
    "title": "get one item",
    "name": "get_one",
    "group": "item",
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
    "filename": "./main.py",
    "groupTitle": "item"
  },
  {
    "type": "POST",
    "url": "/item",
    "title": "insert a new expense",
    "name": "insert",
    "group": "item",
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
    "filename": "./main.py",
    "groupTitle": "item"
  },
  {
    "type": "PUT",
    "url": "/item",
    "title": "update an available item",
    "name": "update",
    "group": "item",
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
    "filename": "./main.py",
    "groupTitle": "item"
  },
  {
    "type": "GET",
    "url": "/user",
    "title": "get user expenses",
    "name": "get_list",
    "group": "user",
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
    "filename": "./main.py",
    "groupTitle": "user"
  },
  {
    "type": "UNLOCK",
    "url": "/login",
    "title": "log in users account",
    "name": "login",
    "group": "user",
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "returns",
            "description": "<p>a token</p>"
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
    "filename": "./main.py",
    "groupTitle": "user"
  },
  {
    "type": "POST",
    "url": "/signup",
    "title": "insert a new user",
    "name": "signup",
    "group": "user",
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
    "filename": "./main.py",
    "groupTitle": "user"
  }
] });