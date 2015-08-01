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
		when('/faq', {
			controller: 'FaqCtrl',
			templateUrl: '/partials/faq.html'
		}).
		otherwise({
			redirectTo: '/'
		});
	$locationProvider.html5Mode(true);
});

app.controller('ChallengeListCtrl', function($scope, $rootScope, $log, $http, $routeParams, $location, $route) {
	$rootScope.htmlPage = {backgroundImage: "url('/img/bg/default.png')"};
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
		$rootScope.htmlPage = {backgroundImage: "url('" + $scope.challenge.background + "')"};
	});
});

app.controller('MainCtrl', function($scope, $rootScope, $log, $http, $routeParams, $location, $route) {
	$http.get('/api/challenges.json').success(function(data) {
		$scope.challenges = data;
	});
});

app.controller('FaqCtrl', function($scope, $rootScope, $log, $http, $routeParams, $location, $route) {
	$rootScope.htmlPage = {backgroundImage: "url('/img/bg/faq.jpg')"};
	$scope.questions = [
		{
			q: "Do you have to play as specific characters?",
			a: "No. You just need to login and play at least one online game that connects to an official game server and you're eligible. Encourage your team mates to partake in challenges though!"
		},
		{
			q: "We finished the challenge! When do I get my skins?!",
			a: "Officially you will have your skins by the following Thursday. With that being said, we usually see them by Monday or Tuesday."
		},
		{
			q: "Cool site! How often does it update?",
			a: "The site pulls information from an API from Turtle Rock Studios. Their API usually updates every fifteen minutes (plus or minus a couple minutes), so my site refreshes no more than five minutes after."
		},
		{
			q: "Why is the data different from what TRS announces?",
			a: "While it appears Turtle Rock Studios uses EvolveChallenges.com/their API to make progress announcements, they run a final official tally after every challenge the following Monday which may differ what this site cuts off. This site will use any data that is given from the API up to 30 minutes after the official challenge end time."
		},
		{
			q: "Does this site provide information for all consoles, or just specific ones?",
			a: "It includes them all: PC, XBOX, PS3"
		},
		{
			q: "I want to stay up to date! Do I need to spam the f*** out of my f5 key?",
			a: "Nope! The site will automatically update itself every 15 minutes for you. You focus on completing the challenges, I'll make sure the site is up-to-date next time you glance over and take a peak."
		},
		{
			q: "We lost percent! What happened? (Or if this happens...)",
			a: "Community Challenges were not a part of Evolve's original plan, and their API was implemented for internal use. Mistakes happen. If the progress or data jumps in any way, it's because there was an error of some kind. If the data does change, my site will automatically recognize these changes when they occur.<br><br>An example of this is Hyde's flamethrower challenge. The starting timezone was set correctly, but was set for the wrong timezone, therefore 7 hours of data was included that should not have been included. This was fixed the next morning causing a huge spike in the graph."
		}
	];
});

app.filter('moment', function () {
	return function (input, momentFn) {
		var args = Array.prototype.slice.call(arguments, 2),
			momentObj = moment(input);
		return momentObj[momentFn].apply(momentObj, args);
	}
});