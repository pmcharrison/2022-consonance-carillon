import numpy as np
import pandas as pd

from psynet.js_synth import InstrumentTimbre

# samples = {}

# for octave in [0, 1, 2, 3, 4]:
#     for pitch_class in ["c", "c#", "d", "d#", "e", "f", "f#", "g", "g#", "a", "a#", "b"]:
#         i = len(samples) + 1
#
#         if i > 50:
#             break
#
#         our_label = f"{pitch_class.upper()}{octave}"
#
#         if octave == 0:
#             url = f"{i}-{pitch_class.upper()}{octave}.mp3"
#         else:
#             url = f"{i}-{pitch_class.lower()}{octave}.mp3"
#
#         url = url.replace("#", "%23")  # URL-encoding the hash symbol
#
#         if octave == 0 and pitch_class == "c#":
#             pass
#         else:
#             samples[our_label] = url


def freq_to_midi(frequency, ref=440):
    return 69 + np.log2(frequency / ref) * 12


assert freq_to_midi(440) == 69


df = pd.read_csv("carillon_samples.csv")
df["midi"] = freq_to_midi(df["f0"])
df["filename"] = df["id"] + ".mp3"
df["url"] = [f.replace("#", "%23") for f in df["filename"]]

df = df.iloc[17:32]  # Only keep items 18-32 inclusive
assert list(df.id)[0] == "18-f#1"
assert list(df.id)[-1] == "32-g#2"

samples = {
    f"{midi:.0f}": url for midi, url in zip(df["midi"], df["url"])
}

carillon_timbre = InstrumentTimbre(
    type="carillon",
    samples=samples,
    base_url="/static/westerkerk-carillon-samples/mp3/",
)


# TODO - Move outside ToneJS for this and instead pitch shift using librosa.effects.resample