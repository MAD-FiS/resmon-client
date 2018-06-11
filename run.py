import requests
import json
import tabulate
import os
import getpass
import keyboard
import sys

if len(sys.argv) < 2:
    print('Usage: python run.py CONFIG_FILE');
else:
    username = input('username: ');
    password = getpass.getpass('password: ')

    f = open(sys.argv[1], 'r');
    config = json.loads(f.read());
    f.close();

    jwt = json.loads(requests.post('http://' + config['auth'] + ':5000/login', json = {'username': username, 'password': password}).content);
    if jwt['message'] == 'Wrong credentials':
        print('Failed to login');
    else:
        token = jwt['access_token'];
        try:
            while True:
                measurements = {};
                for monitor in config['monitors']:
                    for measurement in json.loads(requests.get('http://' + monitor + ':4000/measurements', headers = {'Authorization': 'Bearer ' + token}).content):
                        metricId = measurement['metric_id'];
                        if not metricId in measurements:
                            measurements[metricId] = [];
                        measurements[metricId].append([monitor, measurement['hostname'], measurement['data'][-1]['value']]);

                os.system('cls' if os.name == 'nt' else 'clear');
                for metricId, measurement in measurements.items():
                    measurement.sort(key=lambda m: m[-1]);
                    measurement.reverse();
                    print(tabulate.tabulate(measurement[:10], headers = ['Monitor', 'Host', metricId]));
                    print();
        except KeyboardInterrupt:
            pass