'use strict';

var app = angular.module('evolveApp',
	['ngRoute', 'ui.bootstrap', 'googlechart', 'ngSanitize', 'ngResource']
).run(['$rootScope', '$location', '$window', function($rootScope, $location, $window) {
	$rootScope.$on('$routeChangeSuccess', function(event) {
		if (!$window.ga)
			return;
		$window.ga('send', 'pageview', { page: $location.path() });
	});
}]);

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
		when('/donate', {
			controller: 'DonateCtrl',
			templateUrl: '/partials/donate.html'
		}).
		when('/about', {
			controller: 'AboutCtrl',
			templateUrl: '/partials/about.html'
		}).
		otherwise({
			redirectTo: '/'
		});
	$locationProvider.html5Mode(true);
});

app.controller('ChallengeListCtrl', function($scope, $rootScope, $http) {
	$rootScope.htmlPage = {backgroundImage: "url('/img/bg/default.png')"};
	
	$scope.filter = {};
	
	$http.get('/api/challenges/previous.json').success(function(data) {
		$scope.challenges = data;
	});
});

app.controller('ChallengeDetailCtrl', function($scope, $rootScope, $http, $routeParams, $interval) {

	$scope.Math = window.Math;
	$scope.range = function(n) { return new Array(n) };
	
	$scope.refresh = function() {
		$http.get('/api/challenge/' + $routeParams.challengeSlug + '.json').success(function(data) {
			$scope.challenge = data;
			$scope.challenge['percent'] = $scope.challenge.progress / $scope.challenge.goal * 100;
			$scope.challenge['percent'] = Math.floor($scope.challenge['percent'])
			$scope.challenge['percent_stretch'] =
				($scope.challenge.progress - $scope.challenge.goal)
				/ ($scope.challenge.goal_stretch - $scope.challenge.goal) * 100;
			
			$rootScope.htmlPage = {backgroundImage: "url('" + $scope.challenge.background + "')"};
			
			if ( !$scope.challenge.is_countdown && !$scope.challenge.is_active)
				$interval.cancel($scope.intervalPromise);
			if ( $scope.challenge.type != 'info')
			$scope.refreshChart();
		});
	};

	$scope.refreshChart = function() {

		var chart = {},
			i = 0;
		chart.type="LineChart";
		chart.data = {
			'cols': [
				{id: 't', label: 'Time', type: 'datetime'},
				{id: 'r', label: 'Target', type: 'number'},
				{id: 'p', label: 'Progress', type: 'number'}
			],
			'rows': []
		};
		
		chart.data.rows.push({c: [
			{v: new Date($scope.challenge.start)},
			{v: 0},
			{v: 0}
		]});
		
		for (i = 0; i < $scope.challenge.datapoints.length; i++) {
			chart.data.rows.push({c: [
				{v: new Date($scope.challenge.datapoints[i]['updated'])},
				{v: null},
				{v: $scope.challenge.datapoints[i]['value']}
			]});
		}
		
		chart.data.rows.push({c: [
			{v: new Date($scope.challenge.end)},
			{v: $scope.challenge.goal},
			{v: null}
		]});
		
		chart.options = {
			title: "Challenge Progress",
			titleTextStyle: {color: '#fff'},
			titlePosition: 'none',
			legend: {position: 'none'},
			backgroundColor: 'transparent',
			colors: ['#333', '#FD391E'],
			vAxis: {
				title: $scope.challenge.axis_y_label,
				titleTextStyle: {color: '#fff'},
				baselineColor: '#333',
				ticks: [$scope.challenge.goal],
				maxValue: $scope.challenge.axis_y_max,
				minValue: $scope.challenge.axis_y_min,
				format: 'short',
			},
			hAxis: {
				title: "Time",
				titleTextStyle: {color: '#fff'},
				gridlines: {
					color: '#333',
					count: 6,
				}
			}
		};
		if ($scope.challenge.is_stretch)
			chart.options['vAxis']['ticks'].push($scope.challenge.goal_stretch);
		chart.formatters = {};
		$scope.chartProgress = chart;
	};
	
	$scope.intervalPromise = $interval(function() {
		$scope.refresh();
	}, 15 * 60 * 1000);
	
	$scope.$on("$destroy", function() {
		$interval.cancel($scope.intervalPromise);
	});
	
	$scope.refresh();
});

app.controller('MainCtrl', function($scope, $rootScope, $http) {
	$rootScope.htmlPage = {backgroundImage: "url('/img/bg/default.png')"};
	
	$http.get('/api/challenges/current.json').success(function(data) {
		$scope.challenges = data;
	});
});

