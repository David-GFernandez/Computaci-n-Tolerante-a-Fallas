from prefect import flow

@flow
def hello_world():
    print('Hola mundo')

hello_world()