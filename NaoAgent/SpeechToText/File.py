from faster_whisper import WhisperModel

# Run on GPU with FP16

# or run on GPU with INT8
# model = WhisperModel(model_size, device="cuda", compute_type="int8_float16")
# or run on CPU with INT8
# model = WhisperModel(model_size, device="cpu", compute_type="int8")
def AudioToText(audio_path = "C:\\Users\\Windows 10\\Desktop\\NaoAgent\\utils\\Grabación.m4a"):
    text = ""
    model_size = "small"

    model = WhisperModel(model_size, device="cuda", compute_type="float32")

    segments, info = model.transcribe(audio_path, beam_size=5)

    print("Detected language '%s' with probability %f" % (info.language, info.language_probability))

    for segment in segments:
        print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))
        text = text + segment.text
    return text