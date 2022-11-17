from psynet.js_synth import InstrumentTimbre

carillon_timbre = InstrumentTimbre(
    type="carillon",
    samples={
        "C0": "1-C0.mp3",
        "D0": "2-D0.mp3",
    },
    base_url="/static/westerkerk-carillon-sample-library/mp3/",
    # base_url="https://s3.eu-west-1.amazonaws.com/media.pmcharrison.com/music/westerkerk-carillon-sample-library/mp3/",
)
