'use strict';

var app = angular.module('evolveApp', ['ngRoute']);

app.config(function($routeProvider, $locationProvider) {
	$routeProvider.
		when('/', {
			controller: 'MainCtrl',
			templateUrl: '/partials/main.html'
		}).
		when('/challenges', {
			controller: 'ChallengeListCtrl',
			templateUrl: '/partials/challenge_list.html'
		}).
		when('/challenge/:challengeSlug', {
			controller: 'ChallengeDetailCtrl',
			templateUrl: '/partials/challenge_detail.html'
		}).
		otherwise({
			redirectTo: '/challenges'
		});
	$locationProvider.html5Mode(true);
});

app.controller('ChallengeListCtrl', function($scope, $rootScope, $log, $http, $routeParams, $location, $route) {
	$http.get('/api/challenges.json').success(function(data) {
		$scope.challenges = data;
	});
	$scope.orderProp = 'num';
});

app.controller('ChallengeDetailCtrl', function($scope, $rootScope, $log, $http, $routeParams, $location, $route) {
	$http.get('/api/challenge/' + $routeParams.challengeSlug + '.json').success(function(data) {
		$scope.challenge = data;
	});
});

app.controller('MainCtrl', function($scope, $rootScope, $log, $http, $routeParams, $location, $route) {
	
});