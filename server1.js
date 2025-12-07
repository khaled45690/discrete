const net = require("net");
const readline = require("readline");

// Server 1 - Acts as a TCP server
const PORT = 3000;
const HOST = "localhost";

// RSA Public Key (n, e) = (3233, 17)
const n = 3233;
const e = 17;

// Manual modular exponentiation: (base^exp) % mod
function modPow(base, exp, mod) {
  let result = 1;
  base = base % mod;
  while (exp > 0) {
    if (exp % 2 === 1) {
      result = (result * base) % mod;
    }
    exp = Math.floor(exp / 2);
    base = (base * base) % mod;
  }
  return result;
}

// Convert letter to number (A=01, B=02, ..., Z=26)
// Space = 00
function letterToNumber(letter) {
  letter = letter.toUpperCase();
  if (letter === " ") return 0;
  const code = letter.charCodeAt(0);
  if (code >= 65 && code <= 90) {
    return code - 64; // A=1, B=2, ..., Z=26
  }
  return 0; // For any other character, treat as space
}

// Encrypt message using RSA
// Process two letters at a time
function encryptMessage(message) {
  const encrypted = [];

  // Pad message to even length
  if (message.length % 2 !== 0) {
    message += " ";
  }

  for (let i = 0; i < message.length; i += 2) {
    const letter1 = letterToNumber(message[i]);
    const letter2 = letterToNumber(message[i + 1]);

    // Combine two letters: first_letter * 100 + second_letter
    const m = letter1 * 100 + letter2;

    // Encrypt: c = m^e mod n
    const c = modPow(m, e, n);
    encrypted.push(c);
  }

  return encrypted;
}

let connectedSocket = null;

const server = net.createServer((socket) => {
  console.log(
    "Server 1: Client connected from",
    socket.remoteAddress + ":" + socket.remotePort
  );

  connectedSocket = socket;

  // Handle incoming data from client
  socket.on("data", (data) => {
    console.log("Server 1: Received:", data.toString());
  });

  // Handle connection end
  socket.on("end", () => {
    console.log("Server 1: Client disconnected");
    connectedSocket = null;
  });

  // Handle errors
  socket.on("error", (err) => {
    console.error("Server 1: Socket error:", err.message);
  });
});

// Start listening
server.listen(PORT, HOST, () => {
  console.log(`Server 1 listening on ${HOST}:${PORT}`);
  console.log("RSA Public Key (n, e) = (3233, 17)");
  console.log("\nType messages to encrypt and send to Server 2:");
});

// Handle server errors
server.on("error", (err) => {
  console.error("Server 1 error:", err.message);
});

// Setup readline for user input
const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout,
});

rl.on("line", (input) => {
  if (!connectedSocket) {
    console.log("No client connected. Waiting for Server 2 to connect...");
    return;
  }

  // Encrypt the message
  const encrypted = encryptMessage(input);

  console.log("\n--- Encryption Process ---");
  console.log("Original message:", input);
  console.log("Encrypted blocks:", encrypted.join(", "));

  // Send encrypted message as JSON
  const message = JSON.stringify({ encrypted });
  connectedSocket.write(message);

  console.log("Sent encrypted message to Server 2\n");
});
