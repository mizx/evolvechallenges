'use strict'

var evolveServices = angular.module('evolveServices', ['ngResource']);

evolveServices.factory('Challenge', ['$resource',
	function($resource) {
		return $resource('/api/challenge/:challengeId.json', {}, {
			query: {
				method: 'GET',
				params: {challengeId: 'challenges'},
				isArray: true
			}
		});
	}
]);