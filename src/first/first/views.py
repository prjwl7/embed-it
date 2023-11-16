from django.http import HttpResponse
from django.shortcuts import render
from .scripts.speech_to_speech import process_audio_files
from django.core.files.storage import FileSystemStorage


def home_view(request, *args, **kwargs):
    return render(request, 'home.html', {});
def speech_view(request, *args, **kwargs):
    return render(request, 'speech.html')
def output_speech(request):
    if request.method == 'POST':
        # Handle file uploads
        carrier_file = request.FILES['carrier']
        secret_file = request.FILES['secret']

        # Save uploaded files
        fs = FileSystemStorage()
        carrier_filename = fs.save('media/carrier.wav', carrier_file)
        secret_filename = fs.save('media/secret.wav', secret_file)

        # Process audio files
        output_audio_path = process_audio_files(carrier_filename, secret_filename)

        return render(request, 'output_speech.html', {'output_audio_path': output_audio_path})

    return render(request, 'output_speech.html')