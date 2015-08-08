'use strict';

angular.module('frontEnd')
.controller('FrontCtrl', function(Restangular, $scope) {

    $scope.days = [];
    $scope.daysToList = 7;
    var today = moment();
    var baseMatches = Restangular.all('matches');

    for (var i = 0; i < $scope.daysToList; i++) {
        var qDay = today.add(i, 'days').format('YYYY-MM-DD');
            baseMatches.getList({date: qDay}).then(function(matches) {
                $scope.days.push(matches);
            });
    }
})
.filter('kickoff', function() {
    return function(timeString) {
        // return timeString.substr(0, 5);
        return moment(timeString, 'HH:mm:ss').format('HH:mm');
    };
})

.filter('dayNames', function() {
    return function(date) {
        var today = moment();
        var date = moment(date, 'YYYY-MM-DD');
        if (today.isSame(date, 'day')) {
            return 'Today';
        } else if (date.isSame(today.add(1, 'day'), 'day')) {
            return 'Tomorrow';
        } else {
            return date.format('dddd Do MMMM');
        }
        return 'hey';
    }
});
