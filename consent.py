from dominate.tags import div, p, span, h1, strong, ul, li, em

from psynet.consent import NoConsent
from psynet.modular_page import ModularPage, CheckboxControl
from psynet.page import InfoPage
from psynet.timeline import Module, join

information_sheet = div()

with information_sheet:
    h1("Participant information sheet")
    p(
        """
        This sheet is designed to give you information about what this experiment involves, as well as information about
        the research being undertaken more generally. Please read this carefully – your consent to participate will be
        required before the experiment begins.
        """
    )

    with p():
        strong("About this research.")
        span(
            """
            This project focusses on the carillon, a musical instrument native to the Low Countries, in which a large
            set of bells can be struck, either individually or simultaneously, via a keyboard. It is well-known that
            when bells are struck, their musical pitch can sometimes be unclear; however, precisely what is perceived
            when two bells with different pitches are struck simultaneously is not as well-researched, and is the
            subject of this project.
            """
        )

    with p():
        strong("What is the procedure?")
        span(
            """
            The experiment will take place online, in your web browser. You will be played a series of two-note ‘chords’
            that sound a bit like bells, and asked to rate the sounds as ‘pleasant’, on a scale ranging from 1 (‘completely
            disagree’) to 7 (‘completely agree’).
            """
        )


    with p():
        strong("Is participation voluntary?")
        span(
            """
            Participation is voluntary, and there is no penalty for refusal or withdrawal. Your consent to participate is
            required before the experiment can begin.
            """
        )

    with p():
        strong("Risks of taking part.")
        span(
            """
            There are no risks associated with taking part in this experiment.
            """
        )

    with p():
        strong("Benefits of taking part.")
        span(
            """
            You will be paid a fee for your participation, calculated to reach an approximate hourly rate of £10 per hour
            (assuming a ‘standard’ speed of completing the experiment).
            """
        )

    with p():
        strong("How long will the experiment last?")
        span(
            """
            The experiment generally takes approximately 20 minutes to complete. Your experiment could end early for a
            number of reasons, including but not limited to technical failure – in this case you will be paid pro rata for
            the portion of the experiment that you completed.
            """
        )

    with p():
        strong("Confidentiality.")
        span(
            """
            All data collected is anonymous, as no personal details (e.g. name, contact data) are collected at any stage.
            The data that is collected (‘pleasantness’ ratings) will be processed and presented as part of the experimental
            report.
            """
        )

    with p():
        strong("Ethical review.")
        span(
            """
            The project has been approved by the University of Cambridge Faculty of Music Ethics Committee.
            """
        )

    with p():
        strong("Contact for further information.")
        span(
            """
            If you have further queries about this experiment, please contact James MacConnachie at jmcm4@cam.ac.uk.
            """
        )


consent_form = div()

with consent_form:
    h1("Consent form")

    p(em("Please read the following text and select ‘Agree’ if you consent to these terms."))

    p(
        """
        I have been informed about the procedures to be used in this experiment and the tasks I need to perform, and I
        have agreed to take part. I understand that taking part in this experiment is voluntary and I can withdraw from
        the experiment at any time.
        """
    )

    p(
        """
        I understand that the data collected in this testing session will be stored on electronic media or on paper and
        it may contribute to scientific publications and presentations. I agree that the data can be made available
        anonymously for other researchers, both inside and outside the Centre for Music and Science and Faculty of
        Music. These data will not be linked to me as an individual.
        """
    )

consent = Module(
    "consent",
    join(
        NoConsent(),
        InfoPage(information_sheet, time_estimate=5),
        ModularPage(
            "consent_form",
            consent_form,
            CheckboxControl(
                choices=["I agree"],
                force_selection=True,
            ),
            time_estimate=10,
        ),
    )
)
