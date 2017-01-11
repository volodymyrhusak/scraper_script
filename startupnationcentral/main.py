from myparser import Parser
import csv
import threading
from queue import Queue
import time
lock = threading.Lock()
# best result 4663 item for 38m8.641s


methods = ['get_company_name',              'get_company_short_description', 'get_company_description',
           'get_homepage',                  'get_sector',                    'get_founded',
           'get_business_model',            'get_amount_raised',             'get_funding_stage',
           'get_employees',                 'get_products',                  'get_product_stage',
           'get_tags',                      'get_address',                   'get_offices_abroad',
           'get_geographical_markets',      'get_target_markets',            'get_patent',
           'get_tim_member_1',              'get_tim_member_2',              'get_tim_member_3',
           'get_funding_rounds',            'get_facebook',                  'get_twitter',
           'get_linkedin',                  'get_similar_company_1',         'get_similar_company_2',
           'get_similar_company_3',         'get_url_source',
           ]

# write titles in 'output.csv' file
with open('output.csv', 'a') as out_file:
    writer = csv.writer(out_file)
    title = map(lambda x: x[4:], methods)
    writer.writerow(list(title))
def main(url):
      def remove_non_ascii(text):
          # text.strip()
          response = ''.join(i for i in text if ord(i) < 128)
          return response
      
      # write titles in 'output.csv' file
      # with open('output.csv', 'a') as out_file:
      #     writer = csv.writer(out_file)
      #     title = map(lambda x: x[4:], methods)
      #     writer.writerow(list(title))
      
      # with open('urls.txt') as in_file:
      
          # iterate each url to get information
      # for i, url in enumerate(in_file.readlines()):
      try:      
          result = []
          print(url)
          parser = Parser(url)
          for method in methods:
              response = ''
              try:
                  to_call = getattr(parser, method)
                  response = to_call()
                  response = remove_non_ascii(response)
              finally:
                  result.append(response)
          # add extracted information in 'output.csv'
          with lock:
              with open('output.csv', 'a') as out_file:
                  writer = csv.writer(out_file)
                  writer.writerow(result)
                  print ('ADD!!')
                    # print(threading.current_thread().name,item)
      except Exception as error:
        with lock:
          with open('bad_url.txt', 'a') as out_file:
              out_file.write(url + str(error) + '\n' + '#' * 30 + '\n')
      
def worker():
    while True:
        url = q.get()
        # print (url)
        main(url)
        q.task_done()


q = Queue()
for i in range(10):
     t = threading.Thread(target=worker)
     # print (i)
     t.daemon = True  # thread dies when main thread (only non-daemon thread) exits.
     t.start()

start = time.perf_counter()
with open('urls.txt') as in_file:
  for url in in_file.readlines():
    # print (url) 
    q.put(url.strip())

q.join() 

print('time:',time.perf_counter() - start)