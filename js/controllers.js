'use strict'

var evolveControllers = angular.module('evolveControllers', []);

evolveControllers.controller('ChallengeListCtrl', ['$scope', 'Challenge',
	function($scope, Challenge) {
		$scope.challenges = Challenge.query();
		$scope.orderProp = 'end';
	}]);

evolveControllers.controller('ChallengeDetailCtrl', ['$scope', '$routeParams', 'Challenge',
	function($scope, $routeParams, Challenge) {
		$scope.challenge = Challenge.get({challengeId: $routeParams.challengeId}, function(challenge) {
			$scope.challengeName = challenge.name;
			$scope.challengeSlug = challenge.slug;
			$scope.challengeId = challenge.id;
	});
	
	$scope.setName = function(name) {
		$scope.challengeName = name;
	}
}]);