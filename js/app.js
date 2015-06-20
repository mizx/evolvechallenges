'use strict'

var evolveApp = angular.module('evolveApp', [
	'ngRoute',
	'evolveControllers',
	'evolveServices'
]);

evolveApp.config(['$routeProvider',
	function($routeProvider) {
		$routeProvider.
			when('/challenges', {
				templateUrl: 'partials/challenge-list.html',
				controller: 'ChallengeListCtrl'
			}).
			when('/challenges/:challengeId', {
				templateUrl: 'partials/challenge-detail.html',
				controller: 'ChallengeDetailCtrl'
			}).
			otherwise({
				redirectTo: '/challenges'
			});
	}
]);