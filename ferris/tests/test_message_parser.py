from lib import WithTestBed
from ferris import Model, ndb, messages
from ferris.core.bunch import Bunch
from ferris.core.request_parsers import MessageParser
from ferris.core.view import MessageView
from ferris.core.event import NamedEvents
from protorpc import protojson
import json


class Widget(Model):
    title = ndb.StringProperty(required=True)
    content = ndb.TextProperty()


class TestMessageParserAndView(WithTestBed):

    def testMessageParser(self):
        WidgetMessage = messages.model_message(Widget)

        message = WidgetMessage(title='The Doctor', content='Time Lord')
        request = Bunch(body=unicode(protojson.encode_message(message)))

        parser = MessageParser().process(request, WidgetMessage)

        assert parser.validate()
        assert parser.container == message

    def testMessageView(self):
        WidgetMessage = messages.model_message(Widget)
        controller = Bunch(events=NamedEvents(), response=Bunch())
        view = MessageView(controller)

        view.context['data'] = WidgetMessage(title='Bad Wolf', content='Rose Tyler')

        result = view.render()

        assert result.content_type == 'application/json'
        assert result.unicode_body

        data = json.loads(result.unicode_body)
        assert data['title'] == 'Bad Wolf'
        assert data['content'] == 'Rose Tyler'
