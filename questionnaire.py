from dominate import tags

from psynet.demography.general import Age, Gender
from psynet.demography.gmsi import GMSI
from psynet.modular_page import ModularPage, TextControl
from psynet.page import InfoPage
from psynet.timeline import join


def introduction():
    html = tags.div()
    with html:
        tags.p(
            "Congratulations, you completed the listening part of this experiment!"
        )
        tags.p(
            "Before we finish, we just have a few more questions to ask you. ",
            "They should only take a couple of minutes to complete.",
        )
    return InfoPage(html, time_estimate=10)


def questionnaire():
    return join(
        introduction(),
        Age(),
        Gender(),
        GMSI(subscales=["Musical Training"]),
        feedback(),
    )


def feedback():
    return ModularPage(
        "feedback",
        "Do you have any feedback to give us about the experiment?",
        TextControl(one_line=False),
        bot_response="I am just a bot, I don't have any feedback for you.",
        save_answer="feedback",
        time_estimate=20,
    )


def debrief():
    html = tags.div()

    with html:
        tags.p(
            """
            Thank you for participating in this experiment. The purpose of the experiment is to collect data on how
            ‘pleasant’ pairs of bell sounds, such as the ones you have been listening to, are perceived to be.
            """
        )
        tags.p(
            """
            Pleasantness, or ‘consonance’, is one of a number of perceptual categories studied by music psychologists.
            Others include pitch (the note you hear when an instrument is played) and timbre (the quality of that note -
            whether it is ‘sweet’, ‘sharp’, ‘mellow’ and so on).
            """
        )
        tags.p(
            """
            For most Western instruments, these perceptual categories are fairly unambiguous - a group of people
            listening to the same note from the same instrument would likely agree about the sound’s pitch and timbre.
            However, due to their physical properties bells are often more perceptually challenging. For instance, you
            may have walked past a church while a bell was being rung and found it difficult to hum the note of the bell
            - or, put more scientifically, the bell’s pitch was somewhat ambiguous.
            """
        )
        tags.p(
            """
            While a lot of research has focussed on this phenomenon of pitch ambiguity in bells, comparatively little
            research has explored what happens perceptually when two bell sounds combine. Does the use of bell sounds
            affect the ‘pleasantness’ of note pairs? And if so, can we measure it objectively and use this knowledge to
            reliably predict how ‘pleasant’ any two given bell sounds will be? The data collected during this experiment
            will help to answer these questions.
            """
        )

    return InfoPage(html, time_estimate=25)
