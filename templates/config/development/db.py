MONGO = {
    "uri":      "mongodb://localhost",
    "pymongo_extra": {
        "connectTimeoutMS": 1100,
        "socketKeepAlive": True,
    },
    "dbname":   "{{ project_name }}_dev",
}
