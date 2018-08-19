from pyspark import SparkContext
from pyspark.sql import SQLContext
import time
import sys
import argparse

def use_pip_modules():
    import requests    
    response = requests.get('https://google.com') 
    print('using pip module - response status code from google:', response.status_code)

def use_project_source_code():
    import foo
    some_int = foo.get_some_int()
    print('using project source code - calling foo.get_some_int():', some_int)

def use_sql_context(sql_context):
    df = sql_context.createDataFrame([('Alice', 1), ('Bob', 2)], ['name', 'age'])
    print('use_sql_context - dataframe rows count:', df.count())

def main(sql_context, some_arg):    
    print('reading argument - some_arg value:', some_arg) 
    use_project_source_code()
    use_pip_modules()
    use_sql_context(sql_context)

if __name__ == '__main__': 
    # reading arguments
    parser = argparse.ArgumentParser()    
    parser.add_argument('--pip_modules', required=True, help='pip modules zip path')
    parser.add_argument('--src', required=True, help='source files zip path')
    parser.add_argument('--some_arg', type=str, required=False, default=None, help="some argument")    
    args = parser.parse_args()    

    # creating spark context with source project files and external pip modules
    print('creating spark context. libs:', args.pip_modules, args.src)
    sc = SparkContext(appName="Some App Name", pyFiles=[args.pip_modules, args.src])
    sc.setLogLevel('WARN')
    sql_context = SQLContext(sc)
    print('sql context created')

    # run jobs
    startTime = time.time()
    main(sql_context, args.some_arg)
    endTime = time.time()
    print('jobs total runtime: ', str(int(endTime-startTime)) + 's')
    sc.stop()
