import azure.cognitiveservices.speech as speechsdk
import os
from config import Config

def generate_speech(text, output_path, voice_name="en-US-JennyNeural"):
    """
    Generates speech from text using Azure TTS and saves it to output_path.
    Uses in-memory synthesis to avoid native file I/O issues in containers.
    """
    if not Config.AZURE_SPEECH_KEY or not Config.AZURE_SPEECH_REGION:
        raise ValueError("Azure Speech credentials are not configured.")

    # Validate output directory exists and is writable
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
    
    speech_config = speechsdk.SpeechConfig(
        subscription=Config.AZURE_SPEECH_KEY, 
        region=Config.AZURE_SPEECH_REGION
    )
    speech_config.speech_synthesis_voice_name = voice_name
    
    # Set output format to WAV
    speech_config.set_speech_synthesis_output_format(
        speechsdk.SpeechSynthesisOutputFormat.Riff16Khz16BitMonoPcm
    )
    
    # Use in-memory synthesis (no AudioOutputConfig) to avoid native file I/O issues
    synthesizer = speechsdk.SpeechSynthesizer(
        speech_config=speech_config, 
        audio_config=None  # Synthesize to memory
    )

    # Synthesize to memory
    result = synthesizer.speak_text_async(text).get()

    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        # Write audio data to file using Python's file I/O
        audio_data = result.audio_data
        with open(output_path, 'wb') as audio_file:
            audio_file.write(audio_data)
        return True
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        error_msg = f"Speech synthesis canceled: {cancellation_details.reason}"
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            error_msg += f" - Error details: {cancellation_details.error_details}"
        print(error_msg)
        raise Exception(error_msg)
    
    return False
