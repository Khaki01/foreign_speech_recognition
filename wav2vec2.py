# !pip install transformers
# !pip install datasets
import soundfile as sf
import librosa
import torch
from datasets import load_dataset
from transformers import Wav2Vec2ForCTC, Wav2Vec2Tokenizer

# load pretrained model
tokenizer = Wav2Vec2Tokenizer.from_pretrained("facebook/wav2vec2-base-960h")
model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-base-960h")

# load our audio file
audio, rate = librosa.load("audio/testaudio.wav", sr=16000)


#librispeech_samples_ds = load_dataset("patrickvonplaten/librispeech_asr_dummy", "clean", split="validation")

# load audio
#audio_input, sample_rate = sf.read(librispeech_samples_ds[0]["file"])

# pad input values and return pt tensor
input_values = tokenizer(audio, return_tensors="pt").input_values

# INFERENCE

# retrieve logits & take argmax
logits = model(input_values).logits
predicted_ids = torch.argmax(logits, dim=-1)

# transcribe
transcription = tokenizer.batch_decode(predicted_ids)[0]
print(transcription)
