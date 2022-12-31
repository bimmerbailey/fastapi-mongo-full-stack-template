db = db.getSiblingDB('your_app');
db.createUser(
    {
        user: 'app_user',
        pwd: 'password',
        roles: [
            {role: 'readWrite', db: 'your_app'},
        ],
    },
);
db.createCollection('users');

db = db.getSiblingDB('test_your_app');
db.createUser(
    {
        user: 'app_user',
        pwd: 'password',
        roles: [
            {role: 'readWrite', db: 'test_your_app'}
        ],
    },
);
db.createCollection('users');