app.controller('DonateCtrl', function($rootScope) {
	$rootScope.htmlPage = {backgroundImage: "url('/img/bg/default.png')"};
});

app.controller('AboutCtrl', function($rootScope) {
	$rootScope.htmlPage = {backgroundImage: "url('/img/bg/default.png')"};
});

app.controller('HeaderController', function($scope, $location, $rootScope) {
	$scope.isActive = function(viewLocation) {
		return $location.path().substr(0, viewLocation.length) == viewLocation;
	};
});

app.controller('ChallengeInfo', function($scope, $http, $routeParams) {

	$http.get('/partials/challenges/' + $routeParams.challengeSlug + '.html').success(function(data) {
		$scope.$parent.challenge_info = data;
	});
});

app.controller('FaqCtrl', function($scope, $rootScope) {
	$rootScope.htmlPage = {backgroundImage: "url('/img/bg/faq.jpg')"};
	$scope.questions = [
		{
			q: "Do you have to play as specific characters?",
			a: "No. You just need to login and play at least one online game that connects to an official game server and you're eligible. Encourage your team mates to partake in challenges though!"
		},
		{
			q: "Does solo play count?",
			a: "Make sure you are logged into your 2K account. Your 2K account is what ties your participation to challenges online. Playing in solo mode means you are participating in the challenge and are therefore eligible for the reward, however does not contribute to the overall goal. If you wish to contribute to the goal as well, then join an online multiplayer match and join the Hunt!"
		},
		{
			q: "We finished the challenge! When do I get my rewards?!",
			a: "Officially you will have your rewards by the following Thursday. With that being said, we usually see them by Monday or Tuesday."
		},
		{
			q: "Cool site! How often does it update?",
			a: "The site pulls information from an API from Turtle Rock Studios. Their API usually updates every fifteen minutes (plus or minus a couple minutes), so my site refreshes no more than five minutes after."
		},
		{
			q: "How often does Evolve have challenges?",
			a: "Evolve has generally hosted challenges every other week (with exceptions). I'll do my best to keep this page updated, but right now the plan is to have a community challenge every other weekend in rotation with Community Tournaments by the sound of it. More information can be found <a href=\"https://talk.turtlerockstudios.com/t/evolve-community-tournament/65452\" target=\"_blank\">here</a>."
		},
		{
			q: "Why is the data different from what TRS announces?",
			a: "While it appears Turtle Rock Studios uses EvolveChallenges.com/their API to make progress announcements, they run a final official tally after every challenge the following Monday which may differ what this site cuts off. This site will use any data that is given from the API up to 30 minutes after the official challenge end time."
		},
		{
			q: "Does this site provide information for all platforms?",
			a: "It includes them all: PC, Xbox One, PS4. Everyone who plays Evolve contributes to the challenges."
		},
		{
			q: "Do I need to spam the f*** out of my f5 key?",
			a: "Nope! The site will automatically update itself every 15 minutes for you. You focus on completing the challenges, I'll make sure the site is up-to-date next time you glance over and take a peak."
		},
		{
			q: "We lost percent! What happened? (Or if this happens...)",
			a: "Community Challenges were not a part of Evolve's original plan, and their API was implemented for internal use. Mistakes happen. If the progress or data jumps in any way, it's because there was an error of some kind. If the data does change, my site will automatically recognize these changes when they occur.<br><br>An example of this is Hyde's flamethrower challenge. The starting timezone was set correctly, but was set for the wrong timezone, therefore 7 hours of data was included that should not have been included. This was fixed the next morning causing a huge spike in the graph."
		},
		{
			q: "We already reached the goal, can I still play and be eligible?",
			a: "Yes. As long as the event has not ended (there is still a clock on the challenge page), you are eligible for the rewards."
		},
		{
			q: "I played during the challenge but never received my reward",
			a: "Try restarting your game and double checking to ensure you did not receive your skin. If you are certain you played during the challenge and did not receive a skin contact <a href=\"http://support.2k.com/hc/en-us/sections/200606003-Evolve\" target=\"_blank\">2K Support</a> and they should be able to help you."
		},
		{
			q: "When will we get a shot at the Behemoth Gold Skin?",
			a: "\"One Day...\""
		}
	];
});

app.filter('moment', function () {
	return function (input, momentFn) {
		var args = Array.prototype.slice.call(arguments, 2),
			momentObj = moment.utc(input);
		return momentObj[momentFn].apply(momentObj, args);
	}
});

app.directive('progressBar', function() {
	return {
		templateUrl: '/partials/progress/health_and_armor.html'
	}
});