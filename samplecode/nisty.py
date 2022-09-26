import json
from os import fspath, getcwd
from pathlib import Path

import electos.datamodels.nist.models.edf as edf
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.platypus import (
    Flowable,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)
from reportlab.rl_config import defaultPageSize

PAGE_HEIGHT = defaultPageSize[1]
PAGE_WIDTH = defaultPageSize[0]
styles = getSampleStyleSheet()
styleN = styles["Normal"]
styleH = styles["Heading1"]


def report(edf_file):
    with open(edf_file) as input:
        data = json.load(input)
    return edf.ElectionReport(**data)


def string_of(internationalized_text):
    return internationalized_text.text[0].content


def elections(report):
    return report.election


def gp_units(report):
    return report.gp_unit


def parties(report):
    return report.party


def offices(report):
    return report.office


def people(report):
    return report.person


def election_name(election):
    return string_of(election.name)


def contests(election):
    return election.contest


def candidate_contests(election):
    c_type = "ElectionResults.CandidateContest"
    f = filter(lambda c: c.model__type == c_type, contests(election))
    return list(f)


def ballot_measures(election):
    c_type = "ElectionResults.BallotMeasureContest"
    f = filter(lambda c: c.model__type == c_type, contests(election))
    return list(f)


def ballot_styles(election):
    return election.ballot_style


def ballot_id(ballot_style):
    return ballot_style.external_identifier[0].value


def selections(contest):
    return contest.contest_selection


def candidate_ids(contest):
    return [s.candidate_ids[0] for s in selections(contest) if s.candidate_ids]


def candidate(candidate_id, election):
    f = filter(lambda c: c.model__id == candidate_id, election.candidate)
    return list(f)[0]


def ballot_name(candidate):
    return string_of(candidate.ballot_name)


def ordered_contests(ballot_style):
    return [
        c
        for c in ballot_style.ordered_content
        if c.model__type == "ElectionResults.OrderedContest"
    ]


def flatten(lst):
    return [item for sublist in lst for item in sublist]


def contest_by_id(report, id):
    contests = flatten([e.contest for e in report.election])
    f = filter(lambda x: x.model__id == id, contests)
    return list(f)


def contests(ballot, edf):
    # import pdb; pdb.set_trace()
    contest_ids = [c.contest_id for c in ordered_contests(ballot)]
    return flatten([contest_by_id(edf, id) for id in contest_ids])


class BallotMaker:
    """top-level generator"""

    def __init__(self, edf_file):
        with open(edf_file) as input:
            data = json.load(input)

        self.edf = edf.ElectionReport(**data)

        base_dir = Path(getcwd()).parent
        self.ballot_path = Path.joinpath(base_dir, "ballots")
        self._ballots = []

    @property
    def ballots(self):
        if not self._ballots:
            self._ballots = [
                Ballot(style, self.edf)
                for style in self.edf.election[0].ballot_style
            ]
        return self._ballots

    def make_ballots(self):
        for ballot in self.ballots:
            fpath = self.ballot_path / Path(ballot.identifier).with_suffix(
                ".pdf"
            )
            doc = SimpleDocTemplate(fspath(fpath), pagesize=letter)
            doc.build(ballot.story)


class Ballot:
    def __init__(self, style, edf):
        self.style = style
        self.identifier = self.style.external_identifier[0].value
        self.edf = edf
        self.contests = [
            Contest(contest, edf) for contest in contests(style, edf)
        ]
        self._story = []

    @property
    def story(self):
        if not self._story:
            election_name = string_of(self.edf.election[0].name)
            self._story.append(Paragraph(election_name, styleH))
            self._story.append(Spacer(1, 0.2 * inch))
            precinct_label = self.identifier
            # import pdb; pdb.set_trace()
            self._story.append(Paragraph(precinct_label, styleH))
            self._story.append(Spacer(1, 0.2 * inch))
            for contest in self.contests:
                self._story.append(Paragraph(contest.ballot_title, styleH))
                self._story.append(Spacer(1, 0.2 * inch))
                self._story.append(Table(contest.choices))
                self._story.append(Spacer(1, 0.2 * inch))
        return self._story


