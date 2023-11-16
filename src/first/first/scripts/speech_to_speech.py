import os
import wave
import shutil
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

def encrypt_audio(secret_audio, key):
    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(secret_audio)
    return ciphertext, cipher.nonce

def decrypt_audio(encrypted_audio, key, nonce):
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    secret_audio = cipher.decrypt(encrypted_audio)
    return secret_audio

def embed_audio(carrier_audio, encrypted_audio, output_audio, lsb_depth=1):
    with wave.open(carrier_audio, 'rb') as carrier:
        carrier_samples = list(carrier.readframes(carrier.getnframes()))

    for i in range(len(encrypted_audio)):
        for j in range(lsb_depth):
            carrier_samples[i] = (carrier_samples[i] & ~(1 << j)) | ((encrypted_audio[i] >> j) & 1)

    with wave.open(output_audio, 'wb') as output:
        output.setparams(carrier.getparams())
        output.writeframes(bytes(carrier_samples))

def process_audio_files(carrier_file_or_path, secret_file_or_path):
    # Paths to the audio files
    carrier_audio_path = 'media/carrier.wav'  # Corrected path
    secret_audio_path = 'media/secret.wav'    # Corrected path
    output_audio_path = 'media/output.wav'

    # Save uploaded files or copy provided files
    if isinstance(carrier_file_or_path, str):  # Check if it's a path
        shutil.copyfile(carrier_file_or_path, carrier_audio_path)
    else:  # It's an UploadedFile
        with open(carrier_audio_path, 'wb') as carrier_file_dest:
            for chunk in carrier_file_or_path.chunks():
                carrier_file_dest.write(chunk)

    if isinstance(secret_file_or_path, str):  # Check if it's a path
        shutil.copyfile(secret_file_or_path, secret_audio_path)
    else:  # It's an UploadedFile
        with open(secret_audio_path, 'wb') as secret_file_dest:
            for chunk in secret_file_or_path.chunks():
                secret_file_dest.write(chunk)

    # Encrypt and embed audio
    key = get_random_bytes(16)
    nonce = get_random_bytes(16)

    with open(secret_audio_path, 'rb') as file:
        secret_audio_data = file.read()
        encrypted_audio, nonce = encrypt_audio(secret_audio_data, key)

    embed_audio(carrier_audio_path, encrypted_audio, output_audio_path, lsb_depth=1)
    print("Output audio path:", os.path.abspath(output_audio_path))

    return output_audio_path

