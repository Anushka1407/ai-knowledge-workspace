from unittest.mock import Mock

from app.services.document_intelligence_service import DocumentIntelligenceService


def test_analyze_calls_document_intelligence_and_maps_result():
    page = Mock(page_number=1, width=8.5, height=11, unit="inch", lines=[Mock()])
    paragraph = Mock(content="A heading", role="title")
    poller = Mock(result=Mock(return_value=Mock(pages=[page], paragraphs=[paragraph])))
    client = Mock(begin_analyze_document=Mock(return_value=poller))
    service = object.__new__(DocumentIntelligenceService)
    service.client = client

    result = service.analyze(b"pdf bytes")

    client.begin_analyze_document.assert_called_once()
    assert result["pages"][0]["page_number"] == 1
    assert result["paragraphs"] == [{"content": "A heading", "role": "title"}]