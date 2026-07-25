import inspect

import analyzer
from analyzer import extract_future_scope, extract_title


def test_extract_title_reassembles_multiline_title():
    text = """Deep
Neural Networks for
Speech Recognition

Abstract
This paper introduces a new architecture for speech recognition.
"""

    title = extract_title(text)

    assert title == "Deep Neural Networks for Speech Recognition"


def test_extract_future_scope_detects_future_heading():
    text = """Abstract
This paper introduces a new architecture for speech recognition.

Future Scope
We will extend this work to multilingual speech recognition and mobile deployment.

References
"""

    future_scope = extract_future_scope(text)

    assert "multilingual speech recognition" in future_scope.lower()


def test_extract_title_stops_before_author_block_and_body_text():
    text = """Context-Based Fake News Detection using Graph Based Approach: A COVID-19 Use-case
CHANDRASHEKAR MUNIYAPPA∗, Independent Researcher, USA
DR. SIRISHA VELAMPALLI, UCEK, JNTU Kakinada, LTIMind Tree, India
In today’s digital world, fake news is spreading with immense speed.
"""

    title = extract_title(text)

    assert title == "Context-Based Fake News Detection using Graph Based Approach: A COVID-19 Use-case"


def test_extract_title_excludes_title_case_author_names():
    text = """Speech Recognition for Natural Human-Robot Interaction
Jane Doe, John Smith
Department of Robotics, Example University
Abstract
This paper surveys speech-based natural human-robot interaction.
"""

    assert extract_title(text) == "Speech Recognition for Natural Human-Robot Interaction"


def test_text_cleaning_preserves_title_line_breaks_and_repairs_joined_words():
    cleaned = analyzer.fix_all_text("Title of Paper\nJane Doe\nincludingmultimodal interactionaction")

    assert cleaned.splitlines()[:2] == ["Title of Paper", "Jane Doe"]
    assert "including multimodal interaction action" in cleaned


def test_text_cleaning_repairs_languagebased_and_other_joined_words():
    cleaned = analyzer.fix_all_text("languagebased natural human-robot interaction")

    assert "language-based" in cleaned.lower()
    assert "human-robot" in cleaned.lower()


def test_extract_title_is_defined_once():
    source = inspect.getsource(analyzer)

    assert source.count("def extract_title(") == 1
