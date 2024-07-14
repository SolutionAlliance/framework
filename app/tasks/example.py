from app.tasks import app

@app.task(name='app.tasks.example.hello')
def hello():
    print('验证示例')