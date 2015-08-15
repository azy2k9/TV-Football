'use strict';

angular.module('frontEnd')
.controller('FrontCtrl', function(Restangular, $scope) {

    $scope.days = [];
    $scope.daysToList = 7;
    var today = moment();
    var endDate = moment().add($scope.daysToList, 'days');
    var query = {
        start: today.format('YYYY-MM-DD'),
        end: endDate.format('YYYY-MM-DD')
    };
    var baseMatches = Restangular.all('matches');

    baseMatches.getList(query).then(function(days) {
        for (var i = 0; i < days.length; i++) {
            $scope.days.push(days[i].matches);
        }
    });

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
