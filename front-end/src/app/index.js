'use strict';

angular.module('frontEnd', ['ngAnimate', 'ngCookies', 'ngTouch', 'ngSanitize', 'restangular', 'ui.router'])
  .config(function ($stateProvider, $urlRouterProvider, RestangularProvider) {
    $stateProvider
      .state('home', {
        templateUrl: 'app/main/main.html',
        controller: 'MainCtrl'
      })
      .state('home.front', {
          url: '/',
          templateUrl: 'app/front/front.html',
          controller: 'FrontCtrl'
      })
      .state('home.about', {
          url: '/about',
          templateUrl: 'app/about/about.html'
      });

    $urlRouterProvider.otherwise('/');

    RestangularProvider.setBaseUrl('http://tvfootball.zidhuss.com:8082/api');

    RestangularProvider.addResponseInterceptor(function(data, operation, what, url, resonse, deferred) {
        var extractedData;
        if (operation === 'getList') {
            extractedData = data.data;
        } else {
            extractedData = data;
        }
        return extractedData;
    });

  })
;
