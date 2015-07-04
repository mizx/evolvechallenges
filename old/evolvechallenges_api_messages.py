from protorpc import messages

class ChallengeMessage(message.Message):
	state = messages.StringField(1)