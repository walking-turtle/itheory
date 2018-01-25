import sys,json,requests
from predictor import PredictableText

GLOBAL_SERVER = "https://api.neze.fr/itheory/api"
if len(sys.argv) < 2:
    sys.exit(1)
GLOBAL_TOKEN = sys.argv[1]

GLOBAL_MAX_LOAD = 500

def get_text(url):
    headers = { 'Accept': 'plain/text' }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.text
    return None

def get_task():
    headers = { 'Content-Type': 'application/json' }
    api_url = '{:}/tasks'.format(GLOBAL_SERVER)
    data = { 'token': GLOBAL_TOKEN, 'max': GLOBAL_MAX_LOAD }
    response = requests.post(api_url, headers=headers, json=data)
    if response.status_code == 201:
        r = response.json()
        try:
            r['text'] = get_text(r['text'])
        except KeyError:
            r['text'] = None
        try:
            todo = r['task']['todo']
            ul = list(map(int,todo.split(':')))
            r['task']['upper'] = ul[1]
            r['task']['lower'] = ul[0]
        except KeyError:
            r['text'] = None
        return r
    return None

def put_task(task,correct=0,processed=0):
    api_url = task['uri']
    headers = { 'Content-Type': 'application/json' }
    data = {'correct': correct, 'processed': processed, 'token': task['token']}

    response = requests.put(api_url, headers=headers, json=data)
    if response.status_code == 200:
        return
    return

if __name__=='__main__':
    task = get_task()
    print(task)
    if task is None:
        print('No more job for me.')
        sys.exit(0)
    if task['text'] is None:
        print('No text to process!')
        # Should delete task?
        sys.exit(1)
    t = PredictableText(task['text'],lower=task['task']['lower'],upper=task['task']['upper'])
    for _ in t:
        pass
    s = json.loads(t.fullstats)
    put_task(task['task'],correct=s['correct'],processed=sum(map(lambda x: x[1], s.items())))