class Contest:
    def __init__(self, contest, edf):
        self.contest = contest
        self.edf = edf
        self.id = contest.model__id
        self._choices = []
        self.ballot_title = contest.name

    @property
    def choices(self):
        """The array of choices for the contest.

        The array is generated lazily from the contest_selections
        array in the contest object.
        [ [marker_0, 'Yes'],
          [marker_1, 'No'],
          [marker_2, 'Jane Jetson'],
          [marker_3, 'write-in'],
          [' ', <textbox>] ]

        Each marker is associated with the id of the selection.
        In the write-in case, two 'choices' are generated: one
        for the write-in choice (the id of the write-in selection);
        the other a text box for the written-in name; this widget
        always has an identifier that is the write-in selection id
        with '_text' appended (e.g., 'writeInChoice01_text').
        """
        if not self._choices:
            for selection in self.contest.contest_selection:
                #                marker = VoteChoiceRadio(self.id, selection.model__id)
                marker = VoteChoiceCheck(self.id, selection.model__id)

                if (
                    selection.model__type
                    == "ElectionResults.BallotMeasureSelection"
                ):
                    self._choices.append(
                        [marker, selection.selection.text[0].content]
                    )
                elif selection.is_write_in:
                    self._choices.append([marker, "write-in"])
                    self._choices.append(
                        [
                            "",
                            WriteInTextBox(
                                "_".join((selection.model__id, "text"))
                            ),
                        ]
                    )
                else:
                    candidate_names = [
                        string_of(
                            candidate(
                                candidate_id, self.edf.election[0]
                            ).ballot_name
                        )
                        for candidate_id in selection.candidate_ids
                    ]
                    label = " and ".join(candidate_names)
                    self._choices.append([marker, label])
        return self._choices


class OrderedContent:
    def __init__(self, content, edf):
        self.content = content
        self.edf = edf


class Candidate:
    def __init__(self, candidate, edf):
        self.candidate = candidate
        self.edf = edf


style = getSampleStyleSheet()["BodyText"]


class VoteChoiceCheck(Flowable):
    def __init__(self, contest_id, selection_id):
        super().__init__()
        self.contest_id = contest_id
        self.selection_id = selection_id
        self.size = 12
        self.checked = False
        self.buttonStyle = "check"

    def draw(self):
        self.canv.saveState()
        form = self.canv.acroForm
        form.checkbox(
            name=self.selection_id,
            buttonStyle=self.buttonStyle,
            relative=True,
            size=self.size,
        )

        self.canv.restoreState()


class VoteChoiceRadio(Flowable):
    def __init__(self, contest_id, selection_id):
        super().__init__()
        self.name = contest_id
        self.value = selection_id
        self.buttonStyle = "check"

    def draw(self):
        self.canv.saveState()
        form = self.canv.acroForm
        form.radio(name=self.name, value=self.value, size=12, relative=True)
        self.canv.restoreState()


class WriteInTextBox(Flowable):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def draw(self):
        self.canv.saveState()
        form = self.canv.acroForm
        form.textfield(
            name=self.name, maxlen=60, height=12, width=65, relative=True
        )
        self.canv.restoreState()


# for_spacely = VoteChoiceRadio("mayor", "spacely")
# for_cogswell = VoteChoiceRadio("mayor", "cogswell")

# data = [[for_spacely, "Cosmo Spacely"],
#         [for_cogswell, "Spencer Cogswell"]]
# Story = [Table(data)]
# doc.build(Story)

edf_file = "/Users/cwulfman/projects/nisty/tests/test_case_1.json"
mayor_contest_id = "recIj8OmzqzzvnDbM"
maker = BallotMaker(edf_file)
# ballot = maker.ballots[0]
# doc = SimpleDocTemplate("hello.pdf")
# doc.build(ballot.story)

# ballot.write_election_name()
# ballot.draw_table()
# ballot.build_doc()
