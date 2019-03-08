import json
from time import time
from bson.objectid import ObjectId
from aiohttp import web
from aiohttp_session import get_session
from aiohttp_jinja2 import render_template
from models import User, Task


def redirect(request, router_name):
    url = request.app.router[router_name].url_for()
    raise web.HTTPFound(url)


def set_session(session, user_id, request):
    session['user'] = str(user_id)
    session['last_visit'] = time()
    redirect(request, 'index')


def convert_json(message):
    return json.dumps({'error': message})


class IndexView(web.View):
    async def get(self):
        session = await get_session(self.request)
        if session.get('user'):
            redirect(self.request, 'active')
        redirect(self.request, 'login')


class CreateTaskView(web.View):
    async def get(self):
        context = {}
        return render_template('create_task.html', self.request, context)

    async def post(self):
        data = await self.request.post()
        session = await get_session(self.request)
        _task = Task(self.request.app.db, data, session['user'])
        try:
            result = await _task.save()
        except:
            return web.Response(content_type='application/json', text=convert_json(
                {'error': 'Вы ввели не корректные данные'}))
        if isinstance(result.inserted_id, ObjectId):
            redirect(self.request, 'index')
        else:
            return web.Response(content_type='application/json', text=convert_json(
                {'error': 'Что-то пошло не так'}))


class ActiveTasksView(web.View):
    async def get(self):
        session = await get_session(self.request)
        tasks = await Task.get_tasks(self.request.app.db, session['user'], 'active')
        tasks = await Task.check_status(self.request.app.db, tasks)
        context = {'tasks': tasks}
        return render_template('tasks.html', self.request, context)


class SuccessTasksView(web.View):
    async def get(self):
        session = await get_session(self.request)
        tasks = await Task.get_tasks(self.request.app.db, session['user'], 'success')
        context = {'tasks': tasks}
        return render_template('tasks.html', self.request, context)


class DetailTaskView(web.View):
    async def get(self):
        session = await get_session(self.request)
        _id = self.request.match_info['id']
        _task = await Task.get_task(self.request.app.db, session['user'], _id)
        if _task is None:
            redirect(self.request, 'index')
        context = {'task': _task}
        return render_template('detail.html', self.request, context)

    async def post(self):
        session = await get_session(self.request)
        data = await self.request.post()
        if data:
            _id = data.get('id')
        if data.get('delete') is not None:
            _task = await Task.del_task(self.request.app.db, session['user'], _id)
            redirect(self.request, 'active')
        if data.get('success') is not None:
            _task = await Task.success(self.request.app.db, session['user'], _id)
            redirect(self.request, 'success')
        return web.Response(content_type='application/json', text=convert_json(
            {'error': 'Что-то пошло не так'}))


class NotDoneTasksView(web.View):
    async def get(self):
        session = await get_session(self.request)
        tasks = await Task.get_tasks(self.request.app.db, session['user'], 'not_done')
        tasks = await Task.check_status(self.request.app.db, tasks)
        context = {'tasks': tasks}
        return render_template('tasks.html', self.request, context)


class ProfileView(web.View):
    async def get(self):
        session = await get_session(self.request)
        user = await User.get_user(self.request.app.db, session['user'])
        tasks = await Task.get_all_tasks(self.request.app.db, session['user'])
        tasks = await Task.check_status(self.request.app.db, tasks)
        context = {'user': user, 'tasks': tasks}
        return render_template('profile.html', self.request, context)


class LoginView(web.View):
    async def get(self):
        session = await get_session(self.request)
        if session.get('user'):
            redirect(self.request, 'active')
        context = {}
        return render_template('login.html', self.request, context)

    async def post(self):
        data = await self.request.post()
        user = User(self.request.app.db, data)
        result = await user.check_user()
        if isinstance(result, dict):
            session = await get_session(self.request)
            set_session(session, str(result['_id']), self.request)
            redirect(self.request, 'active')
        else:
            return web.Response(content_type='application/json', text=convert_json(
                {'error': 'Неправильный логин или пароль'}))


class LogoutView(web.View):
    async def get(self):
        session = await get_session(self.request)
        if session.get('user'):
            del session['user']
            redirect(self.request, 'login')
        else:
            raise web.HTTPForbidden(body=b'Forbidden')


class RegisterView(web.View):
    async def get(self):
        session = await get_session(self.request)
        if session.get('user'):
            redirect(self.request, 'active')
        context = {}
        return render_template('register.html', self.request, context)

    async def post(self):
        data = await self.request.post()
        user = User(self.request.app.db, data)
        result = await user.create_user()
        if isinstance(result, ObjectId):
            session = await get_session(self.request)
            set_session(session, str(result), self.request)
            redirect(self.request, 'active')
        else:
            return web.Response(content_type='application/json', text=convert_json(result))
