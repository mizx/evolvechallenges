'use strict'

var evolveServices = angular.module('evolveServices', ['ngResource']);

evolveServices.factory('Challenge', ['$resource',
	function($resource) {
		return $resource('/api/challenge/:challengeSlug.json', {}, {
			query: {
				method: 'GET',
				params: {challengeSlug: 'all'},
				isArray: true
			}
		});
	}
]);