from datetime import date, datetime
from elasticsearch import Elasticsearch
import psutil
Total_Memory= psutil.virtual_memory()[0]
es = Elasticsearch(host='localhost', port=9200)
#Creating a new indices
#es.indices.create(index="localprocess",ignore=400)
def getListOfProcessMemory():
    '''
    Get list of running process Memory Usage
    '''
    listOfProcObjects = []
    # Iterate over the list
    for proc in psutil.process_iter():
       try:
           # Fetch process details as dict
           pinfo = proc.as_dict(attrs=['pid'])
           pinfo['Memory_Percentage'] = round((proc.memory_info().vms / Total_Memory),4)*100
           pinfo['CPU_Percentage'] = proc.cpu_percent(interval=1)

           # Append dict to list
           listOfProcObjects.append(pinfo);
       except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
           pass
    return listOfProcObjects
def main():
    listOfRunningProcess = getListOfProcessMemory()
    for elem in listOfRunningProcess:
        es.index(index="localprocess", body={"pid": elem['pid'],
                                    "cpu_percentage": elem['CPU_Percentage'],
                                    "memory_percentage": elem['Memory_Percentage'],
                                     "timestamp": datetime.now()})
        
if __name__ == '__main__':
   main()
