# Real-Time Scam Word Detection using Speech Recognition

This Python project listens to live microphone input, transcribes the speech using Google's Speech Recognition API, and detects scam-related words in real-time using multiple threads.

Example video of this program can be found on
https://youtu.be/tt9Rog0o_VU

## Features

-  **Real-time speech recognition** using your microphone
-  **Multithreaded processing** with 4 recognition threads
-  **Scam keyword detection** using a customizable list
-  Thread-safe audio queuing
-  Live scam word count display

## Requirements

- Python 3.6+
- `speechrecognition`
- `pyaudio` (for microphone access)

### Install Dependencies

```bash
pip install SpeechRecognition pyaudio
```

> If you have trouble installing `pyaudio` on some systems, try:
> 
> - Windows: `pip install pipwin` then `pipwin install pyaudio`
> - macOS: `brew install portaudio` then `pip install pyaudio`
> - Linux: Make sure `portaudio` dev headers are installed (`apt install portaudio19-dev`)

## How It Works

1. The program starts a microphone stream and continuously records audio.
2. Recorded audio is added to a shared thread-safe queue.
3. Four recognition threads pull audio from the queue and:
   - Transcribe the speech using Google Speech Recognition
   - Scan the text for any scam-related keywords
4. If scam words are detected, they're printed to the console with an alert.
5. A running tally of total scam words is printed every 5 seconds.

## Example Output

```
Listening continuously with 4 recognition threads... Speak now!

[Thread 2] your bank account has been suspended
SCAM ALERT: Detected (bank account, suspended)

Total scam words detected so far: 3
```

## Scam Words List

The default list includes terms like:

```
"bank account", "password", "social security", "IRS", "tax", 
"urgent", "verify", "locked", "refund", "free", "fraud", "click", etc.
```

You can expand or modify the `SCAM_WORDS` list in the Python file to match your own use case.

## Stopping the Program

Press `Ctrl + C` to stop the script gracefully and view the final scam word count.

## Future Improvements

- Process audio locally using Vosk
- Create a REST API where it receives the Audio data and proccesses it locally using Vosk
- That way audio can be sent from different applications such as android, IOS and PC
- Will create a react native application that can listen to the Phone's call and sends the audio data to my Python server to proccess
