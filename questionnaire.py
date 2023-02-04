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
