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
    
    
    # To check the input file size if it does have some data
    file_size = os.path.getsize(carrier_audio)

    # Check if the file size is 0
    if file_size == 0:
        # Display a dialog box in HTML
        html_dialog = """
        <script>
            alert("The carrier file is empty!");
        </script>
        """
        
    with wave.open(carrier_audio, 'rb') as carrier:
        carrier_samples = list(carrier.readframes(carrier.getnframes()))

    print("Carrier Samples Collected!!")
    for i in range(len(encrypted_audio)):
        for j in range(lsb_depth):
            carrier_samples[i] = (carrier_samples[i] & ~(1 << j)) | ((encrypted_audio[i] >> j) & 1)

    with wave.open(output_audio, 'wb') as output:
        output.setparams(carrier.getparams())
        output.writeframes(bytes(carrier_samples))

def process_audio_files(carrier_file_name, secret_file_name):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    common_parent_dir = os.path.abspath(os.path.join(script_dir, '..', '..'))


    folder_path = os.path.join(common_parent_dir, 'media', 'uploads')
    carrier_audio_path = os.path.join(folder_path, carrier_file_name)
    secret_audio_path = os.path.join(folder_path, secret_file_name)

    output_folder_path = os.path.join(common_parent_dir, 'media', 'output')
    os.makedirs(output_folder_path, exist_ok=True)

    output_audio_filename = 'output.wav'
    output_audio_path = os.path.join(output_folder_path, output_audio_filename)

    print(carrier_audio_path)
    
    if not (os.path.exists(carrier_audio_path) and os.path.exists(secret_audio_path)):
        print("Error: Missing audio files in the specified folder.")
        return None
    else:
        print("Files accessed!!")

    key = get_random_bytes(16)
    nonce = get_random_bytes(16)

    with open(secret_audio_path, 'rb') as secret_file:
        secret_audio_data = secret_file.read()
        encrypted_audio, nonce = encrypt_audio(secret_audio_data, key)

    print(len(encrypted_audio))
    embed_audio(carrier_audio_path, encrypted_audio, output_audio_path, lsb_depth=1)
    
    # Get the relative path from the 'templates' directory to 'output_audio_path'
    relative_output_audio_path = os.path.relpath(output_audio_path, os.path.join(common_parent_dir, 'templates'))
    
    print("Relative Output Audio Path:", relative_output_audio_path)
    
    return relative_output_audio_path


