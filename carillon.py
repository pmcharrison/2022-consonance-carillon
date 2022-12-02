import numpy as np
import pandas as pd

from psynet.js_synth import InstrumentTimbre


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

carillon_samples = {
    midi: url for midi, url in zip(df["midi"], df["url"])
}

# TODO - Move outside ToneJS for this and instead pitch shift using librosa.effects.resample