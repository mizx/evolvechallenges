'use strict'

var evolveControllers = angular.module('evolveControllers', []);

evolveControllers.controller('ChallengeListCtrl', ['$rootScope', '$scope', 'Challenge',
	function($rootScope, $scope, Challenge) {
		$scope.challenges = Challenge.query();
		$rootScope.title = 'Evolve Challenges';
	}]);

evolveControllers.controller('ChallengeDetailCtrl', ['$rootScope', '$scope', '$routeParams', 'Challenge',
	function($rootScope, $scope, $routeParams, Challenge) {
		$scope.challenge = Challenge.get({challengeSlug: $routeParams.challengeSlug}, function(challenge) {
			$scope.challengeName = challenge.name;
			$scope.challengeSlug = challenge.slug;
			$scope.challengeId = challenge.id;
			$rootScope.title = challenge.name;
	});
	
	$scope.setName = function(name) {
		$scope.challengeName = name;
	}
}]);