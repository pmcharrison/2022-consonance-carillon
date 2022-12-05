import librosa
import numpy as np
import pandas as pd
import soundfile as sf

from psynet.utils import log_time_taken


def freq_to_midi(frequency, ref=440):
    return 69 + np.log2(frequency / ref) * 12


assert freq_to_midi(440) == 69


def import_carillon_samples():
    df = pd.read_csv("carillon_samples.csv")
    df["midi"] = freq_to_midi(df["f0"])
    df["filename"] = df["id"] + ".wav"
    df["path"] = "static/westerkerk-carillon-samples/wav/" + df["filename"]

    # df["url"] = [f.replace("#", "%23") for f in df["filename"]]  # Not necessary with processing on back end

    df = df.iloc[17:32]  # Only keep items 18-32 inclusive
    assert list(df.id)[0] == "18-f#1"
    assert list(df.id)[-1] == "32-g#2"

    return {
        midi: url for midi, url in zip(df["midi"], df["path"])
    }


carillon_samples = import_carillon_samples()

@log_time_taken
def synth_stimulus(path, lower_pitch, upper_pitch):
    sample_rate = 44100

    pitches = [lower_pitch, upper_pitch]
    chosen_samples = [choose_sample(target_pitch, carillon_samples) for target_pitch in pitches]
    waveforms = [make_waveform(chosen_sample, sample_rate) for chosen_sample in chosen_samples]
    mixed_waveform = mix_waveforms(waveforms)
    sf.write(path, mixed_waveform, sample_rate)


def choose_sample(target_pitch, carillon_samples):
    assert len(carillon_samples) > 0
    best_sample = None
    for sample_pitch, sample_path in carillon_samples.items():
        if best_sample is None or abs(best_sample["sample_pitch"] - target_pitch) > abs(sample_pitch - target_pitch):
            best_sample = dict(
                target_pitch=target_pitch,
                sample_pitch=sample_pitch,
                sample_path=sample_path
            )
    return best_sample


def make_waveform(chosen_sample, expected_sample_rate):
    audio, sample_rate = librosa.load(chosen_sample["sample_path"], sr=None)
    assert sample_rate == expected_sample_rate
    return librosa.effects.pitch_shift(
        audio,
        sr=sample_rate,
        n_steps=chosen_sample["target_pitch"] - chosen_sample["sample_pitch"]
    )


def mix_waveforms(waveforms):
    n_waveforms = len(waveforms)
    n_samples = max([len(waveform) for waveform in waveforms])
    padded_waveforms = [librosa.util.fix_length(waveform, size=n_samples) for waveform in waveforms]
    return np.stack(padded_waveforms).sum(axis = 0) / n_waveforms


# with tempfile.NamedTemporaryFile(suffix=".wav") as f:
#     synth_stimulus(f.name, 60, 67)
#     IPython.display.Audio(f.name)