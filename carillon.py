from psynet.js_synth import InstrumentTimbre

samples = {}

for octave in [0, 1, 2, 3, 4]:
    for pitch_class in ["c", "c#", "d", "d#", "e", "f", "f#", "g", "g#", "a", "a#", "b"]:
        i = len(samples) + 1

        if i > 50:
            break

        our_label = f"{pitch_class.upper()}{octave}"

        if octave == 0:
            url = f"{i}-{pitch_class.upper()}{octave}.mp3"
        else:
            url = f"{i}-{pitch_class.lower()}{octave}.mp3"

        url = url.replace("#", "%23")  # URL-encoding the hash symbol

        if octave == 0 and pitch_class == "c#":
            pass
        else:
            samples[our_label] = url


carillon_timbre = InstrumentTimbre(
    type="carillon",
    samples=samples,
    base_url="/static/westerkerk-carillon-sample-library/mp3/",
)
