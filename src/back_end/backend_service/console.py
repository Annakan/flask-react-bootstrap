from . import publisher, zmqserver, zmqclient


def publisher_run():
    publisher.main()


def zmqclient_run():
    zmqclient.main()


def zmqserver_run():
    zmqserver.main()