db.createUser({
    user: "admin",
    pwd: "secret",
    roles: [
        {role: "userAdminAnyDatabase", db: "admin"},
        {role: "readWrite", db: "cv_database"}
    ]
});