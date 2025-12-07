const net = require("net");

// Server 2 - Acts as a TCP client
const PORT = 3000;
const HOST = "localhost";

// RSA Private Key (n, d) = (3233, 2753)
const n = 3233;
const d = 2753;

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

// Convert number to letter (01=A, 02=B, ..., 26=Z, 00=space)
function numberToLetter(num) {
  if (num === 0) return " ";
  if (num >= 1 && num <= 26) {
    return String.fromCharCode(96 + num);
  }
  return "?";
}

// Decrypt message using RSA
function decryptMessage(encryptedBlocks) {
  let decrypted = "";

  for (let c of encryptedBlocks) {
    // Decrypt: m = c^d mod n
    const m = modPow(c, d, n);

    // Split back into two letters
    const letter1 = Math.floor(m / 100);
    const letter2 = m % 100;

    decrypted += numberToLetter(letter1) + numberToLetter(letter2);
  }

  return decrypted.trim();
}

const client = new net.Socket();

// Connect to Server 1
client.connect(PORT, HOST, () => {
  console.log("Server 2: Connected to Server 1");
  console.log("RSA Private Key (n, d) = (3233, 2753)");
  console.log("Waiting for encrypted messages...\n");
});

// Handle data received from Server 1
client.on("data", (data) => {
  try {
    const message = JSON.parse(data.toString());

    if (message.encrypted) {
      console.log("\n--- Decryption Process ---");
      console.log("Received encrypted blocks:", message.encrypted.join(", "));

      // Decrypt the message
      const decrypted = decryptMessage(message.encrypted);

      console.log("Decrypted message:", decrypted);
      console.log("------------------------\n");
    }
  } catch (err) {
    console.log("Server 2: Received non-encrypted data:", data.toString());
  }
});

// Handle connection close
client.on("close", () => {
  console.log("Server 2: Connection closed");
});

// Handle errors
client.on("error", (err) => {
  console.error("Server 2: Error:", err.message);
});
