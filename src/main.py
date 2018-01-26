#!/usr/bin/env python
import requests,io,zipfile,progressbar,predictor

BIBLEHUB_USERNAME="bh733"
BIBLEHUB_PASSWORD="qx358"
BIBLEHUB_ARCHIVE="http://biblehub.info/data/bibles.zip"

def get_progressbar(name='',maxval=None):
    if isinstance(name,bytes):
        name = name.decode('ascii')
    if len(name)>20:
        name=name[:17]+'...'
    if maxval is None:
        cls = progressbar.widgets.BouncingBar
        maxval = progressbar.base.UnknownLength
    else:
        cls = progressbar.widgets.Bar
    widgets = [\
            '{:20}'.format(name),
            ' (',
            progressbar.widgets.Percentage(),
            ')',
            cls(),
            progressbar.widgets.ETA() ]
    return progressbar.ProgressBar(widgets=widgets,maxval=maxval).start()

def get_bibles():
    # Send HTTP request and get headers
    response = requests.get(BIBLEHUB_ARCHIVE,\
            auth=(BIBLEHUB_USERNAME, BIBLEHUB_PASSWORD),\
            stream=True)
    assert(response.status_code == 200)

    # Get paramaters from response size
    response_size = int(response.headers['Content-Length'])
    chunk_size = max(1024,response_size//99)
    num_bars = -(-response_size//chunk_size)

    # Prepare stream to write data from the response
    zipped_stream = io.BytesIO()

    # Get response and show progressbar
    bar = get_progressbar(name='Downloading bibles', maxval=num_bars)
    i = 0
    for chunk in response.iter_content(chunk_size=chunk_size):
        bar.update(i)
        zipped_stream.write(chunk)
        i+=1
    bar.finish()

    # Rewind stream to read it with zipfile
    zipped_stream.seek(0,0)

    # Open stream as a zipped object
    zipped_object = zipfile.ZipFile(zipped_stream,'r')

    # Get file name then stream to text file
    text_filename = zipped_object.namelist()[0]
    text_stream = zipped_object.open(text_filename, 'r')

    # Get first line of text. This is a tab separated csv file
    csv_header = list(map(lambda x: x.strip(), text_stream.readline().strip().split(b'\t')))[1:]

    # Prepare columns to fill from the text lines
    csv_columns = [list()] + [ list() for _ in csv_header ]

    # Read lines and show bar
    bar = get_progressbar(name='Separating versions')
    i = 0
    csv_line = text_stream.readline()
    while csv_line:
        bar.update(i)
        csv_line = csv_line.strip()
        for c,v in zip(csv_columns,csv_line.split(b'\t')):
            c.append(v.strip())
        csv_line = text_stream.readline()
        i+=1
    bar.finish()

    # Recompose data
    csv_firstcolumn = csv_columns[0]
    csv_columns = csv_columns[1:]
    bibles_data = { k: b'\n'.join(map(lambda x: b'\t'.join(x), zip(csv_firstcolumn,c))) for k,c in zip(csv_header,csv_columns) }
    return bibles_data

if __name__=='__main__':
    bibles = get_bibles()
    substrings = predictor.SubStrings(cache=10)
    print('\n\n**** Reading bibles ****')
    for name,bible in bibles.items():
        bar = get_progressbar(name=name,maxval=len(bible))
        for i in substrings.parseiter(bible):
            bar.update(i)
        bar.finish()

    print('\n\n**** Building predictions ****')
    predictions = predictor.Predictions.from_substrings(substrings)

    print('\n\n**** Running prediction on each bible ****')
    for name,bible in bibles.items():
        print('\n{:}'.format(name))
        result,_ = predictions.run(bible,verb=1)
        print('{:}: {:6.2f}%'.format(name,result*100))
