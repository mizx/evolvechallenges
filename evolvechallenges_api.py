import endpoints
from protorpc import messages
from protorpc import message_types
from protorpc import remote

package = 'Evolve'

class Challenge(messages.Message):
    id = messages.IntegerField(1)
	name = messages.StringField(2)

class ChallengeCollection(messages.Message):
	items = messages.MessageField(Challenge, 1, repeated=True)

STORED_CHALLENGES = ChallengeCollection(items=[
	Challenge(message='val'),
	Challenge(message='hunter'),
])

@endpoints.api(name='evolve', version='v1')
class ChallengeApi(remote.Service):

	@endpoints.method(message_types.VoidMessage, ChallengeCollection, 
						path='challenges', http_method='GET',
						name='challenges.listChallenges')
	def challenges_list(self, unused_request):
		return STORED_CHALLENGES
	
	ID_RESOURCE = endpoints.ResourceContainer(
		message_types.VoidMessage,
		id=messages.IntegerField(1, variant=messages.Variant.INT32)
	)
	
	@endpoints.method(ID_RESOURCE, Challenge,
						path='challenges/{id}', http_method='GET',
						name='challenges.getChallenge')
	def challenge_get(self, request):
		try:
			return STORED_CHALLENGES.items[request.id]
		except (IndexError, TypeError):
			raise endpoints.NotFoundException('Challenge %s not found.' % (request.id))

APPLICATION = endpoints.api_server([ChallengeApi])