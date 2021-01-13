import requests

'''
mo (main operation):
Find main operation available in system by ID. Returns main operation with the specific ID .
[
    {'id': 310, 'name': 'Kenttien hoito'},
    {'id': 20, 'name': 'Latujen hoito'}
]

mt (machine types):
Find all machine types available in system. Returns relevant information of all machine types.
[
    {'id': 172898, 'name': 'Kuorma-auto'},
    {'id': 172926, 'name': 'Kuorma-auto'},
    {'id': 172895, 'name': 'Latukone JT'},
    {'id': 172924, 'name': 'Moottorikelkka JT'},
    {'id': 4219486, 'name': 'seppopa'},
    {'id': 172941, 'name': 'Traktori'},
    {'id': 172912, 'name': 'Traktori Mustonen'}
]

op (operations):
Find all operations available in system. Returns relevant information of all operations.
[
    {'id': 311, 'name': 'Auraus'},
    {'id': 25, 'name': 'Jäädytys'},
    {'id': 17470260, 'name': 'Kenttien kunnostus'},
    {'id': 22, 'name': 'Ladun hoito'},
    {'id': 23, 'name': 'Latujen pohjatyöt'},
    {'id': 24, 'name': 'Pohjajäädytys'},
    {'id': 157139, 'name': 'Siirtymä'},
    {'id': 7781905, 'name': 'Tompan duuni'}
]
'''


URL = 'https://oulu.fluentprogress.fi/LatuOulu/v1/snowplow/'

param = {
}

req = requests.get(url=URL, params=param)
print(req.status_code)

data = req.json()

print(data)
