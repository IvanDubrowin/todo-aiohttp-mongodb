from views import *
from settings import STATIC_ROOT


def setup_routes(app):
    app.router.add_static(STATIC_ROOT, 'static', name='static')
    app.router.add_view('/', IndexView, name='index')
    app.router.add_view('/create_task', CreateTaskView, name='create_task')
    app.router.add_view('/active', ActiveTasksView, name='active')
    app.router.add_view('/success', SuccessTasksView, name='success')
    app.router.add_view('/not_done', NotDoneTasksView, name='not_done')
    app.router.add_view('/detail/{id}', DetailTaskView, name='detail')
    app.router.add_view('/login', LoginView, name='login')
    app.router.add_view('/logout', LogoutView, name='logout')
    app.router.add_view('/register', RegisterView, name='register')
    app.router.add_view('/profile', ProfileView, name='profile')
