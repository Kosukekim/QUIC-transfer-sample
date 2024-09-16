# QUIC-transfer-sample

This is simple program for testing QUIC server and client, using ``aioquic``.

The Client get some data from a local web server, and transmit to QUIC server.
It is exected every two seconds.
The web server process return random float value to Client.

The Server receive data from Client and return message indicating receiving.

Required Modules
----------------
``aioquic``,``fastapi`` and ``uvicorn``.

Usage
---------------
First, cloning repository.

```bash
  git clone https://github.com/Kosukekim/QUIC-transfer-sample.git
```

You can boot web server as following:
```bash
  uvicorn api.main:app --reload

Finally, server and client simply runned as follows:
.. code-block:: console
  python ./server.py
  python ./client.py

You will see following communication between server and client!
![image](https://github.com/user-attachments/assets/47e11046-c4bc-4f8d-82a5-073e0eec825d)



