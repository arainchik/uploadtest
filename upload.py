import httplib
import time
import logging

from Queue import Queue
from threading import Thread

num_threads = 2
num_tries = 10

http_connections = []

def Upload(i, q, hcon):
   while(True):
       item = q.get()
       BODY = "TEST123"*20
       logging.info("%d: Uploading %s", i, item)
       hcon[i].request("PUT", "/file" + item, BODY)
       response = hcon[i].getresponse()
       logging.info("%d: Status: %s %s", i, response.status, response.reason)
       logging.info("%d: Received response: %s", i, response.read())
       q.task_done()

# main_q = Queue()
main_q = Queue(num_threads)

logging.basicConfig(format="%(asctime)s %(message)s", level=logging.INFO)


for i in xrange(num_threads):
    http_connections.append(httplib.HTTPSConnection("transfer.sh"))
    # http_connections[i].set_debuglevel(100)

for i in xrange(num_threads):
   worker = Thread(target=Upload, args=(i, main_q, http_connections))
   worker.setDaemon(True)
   worker.start()


start_time = time.time()

for i in xrange(num_tries):
   main_q.put(str(i))


logging.info("*** Main thread waiting ***")
main_q.join()
logging.info("*** Done")

for c in http_connections:
   c.close()


end_time = time.time() - start_time

logging.info("*** Elapsed time: %.02f seconds" , end_time)
