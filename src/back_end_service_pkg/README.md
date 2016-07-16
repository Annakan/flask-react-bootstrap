# Ze backend

This represent the "meat" of the application doing some stuff (in that cas silly stuff sending random silly names around) organized around a queue
 (technically a ZMQ "device" that implements a queue with a monitoring sink).
 It is a classical "producer/consumer" architecture.
 That architecture is not imposed or set in stone, only the ZMQ queue device in the dependency between producers consumers and the web front end.
 Another Producer/Consumer or Peer architecture could be used as long as some monitoring sink exists for the web clients and the data passed around is
 understood by everyone communicating, at least understood enough by each one to get each job done.