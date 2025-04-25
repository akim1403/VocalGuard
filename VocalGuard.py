import threading
import queue
import speech_recognition as sr
# from collections import deque  # Not currently used, but could be helpful for duplicate filtering

# Queue used to store audio clips that are recorded
audio_queue = queue.Queue()

# List of scam-related keywords or phrases to detect in speech
SCAM_WORDS = [
    "bank account", "password", "credit card", 
    "tax", "urgent", "immediately", "verify", "account",
    "suspended", "locked", "refund", "prize", "winner", "free",
    "gift card", "Amazon", "Microsoft", "Apple", "PayPal",
    "password", "login", "credentials", "overdue", "payment",
    "debt", "fraud", "arrest", "warrant", "lawsuit", "legal",
    "immediate action", "click", "link", "website", "congratulations",
    "selected", "lottery", "inheritance", "investment", "opportunity"
]

# Global counter to keep track of the number of scam words detected
scam_word_count = 0

# Initialize the recognizer and microphone objects from the speech_recognition module
recognizer = sr.Recognizer()
mic = sr.Microphone()

def record_audio():
    """
    Continuously records audio from the microphone
    and puts the captured audio segments into the audio queue.
    Runs in a separate thread.
    """
    with mic as source:
        # Adjusts for background noise to improve recognition accuracy
        recognizer.adjust_for_ambient_noise(source)
        print("Listening continuously with 4 recognition threads... Speak now!")
        
        while True:
            try:
                # Capture audio indefinitely (until a pause is detected)
                audio = recognizer.listen(source, phrase_time_limit=None)
                # Place the recorded audio into the queue for processing
                audio_queue.put(audio)
            except Exception as e:
                print(f"Error recording audio: {e}")

def recognize_audio(thread_id):
    """
    Continuously takes audio from the queue and attempts to recognize speech using Google Speech API.
    If scam-related words are detected in the text, it flags them.
    Each instance runs in its own thread.
    """
    global scam_word_count  # Enables function to update global scam word count
    
    while True:
        try:
            # Retrieve the next audio clip from the queue
            audio = audio_queue.get()

            # Convert the audio to text using Google's Speech Recognition API
            text = recognizer.recognize_google(audio).lower()

            # Check for presence of any scam-related keywords in the text
            detected_scam_words = []
            for word in SCAM_WORDS:
                if word.lower() in text:
                    detected_scam_words.append(word)
                    scam_word_count += 1  # Increment global count for each match
            
            # If any scam words were found, print a warning message
            if detected_scam_words:
                output = f" SCAM ALERT: Detected ({', '.join(detected_scam_words)})"
                print(output, end="", flush=True)
            
        except queue.Empty:
            # If queue is empty, just retry
            continue
        except sr.UnknownValueError:
            # If the speech was unintelligible
            print(f"\n[Thread {thread_id}] [Could not understand]")
        except sr.RequestError as e:
            # If there was an issue reaching the speech recognition API
            print(f"\n[Thread {thread_id}] [Error: {e}]")
        except Exception as e:
            # Catch-all for any unexpected issues
            print(f"\n[Thread {thread_id}] [Unexpected error: {e}]")

# Start the audio recording thread (daemon means it will automatically stop when the main program exits)
recording_thread = threading.Thread(target=record_audio, daemon=True)
recording_thread.start()

# Start 4 separate threads for processing and recognizing speech
for i in range(4):
    thread = threading.Thread(target=recognize_audio, args=(i+1,), daemon=True)
    thread.start()

# Keep the script running until interrupted by user (Ctrl+C)
try:
    while True:
        # Display the number of scam words detected so far every 5 seconds
        threading.Event().wait(5)
        print(f"\n\n Total scam words detected so far: {scam_word_count}\n")
except KeyboardInterrupt:
    # Graceful shutdown
    print(f"\n Stopping all threads... Final scam word count: {scam_word_count}")
