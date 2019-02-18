import endpoints

from protorpc import messages
from protorpc import remote
from data import Programming_Languages

package = 'Resume'

# property class for messages
class Properties(messages.Message):
    number = messages.IntegerField(1, variant=messages.Variant.INT32)
    text = messages.StringField(2)
    image_key = messages.StringField(3)

# Data classs for data to be sent
class Data(messages.Message):
    data = messages.MessageField(Properties, 1, repeated=True)

PL = Data()

# Backend API
@endpoints.api(name='resume', version='v1')
class ResumeApi(remote.Service):

  QUERY_ID = endpoints.ResourceContainer(text = messages.StringField(1))
  
# method takes programming language selected and returns corresponding information about it
  @endpoints.method(QUERY_ID, Data,
                    path='pl/{text}', http_method='GET',
                    name='list.pL')
  def programming_languages(self, request):
    try:
        PL = Data()
        PL.data.append(Properties(text=Programming_Languages.get_by_id(request.text).text))
        return PL

    except (IndexError, TypeError):
      raise endpoints.NotFoundException('%s not found.' %
                                        (request.text))

APPLICATION = endpoints.api_server([ResumeApi])
