from mailing import hello

result = hello.delay()
print(result.ready())

while True:
    if result.ready():
        print('hi')
        print(result.backend())
