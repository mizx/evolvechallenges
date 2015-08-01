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
			redirectTo: '/'
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
		$scope.challenge['percent'] = $scope.challenge.progress / $scope.challenge.goal * 100;
		$scope.challenge.percent = ($scope.challenge.percent > 100) ? 100.0 : $scope.challenge.percent;
		$rootScope.htmlPage = {background: "url('" + $scope.challenge.background + "')"};
	});
});

app.controller('MainCtrl', function($scope, $rootScope, $log, $http, $routeParams, $location, $route) {
	$http.get('/api/challenges.json').success(function(data) {
		$scope.challenges = data;
	});
});

app.filter('moment', function () {
	return function (input, momentFn) {
		var args = Array.prototype.slice.call(arguments, 2),
			momentObj = moment(input);
		return momentObj[momentFn].apply(momentObj, args);
	}
});