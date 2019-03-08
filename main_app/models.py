from datetime import datetime
import timestring
from bson.objectid import ObjectId
from settings import TASK_COLLECTION, USER_COLLECTION


class Task:

    def __init__(self, db, data, user):
        self.collection = db[TASK_COLLECTION]
        self.user = user
        self.title = data.get('title')
        self.text = data.get('text')
        self.day = data.get('day')
        self.time = data.get('time')

    async def save(self):
        result = await self.collection.insert_one(
            {'user': self.user,
             'title': self.title,
             'text': self.text,
             'time_create': datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:00"),
             'deadline': timestring.Date(f'{self.day} {self.time}').date,
             'status': 'active'})
        return result

    @staticmethod
    async def get_tasks(db, user, status):
        tasks = db[TASK_COLLECTION].find({'user': user, 'status': status})
        return await tasks.to_list(length=None)

    @staticmethod
    async def get_all_tasks(db, user):
        tasks = db[TASK_COLLECTION].find({'user': user})
        return await tasks.to_list(length=None)

    @staticmethod
    async def get_task(db, user, _id):
        task = db[TASK_COLLECTION].find_one({'_id': ObjectId(_id), 'user': user})
        return await task

    @staticmethod
    async def success(db, user, _id):
        task = db[TASK_COLLECTION].update_one({'_id': ObjectId(_id), 'user': user},\
                                            {'$set': {'status': 'success'}})
        return await task

    @staticmethod
    async def del_task(db, user, _id):
        task = db[TASK_COLLECTION].delete_many({'_id': ObjectId(_id), 'user': user})
        return await task

    @staticmethod
    async def check_status(db, tasks):
        update_tasks = []
        for task in tasks:
            if datetime.now() >= timestring.Date(task['deadline']):
                task = db[TASK_COLLECTION].update_one(
                    {'_id': task['_id']}, {'$set': {'status': 'not_done'}}
                    )
            update_tasks.append(task)
        return tasks

class User:

    def __init__(self, db, data):
        self.collection = db[USER_COLLECTION]
        self.email = data.get('email')
        self.login = data.get('login')
        self.password = data.get('password')
        self.id = data.get('id')

    async def check_user(self):
        return await self.collection.find_one({'login': self.login})

    async def get_login(self):
        user = await self.collection.find_one({'_id': ObjectId(self.id)})
        return user.get('login')

    async def create_user(self):
        user = await self.check_user()
        if not user:
            result = await self.collection.insert_one(
                {'email': self.email, 'login': self.login, 'password': self.password}
                )
        else:
            result = {'error': 'Пользователь уже существует'}
        return result

    @staticmethod
    async def get_user(db, _id):
        user = db[USER_COLLECTION].find_one({'_id': ObjectId(_id)})
        return await user
