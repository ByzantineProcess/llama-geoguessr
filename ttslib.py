from io import BytesIO
import numpy as np
import scipy.io.wavfile
# import torch
ckpt_converter = 'checkpoints_v2/converter' # cant remember what this does, dont want to remove it
device = "cuda:0" # change if you need to

from melo.api import TTS

model = TTS(language="EN", device=device)

# Speed is adjustable
speed = 1.0
def tts_en(text:str):
    
    speaker_ids = model.hps.data.spk2id
    
    for speaker_key in speaker_ids.keys():
        print(f'Processing {speaker_key}\n')
        if speaker_key != 'EN-BR':
            continue
        # src_path = f'{output_dir}/{speaker_key}.wav'
        speaker_id = speaker_ids[speaker_key]
        speaker_key = speaker_key.lower().replace('_', '-')
        
        # source_se = torch.load(f'checkpoints_v2/base_speakers/ses/{speaker_key}.pth', map_location=device)
        res = model.tts_to_file(text, speaker_id, output_path=None, speed=speed)
        wav_norm = res * (32767 / max(0.01, np.max(np.abs(res))))
        wav_norm = wav_norm.astype(np.int16)
        wav_buffer = BytesIO()
        scipy.io.wavfile.write(wav_buffer, model.hps.data.sampling_rate, wav_norm)
        wav_buffer.seek(0)
        return wav_buffer
