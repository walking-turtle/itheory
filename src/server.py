from flask import Flask,url_for,abort,Response
from flask_restful import Api,Resource
from flask_restful import reqparse
import json,os,binascii,sys

def token_hex(x):
    return binascii.hexlify(os.urandom(x)).decode('ascii')

app = Flask(__name__)
api = Api(app)
GLOBAL_TOKEN = token_hex(24)

if len(sys.argv) < 2:
    filename='/data.txt'
else:
    filename=sys.argv[1]
with open(filename,'r') as f:
    GLOBAL_DATA = f.read()
    GLOBAL_DATA_LEN = len(GLOBAL_DATA)

@app.route('/itheory/text',methods=['GET'],endpoint='text')
def get_text():
    return Response(GLOBAL_DATA,mimetype="text/plain; charset=utf-8")

class AppData:
    def __init__(self,path):
        self.file = path
        self.tasks = list()
        self.tasks_index = dict()
        self.counter = 0
        self.todo = GLOBAL_DATA_LEN

    def dump(self):
        with open(self.file,'w') as f:
            json.dump(self.__dict__, f)
        return self

    def load(self):
        try:
            with open(self.file,'r') as f:
                self.__dict__ = json.load(f)
        except FileNotFoundError:
            pass
        return self

    def get_tasks(self):
        return list(self.tasks)

    def get_task(self,id):
        try:
            return dict(self.tasks[self.tasks_index[id]])
        except (KeyError,IndexError):
            return None

    def put_task(self,id,task):
        try:
            index = self.tasks_index[id]
        except KeyError:
            return None
        self.tasks[index] = dict(task)
        return self

    def new_task(self, max_load):
        id = self.counter
        self.counter+=1
        task = { 'id': id, 'max': max_load }
        task['token'] = token_hex(15)
        todo_upper = self.todo
        if not todo_upper:
            return None
        todo_lower = max(0,self.todo - max_load)
        self.todo = todo_lower
        task['todo'] = '{:d}:{:d}'.format(todo_lower,todo_upper)
        self.tasks_index[id] = len(self.tasks)
        self.tasks.append(task)
        return self.get_task(id)

app_data = AppData('/data/server.json').load()

def make_public_task(task,token=False):
    public_fields = { 'id', 'max', 'correct', 'processed', 'todo' }
    new_task = dict()
    for k,v in task.items():
        if k == 'id':
            new_task['uri'] = url_for('task',id=v,_external=True)
        elif ( k in public_fields ) or ( k == 'token' and token ):
            new_task[k] = v
    return new_task

def make_public_task_list(tasks):
    return list(map(make_public_task,tasks))

class TaskListAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('max', type=int, required=True,\
                help='No maximum load provided.', location='json')
        self.reqparse.add_argument('token', type=str, required=True,\
                help='No auth token provided.', location='json')
        super(TaskListAPI, self).__init__()

    # Get tasks list
    def get(self):
        return {'tasks': make_public_task_list(app_data.get_tasks())}

    # Create a new task
    def post(self):
        args = self.reqparse.parse_args()
        max_load = args['max']
        token = args['token']
        if token != GLOBAL_TOKEN:
            print(token,GLOBAL_TOKEN)
            abort(401)
        task = app_data.new_task(max_load)
        if task is None:
            return {}, 204
        return {'task': make_public_task(task,token=True),'text':url_for('text',_external=True)}, 201

class TaskAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('correct', type=int, required=True,\
                help='No success count provided.', location='json')
        self.reqparse.add_argument('processed', type=int, required=True,\
                help='No processed total provided.', location='json')
        self.reqparse.add_argument('token', type=str, required=True,\
                help='No auth token provided.', location='json')
        super(TaskAPI, self).__init__()

    # Get task details
    def get(self,id):
        task = app_data.get_task(id)
        if task is None:
            abort(404)
        return {'task': make_public_task(task) }

    # Update task (results)
    def put(self,id):
        task = app_data.get_task(id)
        if task is None:
            abort(404)
        args = self.reqparse.parse_args()
        if args['token'] != task['token']:
            abort(401)
        del args['token']
        for k,v in args.items():
            if v != None:
                if k in task:
                    abort(409)
                task[k] = v
        app_data.put_task(id,task)
        return { 'task': make_public_task(task) }

    # Cancel task
    # def delete(self):
        # pass

api.add_resource(TaskListAPI, '/itheory/api/tasks', endpoint='tasks')
api.add_resource(TaskAPI, '/itheory/api/tasks/<int:id>', endpoint='task')

if __name__=='__main__':
    sys.stderr.write('TOKEN="{:}"\n'.format(GLOBAL_TOKEN))
    sys.stderr.flush()
    app.run(host='127.0.0.1',port=8000)
