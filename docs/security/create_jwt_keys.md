# Generating JWT Keys for the Application

This guide provides step-by-step instructions for generating RSA keys for JWT signing and verification. These keys are essential for ensuring secure authentication and communication in your application.

## Prerequisites

- OpenSSH installed on your system.
- Access to the application's `.env` file to set the paths and passphrase.

## Steps to Generate the Keys

### 1. Create a Directory for the Keys

Create a `.keys` directory in the root of your project to store the keys securely.

```bash
mkdir -p .keys
```

Ensure the directory has restricted permissions to prevent unauthorized access:

```bash
chmod 700 .keys
```

### 2. Generate the Private Key

Run the following command to generate a private RSA key with a passphrase:

```bash
ssh-keygen -t rsa -b 2048 -f .keys/private -N "your-strong-passphrase"
```

Replace `your-strong-passphrase` with a secure passphrase. This key will be used for signing JWTs.

Note: Do NOT use the `-m PEM` flag as we need the keys in OpenSSH format.

### 3. Generate the Public Key

The public key will be automatically generated as `.keys/private.pub` when creating the private key. Ensure both files exist:

```bash
ls -l .keys/
```

You should see `private` and `private.pub`.

### 4. Verify the Generated Keys

To check that the keys are in OpenSSH format:

```bash
ssh-keygen -l -f .keys/private
```

To verify the public key format:

```bash
ssh-keygen -l -f .keys/private.pub
```

Both commands should show information about the RSA key, including its fingerprint and bit length.

### 5. Update the .env File

Add the following configurations to your `.env` file:

```env
JWT_PRIVATE_KEY_PATH=".keys/private"
JWT_PUBLIC_KEY_PATH=".keys/private.pub"
JWT_KEYS_PASSPHRASE="your-strong-passphrase"
```

Ensure the passphrase matches the one used during key generation.

### 6. Secure the Keys

- Ensure the `.keys` directory and its contents are not included in version control. Add the following line to your `.gitignore` file:

```gitignore
.keys/
```

- Restrict access to the keys directory:

```bash
chmod 600 .keys/private .keys/private.pub
```

### 7. Test the Application

Start your application and verify that the keys are loaded correctly. Check for any errors related to key loading or JWT signing/verification.

### Troubleshooting

If you see errors like "Not OpenSSH private key format", check that:
1. You didn't use the `-m PEM` flag during key generation
2. The keys are in OpenSSH format (default format for ssh-keygen)
3. The file paths in your .env file match the actual key locations

---

For more details on JWT security best practices, refer to the [JWT Handbook](https://jwt.io/introduction/).
