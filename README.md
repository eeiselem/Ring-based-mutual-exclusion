# Ring-based-mutual-exclusion

will implement the Ring-based Mutual Exclusion (ME) algorithm used in distributed coordination. Recall that ME requires at most one process (or nodes/hosts as used in this assignment) to enter a shared critical section (CS). If more than one process attempts to enter CS, the system will allow only one of them to enter and the rest waits for their turn to come. You are here required to implement the Ring-based ME algorithm (consult the textbook or slides to see the relevant technique). You can also consult the code we developed in class for ME with a central server.

You will be using a simulator to "mimic" the process/node operations (we use the terms node, host, and process interchangeably in this assignment)

The simulator creates processes (termed as Host in the code) and enables them to send and receive messages with some arbitrary (random) channel delay/latency. Each host has two important methods/functions:

send_message(to, message) -- send message to another host/node ("to")
receive_message(frm, message, time) -- this method is called when a message is received from another host/node ("frm" is used instead of "from" because "from" is a keyword reserved in Python)
Additionally, two more functions, "enterCS" and "exitCS," are given to assist in entering and leaving CS.
Each message is an instance of the class Message (appears in simulation.py) that has the following main attributes/fields:

message_id
source host
destination host
message_type
payload
