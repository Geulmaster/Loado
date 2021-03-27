from Loado.app import config_reader

configuration = config_reader()

class Config:

    def __init__(self, host = "localhost", port = "80",
     route = "/", users = str(5), spawn_rate = str(10),
      time = str(30)):
        if configuration:
            self.host = configuration["Load Testing"]["host"]
            self.port = configuration["Load Testing"]["port"]
            self.route = configuration["Load Testing"]["route"]
            self.users = configuration["Load Testing"]["users"]
            self.spawn_rate = configuration["Load Testing"]["spawn_rate"]
            self.time = configuration["Load Testing"]["time"]
        else:
            self.host = host
            self.port = port
            self.route = route
            self.users = users
            self.spawn_rate = spawn_rate
            self.time = time
            