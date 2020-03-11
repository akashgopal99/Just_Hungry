import Pyro4

with Pyro4.Proxy("PYRONAME:example.front") as frontEnd:
    try:
        frontEnd._pyroBind()
        print("Successfully connected to front end server")
    except Pyro4.errors.CommunicationError:
        print("Failed to connect to front end servers", end='')
        exit(1)

name = input("What is your name? ").strip()
number = input("What is your house number? ").strip()
postcode = input('What is your postcode? ').strip()
food = input('What food do you want? ').strip()

print()
print(name, [number, postcode], food)
print(frontEnd.place_order(name, [number, postcode], food))
