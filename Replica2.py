import Pyro4

@Pyro4.expose
@Pyro4.behavior(instance_mode="single")

class Shop(object):
    def __init__(self):
        self.id = []
        self.food = ['Food1', 'Food2', 'Food3']
        self.orders = []
        self.response = []

    def update_replica_order(self):
        if r3:
            replica3.update_orders(self.id, self.orders, self.response)

    def add_order(self, id, address, food):
        orderDetails = []
        if id in self.id:
            for item in range(0, len(self.response)):
                if self.response[item][0] == id:
                    print('Returning Previous Response {0}'.format(self.response[item][1]))
                    return self.response[item][1]
        else:
            if food not in self.food:
                print('{0} is not a valid food to order'.format(food))
                return 'INVALID_FOOD'
            else:
                self.id.append(id)
                orderDetails.append(id)
                orderDetails.append(address)
                orderDetails.append(food)
                self.orders.append(orderDetails)
                self.update_replica_order()
        print(self.id, self.orders)
        return orderDetails

    def update_orders(self, id, orders, response):
        self.id = id
        self.orders = orders
        self.response = response
        print(self.id, self.orders)


daemon = Pyro4.Daemon()  # make a Pyro daemon
ns = Pyro4.locateNS()  # find the name server
uri = daemon.register(Shop)  # register the greeting maker as a Pyro object
ns.register("example.replica2", uri)  # register the object with a name in the name server

with Pyro4.Proxy('PYRONAME:example.replica3') as replica3:
    try:
        replica3._pyroBind()
        r3 = True
        print('Successfully connected to Replica 3')
    except Pyro4.errors.CommunicationError:
        r3 = False
        print('Replica 3 is down')

print("Ready.")
daemon.requestLoop()  # start the event loop of the server to wait for calls
