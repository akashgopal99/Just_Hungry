import Pyro4


@Pyro4.expose
@Pyro4.behavior(instance_mode="single")
class FrontEnd(object):
    def __init__(self):
        self.id = []
        self.r1 = True
        self.r2 = True
        self.r3 = True

    def place_order(self, name, address, food):
        print(self.id, name, address, food)
        self.id.append(len(self.id) + 1)
        if self.r1:
            try:
                order = replica1.add_order(self.id[-1], address, food)
            except Pyro4.errors.CommunicationError:
                print('Could not connect to Replica 1')
                self.r1 = False
                self.r2 = True
        if self.r2 and not self.r1:
            print('trying replica 2')
            try:
                print(self.id[-1], address, food)
                order = replica2.add_order(self.id[-1], address, food)
            except Pyro4.errors.CommunicationError:
                print('Could not connect to Replica 2')
                self.r2 = False
                self.r3 = True
        if self.r3 and not self.r1 and not self.r2:
            try:
                order = replica3.add_order(self.id[-1], address, food)
            except Pyro4.errors.CommunicationError:
                print('Could not connect to Replica 3')
                self.r3 = False
        if order == 'INVALID_FOOD':
            return '{0} is not a valid food to order'.format(food)
        else:
            return "Hello, {0}. Here is your unique order number {1}.\nYour order has been placed successfully" \
                .format(name, self.id[-1])

    def find_address(self, houseNumber, postcode):
        return "House {0} at postcode {1}".format(houseNumber, postcode)


daemon = Pyro4.Daemon()  # make a Pyro daemon
ns = Pyro4.locateNS()  # find the name server
uri = daemon.register(FrontEnd)  # register the greeting maker as a Pyro object
ns.register("example.front", uri)  # register the object with a name in the name server

with Pyro4.Proxy("PYRONAME:example.replica1") as replica1:
    try:
        replica1._pyroBind()
        print("Successfully connected to Replica 1")
    except Pyro4.errors.CommunicationError:
        print('Replica 1 is down')
with Pyro4.Proxy("PYRONAME:example.replica2") as replica2:
    try:
        replica2._pyroBind()
        print("Successfully connected to Replica 2")
    except Pyro4.errors.CommunicationError:
        print('Replica 2 is down')
with Pyro4.Proxy("PYRONAME:example.replica3") as replica3:
    try:
        replica3._pyroBind()
        print("Successfully connected to Replica 3")
    except Pyro4.errors.CommunicationError:
        print("Failed to connect to back end servers", end='')
        exit(1)

print("Ready.")
daemon.requestLoop()  # start the event loop of the server to wait for calls
