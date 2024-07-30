import json
from datetime import datetime
from space.models import *

def insert_launch_data(json_data):
    
    data = json.loads(json_data)
    
    results = data.get('results', [])
    
    for result in results:
        launch = Launch(
            
        )